from typing import List, Optional, Dict, Any

from analyzers.base import BaseAnalyzer
from analyzers.bruteforce import BruteForceAnalyzer
from analyzers.ml_analyzer import MLAnalyzer


def get_analyzers(config: Optional[Dict[str, Any]] = None) -> List[BaseAnalyzer]:
    analyzers: List[BaseAnalyzer] = []

    # базовый анализатор
    analyzers.append(BruteForceAnalyzer(threshold=5))

    # ML модуль
    if config and config.get("use_ml"):
        analyzers.append(MLAnalyzer())

    return analyzers