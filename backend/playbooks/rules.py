from typing import List, Dict, Any

from models.incident import Incident
from playbooks.base import BasePlaybook


class BruteForcePlaybook(BasePlaybook):
    def match(self, incident: Incident) -> bool:
        return (
            incident.type == "bruteforce"
            and incident.severity == "high"
        )

    def execute(self, incident: Incident) -> List[Dict[str, Any]]:
        actions: List[Dict[str, Any]] = []

        if not incident.ip:
            return actions

        actions.append({
            "action": "block_ip",
            "ip": incident.ip
        })

        actions.append({
            "action": "log",
            "message": f"[SOAR] Bruteforce detected from {incident.ip}"
        })

        return actions


class SuspiciousActivityPlaybook(BasePlaybook):
    def match(self, incident: Incident) -> bool:
        return (
            incident.type in ("anomaly", "suspicious_activity")
            and incident.severity in ("medium", "high")
        )

    def execute(self, incident: Incident) -> List[Dict[str, Any]]:
        return [{
            "action": "log",
            "message": f"[SOAR] Suspicious activity: {incident.ip}"
        }]