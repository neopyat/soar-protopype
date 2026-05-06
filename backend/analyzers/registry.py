from typing import List, Optional, Dict, Any

from analyzers.base import BaseAnalyzer
from analyzers.engine_adapter import EngineAnalyzer
from analyzers.bruteforce import BruteForceAnalyzer
from analyzers.ml_analyzer import MLAnalyzer
from analyzers.port_scan import PortScanAnalyzer


def get_analyzers(config: Optional[Dict[str, Any]] = None) -> List[BaseAnalyzer]:
    analyzers: List[BaseAnalyzer] = []

    # главный движок
    analyzers.append(EngineAnalyzer())

    # сигнатурные анализаторы
    analyzers.append(BruteForceAnalyzer(threshold=5))
    analyzers.append(PortScanAnalyzer())

    # ML (опционально)
    if config and config.get("use_ml"):
        analyzers.append(MLAnalyzer())

    return analyzers
