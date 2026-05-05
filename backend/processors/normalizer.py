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


# from typing import List, Dict, Any
# from datetime import datetime, timezone

# from models.event import Event


# def normalize(raw_events: List[Dict[str, Any]]) -> List[Event]:
#     """
#     Преобразует сырые события (dict) в объекты Event
#     Это ЕДИНСТВЕННОЕ место, где создаётся Event
#     """

#     normalized_events: List[Event] = []

#     for e in raw_events:
#         try:
#             # === TIMESTAMP ===
#             ts = e.get("timestamp")

#             if ts is None:
#                 timestamp = datetime.now(timezone.utc).timestamp()
#             elif isinstance(ts, (int, float)):
#                 timestamp = float(ts)
#             elif isinstance(ts, str):
#                 try:
#                     timestamp = datetime.fromisoformat(ts).timestamp()
#                 except Exception:
#                     timestamp = datetime.now(timezone.utc).timestamp()
#             else:
#                 timestamp = datetime.now(timezone.utc).timestamp()

#             # === ОСНОВНЫЕ ПОЛЯ ===
#             event_type = str(e.get("type", "unknown"))
#             ip = str(e.get("ip", ""))

#             raw_data = e.get("raw")
#             if raw_data is None:
#                 raw_data = str(e)

#             # === СОЗДАНИЕ EVENT ===
#             event = Event(
#                 type=event_type,
#                 ip=ip,
#                 timestamp=timestamp,
#                 raw=str(raw_data)
#             )

#             normalized_events.append(event)

#         except Exception as ex:
#             print(f"[Normalizer] Error: {ex} | Data: {e}")

#     return normalized_events