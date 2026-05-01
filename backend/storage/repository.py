import json
from pathlib import Path
from typing import List, Optional, Union

from models.incident import Incident
from storage.compression import write_compressed
from storage.db_writer import DBWriter


class IncidentRepository:
    def __init__(
        self,
        path: Optional[Union[str, Path]] = None
    ) -> None:

        if path is None:
            self.path: Path = Path("data/incidents.json.gz")
        else:
            self.path = Path(path)

        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.db_writer = DBWriter()

    def save(
        self,
        incidents: List[Incident]
    ) -> None:

        if not incidents:
            return

        lines: List[str] = []

        for inc in incidents:
            try:
                data = inc.to_dict()

                # DB
                self.db_writer.save_incident(data)

                # FILE
                serialized = json.dumps(
                    data,
                    ensure_ascii=False
                )

                lines.append(serialized)

            except Exception as e:
                print(f"[!] Serialization error: {e}")

        # COMMIT
        try:
            from web.extensions import db
            db.session.commit()
        except Exception as e:
            print(f"[!] DB commit error: {e}")

        # FILE WRITE
        if lines:
            write_compressed(str(self.path), lines)

# import json
# from pathlib import Path
# from typing import List, Optional, Union

# from models.incident import Incident
# from storage.compression import write_compressed
# from storage.db_writer import DBWriter


# class IncidentRepository:
#     def __init__(
#         self,
#         path: Optional[Union[str, Path]] = None
#     ) -> None:

#         # путь к архиву
#         if path is None:
#             self.path: Path = Path("backend/data/incidents.json.gz")
#         else:
#             self.path = Path(path)

#         # создаём папку если нет
#         self.path.parent.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#         # инициализация DB writer
#         self.db_writer = DBWriter()

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

#                 # -------------------------
#                 # DB STORAGE
#                 # -------------------------
#                 self.db_writer.save_incident(data)

#                 # -------------------------
#                 # ARCHIVE STORAGE
#                 # -------------------------
#                 serialized = json.dumps(
#                     data,
#                     ensure_ascii=False
#                 )

#                 lines.append(serialized)

#             except Exception as e:
#                 print(
#                     f"[!] Serialization error "
#                     f"({getattr(inc, 'id', 'unknown')}): {e}"
#                 )

#         # -------------------------
#         # COMMIT (один раз)
#         # -------------------------
#         try:
#             from web.extensions import db
#             db.session.commit()
#         except Exception as e:
#             print(f"[!] DB commit error: {e}")

#         # -------------------------
#         # ARCHIVE WRITE
#         # -------------------------
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