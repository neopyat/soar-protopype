from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BasePlaybook(ABC):
    @abstractmethod
    def match(self, incident: Dict[str, Any]) -> bool:
        ...

    @abstractmethod
    def execute(self, incident: Dict[str, Any]) -> List[Dict[str, Any]]:
        ...