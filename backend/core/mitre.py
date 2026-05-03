import json
import urllib.request
from typing import Dict


class MitreAttack:
    def __init__(self) -> None:
        self.techniques: Dict[str, str] = {}

    def load(self) -> None:
        url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                data = json.loads(response.read().decode())

            for obj in data.get("objects", []):
                if obj.get("type") == "attack-pattern":
                    external_refs = obj.get("external_references", [])

                    for ref in external_refs:
                        if ref.get("source_name") == "mitre-attack":
                            technique_id = ref.get("external_id")
                            name = obj.get("name")

                            if technique_id and name:
                                self.techniques[technique_id] = name

            print(f"[MITRE] Loaded {len(self.techniques)} techniques")

        except Exception as e:
            print(f"[MITRE] Load failed: {e}")

    def get(self, technique_id: str) -> str:
        return self.techniques.get(technique_id, "unknown")