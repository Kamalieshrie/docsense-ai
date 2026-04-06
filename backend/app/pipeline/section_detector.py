# ============================================================
# section_detector.py
# Tags each word with which document section it belongs to
# e.g. CREDIT, DEBIT, CHECK, SUMMARY, FEES
# ============================================================
from typing import List, Dict, Any

SECTION_KEYWORDS = {
    "CREDIT":  ["deposits", "credits", "credit", "additions"],
    "DEBIT":   ["withdrawals", "debits", "debit", "payments"],
    "CHECK":   ["checks paid", "cheques", "check no"],
    "SUMMARY": ["summary", "account summary"],
    "FEES":    ["fees", "service charge", "charges"],
}


def detect_sections(words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    current_section = "UNKNOWN"
    annotated = []

    for word in sorted(words, key=lambda w: (w["y"], w["x"])):
        text_lower = word["text"].lower()
        for section, keywords in SECTION_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                current_section = section
                break
        word_copy = dict(word)
        word_copy["section"] = current_section
        annotated.append(word_copy)

    return annotated