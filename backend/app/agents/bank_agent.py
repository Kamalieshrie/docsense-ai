# ============================================================
# bank_agent.py
# Verifies: opening + credits - debits - charges = closing
# ============================================================
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class BankAgent(BaseAgent):

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        opening  = self._to_float(data.get("opening_balance"))
        credits  = self._to_float(data.get("total_credits"))
        debits   = self._to_float(data.get("total_debits"))
        closing  = self._to_float(data.get("closing_balance"))
        charges  = self._to_float(data.get("service_charges"))

        computed = round(opening + credits - debits - charges, 2)
        diff     = round(abs(computed - closing), 2)

        # Also total from individual transactions
        txn_credits = sum(
            self._to_float(t.get("credit"))
            for t in data.get("transactions", [])
        )
        txn_debits = sum(
            self._to_float(t.get("debit"))
            for t in data.get("transactions", [])
        )

        data["calculations"] = {
            "computed_closing_balance":  computed,
            "stated_closing_balance":    closing,
            "discrepancy":               diff,
            "balance_verified":          diff < 0.01,
            "transaction_total_credits": round(txn_credits, 2),
            "transaction_total_debits":  round(txn_debits,  2),
        }

        if diff >= 0.01:
            data["discrepancies"] = [
                f"Balance mismatch: computed {computed} ≠ stated {closing}"
            ]
        return data