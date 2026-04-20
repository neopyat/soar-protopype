from typing import Dict, Any


class Incident:
    def __init__(self, type: str, ip: str, severity: str = "low"):
        self.type = type
        self.ip = ip
        self.severity = severity
        self.meta: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "ip": self.ip,
            "severity": self.severity,
            "meta": self.meta
        }

    def __repr__(self) -> str:
        return f"<Incident type={self.type} ip={self.ip} severity={self.severity}>"