import json
import os
from typing import Set

from models.incident import Incident


IOC_PATH = "ioc_list.json"


def _load_blacklist() -> Set[str]:
    if not os.path.exists(IOC_PATH):
        return set()

    try:
        with open(IOC_PATH, "r") as f:
            data = json.load(f)
            return set(data.get("blacklist", []))
    except Exception as e:
        print(f"[!] IOC load error: {e}")
        return set()


def enrich(incident: Incident) -> Incident:
    blacklist = _load_blacklist()

    # -------------------------
    # THREAT INTEL
    # -------------------------
    if incident.ip in blacklist:
        incident.threat = "known_bad"

    # -------------------------
    # MITRE ATT&CK mapping
    # -------------------------
    if incident.type == "bruteforce":
        incident.mitre = "T1110"

    elif incident.type == "port_scan":
        incident.mitre = "T1046"

    elif incident.type == "suspicious_activity":
        incident.mitre = "T1078"

    return incident

# from models.incident import Incident

# # простейший blacklist (потом заменим на IOC/Threat Intel)
# BLACKLIST = {"1.2.3.4"}


# def enrich(incident: Incident) -> Incident:
#     ip = incident.ip

#     # -------------------------
#     # THREAT INTEL
#     # -------------------------
#     if ip in BLACKLIST:
#         incident.threat = "known_bad"

#     # -------------------------
#     # MITRE ATT&CK mapping
#     # -------------------------
#     if incident.type == "bruteforce":
#         incident.mitre = "T1110"

#     elif incident.type == "port_scan":
#         incident.mitre = "T1046"

#     elif incident.type == "suspicious_activity":
#         incident.mitre = "T1078"  # пример

#     return incident