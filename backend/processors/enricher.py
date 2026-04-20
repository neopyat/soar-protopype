from models.incident import Incident

# простейший blacklist (потом заменим на IOC/Threat Intel)
BLACKLIST = {"1.2.3.4"}


def enrich(incident: Incident) -> Incident:
    ip = incident.ip

    # -------------------------
    # THREAT INTEL
    # -------------------------
    if ip in BLACKLIST:
        incident.threat = "known_bad"

    # -------------------------
    # MITRE ATT&CK mapping
    # -------------------------
    if incident.type == "bruteforce":
        incident.mitre = "T1110"

    elif incident.type == "port_scan":
        incident.mitre = "T1046"

    elif incident.type == "suspicious_activity":
        incident.mitre = "T1078"  # пример

    return incident