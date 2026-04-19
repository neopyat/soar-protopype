import time
from typing import List, Dict, Any, Optional

from collectors.base import BaseCollector
from analyzers.base import BaseAnalyzer
from responders.base import BaseResponder
from playbooks.engine import PlaybookEngine
from playbooks.base import BasePlaybook


class SOAREngine:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.collectors: List[BaseCollector] = []
        self.analyzers: List[BaseAnalyzer] = []
        self.responders: List[BaseResponder] = []

        self.playbook_engine: Optional[PlaybookEngine] = None

        self.config: Dict[str, Any] = config or {}
        self.debug: bool = bool(self.config.get("debug", False))

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
    # Pipeline stages
    # -------------------------

    def _collect(self) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []

        for collector in self.collectors:
            try:
                data = collector.collect()
                if data:
                    events.extend(data)
            except Exception as e:
                self._log_error(f"Collector error ({collector.__class__.__name__}): {e}")

        return events

    def _analyze(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        incidents: List[Dict[str, Any]] = []

        for analyzer in self.analyzers:
            try:
                result = analyzer.analyze(events)
                if result:
                    incidents.extend(result)
            except Exception as e:
                self._log_error(f"Analyzer error ({analyzer.__class__.__name__}): {e}")

        return incidents

    def _execute_playbooks(self, incidents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self.playbook_engine or not incidents:
            return []

        try:
            return self.playbook_engine.process(incidents)
        except Exception as e:
            self._log_error(f"Playbook engine error: {e}")
            return []

    def _respond(self, actions: List[Dict[str, Any]]) -> None:
        if not actions:
            return

        for responder in self.responders:
            try:
                responder.respond(actions)
            except Exception as e:
                self._log_error(f"Responder error ({responder.__class__.__name__}): {e}")

    # -------------------------
    # Run cycle
    # -------------------------

    def run(self) -> None:
        start_time = time.time()

        events = self._collect()
        if not events and self.debug:
            self._debug_log(0, 0, 0, start_time)
            return

        incidents = self._analyze(events)
        if not incidents and self.debug:
            self._debug_log(len(events), 0, 0, start_time)
            return

        actions = self._execute_playbooks(incidents)
        self._respond(actions)

        if self.debug:
            self._debug_log(len(events), len(incidents), len(actions), start_time)

    # -------------------------
    # Utils
    # -------------------------

    def _log_error(self, message: str) -> None:
        print(f"[!] {message}")

    def _debug_log(self, events: int, incidents: int, actions: int, start_time: float) -> None:
        duration = round(time.time() - start_time, 4)
        print(
            f"[DEBUG] events={events} "
            f"incidents={incidents} "
            f"actions={actions} "
            f"time={duration}s"
        )

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