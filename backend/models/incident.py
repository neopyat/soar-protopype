import time
import uuid
from typing import List, Dict, Any, Optional

from models.event import Event


class Incident:
    def __init__(
        self,
        type: str,
        ip: str,
        severity: str = "low",
        events: Optional[List[Event]] = None,
        timestamp: Optional[float] = None,
        incident_id: Optional[str] = None,
    ) -> None:
        # базовые поля
        self.id: str = incident_id if incident_id is not None else str(uuid.uuid4())
        self.type: str = str(type)
        self.ip: str = str(ip)

        # нормализация severity
        self.severity: str = self._normalize_severity(severity)

        # timestamp
        self.timestamp: float = timestamp if timestamp is not None else time.time()

        # 🔴 КЛЮЧ: строго типизированный список
        if events is None:
            self.events: List[Event] = []
        else:
            self.events = list(events)

        # статус
        self.status: str = "open"

        # аналитика
        self.mitre: Optional[str] = None
        self.threat: Optional[str] = None

        # мета
        self.meta: Dict[str, Any] = {}

    # -------------------------
    # ВСПОМОГАТЕЛЬНОЕ
    # -------------------------
    def _normalize_severity(self, severity: str) -> str:
        allowed = {"low", "medium", "high", "critical"}
        s = str(severity).lower()
        return s if s in allowed else "low"

    # -------------------------
    # EVENTS
    # -------------------------
    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def add_events(self, events: List[Event]) -> None:
        self.events.extend(events)

    # -------------------------
    # STATUS
    # -------------------------
    def close(self) -> None:
        self.status = "closed"

    # -------------------------
    # SERIALIZATION
    # -------------------------
    def to_dict(self) -> Dict[str, Any]:
        events_serialized: List[Dict[str, Any]] = []

        for e in self.events:
            try:
                events_serialized.append(e.to_dict())
            except Exception:
                continue

        return {
            "id": self.id,
            "type": self.type,
            "ip": self.ip,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "status": self.status,
            "mitre": self.mitre,
            "threat": self.threat,
            "meta": self.meta,
            "events": events_serialized,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Incident":
        raw_events = data.get("events", [])

        events: List[Event] = []
        for e in raw_events:
            try:
                events.append(Event.from_dict(e))
            except Exception:
                continue

        inc = cls(
            type=str(data.get("type", "")),
            ip=str(data.get("ip", "")),
            severity=str(data.get("severity", "low")),
            events=events,
            timestamp=float(data.get("timestamp", time.time())),
            incident_id=str(data.get("id")) if data.get("id") else None,
        )

        inc.status = str(data.get("status", "open"))
        inc.mitre = data.get("mitre")
        inc.threat = data.get("threat")

        meta = data.get("meta")
        inc.meta = meta if isinstance(meta, dict) else {}

        return inc

    # -------------------------
    # DEBUG
    # -------------------------
    def __repr__(self) -> str:
        return (
            f"<Incident id={self.id[:8]} "
            f"type={self.type} "
            f"ip={self.ip} "
            f"severity={self.severity} "
            f"events={len(self.events)}>"
        )


