from typing import List, Dict, Any, Optional

from analyzers.base import BaseAnalyzer
from responders.base import BaseResponder
from playbooks.engine import PlaybookEngine
from storage.repository import IncidentRepository

from models.event import Event
from models.incident import Incident

from processors.enricher import enrich


class Pipeline:
    def __init__(
        self,
        analyzers: List[BaseAnalyzer],
        playbook_engine: Optional[PlaybookEngine],
        responders: List[BaseResponder],
        storage: IncidentRepository,
        debug: bool = False,
    ) -> None:
        self.analyzers = analyzers
        self.playbook_engine = playbook_engine
        self.responders = responders
        self.storage = storage
        self.debug = debug

    def process(self, events: List[Event]) -> Dict[str, int]:
        incidents: List[Incident] = []

        # -------------------------
        # ANALYZE (FIXED: batch mode)
        # -------------------------
        for analyzer in self.analyzers:
            try:
                results = analyzer.analyze(events)

                if not results:
                    continue

                for inc in results:
                    try:
                        enriched_inc: Incident = enrich(inc)
                    except Exception:
                        enriched_inc = inc

                    incidents.append(enriched_inc)

            except Exception as e:
                print(f"[Analyzer Error] {analyzer.__class__.__name__}: {e}")

        # -------------------------
        # STORAGE
        # -------------------------
        if incidents:
            try:
                self.storage.save(incidents)
            except Exception as e:
                print(f"[Storage Error] {e}")

        # -------------------------
        # PLAYBOOK ENGINE
        # -------------------------
        actions: List[Dict[str, Any]] = []

        if self.playbook_engine:
            try:
                actions = self.playbook_engine.process(incidents)
            except Exception as e:
                print(f"[Playbook Engine Error] {e}")

        # -------------------------
        # RESPONDERS
        # -------------------------
        for responder in self.responders:
            try:
                responder.respond(actions)
            except Exception as e:
                print(f"[Responder Error] {responder.__class__.__name__}: {e}")

        # -------------------------
        # DEBUG
        # -------------------------
        if self.debug:
            print("\n========== SOAR DEBUG ==========")
            print(f"[+] Events: {len(events)}")
            print(f"[+] Incidents: {len(incidents)}")
            print(f"[+] Actions: {len(actions)}")

            for inc in incidents:
                print(
                    f"• {inc.type} | IP={inc.ip} | "
                    f"severity={inc.severity} | "
                    f"mitre={inc.mitre} ({getattr(inc, 'mitre_name', '')}) | "
                    f"threat={inc.threat}"
                )

            print("================================\n")

        return {
            "events": len(events),
            "incidents": len(incidents),
            "actions": len(actions),
        }

# from typing import List, Dict, Any, Optional, Union

# from analyzers.base import BaseAnalyzer
# from responders.base import BaseResponder
# from playbooks.engine import PlaybookEngine
# from storage.repository import IncidentRepository

# from models.event import Event
# from models.incident import Incident

# from processors.enricher import enrich


# class Pipeline:
#     def __init__(
#         self,
#         analyzers: List[BaseAnalyzer],
#         playbook_engine: Optional[PlaybookEngine],
#         responders: List[BaseResponder],
#         storage: IncidentRepository,
#         debug: bool = False,
#     ) -> None:
#         self.analyzers = analyzers
#         self.playbook_engine = playbook_engine
#         self.responders = responders
#         self.storage = storage
#         self.debug = debug

#     def process(self, events: List[Event]) -> Dict[str, int]:
#         incidents: List[Incident] = []

#         # -------------------------
#         # ANALYZE
#         # -------------------------
#         for analyzer in self.analyzers:
#             for event in events:
#                 try:
#                     result: Optional[Union[Incident, List[Incident]]] = analyzer.analyze(event)
#                 except Exception as e:
#                     print(f"[Analyzer Error] {analyzer.__class__.__name__}: {e}")
#                     continue

#                 if result is None:
#                     continue

#                 # нормализация результата
#                 if isinstance(result, list):
#                     result_list: List[Incident] = result
#                 else:
#                     result_list = [result]

#                 for inc in result_list:
#                     try:
#                         enriched_inc: Incident = enrich(inc)
#                     except Exception:
#                         enriched_inc = inc

#                     incidents.append(enriched_inc)

#         # -------------------------
#         # STORAGE
#         # -------------------------
#         if incidents:
#             try:
#                 self.storage.save(incidents)
#             except Exception as e:
#                 print(f"[Storage Error] {e}")

#         # -------------------------
#         # PLAYBOOK ENGINE
#         # -------------------------
#         actions: List[Dict[str, Any]] = []

#         if self.playbook_engine:
#             try:
#                 actions = self.playbook_engine.process(incidents)
#             except Exception as e:
#                 print(f"[Playbook Engine Error] {e}")

#         # -------------------------
#         # RESPONDERS
#         # -------------------------
#         for responder in self.responders:
#             try:
#                 responder.respond(actions)
#             except Exception as e:
#                 print(f"[Responder Error] {responder.__class__.__name__}: {e}")

#         # -------------------------
#         # DEBUG
#         # -------------------------
#         if self.debug:
#             print("\n========== SOAR DEBUG ==========")
#             print(f"[+] Events: {len(events)}")
#             print(f"[+] Incidents: {len(incidents)}")
#             print(f"[+] Actions: {len(actions)}")

#             for inc in incidents:
#                 print(
#                     f"• {inc.type} | IP={inc.ip} | "
#                     f"severity={inc.severity} | "
#                     f"mitre={inc.mitre} ({getattr(inc, 'mitre_name', '')}) | "
#                     f"threat={inc.threat}"
#                 )

#             print("================================\n")

#         return {
#             "events": len(events),
#             "incidents": len(incidents),
#             "actions": len(actions),
#         }

# from typing import List, Iterable, Optional, Union, Dict, Any, cast

# from core.threat_intel import ThreatIntel
# from core.mitre import MitreAttack
# from processors.normalizer import normalize


# class Pipeline:
#     def __init__(
#         self,
#         collectors: List[Any],
#         analyzers: List[Any],
#         playbooks: List[Any],
#         responders: List[Any],
#     ) -> None:
#         self.collectors = collectors
#         self.analyzers = analyzers
#         self.playbooks = playbooks
#         self.responders = responders

#         self.threat_intel = ThreatIntel()
#         self.mitre = MitreAttack()

#         self._init_intelligence()

#     def _init_intelligence(self) -> None:
#         print("[*] Loading Threat Intelligence...")
#         self.threat_intel.load_feeds()

#         print("[*] Loading MITRE ATT&CK...")
#         self.mitre.load()

#     def run(self) -> None:
#         raw_events: List[Any] = []

#         for collector in self.collectors:
#             try:
#                 collected: Optional[Iterable[Any]] = collector.collect()
#                 if collected:
#                     raw_events.extend(list(collected))
#             except Exception as e:
#                 print(f"[Collector Error] {e}")

#         if not raw_events:
#             print("[DEBUG] No events received")
#             return

#         try:
#             events: List[Any] = list(normalize(raw_events))
#         except Exception as e:
#             print(f"[Normalizer Error] {e}")
#             return

#         incidents: List[Any] = []

#         for analyzer in self.analyzers:
#             for event in events:
#                 try:
#                     analysis_result: Optional[Union[Any, List[Any]]] = analyzer.analyze(event)
#                 except Exception as e:
#                     print(f"[Analyzer Error] {e}")
#                     continue

#                 if not analysis_result:
#                     continue

#                 if isinstance(analysis_result, list):
#                     inc_list = cast(List[Any], analysis_result)
#                     for inc in inc_list:
#                         self._enrich_incident(inc)
#                         incidents.append(inc)
#                 else:
#                     self._enrich_incident(analysis_result)
#                     incidents.append(analysis_result)

#         actions: List[Dict[str, Any]] = []

#         for playbook in self.playbooks:
#             for incident in incidents:
#                 try:
#                     playbook_result: Optional[List[Dict[str, Any]]] = playbook.run(incident)
#                 except Exception as e:
#                     print(f"[Playbook Error] {e}")
#                     continue

#                 if playbook_result:
#                     actions.extend(playbook_result)

#         for responder in self.responders:
#             try:
#                 responder.respond(actions)
#             except Exception as e:
#                 print(f"[Responder Error] {e}")

#         self._debug(events, incidents, actions)

#     def _enrich_incident(self, inc: Any) -> None:
#         try:
#             ip = getattr(inc, "ip", None)

#             if isinstance(ip, str):
#                 if self.threat_intel.is_malicious(ip):
#                     setattr(inc, "threat", "known_bad_ip")
#                     setattr(inc, "severity", "high")

#             mitre_id = getattr(inc, "mitre", None)
#             if isinstance(mitre_id, str):
#                 setattr(inc, "mitre_name", self.mitre.get(mitre_id))

#         except Exception as e:
#             print(f"[Enrichment Error] {e}")

#     def _debug(
#         self,
#         events: List[Any],
#         incidents: List[Any],
#         actions: List[Dict[str, Any]],
#     ) -> None:
#         print("\n========== SOAR DEBUG ==========")
#         print(f"[+] Events received: {len(events)}")
#         print(f"[+] Incidents detected: {len(incidents)}")

#         print("\n--- Incidents ---")
#         for inc in incidents:
#             print(
#                 f"• {getattr(inc, 'type', None)} | "
#                 f"IP={getattr(inc, 'ip', None)} | "
#                 f"severity={getattr(inc, 'severity', None)} | "
#                 f"mitre={getattr(inc, 'mitre', None)} "
#                 f"({getattr(inc, 'mitre_name', '')}) | "
#                 f"threat={getattr(inc, 'threat', None)}"
#             )

#         print("\n--- Actions ---")
#         if not actions:
#             print("• No actions executed")
#         else:
#             for action in actions:
#                 print(f"• {action}")

#         print("================================\n")


# from typing import List, Any

# from core.threat_intel import ThreatIntel
# from core.mitre import MitreAttack
# from processors.normalizer import normalize


# class Pipeline:
#     def __init__(
#         self,
#         collectors: List[Any],
#         analyzers: List[Any],
#         playbooks: List[Any],
#         responders: List[Any],
#     ) -> None:
#         self.collectors = collectors
#         self.analyzers = analyzers
#         self.playbooks = playbooks
#         self.responders = responders

#         self.threat_intel = ThreatIntel()
#         self.mitre = MitreAttack()

#         self._init_intelligence()

#     def _init_intelligence(self) -> None:
#         print("[*] Loading Threat Intelligence...")
#         self.threat_intel.load_feeds()

#         print("[*] Loading MITRE ATT&CK...")
#         self.mitre.load()

#     def run(self) -> None:
#         raw_events: List[Any] = []

#         # === COLLECT ===
#         for collector in self.collectors:
#             collected = collector.collect()
#             if collected:
#                 raw_events.extend(collected)

#         if not raw_events:
#             print("[DEBUG] No events received")
#             return

#         # === NORMALIZE (КЛЮЧЕВОЙ ФИКС) ===
#         events = normalize(raw_events)

#         incidents: List[Any] = []

#         # === ANALYZE ===
#         for analyzer in self.analyzers:
#             for event in events:
#                 try:
#                     inc = analyzer.analyze(event)
#                 except Exception as e:
#                     print(f"[Analyzer Error] {e}")
#                     continue

#                 if inc:
#                     # THREAT INTEL
#                     ip = getattr(inc, "ip", None)
#                     if isinstance(ip, str):
#                         if self.threat_intel.is_malicious(ip):
#                             setattr(inc, "threat", "known_bad_ip")
#                             setattr(inc, "severity", "high")

#                     # MITRE
#                     mitre_id = getattr(inc, "mitre", None)
#                     if isinstance(mitre_id, str):
#                         setattr(inc, "mitre_name", self.mitre.get(mitre_id))

#                     incidents.append(inc)

#         actions: List[Any] = []

#         # === PLAYBOOKS ===
#         for playbook in self.playbooks:
#             for incident in incidents:
#                 try:
#                     result = playbook.run(incident)
#                 except Exception as e:
#                     print(f"[Playbook Error] {e}")
#                     continue

#                 if result:
#                     actions.extend(result)

#         # === RESPONDERS ===
#         for responder in self.responders:
#             try:
#                 responder.respond(actions)
#             except Exception as e:
#                 print(f"[Responder Error] {e}")

#         self._debug(events, incidents, actions)

#     def _debug(self, events: List[Any], incidents: List[Any], actions: List[Any]) -> None:
#         print("\n========== SOAR DEBUG ==========")
#         print(f"[+] Events received: {len(events)}")
#         print(f"[+] Incidents detected: {len(incidents)}")

#         print("\n--- Incidents ---")
#         for inc in incidents:
#             print(
#                 f"• {getattr(inc, 'type', None)} | "
#                 f"IP={getattr(inc, 'ip', None)} | "
#                 f"severity={getattr(inc, 'severity', None)} | "
#                 f"mitre={getattr(inc, 'mitre', None)} "
#                 f"({getattr(inc, 'mitre_name', '')}) | "
#                 f"threat={getattr(inc, 'threat', None)}"
#             )

#         print("\n--- Actions ---")
#         if not actions:
#             print("• No actions executed")
#         else:
#             for action in actions:
#                 print(f"• {action}")

#         print("================================\n")


# from typing import List, Any

# from core.threat_intel import ThreatIntel
# from core.mitre import MitreAttack


# class Pipeline:
#     def __init__(
#         self,
#         collectors: List[Any],
#         analyzers: List[Any],
#         playbooks: List[Any],
#         responders: List[Any],
#     ) -> None:
#         self.collectors = collectors
#         self.analyzers = analyzers
#         self.playbooks = playbooks
#         self.responders = responders

#         self.threat_intel = ThreatIntel()
#         self.mitre = MitreAttack()

#         self._init_intelligence()

#     def _init_intelligence(self) -> None:
#         print("[*] Loading Threat Intelligence...")
#         self.threat_intel.load_feeds()

#         print("[*] Loading MITRE ATT&CK...")
#         self.mitre.load()

#     def run(self) -> None:
#         events: List[Any] = []

#         for collector in self.collectors:
#             collected = collector.collect()
#             if collected:
#                 events.extend(collected)

#         if not events:
#             print("[DEBUG] No events received")
#             return

#         incidents: List[Any] = []

#         for analyzer in self.analyzers:
#             for event in events:
#                 inc = analyzer.analyze(event)

#                 if inc:
#                     # THREAT INTEL
#                     ip = getattr(inc, "ip", None)
#                     if isinstance(ip, str):
#                         if self.threat_intel.is_malicious(ip):
#                             setattr(inc, "threat", "known_bad_ip")
#                             setattr(inc, "severity", "high")

#                     # MITRE
#                     mitre_id = getattr(inc, "mitre", None)
#                     if isinstance(mitre_id, str):
#                         setattr(inc, "mitre_name", self.mitre.get(mitre_id))

#                     incidents.append(inc)

#         actions: List[Any] = []

#         for playbook in self.playbooks:
#             for incident in incidents:
#                 result = playbook.run(incident)
#                 if result:
#                     actions.extend(result)

#         for responder in self.responders:
#             responder.respond(actions)

#         self._debug(events, incidents, actions)

#     def _debug(self, events: List[Any], incidents: List[Any], actions: List[Any]) -> None:
#         print("\n========== SOAR DEBUG ==========")
#         print(f"[+] Events received: {len(events)}")
#         print(f"[+] Incidents detected: {len(incidents)}")

#         print("\n--- Incidents ---")
#         for inc in incidents:
#             print(
#                 f"• {getattr(inc, 'type', None)} | "
#                 f"IP={getattr(inc, 'ip', None)} | "
#                 f"severity={getattr(inc, 'severity', None)} | "
#                 f"mitre={getattr(inc, 'mitre', None)} "
#                 f"({getattr(inc, 'mitre_name', '')}) | "
#                 f"threat={getattr(inc, 'threat', None)}"
#             )

#         print("\n--- Actions ---")
#         if not actions:
#             print("• No actions executed")
#         else:
#             for action in actions:
#                 print(f"• {action}")

#         print("================================\n")

# from typing import List, Any, Dict

# from models.event import Event
# from models.incident import Incident
# from processors.enricher import enrich
# from core.executor import ActionExecutor


# class Pipeline:
#     def __init__(
#         self,
#         analyzers: List[Any],
#         playbook_engine: Any,
#         responders: List[Any],  # оставляем для совместимости, но НЕ используем
#         storage: Any,
#         debug: bool = False
#     ):
#         self.analyzers = analyzers
#         self.playbook_engine = playbook_engine
#         self.storage = storage
#         self.debug = debug

#         # новый слой исполнения
#         self.executor = ActionExecutor()

#     def process(self, events: List[Event]) -> Dict[str, Any]:
#         incidents: List[Incident] = []

#         # -------------------------
#         # DETECTION
#         # -------------------------
#         for analyzer in self.analyzers:
#             try:
#                 result = analyzer.analyze(events)
#                 if result:
#                     incidents.extend(result)
#             except Exception as e:
#                 print(f"[!] Analyzer error: {e}")

#         # -------------------------
#         # ENRICHMENT
#         # -------------------------
#         enriched_incidents: List[Incident] = []

#         for inc in incidents:
#             try:
#                 enriched = enrich(inc)
#                 enriched_incidents.append(enriched)
#             except Exception as e:
#                 print(f"[!] Enrichment error: {e}")
#                 enriched_incidents.append(inc)

#         # -------------------------
#         # PLAYBOOKS
#         # -------------------------
#         actions: List[Dict[str, Any]] = []

#         if self.playbook_engine:
#             try:
#                 actions = self.playbook_engine.process(enriched_incidents)
#             except Exception as e:
#                 print(f"[!] Playbook error: {e}")

#         # -------------------------
#         # EXECUTION (вместо responders)
#         # -------------------------
#         try:
#             self.executor.execute(actions)
#         except Exception as e:
#             print(f"[!] Execution error: {e}")

#         # -------------------------
#         # STORAGE
#         # -------------------------
#         if self.storage:
#             try:
#                 self.storage.save(enriched_incidents)
#             except Exception as e:
#                 print(f"[!] Storage error: {e}")

#         # -------------------------
#         # DEBUG OUTPUT
#         # -------------------------
#         if self.debug:
#             print("\n========== SOAR DEBUG ==========")
#             print(f"[+] Events received: {len(events)}")
#             print(f"[+] Incidents detected: {len(enriched_incidents)}")

#             if enriched_incidents:
#                 print("\n--- Incidents ---")
#                 for inc in enriched_incidents:
#                     print(
#                         f"• {inc.type} | IP={inc.ip} | "
#                         f"severity={inc.severity} | mitre={inc.mitre}"
#                     )

#             if actions:
#                 print("\n--- Actions ---")
#                 for act in actions:
#                     print(f"• {act}")
#             else:
#                 print("\n--- Actions ---")
#                 print("• No actions executed")

#             print("================================\n")

#         return {
#             "events": len(events),
#             "incidents": len(enriched_incidents),
#             "actions": len(actions),
#         }

# from typing import List, Any, Dict

# from models.event import Event
# from models.incident import Incident
# from processors.enricher import enrich


# class Pipeline:
#     def __init__(
#         self,
#         analyzers: List[Any],
#         playbook_engine: Any,
#         responders: List[Any],
#         storage: Any,
#         debug: bool = False
#     ):
#         self.analyzers = analyzers
#         self.playbook_engine = playbook_engine
#         self.responders = responders
#         self.storage = storage
#         self.debug = debug

#     def process(self, events: List[Event]) -> Dict[str, Any]:
#         incidents: List[Incident] = []

#         # -------------------------
#         # DETECTION
#         # -------------------------
#         for analyzer in self.analyzers:
#             try:
#                 result = analyzer.analyze(events)
#                 if result:
#                     incidents.extend(result)
#             except Exception as e:
#                 print(f"[!] Analyzer error: {e}")

#         # -------------------------
#         # ENRICHMENT
#         # -------------------------
#         enriched_incidents: List[Incident] = []

#         for inc in incidents:
#             try:
#                 enriched = enrich(inc)
#                 enriched_incidents.append(enriched)
#             except Exception as e:
#                 print(f"[!] Enrichment error: {e}")
#                 enriched_incidents.append(inc)

#         # -------------------------
#         # PLAYBOOKS
#         # -------------------------
#         actions: List[Dict[str, Any]] = []

#         if self.playbook_engine:
#             try:
#                 actions = self.playbook_engine.process(enriched_incidents)
#             except Exception as e:
#                 print(f"[!] Playbook error: {e}")

#         # -------------------------
#         # RESPONDERS
#         # -------------------------
#         for responder in self.responders:
#             try:
#                 responder.respond(actions)
#             except Exception as e:
#                 print(f"[!] Responder error: {e}")

#         # -------------------------
#         # STORAGE
#         # -------------------------
#         if self.storage:
#             try:
#                 self.storage.save(enriched_incidents)
#             except Exception as e:
#                 print(f"[!] Storage error: {e}")

#         # -------------------------
#         # DEBUG OUTPUT
#         # -------------------------
#         if self.debug:
#             print("\n========== SOAR DEBUG ==========")
#             print(f"[+] Events received: {len(events)}")
#             print(f"[+] Incidents detected: {len(enriched_incidents)}")

#             if enriched_incidents:
#                 print("\n--- Incidents ---")
#                 for inc in enriched_incidents:
#                     print(f"• {inc.type} | IP={inc.ip} | severity={inc.severity} | mitre={inc.mitre}")

#             if actions:
#                 print("\n--- Actions ---")
#                 for act in actions:
#                     print(f"• {act}")
#             else:
#                 print("\n--- Actions ---")
#                 print("• No actions executed")

#             print("================================\n")

#         return {
#             "events": len(events),
#             "incidents": len(enriched_incidents),
#             "actions": len(actions),
#         }