from typing import List

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


class MLAnalyzer(BaseAnalyzer):
    def analyze(self, events: List[Event]) -> List[Incident]:
        incidents: List[Incident] = []

        for event in events:
            if event.type == "failed_login":
                score = 0

                score += 1

                if event.ip:
                    score += 1

                if score >= 2:
                    inc = Incident(
                        type="suspicious_activity",
                        ip=event.ip,
                        severity="medium",
                        events=[event]
                    )

                    inc.meta["score"] = score
                    incidents.append(inc)

        return incidents