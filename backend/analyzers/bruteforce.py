from collections import defaultdict
from analyzers.base import BaseAnalyzer


class BruteForceAnalyzer(BaseAnalyzer):
    def __init__(self, threshold=5):
        self.threshold = threshold

    def analyze(self, events):
        ip_counter = defaultdict(int)
        incidents = []

        for event in events:
            if event.get("type") == "failed_login":
                ip = event.get("ip")
                if ip:
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