# ============================================================
# documents.py — UPDATED WITH SHAREPOINT INTEGRATION
# backend/app/routes/documents.py
# ============================================================
import os
import json
import sqlite3
from fastapi import APIRouter, HTTPException
from typing import Optional
from app.storage.metadata_store import search as meta_search, DB_PATH, initialize

router = APIRouter()


@router.get("/documents")
async def list_documents(
    doc_type: Optional[str] = None,
    owner:    Optional[str] = None,
    limit:    int = 100
):
    initialize()
    results = meta_search(doc_type=doc_type, owner=owner, limit=limit)
    for r in results:
        if r.get("raw_json"):
            try:
                r["extracted"] = json.loads(r["raw_json"])
            except Exception:
                r["extracted"] = {}
        else:
            r["extracted"] = {}
    return {"total": len(results), "documents": results}


@router.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    initialize()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row  = conn.execute(
        "SELECT * FROM documents WHERE id = ?", (doc_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Document not found")
    doc = dict(row)
    if doc.get("raw_json"):
        try:
            doc["extracted"] = json.loads(doc["raw_json"])
        except Exception:
            doc["extracted"] = {}
    return doc


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    initialize()
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        row  = conn.execute(
            "SELECT * FROM documents WHERE id = ?", (doc_id,)
        ).fetchone()
        if not row:
            raise HTTPException(404, "Not found")
        doc  = dict(row)
        path = doc.get("storage_path", "")

        # ── Delete from local storage ─────────────────────────
        if path and os.path.exists(path):
            os.remove(path)
            print(f"[Delete] ✅ Local file deleted: {path}")

        # ── Delete from SharePoint if URL exists ──────────────
        sharepoint_url      = doc.get("sharepoint_url", "")
        sharepoint_json_url = doc.get("sharepoint_json_url", "")

        if sharepoint_url:
            try:
                from app.storage.file_manager import delete_from_sharepoint
                delete_from_sharepoint(sharepoint_url)
                print(f"[Delete] ✅ SharePoint file deleted")
            except Exception as e:
                print(f"[Delete] ⚠️ SharePoint file delete failed: {e}")

        if sharepoint_json_url:
            try:
                from app.storage.file_manager import delete_from_sharepoint
                delete_from_sharepoint(sharepoint_json_url)
                print(f"[Delete] ✅ SharePoint JSON deleted")
            except Exception as e:
                print(f"[Delete] ⚠️ SharePoint JSON delete failed: {e}")

        # ── Remove hash from hashes.json ──────────────────────
        try:
            from pathlib import Path
            hash_file = Path("./storage/hashes.json")
            if hash_file.exists():
                hashes = json.loads(hash_file.read_text())
                hashes = {k: v for k, v in hashes.items() if v != path}
                hash_file.write_text(json.dumps(hashes, indent=2))
        except Exception as e:
            print(f"[Delete] Hash cleanup error: {e}")

        # ── Delete from database ──────────────────────────────
        conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        conn.commit()
        conn.close()
        return {"status": "deleted", "doc_id": doc_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))