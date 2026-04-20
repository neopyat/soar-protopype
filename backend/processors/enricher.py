from typing import Dict, Any

# простейший blacklist (потом заменим)
BLACKLIST = {"1.2.3.4"}


def enrich(incident: Dict[str, Any]) -> Dict[str, Any]:
    ip = incident.get("ip")

    if ip in BLACKLIST:
        incident["threat"] = "known_bad"

    # MITRE mapping (базовый)
    if incident.get("type") == "bruteforce":
        incident["mitre"] = "T1110"

    if incident.get("type") == "port_scan":
        incident["mitre"] = "T1046"

    return incident