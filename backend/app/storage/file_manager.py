# ============================================================
# file_manager.py — UPDATED WITH SHAREPOINT INTEGRATION
# backend/app/storage/file_manager.py
# ============================================================
import os
import shutil
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

STORAGE_ROOT = "./storage/documents"

CATEGORY_MAP = {
    "bank_statement":   "financial/bank_statements",
    "invoice":          "financial/invoices",
    "receipt":          "financial/receipts",
    "medical_bill":     "medical",
    "certificate":      "education/certificates",
    "id_proof":         "identity",
    "cheque":           "financial/cheques",
    "resume":           "personal/resumes",
    "property_doc":     "legal/property",
    "contract":         "legal/contracts",
    "salary_slip":      "financial/salary_slips",
    "tax_document":     "financial/tax_documents",
    "utility_bill":     "financial/utility_bills",
    "insurance":        "financial/insurance",
    "admission_letter": "education/admission",
    "vehicle_rc":       "identity/vehicle",
    "rental_agreement": "legal/rental",
    "unknown":          "uncategorized",
}


# ── EXISTING — completely unchanged ──────────────────────────
def build_storage_path(doc_data: Dict[str, Any],
                       original_filename: str) -> str:
    doc_type    = doc_data.get("document_type", "unknown")
    category    = CATEGORY_MAP.get(doc_type, "uncategorized")
    institution = _safe(
        doc_data.get("bank_name") or
        doc_data.get("institution") or ""
    )
    owner = _safe(
        doc_data.get("account_holder") or
        doc_data.get("student_name") or
        doc_data.get("full_name") or ""
    )
    date_str = (
        doc_data.get("statement_period", {}).get("from") or
        doc_data.get("date") or ""
    )
    year, month = _parse_date(date_str)

    parts = [STORAGE_ROOT, category]
    if institution: parts.append(institution)
    if owner:       parts.append(owner)
    if year:        parts.append(year)
    if month:       parts.append(month)

    folder = os.path.join(*parts)
    Path(folder).mkdir(parents=True, exist_ok=True)
    return os.path.join(folder, original_filename)


# ── EXISTING — completely unchanged ──────────────────────────
def save_file(src_path: str, dest_path: str) -> str:
    shutil.copy2(src_path, dest_path)
    return dest_path


# ── NEW: Upload document file to SharePoint ──────────────────
def upload_to_sharepoint(local_path: str,
                         doc_type: str,
                         filename: str) -> Optional[str]:
    try:
        from app.storage.sharepoint_manager import (
            upload_file_to_sharepoint,
            is_enabled
        )
        if not is_enabled():
            logger.info("[FileManager] SharePoint not configured")
            return None
        sp_url = upload_file_to_sharepoint(
            local_path=local_path,
            doc_type=doc_type,
            filename=filename
        )
        logger.info(f"[FileManager] ✅ SP file: {sp_url}")
        return sp_url
    except Exception as e:
        logger.warning(f"[FileManager] ⚠️ SP upload failed: {e}")
        return None


# ── NEW: Upload extracted JSON to SharePoint ─────────────────
def upload_json_to_sharepoint(extracted_data: dict,
                               doc_type: str,
                               filename: str) -> Optional[str]:
    try:
        from app.storage.sharepoint_manager import (
            upload_json_to_sharepoint as sp_upload_json,
            is_enabled
        )
        if not is_enabled():
            return None
        sp_json_url = sp_upload_json(
            extracted_data=extracted_data,
            doc_type=doc_type,
            base_filename=filename
        )
        logger.info(f"[FileManager] ✅ SP JSON: {sp_json_url}")
        return sp_json_url
    except Exception as e:
        logger.warning(f"[FileManager] ⚠️ JSON upload failed: {e}")
        return None


# ── NEW: Delete from SharePoint ──────────────────────────────
def delete_from_sharepoint(sharepoint_url: str):
    if not sharepoint_url:
        return
    try:
        from app.storage.sharepoint_manager import (
            delete_file_from_sharepoint
        )
        delete_file_from_sharepoint(sharepoint_url)
        logger.info(f"[FileManager] ✅ SP deleted")
    except Exception as e:
        logger.warning(f"[FileManager] ⚠️ SP delete failed: {e}")


# ── EXISTING helpers — completely unchanged ───────────────────
def _safe(s: str) -> str:
    if not s:
        return ""
    return s.lower().replace(" ", "_").replace("/", "")[:30]


def _parse_date(date_str: str):
    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y",
                "%B %Y", "%b %Y"]:
        try:
            d = datetime.strptime(date_str.strip(), fmt)
            return str(d.year), d.strftime("%B").lower()
        except Exception:
            continue
    return "", ""