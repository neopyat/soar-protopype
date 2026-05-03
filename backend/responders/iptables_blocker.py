from typing import List, Dict, Any, Set
import subprocess

from responders.base import BaseResponder


class IPTablesBlocker(BaseResponder):
    def __init__(self) -> None:
        self.blocked_ips: Set[str] = set()

    def _add_rule(self, ip: str) -> None:
        subprocess.run(
            ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

    def respond(self, actions: List[Dict[str, Any]]) -> None:
        for action in actions:
            if action.get("action") != "block_ip":
                continue

            ip_value: Any = action.get("ip")

            if not isinstance(ip_value, str):
                continue

            ip: str = ip_value

            try:
                if ip in self.blocked_ips:
                    print(f"[SKIP] IP already blocked: {ip}")
                    continue

                self._add_rule(ip)
                self.blocked_ips.add(ip)

                print(f"[ACTION] IPTABLES block {ip}")

            except Exception as exc:
                print(f"[!] IPTables responder error: {exc}")

# from typing import List, Dict, Any
# import subprocess

# from responders.base import BaseResponder


# class IPTablesBlocker(BaseResponder):
#     def _run(self, cmd: List[str]) -> subprocess.CompletedProcess[str]:
#         return subprocess.run(
#             cmd,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#     def _rule_exists(self, ip: str) -> bool:
#         result: subprocess.CompletedProcess[str] = self._run(
#             ["iptables", "-C", "INPUT", "-s", ip, "-j", "DROP"]
#         )
#         return result.returncode == 0

#     def _add_rule(self, ip: str) -> None:
#         subprocess.run(
#             ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL,
#             check=False
#         )

#     def respond(self, actions: List[Dict[str, Any]]) -> None:
#         for action in actions:
#             if action.get("action") != "block_ip":
#                 continue

#             ip_value: Any = action.get("ip")

#             if not isinstance(ip_value, str):
#                 continue

#             ip: str = ip_value

#             try:
#                 if self._rule_exists(ip):
#                     print(f"[SKIP] IP already blocked: {ip}")
#                     continue

#                 self._add_rule(ip)
#                 print(f"[ACTION] IPTABLES block {ip}")

#             except Exception as exc:
#                 print(f"[!] IPTables responder error: {exc}")

# import subprocess
# from typing import List, Dict, Any

# from responders.base import BaseResponder


# class IPTablesBlocker(BaseResponder):
#     def respond(self, actions: List[Dict[str, Any]]) -> None:
#         for action in actions:
#             if action.get("action") != "block_ip":
#                 continue

#             ip = action.get("ip")
#             if not isinstance(ip, str):
#                 continue

#             try:
#                 # проверяем, есть ли уже правило
#                 check = subprocess.run(
#                     ["iptables", "-C", "INPUT", "-s", ip, "-j", "DROP"],
#                     stdout=subprocess.DEVNULL,
#                     stderr=subprocess.DEVNULL
#                 )

#                 if check.returncode == 0:
#                     continue  # уже заблокирован

#                 # добавляем правило
#                 subprocess.run(
#                     ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
#                     check=True
#                 )

#                 print(f"[ACTION] Blocked IP: {ip}")

#             except Exception as e:
#                 print(f"[!] IPTables error: {e}")