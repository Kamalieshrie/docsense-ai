# ============================================================
# schemas.py — Pydantic models for type-safe AI output
# ============================================================
from pydantic import BaseModel, field_validator
from typing import Optional, List, Any


class Transaction(BaseModel):
    date:        Optional[str] = None
    description: Optional[str] = None
    debit:       Optional[str] = None
    credit:      Optional[str] = None
    balance:     Optional[str] = None


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity:    Optional[str] = None
    unit_price:  Optional[str] = None
    total:       Optional[str] = None


class ExtractionResult(BaseModel):
    document_type: str
    raw_data:      dict

    @field_validator("document_type")
    @classmethod
    def check_type(cls, v):
        allowed = [
            "bank_statement", "invoice", "receipt",
            "medical_bill", "certificate", "id_proof",
            "cheque", "resume", "property_doc",
            "contract", "unknown"
        ]
        return v if v in allowed else "unknown"