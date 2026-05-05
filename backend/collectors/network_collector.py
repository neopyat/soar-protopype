from typing import List, Dict, Any, DefaultDict
from collections import defaultdict
import subprocess
import time

from collectors.base import BaseCollector


class NetworkCollector(BaseCollector):
    def __init__(self, threshold: int = 20) -> None:
        self.threshold: int = threshold

    def collect(self) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        connections: DefaultDict[str, int] = defaultdict(int)

        try:
            result = subprocess.run(
                ["ss", "-tn"],
                capture_output=True,
                text=True,
                check=False
            )

            output: str = result.stdout
            lines: List[str] = output.splitlines()

            for line in lines:
                if "ESTAB" not in line:
                    continue

                parts: List[str] = line.split()
                if len(parts) < 5:
                    continue

                src: str = parts[4]

                if ":" not in src:
                    continue

                ip: str = src.rsplit(":", 1)[0]

                if not ip:
                    continue

                connections[ip] += 1

        except Exception as e:
            print(f"[NetworkCollector Error] {e}")
            return events

        now: float = time.time()

        for ip, count in connections.items():
            if count < self.threshold:
                continue

            event: Dict[str, Any] = {
                "type": "connection",
                "ip": ip,
                "connections": count,
                "timestamp": now,
                "raw": f"connections={count}"
            }

            events.append(event)

        return events


# from typing import List, Dict, Any, DefaultDict
# from collections import defaultdict
# import subprocess
# import time

# from collectors.base import BaseCollector


# class NetworkCollector(BaseCollector):
#     def __init__(self, threshold: int = 20) -> None:
#         self.threshold: int = threshold

#     def collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         # ЯВНО типизируем → Pylance доволен
#         connections: DefaultDict[str, int] = defaultdict(int)

#         try:
#             result = subprocess.run(
#                 ["ss", "-tn"],
#                 capture_output=True,
#                 text=True,
#                 check=False
#             )

#             output: str = result.stdout
#             lines: List[str] = output.splitlines()

#             for line in lines:
#                 if "ESTAB" not in line:
#                     continue

#                 parts: List[str] = line.split()
#                 if len(parts) < 5:
#                     continue

#                 src: str = parts[4]

#                 # безопасный парсинг IP
#                 if ":" not in src:
#                     continue

#                 ip: str = src.rsplit(":", 1)[0]

#                 if not ip:
#                     continue

#                 connections[ip] += 1

#         except Exception as e:
#             print(f"[NetworkCollector Error] {e}")
#             return events

#         now: float = time.time()

#         for ip, count in connections.items():
#             if count < self.threshold:
#                 continue

#             event: Dict[str, Any] = {
#                 "type": "connection",
#                 "ip": ip,
#                 "connections": count,
#                 "timestamp": now,
#                 "raw": f"connections={count}"
#             }

#             events.append(event)

#         return events

# from typing import List, Dict, Any
# import subprocess

# from collectors.base import BaseCollector


# class NetworkCollector(BaseCollector):
#     def __init__(self, threshold: int = 50, port: int = 22) -> None:
#         self.threshold = threshold
#         self.port = port

#     def collect(self) -> List[Dict[str, Any]]:
#         try:
#             result = subprocess.run(
#                 ["ss", "-ant"],
#                 capture_output=True,
#                 text=True,
#                 check=False
#             )

#             lines = result.stdout.splitlines()

#             ip_count: Dict[str, int] = {}

#             for line in lines:
#                 if f":{self.port}" not in line:
#                     continue

#                 parts = line.split()

#                 if len(parts) < 5:
#                     continue

#                 remote = parts[4]

#                 if ":" not in remote:
#                     continue

#                 ip = remote.split(":")[0]

#                 if ip == "127.0.0.1":
#                     continue

#                 ip_count[ip] = ip_count.get(ip, 0) + 1

#             events: List[Dict[str, Any]] = []

#             for ip, count in ip_count.items():
#                 if count >= self.threshold:
#                     events.append({
#                         "type": "ddos",
#                         "ip": ip,
#                         "raw": f"connections={count}"
#                     })

#             return events

#         except Exception as e:
#             print(f"[Collector] Network error: {e}")
#             return []