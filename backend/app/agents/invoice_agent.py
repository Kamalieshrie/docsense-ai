# ============================================================
# invoice_agent.py
# Verifies: sum(line totals) = subtotal
#           subtotal + tax - discount = grand_total
# ============================================================
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class InvoiceAgent(BaseAgent):

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        items    = data.get("line_items", [])
        subtotal = self._to_float(data.get("subtotal"))
        tax      = self._to_float(data.get("tax"))
        discount = self._to_float(data.get("discount"))
        grand    = self._to_float(data.get("grand_total"))

        computed_sub   = round(sum(
            self._to_float(i.get("total")) for i in items
        ), 2)
        computed_grand = round(computed_sub + tax - discount, 2)

        data["calculations"] = {
            "computed_subtotal":    computed_sub,
            "stated_subtotal":      subtotal,
            "computed_grand_total": computed_grand,
            "stated_grand_total":   grand,
            "line_items_verified":  abs(computed_sub   - subtotal) < 0.01,
            "grand_total_verified": abs(computed_grand - grand)    < 0.01,
        }

        discrepancies = []
        if abs(computed_sub - subtotal) >= 0.01:
            discrepancies.append(
                f"Subtotal mismatch: computed {computed_sub} ≠ stated {subtotal}"
            )
        if abs(computed_grand - grand) >= 0.01:
            discrepancies.append(
                f"Grand total mismatch: computed {computed_grand} ≠ stated {grand}"
            )
        if discrepancies:
            data["discrepancies"] = discrepancies

        return data