from typing import Dict, Any, List
from playbooks.base import BasePlaybook


class BruteForcePlaybook(BasePlaybook):
    def match(self, incident: Dict[str, Any]) -> bool:
        return incident.get("type") == "bruteforce"

    def execute(self, incident: Dict[str, Any]) -> List[Dict[str, Any]]:
        ip = incident.get("ip")

        if not ip:
            return []

        return [
            {
                "action": "block_ip",
                "ip": ip,
                "reason": "bruteforce detected"
            },
            {
                "action": "log",
                "message": f"Bruteforce attack from {ip}"
            }
        ]