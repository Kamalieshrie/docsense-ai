# ============================================================
# metadata_store.py — SQLite structured queries
# Exact searches: all invoices 2024 / amount > 5000
# ============================================================
import sqlite3
import json
from typing import List, Dict, Any
from pathlib import Path

DB_PATH = "./storage/docsense.db"


def _conn():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize():
    with _conn() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id            TEXT PRIMARY KEY,
            doc_type      TEXT,
            owner_name    TEXT,
            date          TEXT,
            amount        REAL,
            institution   TEXT,
            file_path     TEXT,
            storage_path  TEXT,
            raw_json      TEXT,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        con.commit()


def save(doc_id: str, meta: Dict[str, Any], raw_json: Dict):
    initialize()
    with _conn() as con:
        con.execute("""
        INSERT OR REPLACE INTO documents
        (id, doc_type, owner_name, date, amount,
         institution, file_path, storage_path, raw_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc_id,
            meta.get("doc_type"),
            meta.get("owner_name"),
            meta.get("date"),
            meta.get("amount", 0),
            meta.get("institution"),
            meta.get("file_path"),
            meta.get("storage_path"),
            json.dumps(raw_json),
        ))
        con.commit()


def search(doc_type=None, owner=None, limit=50) -> List[Dict]:
    initialize()
    query  = "SELECT * FROM documents WHERE 1=1"
    params = []
    if doc_type:
        query += " AND doc_type = ?"
        params.append(doc_type)
    if owner:
        query += " AND owner_name LIKE ?"
        params.append(f"%{owner}%")
    query += f" ORDER BY created_at DESC LIMIT {limit}"

    with _conn() as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(query, params).fetchall()
    return [dict(r) for r in rows]