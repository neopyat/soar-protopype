from typing import List, Dict, Any

from analyzers.base import BaseAnalyzer


class MLAnalyzer(BaseAnalyzer):
    def analyze(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        incidents: List[Dict[str, Any]] = []

        for event in events:
            if event.get("type") == "failed_login":
                score = 0

                # простая логика
                score += 1

                if event.get("ip"):
                    score += 1

                if score >= 2:
                    incidents.append({
                        "type": "suspicious_activity",
                        "ip": event.get("ip"),
                        "score": score,
                        "severity": "medium"
                    })

        return incidents