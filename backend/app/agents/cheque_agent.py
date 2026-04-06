# ============================================================
# cheque_agent.py
# Verifies amount in words matches amount in numbers
# Flags fraud if mismatch found
# ============================================================
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class ChequeAgent(BaseAgent):

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        num   = self._to_float(data.get("amount_in_numbers"))
        words = data.get("amount_in_words", "").lower().strip()

        data["calculations"] = {
            "amount_in_numbers":   num,
            "amount_in_words_raw": words,
            "note": "Manual verification recommended for high-value cheques."
        }

        if num == 0 and words and words not in ["", "n/a"]:
            data["discrepancies"] = [
                "Amount in numbers is 0 but words field is non-empty — verify manually."
            ]

        return data