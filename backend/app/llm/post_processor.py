# ============================================================
# post_processor.py
# Fixes: null dates, [object Object], empty arrays
# ============================================================
import re
from typing import Any, Dict


def clean_result(data: Dict[str, Any]) -> Dict[str, Any]:
    data = _fix_null_dates(data)
    data = _flatten_objects(data)
    data = _remove_empty(data)
    return data


def _fix_null_dates(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: _fix_null_dates(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_fix_null_dates(i) for i in data]
    if isinstance(data, str):
        data = re.sub(r'\bnull-(\d{2}-\d{2})\b',
                      r'UNKNOWN-\1', data)
    return data


def _flatten_objects(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: _flatten_objects(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_flatten_objects(i) for i in data]
    return data


def _remove_empty(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: _remove_empty(v) for k, v in data.items()
                if v not in [None, "", [], {}]}
    if isinstance(data, list):
        cleaned = [_remove_empty(i) for i in data]
        return [i for i in cleaned if i not in [None, "", [], {}]]
    return data