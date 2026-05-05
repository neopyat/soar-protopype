from typing import Dict, Any, Optional, Union


class Event:
    def __init__(
        self,
        type: str,
        ip: Optional[str] = None,
        timestamp: Optional[float] = None,
        raw: Optional[Union[str, Dict[str, Any]]] = None,
    ) -> None:
        self.type: str = type
        self.ip: Optional[str] = ip
        self.timestamp: float = float(timestamp) if timestamp is not None else 0.0

        # raw может быть dict → приводим к строке
        if isinstance(raw, dict):
            self.raw: str = str(raw)
        else:
            self.raw: str = raw or ""

    # -------------------------
    # SERIALIZATION
    # -------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "ip": self.ip,
            "timestamp": self.timestamp,
            "raw": self.raw,
        }

    # -------------------------
    # DESERIALIZATION
    # -------------------------
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        type_val = str(data.get("type", "unknown"))

        ip_raw = data.get("ip")
        ip_val = str(ip_raw) if ip_raw is not None else None

        timestamp_raw = data.get("timestamp", 0.0)
        if isinstance(timestamp_raw, (int, float)):
            timestamp_val = float(timestamp_raw)
        else:
            timestamp_val = 0.0

        raw_val = data.get("raw", data)

        return cls(
            type=type_val,
            ip=ip_val,
            timestamp=timestamp_val,
            raw=raw_val,
        )

    def __repr__(self) -> str:
        return f"<Event type={self.type} ip={self.ip} timestamp={self.timestamp}>"


# from typing import Dict, Any


# class Event:
#     def __init__(self, type: str, ip: str, timestamp: float, raw: str):
#         self.type = type
#         self.ip = ip
#         self.timestamp = timestamp
#         self.raw = raw

#     def to_dict(self) -> Dict[str, Any]:
#         return {
#             "type": self.type,
#             "ip": self.ip,
#             "timestamp": self.timestamp,
#             "raw": self.raw
#         }

#     @classmethod
#     def from_dict(cls, data: Dict[str, Any]) -> "Event":
#         type_val = str(data.get("type", ""))
#         ip_val = str(data.get("ip", ""))

#         timestamp_raw = data.get("timestamp", 0.0)
#         if isinstance(timestamp_raw, (int, float)):
#             timestamp_val = float(timestamp_raw)
#         else:
#             timestamp_val = 0.0

#         raw_val = str(data.get("raw", ""))

#         return cls(
#             type=type_val,
#             ip=ip_val,
#             timestamp=timestamp_val,
#             raw=raw_val
#         )

#     def __repr__(self) -> str:
#         return f"<Event type={self.type} ip={self.ip} timestamp={self.timestamp}>"