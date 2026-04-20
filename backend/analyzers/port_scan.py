from typing import List

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


class PortScanAnalyzer(BaseAnalyzer):
    def analyze(self, events: List[Event]) -> List[Incident]:
        # пока заглушка, но уже в правильной архитектуре
        return []