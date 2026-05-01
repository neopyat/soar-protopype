from typing import List, Dict, Any

from models.incident import Incident
from playbooks.base import BasePlaybook


class BruteForcePlaybook(BasePlaybook):
    def match(self, incident: Incident) -> bool:
        return (
            incident.type == "bruteforce"
            and incident.severity == "high"
            and incident.mitre == "T1110"
        )

    def execute(self, incident: Incident) -> List[Dict[str, Any]]:
        if not incident.ip:
            return []

        return [
            {
                "action": "block_ip",
                "ip": incident.ip,
                "incident_id": incident.id
            },
            {
                "action": "log",
                "message": f"[SOAR] Bruteforce detected from {incident.ip}",
                "incident_id": incident.id
            }
        ]


class SuspiciousActivityPlaybook(BasePlaybook):
    def match(self, incident: Incident) -> bool:
        return (
            incident.type == "suspicious_activity"
            and incident.severity in ("medium", "high")
        )

    def execute(self, incident: Incident) -> List[Dict[str, Any]]:
        return [
            {
                "action": "log",
                "message": f"[SOAR] Suspicious activity: {incident.ip}",
                "incident_id": incident.id
            }
        ]