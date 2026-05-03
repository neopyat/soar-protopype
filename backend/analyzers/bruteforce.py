from collections import defaultdict
from typing import Dict, List, Optional

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


class BruteForceAnalyzer(BaseAnalyzer):
    def __init__(self, threshold: int = 5):
        self.threshold = threshold
        self.ip_counter: Dict[str, List[Event]] = defaultdict(list)

    def analyze(self, event: Event) -> Optional[Incident]:
        # учитываем только неудачные логины
        if event.type != "failed_login" or not event.ip:
            return None

        self.ip_counter[event.ip].append(event)

        # проверяем threshold
        if len(self.ip_counter[event.ip]) >= self.threshold:
            ev_list = self.ip_counter[event.ip]

            inc = Incident(
                type="bruteforce",
                ip=event.ip,
                severity="high",
                events=ev_list
            )

            inc.meta["attempts"] = len(ev_list)

            # сбрасываем счётчик, чтобы не спамить
            self.ip_counter[event.ip] = []

            return inc

        return None