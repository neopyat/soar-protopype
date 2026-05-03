from typing import Optional

from analyzers.base import BaseAnalyzer
from analyzers.engine import DetectionEngine
from models.event import Event
from models.incident import Incident


class EngineAnalyzer(BaseAnalyzer):
    def __init__(self) -> None:
        self.engine = DetectionEngine()

    def analyze(self, event: Event) -> Optional[Incident]:
        incidents = self.engine.process(event)

        if incidents:
            return incidents[0]

        return None