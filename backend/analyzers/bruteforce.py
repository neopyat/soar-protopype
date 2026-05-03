from collections import defaultdict
from typing import Dict, Optional

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


class BruteForceAnalyzer(BaseAnalyzer):
    def __init__(self, threshold: int = 5):
        self.threshold = threshold
        self.ip_counter: Dict[str, int] = defaultdict(int)

    def analyze(self, event: Event) -> Optional[Incident]:
        if event.type != "failed_login" or not event.ip:
            return None

        self.ip_counter[event.ip] += 1

        if self.ip_counter[event.ip] >= self.threshold:
            inc = Incident(
                type="bruteforce",
                ip=event.ip,
                severity="high"
            )

            inc.meta["attempts"] = self.ip_counter[event.ip]
            inc.mitre = "T1110"

            self.ip_counter[event.ip] = 0
            return inc

        return None