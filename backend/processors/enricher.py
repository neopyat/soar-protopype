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
