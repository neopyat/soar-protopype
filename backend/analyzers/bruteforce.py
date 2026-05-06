from typing import Dict, Optional
from collections import defaultdict

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


class BruteForceAnalyzer(BaseAnalyzer):
    def __init__(self, threshold: int = 5) -> None:
        self.threshold: int = threshold
        self.ip_counter: Dict[str, int] = defaultdict(int)

    def analyze(self, event: Event) -> Optional[Incident]:
        # интересуют только неудачные логины
        if event.type != "failed_login":
            return None

        if not event.ip:
            return None

        # увеличиваем счётчик
        self.ip_counter[event.ip] += 1

        # достигли порога → инцидент
        if self.ip_counter[event.ip] >= self.threshold:
            inc = Incident(
                type="bruteforce",
                ip=event.ip,
                severity="high"
            )

            inc.add_event(event)

            # метаданные
            inc.meta["attempts"] = self.ip_counter[event.ip]
            inc.mitre = "T1110"

            # сброс счётчика
            self.ip_counter[event.ip] = 0

            return inc

        return None
