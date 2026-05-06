from collections import defaultdict
from typing import Dict, List, TypedDict

from models.event import Event
from models.incident import Incident


class Rule(TypedDict):
    event_type: str
    threshold: int
    mitre: str
    severity: str


class DetectionEngine:
    def __init__(self) -> None:
        self.counters: Dict[str, int] = defaultdict(int)
        self.buffers: Dict[str, List[Event]] = defaultdict(list)

        self.rules: Dict[str, Rule] = {
            "bruteforce": {
                "event_type": "failed_login",
                "threshold": 5,
                "mitre": "T1110",
                "severity": "high",
            },
            "ddos": {
                "event_type": "ddos",
                "threshold": 50,
                "mitre": "T1499",
                "severity": "high",
            },
        }

    def process(self, event: Event) -> List[Incident]:
        incidents: List[Incident] = []

        # 🔴 нормализация IP
        ip: str = event.ip if event.ip else "unknown"

        for rule_name, rule in self.rules.items():
            if event.type != rule["event_type"]:
                continue

            key: str = f"{rule_name}:{ip}"

            self.counters[key] += 1
            self.buffers[key].append(event)

            if self.counters[key] >= rule["threshold"]:
                inc = Incident(
                    type=rule_name,
                    ip=ip,
                    severity=rule["severity"],
                    events=self.buffers[key],
                )

                inc.mitre = rule["mitre"]
                inc.meta["rule"] = rule_name
                inc.meta["count"] = self.counters[key]

                incidents.append(inc)

                self.counters[key] = 0
                self.buffers[key] = []

        return incidents
