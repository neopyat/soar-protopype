import json
from typing import List, Dict, Any

from storage.compression import write_compressed


class IncidentRepository:
    def __init__(self, path: str = "backend/data/incidents.json.gz"):
        self.path = path

    def save(self, incidents: List[Dict[str, Any]]) -> None:
        if not incidents:
            return

        lines = [json.dumps(i) for i in incidents]
        write_compressed(self.path, lines)