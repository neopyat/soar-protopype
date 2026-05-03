import time
import re

from pathlib import Path
from typing import List, Optional, TextIO, Union, Dict, Any

from collectors.base import BaseCollector


class AuthLogCollector(BaseCollector):
    def __init__(
        self,
        log_path: Optional[Union[str, Path]] = None
    ) -> None:

        if log_path is None:
            self.log_path: Path = Path("/var/log/auth.log")
        else:
            self.log_path = Path(log_path)

        self._file: Optional[TextIO] = None

    def _open_file(self) -> None:
        if self._file is None:
            try:
                self.log_path.parent.mkdir(parents=True, exist_ok=True)
                self.log_path.touch(exist_ok=True)

                self._file = open(
                    self.log_path,
                    "r",
                    encoding="utf-8"
                )

                # читаем с конца файла
                self._file.seek(0, 2)

            except Exception as e:
                print(f"[!] File open error: {e}")
                self._file = None

    def collect(self) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []

        self._open_file()

        if self._file is None:
            return events

        try:
            lines = self._file.readlines()
        except Exception as e:
            print(f"[!] Read error: {e}")
            return events

        for line in lines:
            event = self._parse_line(line)

            if event is not None:
                events.append(event)

        return events

    def _parse_line(self, line: str) -> Optional[Dict[str, Any]]:

        if "Failed password" in line:
            ip = self._extract_ip(line)

            if ip:
                return {
                    "type": "failed_login",
                    "ip": ip,
                    "raw": line.strip(),
                    "timestamp": time.time()
                }

        if "Accepted password" in line:
            ip = self._extract_ip(line)

            if ip:
                return {
                    "type": "successful_login",
                    "ip": ip,
                    "raw": line.strip(),
                    "timestamp": time.time()
                }

        return None

    def _extract_ip(self, line: str) -> Optional[str]:
        match = re.search(r"\d+\.\d+\.\d+\.\d+", line)

        if match:
            return match.group(0)

        return None


# import time
# import re

# from pathlib import Path
# from typing import List, Optional, TextIO, Union

# from collectors.base import BaseCollector
# from models.event import Event


# class AuthLogCollector(BaseCollector):
#     def __init__(
#         self,
#         log_path: Optional[Union[str, Path]] = None
#     ) -> None:

#         if log_path is None:
#             self.log_path: Path = Path("/var/log/auth.log")
#         else:
#             self.log_path = Path(log_path)

#         self._file: Optional[TextIO] = None

#     def _open_file(self) -> None:
#         if self._file is None:
#             try:
#                 self.log_path.parent.mkdir(parents=True, exist_ok=True)
#                 self.log_path.touch(exist_ok=True)

#                 self._file = open(
#                     self.log_path,
#                     "r",
#                     encoding="utf-8"
#                 )

#                 self._file.seek(0, 2)

#             except Exception as e:
#                 print(f"[!] File open error: {e}")
#                 self._file = None

#     def collect(self) -> List[Event]:
#         events: List[Event] = []

#         self._open_file()

#         if self._file is None:
#             return events

#         try:
#             lines = self._file.readlines()
#         except Exception as e:
#             print(f"[!] Read error: {e}")
#             return events

#         for line in lines:
#             event = self._parse_line(line)

#             if event is not None:
#                 events.append(event)

#         return events

#     def _parse_line(self, line: str) -> Optional[Event]:

#         if "Failed password" in line:
#             ip = self._extract_ip(line)

#             if ip:
#                 return Event(
#                     type="failed_login",
#                     ip=ip,
#                     raw=line.strip(),
#                     timestamp=time.time()
#                 )

#         if "Accepted password" in line:
#             ip = self._extract_ip(line)

#             if ip:
#                 return Event(
#                     type="successful_login",
#                     ip=ip,
#                     raw=line.strip(),
#                     timestamp=time.time()
#                 )

#         return None

#     def _extract_ip(self, line: str) -> Optional[str]:
#         match = re.search(r"\d+\.\d+\.\d+\.\d+", line)

#         if match:
#             return match.group(0)

#         return None


# import time
# import re

# from pathlib import Path
# from typing import List, Dict, Any, Optional, TextIO, Union

# from collectors.base import BaseCollector


# class AuthLogCollector(BaseCollector):
#     def __init__(
#         self,
#         log_path: Optional[Union[str, Path]] = None
#     ) -> None:

#         if log_path is None:
#             self.log_path: Path = Path("/var/log/auth.log")
#         else:
#             self.log_path = Path(log_path)

#         self._file: Optional[TextIO] = None

#     def _open_file(self) -> None:
#         if self._file is None:
#             try:
#                 self.log_path.parent.mkdir(parents=True, exist_ok=True)
#                 self.log_path.touch(exist_ok=True)

#                 self._file = open(
#                     self.log_path,
#                     "r",
#                     encoding="utf-8"
#                 )

#                 self._file.seek(0, 2)

#             except Exception as e:
#                 print(f"[!] File open error: {e}")
#                 self._file = None

#     def collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         self._open_file()

#         if self._file is None:
#             return events

#         try:
#             lines = self._file.readlines()

#         except Exception as e:
#             print(f"[!] Read error: {e}")
#             return events

#         for line in lines:
#             event = self._parse_line(line)

#             if event is not None:
#                 events.append(event)

#         return events

#     def _parse_line(
#         self,
#         line: str
#     ) -> Optional[Dict[str, Any]]:

#         if "Failed password" in line:
#             ip = self._extract_ip(line)

#             if ip:
#                 return {
#                     "type": "failed_login",
#                     "ip": ip,
#                     "raw": line.strip(),
#                     "timestamp": time.time()
#                 }

#         if "Accepted password" in line:
#             ip = self._extract_ip(line)

#             if ip:
#                 return {
#                     "type": "successful_login",
#                     "ip": ip,
#                     "raw": line.strip(),
#                     "timestamp": time.time()
#                 }

#         return None

#     def _extract_ip(
#         self,
#         line: str
#     ) -> Optional[str]:

#         match = re.search(
#             r"\d+\.\d+\.\d+\.\d+",
#             line
#         )

#         if match:
#             return match.group(0)

#         return None

# import time
# import re
# from pathlib import Path
# from typing import List, Dict, Any, Optional, TextIO

# from collectors.base import BaseCollector
# from paths import AUTH_LOG


# class AuthLogCollector(BaseCollector):
#     def __init__(self, log_path=None):
#         self.log_path = Path(log_path) if log_path else AUTH_LOG
#         self._file: Optional[TextIO] = None

#     def _open_file(self) -> None:
#         if self._file is None:
#             try:
#                 self.log_path.parent.mkdir(parents=True, exist_ok=True)
#                 self.log_path.touch(exist_ok=True)

#                 self._file = open(self.log_path, "r", encoding="utf-8")
#                 self._file.seek(0, 2)

#             except Exception as e:
#                 print(f"[!] File open error: {e}")
#                 self._file = None

#     def collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         self._open_file()

#         if not self._file:
#             return events

#         try:
#             lines = self._file.readlines()
#         except Exception as e:
#             print(f"[!] Read error: {e}")
#             return events

#         for line in lines:
#             event = self._parse_line(line)
#             if event:
#                 events.append(event)

#         return events

#     def _parse_line(self, line: str) -> Optional[Dict[str, Any]]:
#         if "Failed password" in line:
#             ip = self._extract_ip(line)

#             if ip:
#                 return {
#                     "type": "failed_login",
#                     "ip": ip,
#                     "raw": line.strip(),
#                     "timestamp": time.time()
#                 }

#         if "Accepted password" in line:
#             ip = self._extract_ip(line)

#             if ip:
#                 return {
#                     "type": "successful_login",
#                     "ip": ip,
#                     "raw": line.strip(),
#                     "timestamp": time.time()
#                 }

#         return None

#     def _extract_ip(self, line: str) -> Optional[str]:
#         match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
#         return match.group(0) if match else None

# import time
# import re
# from typing import List, Dict, Any, Optional, TextIO

# from collectors.base import BaseCollector


# class AuthLogCollector(BaseCollector):
#     def __init__(self, log_path: str = "/var/log/auth.log"):
#         # ✅ локальный файл по умолчанию
#         self.log_path = log_path
#         self._file: Optional[TextIO] = None

#     def _open_file(self) -> None:
#         if self._file is None:
#             try:
#                 self._file = open(self.log_path, "r")
#                 self._file.seek(0, 2)
#             except Exception as e:
#                 print(f"[!] File open error: {e}")
#                 self._file = None

#     def collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         self._open_file()

#         if not self._file:
#             return events

#         try:
#             lines = self._file.readlines()
#         except Exception as e:
#             print(f"[!] Read error: {e}")
#             return events

#         for line in lines:
#             event = self._parse_line(line)
#             if event:
#                 events.append(event)

#         return events

#     def _parse_line(self, line: str) -> Optional[Dict[str, Any]]:
#         if "Failed password" in line:
#             ip = self._extract_ip(line)
#             if ip:
#                 return {
#                     "type": "failed_login",
#                     "ip": ip,
#                     "raw": line.strip(),
#                     "timestamp": time.time()
#                 }

#         if "Accepted password" in line:
#             ip = self._extract_ip(line)
#             if ip:
#                 return {
#                     "type": "successful_login",
#                     "ip": ip,
#                     "raw": line.strip(),
#                     "timestamp": time.time()
#                 }

#         return None

#     def _extract_ip(self, line: str) -> Optional[str]:
#         match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
#         return match.group(0) if match else None

# import time
# import re
# from typing import List, Dict, Any, Optional, TextIO

# from collectors.base import BaseCollector


# class AuthLogCollector(BaseCollector):
#     def __init__(self, log_path: str = "/var/log/auth.log"):
#         self.log_path = log_path
#         self._file: Optional[TextIO] = None

#     def _open_file(self) -> None:
#         if self._file is None:
#             try:
#                 self._file = open(self.log_path, "r")
#                 self._file.seek(0, 2)
#             except Exception as e:
#                 print(f"[!] File open error: {e}")
#                 self._file = None

#     def collect(self) -> List[Dict[str, Any]]:
#         events: List[Dict[str, Any]] = []

#         self._open_file()

#         if not self._file:
#             return events

#         try:
#             lines = self._file.readlines()
#         except Exception as e:
#             print(f"[!] Read error: {e}")
#             return events

#         for line in lines:
#             event = self._parse_line(line)
#             if event:
#                 events.append(event)

#         return events

#     def _parse_line(self, line: str) -> Optional[Dict[str, Any]]:
#         if "Failed password" in line:
#             ip = self._extract_ip(line)
#             if ip:
#                 return {
#                     "type": "failed_login",
#                     "ip": ip,
#                     "raw": line.strip(),
#                     "timestamp": time.time()
#                 }

#         if "Accepted password" in line:
#             ip = self._extract_ip(line)
#             if ip:
#                 return {
#                     "type": "successful_login",
#                     "ip": ip,
#                     "raw": line.strip(),
#                     "timestamp": time.time()
#                 }

#         return None

#     def _extract_ip(self, line: str) -> Optional[str]:
#         match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
#         return match.group(0) if match else None