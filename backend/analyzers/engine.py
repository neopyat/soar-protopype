from collections import defaultdict
from typing import Dict, List, TypedDict

from models.event import Event
from models.incident import Incident


# 🔴 строго описываем структуру правила
class Rule(TypedDict):
    event_type: str
    threshold: int
    mitre: str
    severity: str


class DetectionEngine:
    def __init__(self) -> None:
        # состояние
        self.counters: Dict[str, int] = defaultdict(int)
        self.buffers: Dict[str, List[Event]] = defaultdict(list)

        # 🔴 теперь rules типизирован
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

        for rule_name, rule in self.rules.items():
            if event.type != rule["event_type"]:
                continue

            key = f"{rule_name}:{event.ip}"

            self.counters[key] += 1
            self.buffers[key].append(event)

            if self.counters[key] >= rule["threshold"]:
                inc = Incident(
                    type=rule_name,
                    ip=event.ip,
                    severity=rule["severity"],
                    events=self.buffers[key],
                )

                # MITRE автоматически
                inc.mitre = rule["mitre"]
                inc.meta["rule"] = rule_name
                inc.meta["count"] = self.counters[key]

                incidents.append(inc)

                # сброс
                self.counters[key] = 0
                self.buffers[key] = []

        return incidents