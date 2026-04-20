# models/incident.py

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
    ):
        # базовые поля
        self.id: str = incident_id or str(uuid.uuid4())
        self.type: str = type
        self.ip: str = ip
        self.severity: str = severity

        # временная метка
        self.timestamp: float = timestamp or time.time()

        # связанные события (очень важно для диплома)
        self.events: List[Event] = events or []

        # статус инцидента
        self.status: str = "open"

        # обогащение / аналитика
        self.mitre: Optional[str] = None
        self.threat: Optional[str] = None

        # дополнительные данные (расширяемость)
        self.meta: Dict[str, Any] = {}

    # -------------------------
    # Работа с событиями
    # -------------------------
    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def add_events(self, events: List[Event]) -> None:
        self.events.extend(events)

    # -------------------------
    # Управление статусом
    # -------------------------
    def close(self) -> None:
        self.status = "closed"

    # -------------------------
    # Сериализация
    # -------------------------
    def to_dict(self) -> Dict[str, Any]:
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
            "events": [e.to_dict() for e in self.events],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Incident":
        events_data = data.get("events", [])
        events = [Event.from_dict(e) for e in events_data]

        inc = cls(
            type=str(data.get("type", "")),
            ip=str(data.get("ip", "")),
            severity=str(data.get("severity", "low")),
            events=events,
            timestamp=float(data.get("timestamp", time.time())),
            incident_id=str(data.get("id", "")) or None,
        )

        inc.status = str(data.get("status", "open"))
        inc.mitre = data.get("mitre")
        inc.threat = data.get("threat")
        inc.meta = data.get("meta", {})

        return inc

    # -------------------------
    # Debug
    # -------------------------
    def __repr__(self) -> str:
        return (
            f"<Incident id={self.id[:8]} "
            f"type={self.type} "
            f"ip={self.ip} "
            f"severity={self.severity} "
            f"events={len(self.events)}>"
        )