# ============================================================
# base_agent.py — Abstract base for all document agents
# Rule: AI extracts values. Python does ALL math. Always.
# ============================================================
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):

    @abstractmethod
    def run(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @staticmethod
    def _to_float(value: Any) -> float:
        """Safely convert any extracted value to float."""
        if value is None or value == "":
            return 0.0
        s = str(value).replace(",", "").replace("$", "").replace("₹", "").replace(" ", "").strip()
        try:
            return float(s)
        except ValueError:
            return 0.0