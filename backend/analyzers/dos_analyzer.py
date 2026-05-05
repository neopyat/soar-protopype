from typing import Optional

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


class DoSAnalyzer(BaseAnalyzer):
    def __init__(self, conn_threshold: int = 50, cpu_threshold: float = 80.0) -> None:
        self.conn_threshold: int = conn_threshold
        self.cpu_threshold: float = cpu_threshold

    def analyze(self, event: Event) -> Optional[Incident]:
        # 🔴 гарантируем str
        ip: str = event.ip if event.ip else "unknown"

        # -------------------------
        # NETWORK FLOOD
        # -------------------------
        if event.type == "connection":
            connections: int = int(getattr(event, "connections", 0))

            if connections >= self.conn_threshold:
                inc = Incident(
                    type="dos_attack",
                    ip=ip,
                    severity="high"
                )

                inc.add_event(event)

                inc.meta["connections"] = connections
                inc.mitre = "T1499"

                return inc

        # -------------------------
        # CPU OVERLOAD
        # -------------------------
        if event.type == "system_metrics":
            cpu: float = float(getattr(event, "cpu", 0.0))

            if cpu >= self.cpu_threshold:
                inc = Incident(
                    type="resource_abuse",
                    ip=ip,
                    severity="high"
                )

                inc.add_event(event)

                inc.meta["cpu"] = cpu
                inc.mitre = "T1499"

                return inc

        return None

# from typing import Optional

# from analyzers.base import BaseAnalyzer
# from models.event import Event
# from models.incident import Incident


# class DoSAnalyzer(BaseAnalyzer):
#     def __init__(self, conn_threshold: int = 50, cpu_threshold: float = 80.0) -> None:
#         self.conn_threshold: int = conn_threshold
#         self.cpu_threshold: float = cpu_threshold

#     def analyze(self, event: Event) -> Optional[Incident]:
#         # -------------------------
#         # NETWORK FLOOD
#         # -------------------------
#         if event.type == "connection":
#             connections: int = getattr(event, "connections", 0)

#             if connections >= self.conn_threshold:
#                 inc = Incident(
#                     type="dos_attack",
#                     ip=event.ip,
#                     severity="high"
#                 )

#                 inc.add_event(event)

#                 inc.meta["connections"] = connections
#                 inc.mitre = "T1499"

#                 return inc

#         # -------------------------
#         # CPU OVERLOAD
#         # -------------------------
#         if event.type == "system_metrics":
#             cpu: float = getattr(event, "cpu", 0.0)

#             if cpu >= self.cpu_threshold:
#                 inc = Incident(
#                     type="resource_abuse",
#                     ip=event.ip,
#                     severity="high"
#                 )

#                 inc.add_event(event)

#                 inc.meta["cpu"] = cpu
#                 inc.mitre = "T1499"

#                 return inc

#         return None

# from typing import Optional

# from analyzers.base import BaseAnalyzer
# from models.event import Event
# from models.incident import Incident


# class DoSAnalyzer(BaseAnalyzer):
#     def __init__(self, conn_threshold: int = 50, cpu_threshold: float = 80.0):
#         self.conn_threshold = conn_threshold
#         self.cpu_threshold = cpu_threshold

#     def analyze(self, event: Event) -> Optional[Incident]:
#         # --- NETWORK FLOOD ---
#         if event.type == "connection":
#             connections = getattr(event, "connections", 0)

#             if connections >= self.conn_threshold:
#                 inc = Incident(
#                     type="dos_attack",
#                     ip=event.ip,
#                     severity="high"
#                 )

#                 inc.meta["connections"] = connections
#                 inc.mitre = "T1499"

#                 return inc

#         # --- SYSTEM OVERLOAD ---
#         if event.type == "system_metrics":
#             cpu = getattr(event, "cpu", 0)

#             if cpu >= self.cpu_threshold:
#                 inc = Incident(
#                     type="resource_abuse",
#                     ip="local",
#                     severity="high"
#                 )

#                 inc.meta["cpu"] = cpu
#                 inc.mitre = "T1499"

#                 return inc

#         return None