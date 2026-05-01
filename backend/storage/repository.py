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

        if path is None:
            self.path: Path = Path("backend/data/incidents.json.gz")
        else:
            self.path = Path(path)

        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.db: Database = Database()

    def save(self, incidents: List[Incident]) -> None:
        if not incidents:
            return

        lines: List[str] = []

        for inc in incidents:
            try:
                # DB
                self.db.insert_incident(inc)

                # FILE
                data = inc.to_dict()
                serialized = json.dumps(data, ensure_ascii=False)
                lines.append(serialized)

            except Exception as e:
                print(f"[!] Serialization error ({inc.id}): {e}")

        if lines:
            write_compressed(str(self.path), lines)

# import json
# from pathlib import Path
# from typing import List, Optional, Union

# from models.incident import Incident
# from storage.compression import write_compressed
# from storage.db import Database


# class IncidentRepository:
#     def __init__(
#         self,
#         path: Optional[Union[str, Path]] = None
#     ) -> None:

#         if path is None:
#             self.path: Path = Path(
#                 "backend/data/incidents.json.gz"
#             )
#         else:
#             self.path = Path(path)

#         self.path.parent.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#         self.db: Database = Database()

#     def save(
#         self,
#         incidents: List[Incident]
#     ) -> None:

#         if not incidents:
#             return

#         lines: List[str] = []

#         for inc in incidents:
#             try:
#                 # DB
#                 self.db.insert_incident(inc)

#                 # FILE
#                 data = inc.to_dict()

#                 serialized = json.dumps(
#                     data,
#                     ensure_ascii=False
#                 )

#                 lines.append(serialized)

#             except Exception as e:
#                 print(f"[!] Serialization error ({inc.id}): {e}")

#         if lines:
#             write_compressed(
#                 str(self.path),
#                 lines
#             )

# import json
# from pathlib import Path
# from typing import List, Optional, Union

# from models.incident import Incident
# from storage.compression import write_compressed
# from storage.db import Database


# class IncidentRepository:
#     def __init__(
#         self,
#         path: Optional[Union[str, Path]] = None
#     ) -> None:

#         if path is None:
#             self.path: Path = Path(
#                 "backend/data/incidents.json.gz"
#             )
#         else:
#             self.path = Path(path)

#         self.path.parent.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#         # ИНИЦИАЛИЗАЦИЯ БД
#         self.db = Database()

#     def save(
#         self,
#         incidents: List[Incident]
#     ) -> None:

#         if not incidents:
#             return

#         lines: List[str] = []

#         for inc in incidents:
#             try:
#                 # --- DB SAVE ---
#                 self.db.insert_incident(inc)

#                 # --- FILE SAVE ---
#                 data = inc.to_dict()

#                 serialized = json.dumps(
#                     data,
#                     ensure_ascii=False
#                 )

#                 lines.append(serialized)

#             except Exception as e:
#                 print(
#                     f"[!] Serialization error "
#                     f"({inc.id}): {e}"
#                 )

#         if lines:
#             write_compressed(
#                 str(self.path),
#                 lines
#             )

# import json

# from pathlib import Path
# from typing import List, Optional, Union

# from models.incident import Incident
# from storage.compression import write_compressed


# class IncidentRepository:
#     def __init__(
#         self,
#         path: Optional[Union[str, Path]] = None
#     ) -> None:

#         if path is None:
#             self.path: Path = Path(
#                 "backend/data/incidents.json.gz"
#             )
#         else:
#             self.path = Path(path)

#         self.path.parent.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#     def save(
#         self,
#         incidents: List[Incident]
#     ) -> None:

#         if not incidents:
#             return

#         lines: List[str] = []

#         for inc in incidents:
#             try:
#                 data = inc.to_dict()

#                 serialized = json.dumps(
#                     data,
#                     ensure_ascii=False
#                 )

#                 lines.append(serialized)

#             except Exception as e:
#                 print(
#                     f"[!] Serialization error "
#                     f"({inc.id}): {e}"
#                 )

#         if lines:
#             write_compressed(
#                 str(self.path),
#                 lines
#             )

# import json
# import os
# from typing import List

# from models.incident import Incident
# from storage.compression import write_compressed
# from paths import INCIDENTS_FILE


# class IncidentRepository:
#     def __init__(self, path=None):
#         self.path = str(path or INCIDENTS_FILE)

#         os.makedirs(os.path.dirname(self.path), exist_ok=True)

#     def save(self, incidents: List[Incident]) -> None:
#         if not incidents:
#             return

#         lines: List[str] = []

#         for inc in incidents:
#             try:
#                 data = inc.to_dict()
#                 serialized = json.dumps(data, ensure_ascii=False)
#                 lines.append(serialized)

#             except Exception as e:
#                 print(f"[!] Serialization error ({inc.id}): {e}")

#         if lines:
#             write_compressed(self.path, lines)

# import json
# import os
# from typing import List

# from models.incident import Incident
# from storage.compression import write_compressed


# class IncidentRepository:
#     def __init__(self, path: str = "backend/data/incidents.json.gz"):
#         self.path = path


#         os.makedirs(os.path.dirname(self.path), exist_ok=True)

#     def save(self, incidents: List[Incident]) -> None:
#         if not incidents:
#             return

#         lines: List[str] = []

#         for inc in incidents:
#             try:
#                 data = inc.to_dict()
#                 serialized = json.dumps(data, ensure_ascii=False)
#                 lines.append(serialized)

#             except Exception as e:
#                 print(f"[!] Serialization error (incident {inc.id}): {e}")

#         if lines:
#             write_compressed(self.path, lines)

# import json
# from typing import List

# from models.incident import Incident
# from storage.compression import write_compressed


# class IncidentRepository:
#     def __init__(self, path: str = "backend/data/incidents.json.gz"):
#         self.path = path

#     def save(self, incidents: List[Incident]) -> None:
#         if not incidents:
#             return

#         lines: List[str] = []

#         for inc in incidents:
#             try:
#                 data = inc.to_dict()

#                 # защита от не-сериализуемых значений
#                 serialized = json.dumps(data, ensure_ascii=False)

#                 lines.append(serialized)

#             except Exception as e:
#                 print(f"[!] Serialization error (incident {inc.id}): {e}")

#         if lines:
#             write_compressed(self.path, lines)