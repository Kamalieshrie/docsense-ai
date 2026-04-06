# ============================================================
# upload.py — UPDATED WITH SHAREPOINT INTEGRATION
# backend/app/routes/upload.py
# ============================================================
import os
import uuid
import json
import sqlite3
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.pipeline.format_converter import convert_to_images
from app.pipeline.document_brain   import process_document
from app.storage.dedup_checker     import is_duplicate, register
from app.storage.file_manager      import (
    build_storage_path,
    save_file,
    upload_to_sharepoint,        # ← NEW
)
from app.storage.metadata_store    import save as meta_save, DB_PATH, initialize
from app.storage.vector_store      import store_document
from app.agents.bank_agent         import BankAgent
from app.agents.invoice_agent      import InvoiceAgent
from app.agents.cheque_agent       import ChequeAgent
from app.agents.certificate_agent  import CertificateAgent

router     = APIRouter()
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

AGENTS = {
    "bank_statement": BankAgent(),
    "invoice":        InvoiceAgent(),
    "cheque":         ChequeAgent(),
    "certificate":    CertificateAgent(),
}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    tmp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # ── Duplicate → return EXISTING result ──────────────
        dup_path = is_duplicate(tmp_path)
        if dup_path:
            os.remove(tmp_path)
            initialize()
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            row  = conn.execute(
                "SELECT * FROM documents WHERE storage_path = ?",
                (dup_path,)
            ).fetchone()
            conn.close()
            if row:
                doc = dict(row)
                existing = {}
                if doc.get("raw_json"):
                    try:
                        existing = json.loads(doc["raw_json"])
                    except Exception:
                        pass
                return JSONResponse({
                    "status":         "duplicate",
                    "message":        "Already stored — showing existing result",
                    "doc_id":         doc["id"],
                    "sharepoint_url": doc.get("sharepoint_url", ""),
                    "result":         existing
                })
            return JSONResponse({
                "status":  "duplicate",
                "message": "Already stored."
            })

        # ── Convert + process ────────────────────────────────
        pages = convert_to_images(tmp_path)
        if not pages:
            raise HTTPException(400, "Could not read document")

        result   = process_document(pages)
        doc_type = result.get("document_type", "unknown")

        agent = AGENTS.get(doc_type)
        if agent:
            result = agent.run(result)

        # ── Save locally first (needed for OCR processing) ───
        doc_id       = str(uuid.uuid4())
        storage_path = build_storage_path(result, file.filename)
        save_file(tmp_path, storage_path)
        register(storage_path)

        # ── Upload to SharePoint ─────────────────────────────
        sharepoint_url      = None

        # Upload original document file
        sharepoint_url = upload_to_sharepoint(
            local_path=storage_path,
            doc_type=doc_type,
            filename=file.filename
        )


        if sharepoint_url:
            print(f"[Upload] ✅ SP file : {sharepoint_url}")

        # ── Save metadata to SQLite ───────────────────────────
        meta_save(doc_id, {
            "doc_type":            doc_type,
            "owner_name":          (result.get("account_holder") or
                                    result.get("full_name") or
                                    result.get("student_name") or ""),
            "date":                result.get("date", ""),
            "amount":              0,
            "institution":         (result.get("bank_name") or
                                    result.get("institution") or ""),
            "file_path":           tmp_path,
            "storage_path":        storage_path,
            "sharepoint_url":      sharepoint_url      or "",  # ← NEW
        }, result)

        store_document(
            doc_id,
            str(result)[:2000],
            {"doc_type": doc_type, "storage_path": storage_path}
        )

        if os.path.exists(tmp_path):
            os.remove(tmp_path)

        return JSONResponse({
            "status":              "success",
            "doc_id":              doc_id,
            "storage_backend":     "sharepoint" if sharepoint_url else "local",
            "sharepoint_url":      sharepoint_url      or "",   # ← NEW
            "result":              result
        })

    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise HTTPException(500, str(e))