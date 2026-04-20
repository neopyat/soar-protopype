from typing import List, Dict, Any

from analyzers.base import BaseAnalyzer


class PortScanAnalyzer(BaseAnalyzer):
    def analyze(self, events: List[Any]) -> List[Dict[str, Any]]:
        # базовая заглушка
        return []