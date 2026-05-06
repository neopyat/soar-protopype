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

