from typing import Any, Dict, List, Optional

from collectors.base import BaseCollector
from collectors.auth_log import AuthLogCollector
from collectors.network_collector import NetworkCollector
from collectors.system_metrics import SystemMetricsCollector


def get_collectors(
    config: Optional[Dict[str, Any]] = None
) -> List[BaseCollector]:

    config = config or {}

    collectors: List[BaseCollector] = []

    # -------------------------
    # SSH auth log collector
    # VM2 -> /var/log/auth.log
    # -------------------------
    ssh_host: str = config.get("ssh_host", "192.168.0.109")
    ssh_user: str = config.get("ssh_user", "srvr")
    ssh_log_path: str = config.get(
        "ssh_log_path",
        "/var/log/auth.log"
    )

    collectors.append(
        AuthLogCollector(
            host=ssh_host,
            user=ssh_user,
            log_path=ssh_log_path
        )
    )

    # -------------------------
    # Network collector
    # DDoS / flood detection
    # -------------------------
    if config.get("enable_network_monitoring", True):

        ddos_threshold: int = int(
            config.get("ddos_threshold", 30)
        )

        collectors.append(
            NetworkCollector(
                threshold=ddos_threshold
            )
        )

    # -------------------------
    # Local system metrics
    # CPU / resource abuse
    # -------------------------
    if config.get("enable_system_metrics", True):

        cpu_threshold: float = float(
            config.get("cpu_threshold", 80.0)
        )

        collectors.append(
            SystemMetricsCollector(
                cpu_threshold=cpu_threshold
            )
        )

    return collectors


# from typing import List, Optional, Dict, Any

# from collectors.base import BaseCollector
# from collectors.auth_log import AuthLogCollector
# from collectors.network_collector import NetworkCollector


# def get_collectors(config: Optional[Dict[str, Any]] = None) -> List[BaseCollector]:
#     collectors: List[BaseCollector] = []

#     # -------------------------
#     # Default collectors
#     # -------------------------
#     collectors.append(AuthLogCollector())

#     # -------------------------
#     # Network collector (DDoS detection)
#     # -------------------------
#     if config is None or config.get("enable_network_monitoring", True):
#         threshold = 30
#         if config:
#             threshold = config.get("ddos_threshold", 30)

#         collectors.append(NetworkCollector(threshold=threshold))

#     return collectors