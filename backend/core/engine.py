import time
from typing import List, Dict, Any, Optional, Iterable

from collectors.base import BaseCollector
from analyzers.base import BaseAnalyzer
from responders.base import BaseResponder
from playbooks.engine import PlaybookEngine
from playbooks.base import BasePlaybook

from storage.repository import IncidentRepository
from models.event import Event
from models.incident import Incident

from processors.normalizer import normalize


class SOAREngine:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.collectors: List[BaseCollector] = []
        self.analyzers: List[BaseAnalyzer] = []
        self.responders: List[BaseResponder] = []
        self.playbook_engine: Optional[PlaybookEngine] = None

        self.config: Dict[str, Any] = config or {}
        self.debug: bool = bool(self.config.get("debug", False))

        self.storage = IncidentRepository()

    # -------------------------
    # Registration
    # -------------------------

    def register_collector(self, collector: BaseCollector) -> None:
        self.collectors.append(collector)

    def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
        self.analyzers.append(analyzer)

    def register_responder(self, responder: BaseResponder) -> None:
        self.responders.append(responder)

    def register_playbooks(self, playbooks: List[BasePlaybook]) -> None:
        self.playbook_engine = PlaybookEngine(playbooks)

    # -------------------------
    # Collect
    # -------------------------

    def _collect(self) -> List[Event]:
        raw_events: List[Any] = []

        for collector in self.collectors:
            try:
                data: Optional[Iterable[Any]] = collector.collect()
                if data:
                    raw_events.extend(list(data))
            except Exception as e:
                print(f"[Collector Error] {collector.__class__.__name__}: {e}")

        try:
            return list(normalize(raw_events))
        except Exception as e:
            print(f"[Normalizer Error] {e}")
            return []

    # -------------------------
    # Run
    # -------------------------

    def run(self) -> None:
        start_time = time.time()

        events: List[Event] = self._collect()

        if not events:
            if self.debug:
                print("[DEBUG] No events")
            return

        incidents: List[Incident] = []

        for event in events:
            for analyzer in self.analyzers:
                try:
                    result = analyzer.analyze(event)

                    if result is None:
                        continue

                    incidents.append(result)

                except Exception as e:
                    print(f"[Analyzer Error] {analyzer.__class__.__name__}: {e}")

        # -------------------------
        # Playbooks
        # -------------------------

        actions: List[Dict[str, Any]] = []

        if self.playbook_engine and incidents:
            try:
                actions = self.playbook_engine.process(incidents)
            except Exception as e:
                print(f"[Playbook Error] {e}")

        # -------------------------
        # Responders
        # -------------------------

        for responder in self.responders:
            try:
                responder.respond(actions)
            except Exception as e:
                print(f"[Responder Error] {responder.__class__.__name__}: {e}")

        # -------------------------
        # Storage
        # -------------------------

        if incidents:
            try:
                self.storage.save(incidents)
            except Exception as e:
                print(f"[Storage Error] {e}")

        # -------------------------
        # Debug
        # -------------------------

        if self.debug:
            duration = round(time.time() - start_time, 4)

            print("\n========== SOAR DEBUG ==========")
            print(f"[+] Events: {len(events)}")
            print(f"[+] Incidents: {len(incidents)}")
            print(f"[+] Actions: {len(actions)}")

            for inc in incidents:
                print(
                    f"• {getattr(inc, 'type', None)} | "
                    f"IP={getattr(inc, 'ip', None)} | "
                    f"severity={getattr(inc, 'severity', None)}"
                )

            print(f"[DEBUG] time={duration}s")
            print("================================\n")

# import time
# from typing import List, Dict, Any, Optional

# from collectors.base import BaseCollector
# from analyzers.base import BaseAnalyzer
# from responders.base import BaseResponder

# from playbooks.engine import PlaybookEngine
# from playbooks.base import BasePlaybook

# from core.pipeline import Pipeline
# from storage.repository import IncidentRepository
# from processors.normalizer import normalize
# from models.event import Event


# class SOAREngine:
#     def __init__(self, config: Optional[Dict[str, Any]] = None):
#         self.collectors: List[BaseCollector] = []
#         self.analyzers: List[BaseAnalyzer] = []
#         self.responders: List[BaseResponder] = []
#         self.playbooks: List[BasePlaybook] = []

#         self.config: Dict[str, Any] = config or {}
#         self.debug: bool = bool(self.config.get("debug", False))

#         self.storage = IncidentRepository()
#         self.playbook_engine: Optional[PlaybookEngine] = None

#         # pipeline создаётся без playbook_engine (пока нет playbooks)
#         self.pipeline = Pipeline(
#             analyzers=self.analyzers,
#             playbook_engine=None,
#             responders=self.responders,
#             storage=self.storage,
#             debug=self.debug,
#         )

#     # -------------------------
#     # Registration
#     # -------------------------

#     def register_collector(self, collector: BaseCollector) -> None:
#         self.collectors.append(collector)

#     def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
#         self.analyzers.append(analyzer)

#     def register_responder(self, responder: BaseResponder) -> None:
#         self.responders.append(responder)

#     def register_playbooks(self, playbooks: List[BasePlaybook]) -> None:
#         self.playbooks.extend(playbooks)

#         # создаём engine
#         self.playbook_engine = PlaybookEngine(self.playbooks)

#         # 🔥 синхронизация с pipeline
#         self.pipeline.playbook_engine = self.playbook_engine

#     # -------------------------
#     # Collect
#     # -------------------------

#     def _collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         for collector in self.collectors:
#             try:
#                 data = collector.collect()
#                 if data:
#                     events.extend(data)
#             except Exception as e:
#                 self._log_error(f"Collector error ({collector.__class__.__name__}): {e}")

#         return events

#     # -------------------------
#     # Run loop
#     # -------------------------

#     def run(self) -> None:
#         print("[*] SOAR Engine started")

#         interval = int(self.config.get("loop_interval", 2))

#         while True:
#             start_time = time.time()

#             try:
#                 raw_events = self._collect()

#                 if not raw_events:
#                     if self.debug:
#                         print("[DEBUG] No events")
#                     time.sleep(interval)
#                     continue

#                 # нормализация
#                 events: List[Event] = normalize(raw_events)

#                 stats = self.pipeline.process(events)

#                 if self.debug:
#                     duration = round(time.time() - start_time, 4)
#                     print(
#                         f"[DEBUG] events={stats['events']} "
#                         f"incidents={stats['incidents']} "
#                         f"actions={stats['actions']} "
#                         f"time={duration}s"
#                     )

#             except KeyboardInterrupt:
#                 print("\n[!] Stopped")
#                 break

#             except Exception as e:
#                 self._log_error(f"Runtime error: {e}")

#             time.sleep(interval)

#     # -------------------------
#     # Utils
#     # -------------------------

#     def _log_error(self, message: str) -> None:
#         print(f"[!] {message}")

# import time
# from typing import List, Dict, Any, Optional

# from collectors.base import BaseCollector
# from analyzers.base import BaseAnalyzer
# from responders.base import BaseResponder
# from playbooks.base import BasePlaybook

# from core.pipeline import Pipeline


# class SOAREngine:
#     def __init__(self, config: Optional[Dict[str, Any]] = None):
#         self.collectors: List[BaseCollector] = []
#         self.analyzers: List[BaseAnalyzer] = []
#         self.responders: List[BaseResponder] = []
#         self.playbooks: List[BasePlaybook] = []

#         self.config: Dict[str, Any] = config or {}
#         self.debug: bool = bool(self.config.get("debug", False))

#         # ✅ ПРАВИЛЬНЫЙ pipeline (под текущую архитектуру)
#         self.pipeline = Pipeline(
#             collectors=self.collectors,
#             analyzers=self.analyzers,
#             playbooks=self.playbooks,
#             responders=self.responders,
#         )

#     # -------------------------
#     # Registration
#     # -------------------------

#     def register_collector(self, collector: BaseCollector) -> None:
#         self.collectors.append(collector)

#     def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
#         self.analyzers.append(analyzer)

#     def register_responder(self, responder: BaseResponder) -> None:
#         self.responders.append(responder)

#     def register_playbooks(self, playbooks: List[BasePlaybook]) -> None:
#         self.playbooks.extend(playbooks)

#     # -------------------------
#     # Run
#     # -------------------------

#     def run(self) -> None:
#         print("[*] SOAR Engine started")

#         while True:
#             start_time = time.time()

#             try:
#                 self.pipeline.run()
#             except KeyboardInterrupt:
#                 print("\n[!] Stopped by user")
#                 break
#             except Exception as e:
#                 self._log_error(f"Pipeline error: {e}")

#             if self.debug:
#                 duration = round(time.time() - start_time, 4)
#                 print(f"[DEBUG] Cycle time: {duration}s")

#     # -------------------------
#     # Utils
#     # -------------------------

#     def _log_error(self, message: str) -> None:
#         print(f"[!] {message}")


# import time
# from typing import List, Dict, Any, Optional

# from collectors.base import BaseCollector
# from analyzers.base import BaseAnalyzer
# from responders.base import BaseResponder
# from playbooks.engine import PlaybookEngine
# from playbooks.base import BasePlaybook

# from core.pipeline import Pipeline
# from processors.normalizer import normalize
# from storage.repository import IncidentRepository
# from models.event import Event


# class SOAREngine:
#     def __init__(self, config: Optional[Dict[str, Any]] = None):
#         self.collectors: List[BaseCollector] = []
#         self.analyzers: List[BaseAnalyzer] = []
#         self.responders: List[BaseResponder] = []

#         self.playbook_engine: Optional[PlaybookEngine] = None

#         self.config: Dict[str, Any] = config or {}
#         self.debug: bool = bool(self.config.get("debug", False))

#         self.storage = IncidentRepository()

#         # ✅ ВАЖНО: передаём debug в pipeline
#         self.pipeline = Pipeline(
#             analyzers=self.analyzers,
#             playbook_engine=self.playbook_engine,
#             responders=self.responders,
#             storage=self.storage,
#             debug=self.debug
#         )

#     # -------------------------
#     # Registration
#     # -------------------------

#     def register_collector(self, collector: BaseCollector) -> None:
#         self.collectors.append(collector)

#     def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
#         self.analyzers.append(analyzer)

#     def register_responder(self, responder: BaseResponder) -> None:
#         self.responders.append(responder)

#     def register_playbooks(self, playbooks: List[BasePlaybook]) -> None:
#         self.playbook_engine = PlaybookEngine(playbooks)

#         # 🔴 синхронизация с pipeline
#         self.pipeline.playbook_engine = self.playbook_engine

#     # -------------------------
#     # Collect
#     # -------------------------

#     def _collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         for collector in self.collectors:
#             try:
#                 data = collector.collect()
#                 if data:
#                     events.extend(data)
#             except Exception as e:
#                 self._log_error(f"Collector error ({collector.__class__.__name__}): {e}")

#         return events

#     # -------------------------
#     # Run
#     # -------------------------

#     def run(self) -> None:
#         start_time = time.time()

#         raw_events = self._collect()

#         if not raw_events:
#             if self.debug:
#                 print("[DEBUG] No events received")
#             return

#         # нормализация
#         events: List[Event] = normalize(raw_events)

#         # 🔴 pipeline возвращает статистику
#         stats = self.pipeline.process(events)

#         if self.debug:
#             duration = round(time.time() - start_time, 4)

#             print("\n========= SUMMARY =========")
#             print(f"Events:    {stats['events']}")
#             print(f"Incidents: {stats['incidents']}")
#             print(f"Actions:   {stats['actions']}")
#             print(f"Time:      {duration}s")
#             print("===========================\n")

#     # -------------------------
#     # Utils
#     # -------------------------

#     def _log_error(self, message: str) -> None:
#         print(f"[!] {message}")

# import time
# from typing import List, Dict, Any, Optional

# from collectors.base import BaseCollector
# from analyzers.base import BaseAnalyzer
# from responders.base import BaseResponder
# from playbooks.engine import PlaybookEngine
# from playbooks.base import BasePlaybook

# from core.pipeline import Pipeline
# from processors.normalizer import normalize
# from storage.repository import IncidentRepository
# from models.event import Event


# class SOAREngine:
#     def __init__(self, config: Optional[Dict[str, Any]] = None):
#         self.collectors: List[BaseCollector] = []
#         self.analyzers: List[BaseAnalyzer] = []
#         self.responders: List[BaseResponder] = []

#         self.playbook_engine: Optional[PlaybookEngine] = None

#         self.config: Dict[str, Any] = config or {}
#         self.debug: bool = bool(self.config.get("debug", False))

#         # 🔴 NEW: storage + pipeline
#         self.storage = IncidentRepository()

#         self.pipeline = Pipeline(
#             analyzers=self.analyzers,
#             playbook_engine=self.playbook_engine,
#             responders=self.responders,
#             storage=self.storage
#         )

#     # -------------------------
#     # Registration
#     # -------------------------

#     def register_collector(self, collector: BaseCollector) -> None:
#         self.collectors.append(collector)

#     def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
#         self.analyzers.append(analyzer)

#     def register_responder(self, responder: BaseResponder) -> None:
#         self.responders.append(responder)

#     def register_playbooks(self, playbooks: List[BasePlaybook]) -> None:
#         self.playbook_engine = PlaybookEngine(playbooks)

#         # 🔴 важно обновить pipeline
#         self.pipeline.playbook_engine = self.playbook_engine

#     # -------------------------
#     # Pipeline stages
#     # -------------------------

#     def _collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         for collector in self.collectors:
#             try:
#                 data = collector.collect()
#                 if data:
#                     events.extend(data)
#             except Exception as e:
#                 self._log_error(f"Collector error ({collector.__class__.__name__}): {e}")

#         return events

#     # -------------------------
#     # Run cycle
#     # -------------------------

#     def run(self) -> None:
#         start_time = time.time()

#         raw_events = self._collect()

#         if not raw_events:
#             if self.debug:
#                 self._debug_log(0, 0, 0, start_time)
#             return

#         # 🔴 NORMALIZATION
#         events: List[Event] = normalize(raw_events)

#         # 🔴 PIPELINE (анализ + playbooks + responders + storage)
#         self.pipeline.process(events)

#         if self.debug:
#             duration = round(time.time() - start_time, 4)
#             print(
#                 f"[DEBUG] events={len(events)} "
#                 f"time={duration}s"
#             )

#     # -------------------------
#     # Utils
#     # -------------------------

#     def _log_error(self, message: str) -> None:
#         print(f"[!] {message}")

#     def _debug_log(self, events: int, incidents: int, actions: int, start_time: float) -> None:
#         duration = round(time.time() - start_time, 4)
#         print(
#             f"[DEBUG] events={events} "
#             f"incidents={incidents} "
#             f"actions={actions} "
#             f"time={duration}s"
#         )

# import time
# from typing import List, Dict, Any, Optional

# from collectors.base import BaseCollector
# from analyzers.base import BaseAnalyzer
# from responders.base import BaseResponder
# from playbooks.engine import PlaybookEngine
# from playbooks.base import BasePlaybook


# class SOAREngine:
#     def __init__(self, config: Optional[Dict[str, Any]] = None):
#         self.collectors: List[BaseCollector] = []
#         self.analyzers: List[BaseAnalyzer] = []
#         self.responders: List[BaseResponder] = []

#         self.playbook_engine: Optional[PlaybookEngine] = None

#         self.config: Dict[str, Any] = config or {}
#         self.debug: bool = bool(self.config.get("debug", False))

#     # -------------------------
#     # Registration
#     # -------------------------

#     def register_collector(self, collector: BaseCollector) -> None:
#         self.collectors.append(collector)

#     def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
#         self.analyzers.append(analyzer)

#     def register_responder(self, responder: BaseResponder) -> None:
#         self.responders.append(responder)

#     def register_playbooks(self, playbooks: List[BasePlaybook]) -> None:
#         self.playbook_engine = PlaybookEngine(playbooks)

#     # -------------------------
#     # Pipeline stages
#     # -------------------------

#     def _collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         for collector in self.collectors:
#             try:
#                 data = collector.collect()
#                 if data:
#                     events.extend(data)
#             except Exception as e:
#                 self._log_error(f"Collector error ({collector.__class__.__name__}): {e}")

#         return events

#     def _analyze(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         incidents: List[Dict[str, Any]] = []

#         for analyzer in self.analyzers:
#             try:
#                 result = analyzer.analyze(events)
#                 if result:
#                     incidents.extend(result)
#             except Exception as e:
#                 self._log_error(f"Analyzer error ({analyzer.__class__.__name__}): {e}")

#         return incidents

#     def _execute_playbooks(self, incidents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         if not self.playbook_engine or not incidents:
#             return []

#         try:
#             return self.playbook_engine.process(incidents)
#         except Exception as e:
#             self._log_error(f"Playbook engine error: {e}")
#             return []

#     def _respond(self, actions: List[Dict[str, Any]]) -> None:
#         if not actions:
#             return

#         for responder in self.responders:
#             try:
#                 responder.respond(actions)
#             except Exception as e:
#                 self._log_error(f"Responder error ({responder.__class__.__name__}): {e}")

#     # -------------------------
#     # Run cycle
#     # -------------------------

#     def run(self) -> None:
#         start_time = time.time()

#         events = self._collect()
#         if not events and self.debug:
#             self._debug_log(0, 0, 0, start_time)
#             return

#         incidents = self._analyze(events)
#         if not incidents and self.debug:
#             self._debug_log(len(events), 0, 0, start_time)
#             return

#         actions = self._execute_playbooks(incidents)
#         self._respond(actions)

#         if self.debug:
#             self._debug_log(len(events), len(incidents), len(actions), start_time)

#     # -------------------------
#     # Utils
#     # -------------------------

#     def _log_error(self, message: str) -> None:
#         print(f"[!] {message}")

#     def _debug_log(self, events: int, incidents: int, actions: int, start_time: float) -> None:
#         duration = round(time.time() - start_time, 4)
#         print(
#             f"[DEBUG] events={events} "
#             f"incidents={incidents} "
#             f"actions={actions} "
#             f"time={duration}s"
#         )

# import time
# from typing import List, Dict, Any, Optional

# from collectors.base import BaseCollector
# from analyzers.base import BaseAnalyzer
# from responders.base import BaseResponder
# from playbooks.engine import PlaybookEngine
# from playbooks.base import BasePlaybook


# class SOAREngine:
#     def __init__(self, config: Optional[Dict[str, Any]] = None):
#         self.collectors: List[BaseCollector] = []
#         self.analyzers: List[BaseAnalyzer] = []
#         self.responders: List[BaseResponder] = []

#         self.playbook_engine: Optional[PlaybookEngine] = None

#         self.config: Dict[str, Any] = config or {}
#         self.debug: bool = bool(self.config.get("debug", False))

#     # -------------------------
#     # Registration
#     # -------------------------

#     def register_collector(self, collector: BaseCollector) -> None:
#         self.collectors.append(collector)

#     def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
#         self.analyzers.append(analyzer)

#     def register_responder(self, responder: BaseResponder) -> None:
#         self.responders.append(responder)

#     def register_playbooks(self, playbooks: List[BasePlaybook]) -> None:
#         self.playbook_engine = PlaybookEngine(playbooks)

#     # -------------------------
#     # Pipeline stages
#     # -------------------------

#     def _collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         for collector in self.collectors:
#             try:
#                 data = collector.collect()
#                 if data:
#                     events.extend(data)
#             except Exception as e:
#                 self._log_error(f"Collector error ({collector.__class__.__name__}): {e}")

#         return events

#     def _analyze(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         incidents: List[Dict[str, Any]] = []

#         for analyzer in self.analyzers:
#             try:
#                 result = analyzer.analyze(events)
#                 if result:
#                     incidents.extend(result)
#             except Exception as e:
#                 self._log_error(f"Analyzer error ({analyzer.__class__.__name__}): {e}")

#         return incidents

#     def _execute_playbooks(self, incidents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         if not self.playbook_engine:
#             return []

#         try:
#             return self.playbook_engine.process(incidents)
#         except Exception as e:
#             self._log_error(f"Playbook engine error: {e}")
#             return []

#     def _respond(self, actions: List[Dict[str, Any]]) -> None:
#         for responder in self.responders:
#             try:
#                 responder.respond(actions)
#             except Exception as e:
#                 self._log_error(f"Responder error ({responder.__class__.__name__}): {e}")

#     # -------------------------
#     # Run cycle
#     # -------------------------

#     def run(self) -> None:
#         start_time = time.time()

#         events = self._collect()
#         incidents = self._analyze(events)
#         actions = self._execute_playbooks(incidents)
#         self._respond(actions)

#         if self.debug:
#             duration = round(time.time() - start_time, 4)
#             print(
#                 f"[DEBUG] events={len(events)} "
#                 f"incidents={len(incidents)} "
#                 f"actions={len(actions)} "
#                 f"time={duration}s"
#             )

#     # -------------------------
#     # Utils
#     # -------------------------

#     def _log_error(self, message: str) -> None:
#         print(f"[!] {message}")