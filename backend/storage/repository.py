import json
from typing import List

from models.incident import Incident
from storage.compression import write_compressed


class IncidentRepository:
    def __init__(self, path: str = "backend/data/incidents.json.gz"):
        self.path = path

    def save(self, incidents: List[Incident]) -> None:
        if not incidents:
            return

        lines: List[str] = []

        for inc in incidents:
            try:
                data = inc.to_dict()

                # защита от не-сериализуемых значений
                serialized = json.dumps(data, ensure_ascii=False)

                lines.append(serialized)

            except Exception as e:
                print(f"[!] Serialization error (incident {inc.id}): {e}")

        if lines:
            write_compressed(self.path, lines)