from typing import List, Any

from models.event import Event


class Pipeline:
    def __init__(
        self,
        analyzers: List[Any],
        playbook_engine: Any,
        responders: List[Any],
        storage: Any
    ):
        self.analyzers = analyzers
        self.playbook_engine = playbook_engine
        self.responders = responders
        self.storage = storage

    def process(self, events: List[Event]) -> None:
        incidents: List[Any] = []

        for analyzer in self.analyzers:
            try:
                result = analyzer.analyze(events)
                if result:
                    incidents.extend(result)
            except Exception as e:
                print(f"[!] Analyzer error: {e}")

        actions: List[Any] = []

        if self.playbook_engine:
            try:
                actions = self.playbook_engine.process(incidents)
            except Exception as e:
                print(f"[!] Playbook error: {e}")

        for responder in self.responders:
            try:
                responder.respond(actions)
            except Exception as e:
                print(f"[!] Responder error: {e}")

        if self.storage:
            self.storage.save(incidents)