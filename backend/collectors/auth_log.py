import time
import re
import subprocess

from typing import List, Dict, Any, Optional, Set

from collectors.base import BaseCollector


class AuthLogCollector(BaseCollector):

    def __init__(
        self,
        host: str = "192.168.0.109",
        user: str = "srvr",
        log_path: str = "/var/log/auth.log"
    ) -> None:

        self.host: str = host
        self.user: str = user
        self.log_path: str = log_path

        self.last_lines: Set[str] = set()

    # -------------------------
    # MAIN COLLECTION
    # -------------------------
    def collect(self) -> List[Dict[str, Any]]:

        events: List[Dict[str, Any]] = []

        try:
            result = subprocess.run(
                [
                    "ssh",
                    f"{self.user}@{self.host}",
                    f"tail -n 20 {self.log_path}"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                print(f"[SSH Error] {result.stderr}")
                return events

            lines: List[str] = result.stdout.splitlines()

        except Exception as e:
            print(f"[SSH Collector Error] {e}")
            return events

        # -------------------------
        # PARSE LOGS
        # -------------------------
        for line in lines:

            if line in self.last_lines:
                continue

            self.last_lines.add(line)

            event = self._parse_line(line)

            if event is not None:
                events.append(event)

        # -------------------------
        # LIMIT MEMORY
        # -------------------------
        if len(self.last_lines) > 1000:
            self.last_lines = set(list(self.last_lines)[-500:])

        return events

    # -------------------------
    # PARSE SINGLE LINE
    # -------------------------
    def _parse_line(
        self,
        line: str
    ) -> Optional[Dict[str, Any]]:

        # failed login
        if "Failed password" in line:

            ip = self._extract_ip(line)

            if ip:
                return {
                    "type": "failed_login",
                    "ip": ip,
                    "raw": line.strip(),
                    "timestamp": time.time()
                }

        # successful login
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

    # -------------------------
    # EXTRACT IP
    # -------------------------
    def _extract_ip(
        self,
        line: str
    ) -> Optional[str]:

        match = re.search(
            r"\d+\.\d+\.\d+\.\d+",
            line
        )

        if match:
            return match.group(0)

        return None

