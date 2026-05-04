from typing import List, Dict, Any

from models.incident import Incident
from playbooks.base import BasePlaybook


class PlaybookEngine:
    def __init__(self, playbooks: List[BasePlaybook]):
        self.playbooks = playbooks

    def process(self, incidents: List[Incident]) -> List[Dict[str, Any]]:
        actions: List[Dict[str, Any]] = []

        for inc in incidents:
            for pb in self.playbooks:
                try:
                    result = pb.run(inc)  # 🔥 ВАЖНО

                    if result:
                        actions.extend(result)

                except Exception as e:
                    print(f"[!] Playbook error ({pb.__class__.__name__}): {e}")

        return actions