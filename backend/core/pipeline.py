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
        self.analyzers: List[BaseAnalyzer] = analyzers
        self.playbook_engine: Optional[PlaybookEngine] = playbook_engine
        self.responders: List[BaseResponder] = responders
        self.storage: IncidentRepository = storage
        self.debug: bool = debug

    def process(self, events: List[Event]) -> Dict[str, int]:
        incidents: List[Incident] = []

        # -------------------------
        # ANALYZE (event-by-event)
        # -------------------------
        for event in events:
            for analyzer in self.analyzers:
                try:
                    result: Optional[Incident] = analyzer.analyze(event)

                    if result is None:
                        continue

                    # enrichment
                    try:
                        enriched_inc: Incident = enrich(result)
                    except Exception:
                        enriched_inc = result

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
