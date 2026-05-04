from abc import ABC, abstractmethod
from typing import List

from models.event import Event
from models.incident import Incident


class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, events: List[Event]) -> List[Incident]:
        ...