from typing import Dict, List, Optional
from collections import defaultdict
import time

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


class PortScanAnalyzer(BaseAnalyzer):
    def __init__(self, threshold: int = 10, window: int = 10) -> None:
        self.threshold: int = threshold
        self.window: int = window

        # ip -> список временных меток
        self.ip_connections: Dict[str, List[float]] = defaultdict(list)

    def analyze(self, event: Event) -> Optional[Incident]:
        # нужен IP
        if not event.ip:
            return None

        
        now: float = time.time()

        # добавляем событие
        self.ip_connections[event.ip].append(now)

        # очищаем окно
        self.ip_connections[event.ip] = [
            t for t in self.ip_connections[event.ip]
            if now - t <= self.window
        ]

        # если превышен порог — считаем сканированием
        if len(self.ip_connections[event.ip]) >= self.threshold:
            inc = Incident(
                type="port_scan",
                ip=event.ip,
                severity="medium"
            )

            inc.add_event(event)

            inc.meta["connections"] = len(self.ip_connections[event.ip])
            inc.mitre = "T1046"

            # сброс окна 
            self.ip_connections[event.ip] = []

            return inc

        return None

