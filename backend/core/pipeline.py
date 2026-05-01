from typing import List, Any, Dict

from models.event import Event
from models.incident import Incident
from processors.enricher import enrich
from core.executor import ActionExecutor


class Pipeline:
    def __init__(
        self,
        analyzers: List[Any],
        playbook_engine: Any,
        responders: List[Any],  # оставляем для совместимости, но НЕ используем
        storage: Any,
        debug: bool = False
    ):
        self.analyzers = analyzers
        self.playbook_engine = playbook_engine
        self.storage = storage
        self.debug = debug

        # новый слой исполнения
        self.executor = ActionExecutor()

    def process(self, events: List[Event]) -> Dict[str, Any]:
        incidents: List[Incident] = []

        # -------------------------
        # DETECTION
        # -------------------------
        for analyzer in self.analyzers:
            try:
                result = analyzer.analyze(events)
                if result:
                    incidents.extend(result)
            except Exception as e:
                print(f"[!] Analyzer error: {e}")

        # -------------------------
        # ENRICHMENT
        # -------------------------
        enriched_incidents: List[Incident] = []

        for inc in incidents:
            try:
                enriched = enrich(inc)
                enriched_incidents.append(enriched)
            except Exception as e:
                print(f"[!] Enrichment error: {e}")
                enriched_incidents.append(inc)

        # -------------------------
        # PLAYBOOKS
        # -------------------------
        actions: List[Dict[str, Any]] = []

        if self.playbook_engine:
            try:
                actions = self.playbook_engine.process(enriched_incidents)
            except Exception as e:
                print(f"[!] Playbook error: {e}")

        # -------------------------
        # EXECUTION (вместо responders)
        # -------------------------
        try:
            self.executor.execute(actions)
        except Exception as e:
            print(f"[!] Execution error: {e}")

        # -------------------------
        # STORAGE
        # -------------------------
        if self.storage:
            try:
                self.storage.save(enriched_incidents)
            except Exception as e:
                print(f"[!] Storage error: {e}")

        # -------------------------
        # DEBUG OUTPUT
        # -------------------------
        if self.debug:
            print("\n========== SOAR DEBUG ==========")
            print(f"[+] Events received: {len(events)}")
            print(f"[+] Incidents detected: {len(enriched_incidents)}")

            if enriched_incidents:
                print("\n--- Incidents ---")
                for inc in enriched_incidents:
                    print(
                        f"• {inc.type} | IP={inc.ip} | "
                        f"severity={inc.severity} | mitre={inc.mitre}"
                    )

            if actions:
                print("\n--- Actions ---")
                for act in actions:
                    print(f"• {act}")
            else:
                print("\n--- Actions ---")
                print("• No actions executed")

            print("================================\n")

        return {
            "events": len(events),
            "incidents": len(enriched_incidents),
            "actions": len(actions),
        }

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