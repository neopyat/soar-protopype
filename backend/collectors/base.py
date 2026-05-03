from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseCollector(ABC):
    """
    Базовый класс для всех collectors

    Collector возвращает СЫРЫЕ события (dict),
    нормализация происходит отдельно в processors.normalizer
    """

    @abstractmethod
    def collect(self) -> List[Dict[str, Any]]:
        pass