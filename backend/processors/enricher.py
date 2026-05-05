from typing import Dict, Any
from models.incident import Incident


MITRE_MAP: Dict[str, str] = {
    "bruteforce": "T1110",
    "port_scan": "T1046",
    "dos_attack": "T1499",
    "resource_abuse": "T1499",
    "anomaly": "T1204",
}


MITRE_NAMES: Dict[str, str] = {
    "T1110": "Brute Force",
    "T1046": "Network Service Discovery",
    "T1499": "Endpoint Denial of Service",
    "T1204": "User Execution",
}


def enrich(incident: Incident) -> Incident:
    try:
        # -------------------------
        # MITRE
        # -------------------------
        mitre_id: str = MITRE_MAP.get(incident.type, "T0000")
        incident.mitre = mitre_id

        # ⚠️ если в модели есть поле — используем напрямую
        # если нет — просто игнорируется (не критично)
        try:
            incident.mitre_name = MITRE_NAMES.get(mitre_id, "Unknown")  # type: ignore
        except Exception:
            pass

        # -------------------------
        # THREAT (СТРОГО ПОД ТВОЮ МОДЕЛЬ → str)
        # -------------------------
        if incident.threat is None:
            threat_value: float = _calculate_threat(incident)

            # 🔴 КЛЮЧ: приведение к строке
            incident.threat = str(round(threat_value, 4))

    except Exception as e:
        print(f"[Enricher Error] {e}")

    return incident


def _calculate_threat(incident: Incident) -> float:
    severity_map: Dict[str, float] = {
        "low": 0.3,
        "medium": 0.6,
        "high": 0.9,
        "critical": 1.0,
    }

    base: float = severity_map.get(incident.severity, 0.5)

    # meta уже Dict → без isinstance
    meta: Dict[str, Any] = incident.meta

    risk_raw: Any = meta.get("risk", 0.0)

    try:
        risk: float = float(risk_raw)
    except Exception:
        risk = 0.0

    return min(1.0, base + risk * 0.5)

# import json
# from typing import Set

# from models.incident import Incident
# from paths import IOC_FILE


# def _load_blacklist() -> Set[str]:
#     if not IOC_FILE.exists():
#         return set()

#     try:
#         with open(IOC_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             return set(data.get("blacklist", []))

#     except Exception as e:
#         print(f"[!] IOC load error: {e}")
#         return set()


# def enrich(incident: Incident) -> Incident:
#     blacklist = _load_blacklist()

#     # Threat intel
#     if incident.ip in blacklist:
#         incident.threat = "known_bad"

#     # MITRE mapping
#     if incident.type == "bruteforce":
#         incident.mitre = "T1110"

#     elif incident.type == "port_scan":
#         incident.mitre = "T1046"

#     elif incident.type == "suspicious_activity":
#         incident.mitre = "T1078"

#     return incident

# import json
# import os
# from typing import Set

# from models.incident import Incident


# IOC_PATH = "ioc_list.json"


# def _load_blacklist() -> Set[str]:
#     if not os.path.exists(IOC_PATH):
#         return set()

#     try:
#         with open(IOC_PATH, "r") as f:
#             data = json.load(f)
#             return set(data.get("blacklist", []))
#     except Exception as e:
#         print(f"[!] IOC load error: {e}")
#         return set()


# def enrich(incident: Incident) -> Incident:
#     blacklist = _load_blacklist()

#     # -------------------------
#     # THREAT INTEL
#     # -------------------------
#     if incident.ip in blacklist:
#         incident.threat = "known_bad"

#     # -------------------------
#     # MITRE ATT&CK mapping
#     # -------------------------
#     if incident.type == "bruteforce":
#         incident.mitre = "T1110"

#     elif incident.type == "port_scan":
#         incident.mitre = "T1046"

#     elif incident.type == "suspicious_activity":
#         incident.mitre = "T1078"

#     return incident

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