import json
from pathlib import Path
from typing import List, Optional, Union

from models.incident import Incident
from storage.compression import write_compressed
from storage.db import Database


class IncidentRepository:
    def __init__(
        self,
        path: Optional[Union[str, Path]] = None
    ) -> None:

        # путь к gzip логам
        if path is None:
            self.path: Path = Path("backend/data/incidents.json.gz")
        else:
            self.path = Path(path)

        self.path.parent.mkdir(parents=True, exist_ok=True)

        # DB
        self.db: Database = Database()

    # -------------------------
    # SAVE INCIDENTS
    # -------------------------
    def save(self, incidents: List[Incident]) -> None:
        if not incidents:
            return

        lines: List[str] = []

        for inc in incidents:
            try:
                # --- DB SAVE ---
                self.db.insert_incident(inc)

                # --- FILE SAVE ---
                data = inc.to_dict()
                serialized = json.dumps(data, ensure_ascii=False)

                lines.append(serialized)

            except Exception as e:
                print(f"[Repository Error] {inc.id}: {e}")

        if lines:
            write_compressed(str(self.path), lines)

    # -------------------------
    # SAVE ACTION
    # -------------------------
    def save_action(
        self,
        incident_id: Optional[str],
        action_type: str,
        target: str,
        timestamp: float
    ) -> None:
        try:
            self.db.insert_action(
                incident_id=incident_id,
                action_type=action_type,
                target=target,
                timestamp=timestamp
            )
        except Exception as e:
            print(f"[Repository Action Error]: {e}")

    # -------------------------
    # CHECK BLOCK
    # -------------------------
    def is_ip_blocked(self, ip: str) -> bool:
        try:
            return self.db.is_ip_blocked(ip)
        except Exception:
            return False

    # -------------------------
    # UPDATE INCIDENT
    # -------------------------
    def update_status(self, incident_id: str, status: str) -> None:
        try:
            self.db.update_incident_status(incident_id, status)
        except Exception as e:
            print(f"[Repository Update Error]: {e}")

    # -------------------------
    # CLOSE
    # -------------------------
    def close(self) -> None:
        self.db.close()

