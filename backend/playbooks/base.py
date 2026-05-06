from abc import ABC, abstractmethod
from typing import List, Dict, Any

from models.incident import Incident


class BasePlaybook(ABC):
    @abstractmethod
    def match(self, incident: Incident) -> bool:
        ...

    @abstractmethod
    def execute(self, incident: Incident) -> List[Dict[str, Any]]:
        ...

    # 🔴 ДОБАВЛЯЕМ ЭТО
    def run(self, incident: Incident) -> List[Dict[str, Any]]:
        if not self.match(incident):
            return []

        return self.execute(incident)
