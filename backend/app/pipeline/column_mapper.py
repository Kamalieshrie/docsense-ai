# ============================================================
# column_mapper.py
# Groups OCR words into table rows and columns
# using pixel (x, y) coordinates — fixes wrong column bug
# ============================================================
from typing import List, Dict, Any
import numpy as np


def map_to_table(words: List[Dict[str, Any]],
                 row_tolerance: int = 12) -> List[Dict[str, str]]:
    if not words:
        return []

    # ── Group into rows by y-coordinate ────────────────────
    words_sorted = sorted(words, key=lambda w: w["y"])
    rows: List[List[Dict]] = []
    current_row = [words_sorted[0]]

    for word in words_sorted[1:]:
        if abs(word["y"] - current_row[-1]["y"]) <= row_tolerance:
            current_row.append(word)
        else:
            rows.append(sorted(current_row, key=lambda w: w["x"]))
            current_row = [word]
    rows.append(sorted(current_row, key=lambda w: w["x"]))

    if not rows:
        return []

    # ── First row = headers ─────────────────────────────────
    header_row = rows[0]
    col_names  = [w["text"].upper() for w in header_row]
    col_xs     = [w["x"] for w in header_row]

    # ── Map each word to nearest column ────────────────────
    result = []
    for row in rows[1:]:
        row_dict = {col: "" for col in col_names}
        for word in row:
            distances = [abs(word["x"] - cx) for cx in col_xs]
            nearest_i = int(np.argmin(distances))
            col = col_names[nearest_i]
            row_dict[col] = (row_dict[col] + " " + word["text"]).strip()
        result.append(row_dict)

    return result