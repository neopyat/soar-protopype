import time
from typing import List, Dict, Any, cast

from collectors.base import BaseCollector
from core.pipeline import Pipeline
from models.event import Event


class SOAREngine:
    def __init__(
        self,
        collectors: List[BaseCollector],
        pipeline: Pipeline,
        interval: int = 2,
        debug: bool = False,
    ) -> None:
        self.collectors = collectors
        self.pipeline = pipeline
        self.interval = interval
        self.debug = debug
        self._running = False

    # -------------------------
    # START / STOP
    # -------------------------
    def start(self) -> None:
        print("[*] SOAR Engine started")
        self._running = True

        try:
            while self._running:
                start_time = time.time()

                events = self._collect_events()

                if not events:
                    if self.debug:
                        print("[DEBUG] No events")
                    time.sleep(self.interval)
                    continue

                stats = self.pipeline.process(events)

                if self.debug:
                    duration = time.time() - start_time

                    print("\n========== SOAR DEBUG ==========")
                    print(f"[+] Events: {stats.get('events')}")
                    print(f"[+] Incidents: {stats.get('incidents')}")
                    print(f"[+] Actions: {stats.get('actions')}")
                    print(f"[DEBUG] time={round(duration, 4)}s")
                    print("================================\n")

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("\n[*] SOAR stopped by user")
            self.stop()

    def stop(self) -> None:
        self._running = False

    # -------------------------
    # COLLECT EVENTS
    # -------------------------
    def _collect_events(self) -> List[Event]:
        events: List[Event] = []

        for collector in self.collectors:
            try:
                raw_events = collector.collect()

                if not raw_events:
                    continue

                for item in raw_events:
                    try:
                        event = self._normalize_event(item)
                        events.append(event)
                    except Exception as e:
                        print(f"[Normalize Error] {e}")

            except Exception as e:
                print(f"[Collector Error] {collector.__class__.__name__}: {e}")

        return events

    # -------------------------
    # NORMALIZE (dict → Event)
    # -------------------------
    def _normalize_event(self, data: Any) -> Event:
        if isinstance(data, Event):
            return data

        if isinstance(data, dict):
            data_dict = cast(Dict[str, Any], data)

            return Event(
                type=data_dict.get("type", "unknown"),
                ip=data_dict.get("ip"),
                timestamp=data_dict.get("timestamp"),
            )

        raise ValueError(f"Unsupported event format: {type(data)}")

