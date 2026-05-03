from typing import List, Optional, Dict, Any

from collectors.base import BaseCollector
from collectors.auth_log import AuthLogCollector
from collectors.network_collector import NetworkCollector


def get_collectors(config: Optional[Dict[str, Any]] = None) -> List[BaseCollector]:
    collectors: List[BaseCollector] = []

    # -------------------------
    # Default collectors
    # -------------------------
    collectors.append(AuthLogCollector())

    # -------------------------
    # Network collector (DDoS detection)
    # -------------------------
    if config is None or config.get("enable_network_monitoring", True):
        threshold = 30
        if config:
            threshold = config.get("ddos_threshold", 30)

        collectors.append(NetworkCollector(threshold=threshold))

    return collectors