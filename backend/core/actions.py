from __future__ import annotations

from typing import Dict, Any, Optional


class Action:
    def __init__(
        self,
        action_type: str,
        target: str,
        metadata: Optional[Dict[str, Any]] = None,
        incident_id: Optional[str] = None
    ) -> None:
        self.type: str = action_type
        self.target: str = target
        self.metadata: Dict[str, Any] = metadata or {}
        self.incident_id: Optional[str] = incident_id

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        return cls(
            action_type=str(data.get("action", "")),
            target=str(data.get("ip", "")),
            metadata=data,
            incident_id=data.get("incident_id")
        )