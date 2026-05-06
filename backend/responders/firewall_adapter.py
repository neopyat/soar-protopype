import subprocess


class FirewallAdapter:

    def __init__(
        self,
        remote_host: str = "192.168.0.109",
        remote_user: str = "srvr"
    ) -> None:

        self.remote_host: str = remote_host
        self.remote_user: str = remote_user

    # -------------------------
    # SSH EXECUTION
    # -------------------------
    def _run_remote(
        self,
        command: str
    ) -> subprocess.CompletedProcess[str]:

        return subprocess.run(
            [
                "ssh",
                f"{self.remote_user}@{self.remote_host}",
                command
            ],
            capture_output=True,
            text=True
        )

    # -------------------------
    # ENSURE NFTABLES
    # -------------------------
    def _ensure_nftables(self) -> None:

        commands: list[str] = [
            "sudo nft add table inet soar",
            (
                "sudo nft add chain inet soar blacklist "
                "'{ type filter hook input priority 0; policy accept; }'"
            )
        ]

        for cmd in commands:
            self._run_remote(cmd)

    # -------------------------
    # RULE EXISTS
    # -------------------------
    def _rule_exists(
        self,
        ip: str
    ) -> bool:

        result = self._run_remote(
            "sudo nft list chain inet soar blacklist"
        )

        return ip in result.stdout

    # -------------------------
    # BLOCK IP
    # -------------------------
    def block_ip(
        self,
        ip: str
    ) -> None:

        if not ip.strip():
            return

        self._ensure_nftables()

        if self._rule_exists(ip):
            print(f"[FW] remote nft: {ip} already blocked")
            return

        command = (
            f"sudo nft add rule inet soar blacklist "
            f"ip saddr {ip} drop"
        )

        result = self._run_remote(command)

        if result.returncode == 0:
            print(f"[FW] remote nft: blocked {ip}")

        else:
            print(
                "[FW ERROR] remote nft failed: "
                f"{result.stderr.strip()}"
            )


# import subprocess


# class FirewallAdapter:
#     def __init__(self) -> None:
#         self.backend: str = self._detect_backend()

#     # -------------------------
#     # DETECT BACKEND
#     # -------------------------
#     def _detect_backend(self) -> str:
#         try:
#             subprocess.run(
#                 ["nft", "list", "ruleset"],
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.DEVNULL,
#                 check=True
#             )
#             return "nft"
#         except Exception:
#             return "iptables"

#     # -------------------------
#     # PUBLIC API
#     # -------------------------
#     def block_ip(self, ip: str) -> None:
#         if self.backend == "nft":
#             self._block_ip_nft(ip)
#         else:
#             self._block_ip_iptables(ip)

#     # -------------------------
#     # NFTABLES
#     # -------------------------
#     def _ensure_nft_structure(self) -> None:
#         try:
#             subprocess.run(
#                 ["nft", "add", "table", "inet", "soar"],
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.DEVNULL,
#                 check=False
#             )

#             subprocess.run(
#                 [
#                     "nft", "add", "chain", "inet", "soar", "input",
#                     "{", "type", "filter", "hook", "input", "priority", "0", ";", "}"
#                 ],
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.DEVNULL,
#                 check=False
#             )
#         except Exception:
#             pass

#     def _rule_exists_nft(self, ip: str) -> bool:
#         try:
#             result = subprocess.run(
#                 ["nft", "list", "chain", "inet", "soar", "input"],
#                 capture_output=True,
#                 text=True,
#                 check=False
#             )
#             return ip in result.stdout
#         except Exception:
#             return False

#     def _block_ip_nft(self, ip: str) -> None:
#         self._ensure_nft_structure()

#         if self._rule_exists_nft(ip):
#             print(f"[FW] nft: {ip} already blocked")
#             return

#         try:
#             subprocess.run(
#                 ["nft", "add", "rule", "inet", "soar", "input", "ip", "saddr", ip, "drop"],
#                 check=True
#             )
#             print(f"[FW] nft: blocked {ip}")
#         except Exception as e:
#             print(f"[FW ERROR] nft block failed: {e}")

#     # -------------------------
#     # IPTABLES
#     # -------------------------
#     def _rule_exists_iptables(self, ip: str) -> bool:
#         try:
#             result = subprocess.run(
#                 ["iptables", "-L", "INPUT", "-n"],
#                 capture_output=True,
#                 text=True,
#                 check=False
#             )
#             return ip in result.stdout
#         except Exception:
#             return False

#     def _block_ip_iptables(self, ip: str) -> None:
#         if self._rule_exists_iptables(ip):
#             print(f"[FW] iptables: {ip} already blocked")
#             return

#         try:
#             subprocess.run(
#                 ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
#                 check=True
#             )
#             print(f"[FW] iptables: blocked {ip}")
#         except Exception as e:
#             print(f"[FW ERROR] iptables block failed: {e}")


# import subprocess
# from typing import List


# class FirewallAdapter:
#     """
#     Унифицированный firewall адаптер:
#     - iptables / nft auto-detect
#     - block / unblock
#     - проверка существования правил
#     """

#     def __init__(self) -> None:
#         self.mode: str = self._detect_mode()

#     # -------------------------
#     # CORE UTILS
#     # -------------------------
#     def _run(self, cmd: List[str]) -> subprocess.CompletedProcess[str]:
#         return subprocess.run(
#             cmd,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#     def _detect_mode(self) -> str:
#         try:
#             result = self._run(["iptables", "--version"])

#             if "nf_tables" in result.stdout.lower():
#                 return "nft"

#             return "iptables"

#         except Exception:
#             return "unknown"

#     # -------------------------
#     # PUBLIC API
#     # -------------------------
#     def block_ip(self, ip: str) -> None:
#         if not ip:
#             return

#         if self.mode == "iptables":
#             self._block_iptables(ip)

#         elif self.mode == "nft":
#             self._block_nft(ip)

#         else:
#             print("[!] No firewall backend available")

#     def unblock_ip(self, ip: str) -> None:
#         if not ip:
#             return

#         if self.mode == "iptables":
#             self._unblock_iptables(ip)

#         elif self.mode == "nft":
#             self._unblock_nft(ip)

#         else:
#             print("[!] No firewall backend available")

#     # -------------------------
#     # IPTABLES
#     # -------------------------
#     def _iptables_rule_exists(self, ip: str) -> bool:
#         result = self._run(["iptables", "-C", "INPUT", "-s", ip, "-j", "DROP"])
#         return result.returncode == 0

#     def _block_iptables(self, ip: str) -> None:
#         try:
#             if self._iptables_rule_exists(ip):
#                 print(f"[SKIP] IPTABLES already blocked: {ip}")
#                 return

#             subprocess.run(
#                 ["iptables", "-I", "INPUT", "1", "-s", ip, "-j", "DROP"],
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.DEVNULL,
#                 check=False
#             )

#             print(f"[ACTION] IPTABLES block {ip}")

#         except Exception as e:
#             print(f"[!] IPTABLES block error: {e}")

#     def _unblock_iptables(self, ip: str) -> None:
#         try:
#             if not self._iptables_rule_exists(ip):
#                 return

#             subprocess.run(
#                 ["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"],
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.DEVNULL,
#                 check=False
#             )

#             print(f"[ACTION] IPTABLES unblock {ip}")

#         except Exception as e:
#             print(f"[!] IPTABLES unblock error: {e}")

#     # -------------------------
#     # NFTABLES
#     # -------------------------
#     def _ensure_nft(self) -> None:
#         subprocess.run(
#             ["nft", "add", "table", "inet", "filter"],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL,
#             check=False
#         )

#         subprocess.run(
#             [
#                 "nft", "add", "chain", "inet", "filter", "input",
#                 "{", "type", "filter", "hook", "input", "priority", "0", ";", "}"
#             ],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL,
#             check=False
#         )

#     def _nft_rule_exists(self, ip: str) -> bool:
#         try:
#             result = self._run(["nft", "list", "ruleset"])
#             return f"ip saddr {ip} drop" in result.stdout
#         except Exception:
#             return False

#     def _block_nft(self, ip: str) -> None:
#         try:
#             self._ensure_nft()

#             if self._nft_rule_exists(ip):
#                 print(f"[SKIP] NFT already blocked: {ip}")
#                 return

#             subprocess.run(
#                 [
#                     "nft", "add", "rule",
#                     "inet", "filter", "input",
#                     "ip", "saddr", ip, "drop"
#                 ],
#                 check=True
#             )

#             print(f"[ACTION] NFT block {ip}")

#         except Exception as e:
#             print(f"[!] NFT block error: {e}")

#     def _unblock_nft(self, ip: str) -> None:
#         try:
#             # Удаляем все правила с этим IP (упрощённый подход)
#             subprocess.run(
#                 [
#                     "nft", "delete", "rule",
#                     "inet", "filter", "input",
#                     "ip", "saddr", ip, "drop"
#                 ],
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.DEVNULL,
#                 check=False
#             )

#             print(f"[ACTION] NFT unblock {ip}")

#         except Exception as e:
#             print(f"[!] NFT unblock error: {e}")


# import subprocess
# from typing import List


# class FirewallAdapter:
#     """
#     Унифицированный адаптер для работы с firewall:
#     - автоматически определяет backend (nft / iptables)
#     - для nft создаёт таблицу/цепочку при необходимости
#     - не дублирует правила (по возможности)
#     """

#     def __init__(self) -> None:
#         self.mode: str = self._detect_mode()

#     # -------------------------
#     # Utils
#     # -------------------------
#     def _run(self, cmd: List[str]) -> subprocess.CompletedProcess[str]:
#         return subprocess.run(
#             cmd,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#     def _detect_mode(self) -> str:
#         """
#         Определяем, используется ли nft или iptables.
#         """
#         try:
#             result = self._run(["iptables", "--version"])

#             if "nf_tables" in result.stdout.lower():
#                 return "nft"

#             return "iptables"

#         except Exception:
#             return "unknown"

#     # -------------------------
#     # Public API
#     # -------------------------
#     def block_ip(self, ip: str) -> None:
#         if not ip:
#             return

#         if self.mode == "nft":
#             self._block_nft(ip)

#         elif self.mode == "iptables":
#             self._block_iptables(ip)

#         else:
#             print("[!] Firewall backend not available")

#     # -------------------------
#     # IPTABLES
#     # -------------------------
#     def _iptables_rule_exists(self, ip: str) -> bool:
#         result = self._run(["iptables", "-C", "INPUT", "-s", ip, "-j", "DROP"])
#         return result.returncode == 0

#     def _block_iptables(self, ip: str) -> None:
#         try:
#             if self._iptables_rule_exists(ip):
#                 print(f"[SKIP] IPTABLES already blocked: {ip}")
#                 return

#             subprocess.run(
#                 ["iptables", "-I", "INPUT", "1", "-s", ip, "-j", "DROP"],
#                 check=False
#             )

#             print(f"[ACTION] IPTABLES block {ip}")

#         except Exception as e:
#             print(f"[!] IPTABLES error: {e}")

#     # -------------------------
#     # NFTABLES
#     # -------------------------
#     def _ensure_nft_table_chain(self) -> None:
#         """
#         Гарантирует наличие:
#         table inet filter
#         chain input (hook input)
#         """
#         # table
#         subprocess.run(
#             ["nft", "add", "table", "inet", "filter"],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL,
#             check=False
#         )

#         # chain
#         subprocess.run(
#             [
#                 "nft", "add", "chain", "inet", "filter", "input",
#                 "{", "type", "filter", "hook", "input", "priority", "0", ";", "}"
#             ],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL,
#             check=False
#         )

#     def _nft_rule_exists(self, ip: str) -> bool:
#         try:
#             result = self._run(["nft", "list", "ruleset"])
#             return f"ip saddr {ip} drop" in result.stdout
#         except Exception:
#             return False

#     def _block_nft(self, ip: str) -> None:
#         try:
#             self._ensure_nft_table_chain()

#             if self._nft_rule_exists(ip):
#                 print(f"[SKIP] NFT already blocked: {ip}")
#                 return

#             subprocess.run(
#                 [
#                     "nft", "add", "rule",
#                     "inet", "filter", "input",
#                     "ip", "saddr", ip, "drop"
#                 ],
#                 check=True
#             )

#             print(f"[ACTION] NFT block {ip}")

#         except Exception as e:
#             print(f"[!] NFT error: {e}")

# import subprocess


# class FirewallAdapter:
#     def __init__(self):
#         self.mode = self._detect_mode()

#     def _detect_mode(self) -> str:
#         try:
#             result = subprocess.run(
#                 ["iptables", "--version"],
#                 capture_output=True,
#                 text=True
#             )

#             if "nf_tables" in result.stdout:
#                 return "nft"

#             return "iptables"

#         except Exception:
#             return "unknown"

#     def block_ip(self, ip: str) -> None:
#         if not ip:
#             return

#         if self.mode == "iptables":
#             self._block_iptables(ip)

#         elif self.mode == "nft":
#             self._block_nft(ip)

#         else:
#             print("[!] No firewall backend available")

#     def _block_iptables(self, ip: str) -> None:
#         subprocess.run(
#             ["/usr/sbin/iptables", "-I", "INPUT", "1", "-s", ip, "-j", "DROP"]
#         )
#         print(f"[ACTION] IPTABLES block {ip}")

#     def _block_nft(self, ip: str) -> None:
#         try:
#             subprocess.run(
#                 ["nft", "add", "rule", "inet", "filter", "input", "ip", "saddr", ip, "drop"],
#                 check=True
#             )
#             print(f"[ACTION] NFT block {ip}")

#         except Exception as e:
#             print(f"[!] NFT error: {e}")