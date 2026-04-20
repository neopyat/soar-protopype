from collections import defaultdict
from typing import List, Dict

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


class BruteForceAnalyzer(BaseAnalyzer):
    def __init__(self, threshold: int = 5):
        self.threshold = threshold

    def analyze(self, events: List[Event]) -> List[Incident]:
        ip_events: Dict[str, List[Event]] = defaultdict(list)
        incidents: List[Incident] = []

        # группируем события по IP
        for event in events:
            if event.type == "failed_login" and event.ip:
                ip_events[event.ip].append(event)

        # создаём инциденты
        for ip, ev_list in ip_events.items():
            if len(ev_list) >= self.threshold:
                inc = Incident(
                    type="bruteforce",
                    ip=ip,
                    severity="high",
                    events=ev_list
                )

                inc.meta["attempts"] = len(ev_list)
                incidents.append(inc)

        return incidents