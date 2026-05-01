import subprocess
from typing import List, Dict, Any

from responders.base import BaseResponder


class IPTablesBlocker(BaseResponder):
    def respond(self, actions: List[Dict[str, Any]]) -> None:
        for action in actions:
            if action.get("action") != "block_ip":
                continue

            ip = action.get("ip")
            if not isinstance(ip, str):
                continue

            try:
                # проверяем, есть ли уже правило
                check = subprocess.run(
                    ["iptables", "-C", "INPUT", "-s", ip, "-j", "DROP"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                if check.returncode == 0:
                    continue  # уже заблокирован

                # добавляем правило
                subprocess.run(
                    ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
                    check=True
                )

                print(f"[ACTION] Blocked IP: {ip}")

            except Exception as e:
                print(f"[!] IPTables error: {e}")