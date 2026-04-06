# ============================================================
# sharepoint_manager.py
# backend/app/storage/sharepoint_manager.py
# FIXED: Using Microsoft Graph API — no app-only token issues!
# ============================================================
import os
import json
import logging
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

CLIENT_ID     = os.getenv("SHAREPOINT_CLIENT_ID")
CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET")
TENANT_ID     = os.getenv("SHAREPOINT_TENANT_ID")
SITE_URL      = os.getenv("SHAREPOINT_SITE_URL", "").rstrip("/")
BASE_FOLDER   = os.getenv("SHAREPOINT_FOLDER", "DocSense-AI")

# ============================================================
# CATEGORY MAP — Flat structure, NO subfolders inside folders
# Only 7 top-level folders: education, financial, identity,
#                           medical, personal, legal, uncategorized
# ============================================================
CATEGORY_MAP = {

    # ── EDUCATION ───────────────────────────────────────────
    # School, college, university certificates & marksheets
    "certificate":              "education",
    "degree_certificate":       "education",
    "diploma_certificate":      "education",
    "school_certificate":       "education",
    "marksheet":                "education",
    "transcript":               "education",
    "grade_card":               "education",
    "report_card":              "education",
    # Admission & enrollment
    "admission_letter":         "education",
    "admission_form":           "education",
    "enrollment_form":          "education",
    "offer_letter_education":   "education",
    # Professional / work certifications
    "work_certificate":         "education",
    "experience_certificate":   "education",
    "training_certificate":     "education",
    "internship_certificate":   "education",
    "course_completion":        "education",
    "professional_certificate": "education",
    "noc_education":            "education",   # No Objection Certificate
    "bonafide_certificate":     "education",
    "migration_certificate":    "education",
    "transfer_certificate":     "education",
    # Scholarships & fees
    "scholarship_letter":       "education",
    "fee_receipt":              "education",
    "hall_ticket":              "education",
    "exam_admit_card":          "education",

    # ── FINANCIAL ───────────────────────────────────────────
    # Bank documents
    "bank_statement":           "financial",
    "bank_passbook":            "financial",
    "cheque":                   "financial",
    "cheque_book":              "financial",
    "demand_draft":             "financial",
    "bank_certificate":         "financial",
    "bank_letter":              "financial",
    # Invoices, bills & receipts
    "invoice":                  "financial",
    "bill":                     "financial",
    "receipt":                  "financial",
    "purchase_order":           "financial",
    "quotation":                "financial",
    "proforma_invoice":         "financial",
    "credit_note":              "financial",
    "debit_note":               "financial",
    "delivery_challan":         "financial",
    "e_way_bill":               "financial",
    # Salary & employment income
    "salary_slip":              "financial",
    "payslip":                  "financial",
    "salary_certificate":       "financial",
    "form_16":                  "financial",   # TDS certificate India
    "form_16a":                 "financial",
    # Tax documents
    "tax_document":             "financial",
    "income_tax_return":        "financial",
    "itr":                      "financial",
    "tax_assessment":           "financial",
    "tax_notice":               "financial",
    "gst_certificate":          "financial",
    "gst_return":               "financial",
    "gst_invoice":              "financial",
    "pan_acknowledgement":      "financial",
    "tds_certificate":          "financial",
    "tds_return":               "financial",
    "tax_clearance":            "financial",
    "advance_tax":              "financial",
    # Insurance
    "insurance":                "financial",
    "insurance_policy":         "financial",
    "insurance_certificate":    "financial",
    "life_insurance":           "financial",
    "health_insurance":         "financial",
    "vehicle_insurance":        "financial",
    "home_insurance":           "financial",
    "travel_insurance":         "financial",
    "insurance_renewal":        "financial",
    "insurance_claim":          "financial",
    # Loans & credit
    "loan_agreement":           "financial",
    "loan_statement":           "financial",
    "loan_sanction_letter":     "financial",
    "emi_schedule":             "financial",
    "credit_report":            "financial",
    "noc_loan":                 "financial",
    # Investments
    "mutual_fund_statement":    "financial",
    "demat_statement":          "financial",
    "stock_statement":          "financial",
    "investment_certificate":   "financial",
    "fixed_deposit":            "financial",
    "ppf_statement":            "financial",
    "nps_statement":            "financial",
    # Utility bills (financial obligations)
    "utility_bill":             "financial",
    "electricity_bill":         "financial",
    "water_bill":               "financial",
    "gas_bill":                 "financial",
    "telephone_bill":           "financial",
    "internet_bill":            "financial",
    "mobile_bill":              "financial",
    "dth_bill":                 "financial",
    "maintenance_bill":         "financial",

    # ── IDENTITY ────────────────────────────────────────────
    # Government photo IDs
    "id_proof":                 "identity",
    "aadhaar":                  "identity",
    "aadhar":                   "identity",
    "pan_card":                 "identity",
    "passport":                 "identity",
    "voter_id":                 "identity",
    "driving_license":          "identity",
    # Vehicle documents
    "vehicle_rc":               "identity",
    "rc_book":                  "identity",
    "vehicle_registration":     "identity",
    # Community & status certificates
    "caste_certificate":        "identity",
    "community_certificate":    "identity",
    "obc_certificate":          "identity",
    "sc_st_certificate":        "identity",
    "income_certificate":       "identity",
    "domicile_certificate":     "identity",
    "residence_certificate":    "identity",
    "nativity_certificate":     "identity",
    # Civil / vital records
    "birth_certificate":        "identity",
    "death_certificate":        "identity",
    "marriage_certificate":     "identity",
    "divorce_certificate":      "identity",
    "name_change_certificate":  "identity",
    # Address proof
    "address_proof":            "identity",
    "ration_card":              "identity",
    "electricity_bill_address": "identity",  # when used as address proof
    # Immigration
    "visa":                     "identity",
    "work_permit":              "identity",
    "oci_card":                 "identity",
    "pcc":                      "identity",   # Police Clearance Certificate

    # ── MEDICAL ─────────────────────────────────────────────
    # Diagnostics & reports
    "medical_report":           "medical",
    "lab_report":               "medical",
    "blood_report":             "medical",
    "radiology_report":         "medical",
    "xray_report":              "medical",
    "mri_report":               "medical",
    "scan_report":              "medical",
    "pathology_report":         "medical",
    "ecg_report":               "medical",
    # Clinical documents
    "prescription":             "medical",
    "doctor_prescription":      "medical",
    "discharge_summary":        "medical",
    "clinical_notes":           "medical",
    "referral_letter":          "medical",
    "fitness_certificate":      "medical",
    "vaccination_certificate":  "medical",
    "covid_certificate":        "medical",
    # Billing & insurance claims
    "medical_bill":             "medical",
    "medical_invoice":          "medical",
    "hospital_bill":            "medical",
    "pharmacy_bill":            "medical",
    "medical_receipt":          "medical",
    "insurance_claim_medical":  "medical",
    "cashless_authorization":   "medical",
    "reimbursement_form":       "medical",

    # ── PERSONAL ────────────────────────────────────────────
    # Career documents
    "resume":                   "personal",
    "cv":                       "personal",
    "cover_letter":             "personal",
    "job_offer_letter":         "personal",
    "appointment_letter":       "personal",
    "relieving_letter":         "personal",
    "resignation_letter":       "personal",
    "recommendation_letter":    "personal",
    "reference_letter":         "personal",
    # Personal correspondence
    "personal_letter":          "personal",
    "affidavit":                "personal",
    "declaration":              "personal",
    "power_of_attorney":        "personal",
    "will":                     "personal",
    "nomination_form":          "personal",
    # Travel
    "travel_itinerary":         "personal",
    "ticket":                   "personal",
    "boarding_pass":            "personal",
    "hotel_booking":            "personal",
    "travel_insurance_doc":     "personal",
    # Miscellaneous personal
    "photograph":               "personal",
    "signature_proof":          "personal",

    # ── LEGAL ───────────────────────────────────────────────
    # Property
    "property_doc":             "legal",
    "sale_deed":                "legal",
    "title_deed":               "legal",
    "encumbrance_certificate":  "legal",
    "property_tax_receipt":     "legal",
    "khata_certificate":        "legal",
    "patta":                    "legal",
    # Agreements & contracts
    "contract":                 "legal",
    "agreement":                "legal",
    "rental_agreement":         "legal",
    "lease_agreement":          "legal",
    "mou":                      "legal",
    "nda":                      "legal",
    "service_agreement":        "legal",
    # Court & legal notices
    "court_order":              "legal",
    "legal_notice":             "legal",
    "fir":                      "legal",
    "police_report":            "legal",
    "affidavit_legal":          "legal",
    # Company / business
    "incorporation_certificate":"legal",
    "gst_registration":         "legal",
    "trade_license":            "legal",
    "shop_act":                 "legal",
    "msme_certificate":         "legal",
    "udyam_certificate":        "legal",

    # ── FALLBACK ────────────────────────────────────────────
    "unknown":                  "uncategorized",
    "other":                    "uncategorized",
    "misc":                     "uncategorized",
}

# ── Cache site/drive IDs so we don't fetch every upload ──────
_cache = {}


def is_enabled() -> bool:
    return all([CLIENT_ID, CLIENT_SECRET, TENANT_ID, SITE_URL])


def _get_token() -> str:
    """Get Microsoft Graph token."""
    import msal
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    if "access_token" in result:
        print(f"[SharePoint] ✅ Token acquired successfully")
        return result["access_token"]
    error = result.get("error_description", str(result))
    print(f"[SharePoint] ❌ Token failed: {error}")
    raise Exception(f"Token failed: {error}")


def _get_site_and_drive(token: str) -> tuple:
    """Get SharePoint site ID and drive ID. Cached after first call."""
    if "site_id" in _cache and "drive_id" in _cache:
        return _cache["site_id"], _cache["drive_id"]

    hostname = SITE_URL.replace("https://", "").split("/")[0]
    headers  = {"Authorization": f"Bearer {token}"}

    # Get site ID
    site_url = f"https://graph.microsoft.com/v1.0/sites/{hostname}"
    resp     = requests.get(site_url, headers=headers)
    if not resp.ok:
        print(f"[SharePoint] ❌ Site fetch failed: {resp.status_code} {resp.text[:200]}")
    resp.raise_for_status()
    site_id = resp.json()["id"]
    print(f"[SharePoint] ✅ Site ID: {site_id}")

    # Get drive ID
    drives_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
    resp       = requests.get(drives_url, headers=headers)
    resp.raise_for_status()
    drives     = resp.json().get("value", [])

    drive_id = None
    for d in drives:
        if d.get("name") in ["Documents", "Shared Documents"]:
            drive_id = d["id"]
            break
    if not drive_id:
        drive_id = drives[0]["id"]
    print(f"[SharePoint] ✅ Drive ID: {drive_id}")

    _cache["site_id"]  = site_id
    _cache["drive_id"] = drive_id
    return site_id, drive_id


def _folder_path(doc_type: str) -> str:
    """
    Flat folder path inside Documents library.
    Structure: DocSense-AI/<category>
    No subfolders — everything sits directly in one of the 7 folders.
    """
    category = CATEGORY_MAP.get(doc_type, "uncategorized")
    return f"{BASE_FOLDER}/{category}"


def upload_file_to_sharepoint(local_path: str,
                               doc_type: str,
                               filename: str) -> str:
    """Upload file via Microsoft Graph API."""
    token             = _get_token()
    site_id, drive_id = _get_site_and_drive(token)
    folder            = _folder_path(doc_type)

    url = (
        f"https://graph.microsoft.com/v1.0"
        f"/sites/{site_id}/drives/{drive_id}"
        f"/root:/{folder}/{filename}:/content"
    )

    with open(local_path, "rb") as f:
        file_bytes = f.read()

    print(f"[SharePoint] Uploading file to: {folder}/{filename}")
    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/octet-stream"
        },
        data=file_bytes
    )

    if not resp.ok:
        print(f"[SharePoint] ❌ Upload failed: {resp.status_code} {resp.text[:300]}")
    resp.raise_for_status()

    sp_url = resp.json().get("webUrl", f"{SITE_URL}/{folder}/{filename}")
    print(f"[SharePoint] ✅ File uploaded: {sp_url}")
    logger.info(f"[SharePoint] ✅ File uploaded: {sp_url}")
    return sp_url


def upload_json_to_sharepoint(extracted_data: dict,
                               doc_type: str,
                               base_filename: str) -> str:
    """Upload JSON via Microsoft Graph API."""
    token             = _get_token()
    site_id, drive_id = _get_site_and_drive(token)
    folder            = _folder_path(doc_type)
    json_filename     = Path(base_filename).stem + ".json"

    url = (
        f"https://graph.microsoft.com/v1.0"
        f"/sites/{site_id}/drives/{drive_id}"
        f"/root:/{folder}/{json_filename}:/content"
    )

    json_bytes = json.dumps(
        extracted_data, indent=2, ensure_ascii=False
    ).encode("utf-8")

    print(f"[SharePoint] Uploading JSON to: {folder}/{json_filename}")
    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/json"
        },
        data=json_bytes
    )

    if not resp.ok:
        print(f"[SharePoint] ❌ JSON failed: {resp.status_code} {resp.text[:300]}")
    resp.raise_for_status()

    sp_url = resp.json().get("webUrl", f"{SITE_URL}/{folder}/{json_filename}")
    print(f"[SharePoint] ✅ JSON uploaded: {sp_url}")
    logger.info(f"[SharePoint] ✅ JSON uploaded: {sp_url}")
    return sp_url


def delete_file_from_sharepoint(sharepoint_url: str):
    """Delete file via Microsoft Graph API."""
    if not sharepoint_url:
        return
    try:
        token             = _get_token()
        site_id, drive_id = _get_site_and_drive(token)

        # Extract path after /Documents/
        if "/Documents/" in sharepoint_url:
            path = sharepoint_url.split("/Documents/")[-1]
        else:
            path = sharepoint_url.split(SITE_URL)[-1].lstrip("/")

        url = (
            f"https://graph.microsoft.com/v1.0"
            f"/sites/{site_id}/drives/{drive_id}"
            f"/root:/{path}"
        )
        resp = requests.delete(
            url,
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"[SharePoint] ✅ Deleted: {path}")
        logger.info(f"[SharePoint] ✅ Deleted: {path}")
    except Exception as e:
        logger.warning(f"[SharePoint] ⚠️ Delete failed: {e}")
        print(f"[SharePoint] ⚠️ Delete failed: {e}")


def test_connection() -> dict:
    if not is_enabled():
        return {"connected": False, "reason": "Missing credentials"}
    try:
        token           = _get_token()
        site_id, drive_id = _get_site_and_drive(token)
        return {
            "connected": True,
            "site_id":   site_id,
            "drive_id":  drive_id
        }
    except Exception as e:
        return {"connected": False, "reason": str(e)}