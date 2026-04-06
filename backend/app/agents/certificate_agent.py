# ============================================================
# certificate_agent.py
# Computes total marks and percentage from subject list
# ============================================================
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class CertificateAgent(BaseAgent):

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        subjects   = data.get("subjects", [])
        obtained   = sum(self._to_float(s.get("marks_obtained")) for s in subjects)
        maximum    = sum(self._to_float(s.get("max_marks"))      for s in subjects)
        percentage = round((obtained / maximum * 100), 2) if maximum else 0

        data["calculations"] = {
            "total_marks_obtained": round(obtained,   2),
            "total_max_marks":      round(maximum,    2),
            "computed_percentage":  percentage,
            "stated_percentage":    data.get("percentage", ""),
        }

        return data