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


class PortScanPlaybook(BasePlaybook):
    def match(self, incident: Incident) -> bool:
        return incident.type == "port_scan"

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
                "message": f"[SOAR] Port scan detected from {incident.ip}",
                "incident_id": incident.id
            }
        ]


class DoSPlaybook(BasePlaybook):
    def match(self, incident: Incident) -> bool:
        return incident.type == "dos_attack"

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
                "message": f"[SOAR] DoS attack detected from {incident.ip}",
                "incident_id": incident.id
            }
        ]


class ResourceAbusePlaybook(BasePlaybook):
    def match(self, incident: Incident) -> bool:
        return incident.type == "resource_abuse"

    def execute(self, incident: Incident) -> List[Dict[str, Any]]:
        return [
            {
                "action": "log",
                "message": f"[SOAR] High CPU usage detected ({incident.meta.get('cpu')})",
                "incident_id": incident.id
            }
        ]


class SuspiciousActivityPlaybook(BasePlaybook):
    def match(self, incident: Incident) -> bool:
        return (
            incident.type == "anomaly"
            and incident.severity in ("medium", "high")
        )

    def execute(self, incident: Incident) -> List[Dict[str, Any]]:
        actions: List[Dict[str, Any]] = [
            {
                "action": "log",
                "message": f"[SOAR] Anomaly detected from {incident.ip} (risk={incident.meta.get('risk')})",
                "incident_id": incident.id
            }
        ]

        # если высокая вероятность — блокируем
        if incident.severity == "high" and incident.ip:
            actions.append(
                {
                    "action": "block_ip",
                    "ip": incident.ip,
                    "incident_id": incident.id
                }
            )

        return actions


# from typing import List, Dict, Any

# from models.incident import Incident
# from playbooks.base import BasePlaybook


# class BruteForcePlaybook(BasePlaybook):
#     def match(self, incident: Incident) -> bool:
#         return (
#             incident.type == "bruteforce"
#             and incident.severity == "high"
#         )

#     def execute(self, incident: Incident) -> List[Dict[str, Any]]:
#         if not incident.ip:
#             return []

#         return [
#             {
#                 "action": "block_ip",
#                 "ip": incident.ip,
#                 "incident_id": incident.id
#             },
#             {
#                 "action": "log",
#                 "message": f"[SOAR] Bruteforce detected from {incident.ip}",
#                 "incident_id": incident.id
#             }
#         ]


# class SuspiciousActivityPlaybook(BasePlaybook):
#     def match(self, incident: Incident) -> bool:
#         return (
#             incident.type == "suspicious_activity"
#             and incident.severity in ("medium", "high")
#         )

#     def execute(self, incident: Incident) -> List[Dict[str, Any]]:
#         return [
#             {
#                 "action": "log",
#                 "message": f"[SOAR] Suspicious activity: {incident.ip}",
#                 "incident_id": incident.id
#             }
#         ]