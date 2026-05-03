from typing import List, Dict, Any
from datetime import datetime, timezone

from models.event import Event


def normalize(raw_events: List[Dict[str, Any]]) -> List[Event]:
    """
    Преобразует сырые события (dict) в объекты Event
    Это ЕДИНСТВЕННОЕ место, где создаётся Event
    """

    normalized_events: List[Event] = []

    for e in raw_events:
        try:
            # === TIMESTAMP ===
            ts = e.get("timestamp")

            if ts is None:
                timestamp = datetime.now(timezone.utc).timestamp()
            elif isinstance(ts, (int, float)):
                timestamp = float(ts)
            elif isinstance(ts, str):
                try:
                    timestamp = datetime.fromisoformat(ts).timestamp()
                except Exception:
                    timestamp = datetime.now(timezone.utc).timestamp()
            else:
                timestamp = datetime.now(timezone.utc).timestamp()

            # === ОСНОВНЫЕ ПОЛЯ ===
            event_type = str(e.get("type", "unknown"))
            ip = str(e.get("ip", ""))

            raw_data = e.get("raw")
            if raw_data is None:
                raw_data = str(e)

            # === СОЗДАНИЕ EVENT ===
            event = Event(
                type=event_type,
                ip=ip,
                timestamp=timestamp,
                raw=str(raw_data)
            )

            normalized_events.append(event)

        except Exception as ex:
            print(f"[Normalizer] Error: {ex} | Data: {e}")

    return normalized_events