from typing import List, Dict, Any
import time

import psutil

from collectors.base import BaseCollector


class SystemMetricsCollector(BaseCollector):
    def __init__(self, cpu_threshold: float = 80.0) -> None:
        self.cpu_threshold: float = cpu_threshold

    def collect(self) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []

        try:
            cpu: float = psutil.cpu_percent(interval=0.5)
            connections: int = len(psutil.net_connections())

            if cpu < self.cpu_threshold:
                return events

            event: Dict[str, Any] = {
                "type": "system_metrics",
                "ip": "local",
                "cpu": cpu,
                "connections": connections,
                "timestamp": time.time(),
                "raw": f"cpu={cpu}, connections={connections}"
            }

            events.append(event)

        except Exception as e:
            print(f"[SystemMetricsCollector Error] {e}")

        return events


# import time
# from typing import List, Dict, Any

# import psutil

# from collectors.base import BaseCollector


# class SystemMetricsCollector(BaseCollector):
#     def collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         try:
#             cpu = psutil.cpu_percent(interval=0.5)
#             connections = len(psutil.net_connections())

#             events.append({
#                 "type": "system_metrics",
#                 "cpu": cpu,
#                 "connections": connections,
#                 "timestamp": time.time(),
#                 "raw": f"cpu={cpu}, connections={connections}"
#             })

#         except Exception as e:
#             print(f"[SystemMetricsCollector Error] {e}")

#         return events