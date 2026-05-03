from abc import ABC, abstractmethod
from typing import Optional

from models.event import Event
from models.incident import Incident


class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, event: Event) -> Optional[Incident]:
        """
        Принимает одно событие и возвращает инцидент или None
        """
        ...