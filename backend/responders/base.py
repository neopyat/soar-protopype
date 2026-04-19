from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseResponder(ABC):
    @abstractmethod
    def respond(self, actions: List[Dict[str, Any]]) -> None:
        ...