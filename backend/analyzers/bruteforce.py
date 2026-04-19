from collections import defaultdict
from typing import List, Dict, Any

from analyzers.base import BaseAnalyzer


class BruteForceAnalyzer(BaseAnalyzer):
    def __init__(self, threshold: int = 5):
        self.threshold = threshold

    def analyze(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ip_counter: Dict[str, int] = defaultdict(int)
        incidents: List[Dict[str, Any]] = []

        for event in events:
            if event.get("type") == "failed_login":
                ip = event.get("ip")
                if isinstance(ip, str):
                    ip_counter[ip] += 1

        for ip, count in ip_counter.items():
            if count >= self.threshold:
                incidents.append({
                    "type": "bruteforce",
                    "ip": ip,
                    "attempts": count,
                    "severity": "high"
                })

        return incidents