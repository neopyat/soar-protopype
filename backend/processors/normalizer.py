from typing import List, Dict, Any

from models.event import Event


def normalize(raw_events: List[Dict[str, Any]]) -> List[Event]:
    events: List[Event] = []

    for e in raw_events:
        try:
            event = Event(
                type=str(e.get("type", "")),
                ip=str(e.get("ip", "")),
                timestamp=float(e.get("timestamp", 0.0)),
                raw=str(e.get("raw", ""))
            )
            events.append(event)
        except Exception:
            continue

    return events

# from typing import List, Dict, Any

# from models.event import Event


# def normalize(raw_events: List[Dict[str, Any]]) -> List[Event]:
#     events: List[Event] = []

#     for e in raw_events:
#         try:
#             event = Event(
#                 type=str(e.get("type", "")),
#                 ip=str(e.get("ip", "")),
#                 timestamp=float(e.get("timestamp", 0.0)),
#                 raw=str(e.get("raw", ""))
#             )
#             events.append(event)
#         except Exception:
#             continue

#     return events