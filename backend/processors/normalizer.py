from typing import Dict, Any

from models.event import Event


def normalize(data: Dict[str, Any]) -> Event:
    """
    Преобразует сырой dict → Event
    (используется если захочешь вынести нормализацию из engine)
    """

    type_val = str(data.get("type", "unknown"))

    ip_raw = data.get("ip")
    ip_val = str(ip_raw) if ip_raw is not None else None

    timestamp_raw = data.get("timestamp", 0.0)
    if isinstance(timestamp_raw, (int, float)):
        timestamp_val = float(timestamp_raw)
    else:
        timestamp_val = 0.0

    raw_val = data

    return Event(
        type=type_val,
        ip=ip_val,
        timestamp=timestamp_val,
        raw=raw_val,
    )

