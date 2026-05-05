from typing import Optional, Dict, List
from collections import defaultdict
import time

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


class PortScanAnalyzer(BaseAnalyzer):
    def __init__(self, threshold: int = 10, window: int = 10):
        self.threshold = threshold
        self.window = window

        # ip -> timestamps
        self.ip_connections: Dict[str, List[float]] = defaultdict(list)

    def analyze(self, event: Event) -> Optional[Incident]:
        if event.type != "connection" or not event.ip:
            return None

        now = time.time()

        self.ip_connections[event.ip].append(now)

        # очищаем окно
        self.ip_connections[event.ip] = [
            t for t in self.ip_connections[event.ip]
            if now - t <= self.window
        ]

        if len(self.ip_connections[event.ip]) >= self.threshold:
            return Incident(
                type="port_scan",
                ip=event.ip,
                severity="medium"
            )

        return None

# from typing import List

# from analyzers.base import BaseAnalyzer
# from models.event import Event
# from models.incident import Incident


# class PortScanAnalyzer(BaseAnalyzer):
#     def analyze(self, events: List[Event]) -> List[Incident]:
#         # пока заглушка, но уже в правильной архитектуре
#         return []