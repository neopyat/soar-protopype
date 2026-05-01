from typing import Dict, Any

from web.extensions import db
from web.models.incident import Incident


class DBWriter:

    def save_incident(self, incident_data: Dict[str, Any]) -> None:
        incident = Incident(
            type=incident_data.get("type"),
            ip=incident_data.get("ip"),
            severity=incident_data.get("severity", "low"),
            mitre=incident_data.get("mitre"),
            raw_log=str(incident_data),
        )

        db.session.add(incident)