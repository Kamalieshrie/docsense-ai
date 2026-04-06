# ============================================================
# dedup_checker.py
# SHA-256 exact duplicate detection
# Prevents same document being stored twice
# ============================================================
import hashlib
import json
from pathlib import Path
from typing import Optional

_HASH_STORE = "./storage/hashes.json"


def _load() -> dict:
    if Path(_HASH_STORE).exists():
        return json.loads(Path(_HASH_STORE).read_text())
    return {}


def _save(store: dict):
    Path(_HASH_STORE).parent.mkdir(parents=True, exist_ok=True)
    Path(_HASH_STORE).write_text(json.dumps(store, indent=2))


def file_hash(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def is_duplicate(file_path: str) -> Optional[str]:
    """Returns path of existing file if duplicate found, else None."""
    store = _load()
    fhash = file_hash(file_path)
    if fhash in store:
        return store[fhash]
    return None


def register(file_path: str):
    """Register file hash after successful storage."""
    store = _load()
    store[file_hash(file_path)] = file_path
    _save(store)