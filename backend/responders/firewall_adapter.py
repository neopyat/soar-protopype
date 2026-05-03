import subprocess
from typing import List


class FirewallAdapter:
    """
    Унифицированный адаптер для работы с firewall:
    - автоматически определяет backend (nft / iptables)
    - для nft создаёт таблицу/цепочку при необходимости
    - не дублирует правила (по возможности)
    """

    def __init__(self) -> None:
        self.mode: str = self._detect_mode()

    # -------------------------
    # Utils
    # -------------------------
    def _run(self, cmd: List[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    def _detect_mode(self) -> str:
        """
        Определяем, используется ли nft или iptables.
        """
        try:
            result = self._run(["iptables", "--version"])

            if "nf_tables" in result.stdout.lower():
                return "nft"

            return "iptables"

        except Exception:
            return "unknown"

    # -------------------------
    # Public API
    # -------------------------
    def block_ip(self, ip: str) -> None:
        if not ip:
            return

        if self.mode == "nft":
            self._block_nft(ip)

        elif self.mode == "iptables":
            self._block_iptables(ip)

        else:
            print("[!] Firewall backend not available")

    # -------------------------
    # IPTABLES
    # -------------------------
    def _iptables_rule_exists(self, ip: str) -> bool:
        result = self._run(["iptables", "-C", "INPUT", "-s", ip, "-j", "DROP"])
        return result.returncode == 0

    def _block_iptables(self, ip: str) -> None:
        try:
            if self._iptables_rule_exists(ip):
                print(f"[SKIP] IPTABLES already blocked: {ip}")
                return

            subprocess.run(
                ["iptables", "-I", "INPUT", "1", "-s", ip, "-j", "DROP"],
                check=False
            )

            print(f"[ACTION] IPTABLES block {ip}")

        except Exception as e:
            print(f"[!] IPTABLES error: {e}")

    # -------------------------
    # NFTABLES
    # -------------------------
    def _ensure_nft_table_chain(self) -> None:
        """
        Гарантирует наличие:
        table inet filter
        chain input (hook input)
        """
        # table
        subprocess.run(
            ["nft", "add", "table", "inet", "filter"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

        # chain
        subprocess.run(
            [
                "nft", "add", "chain", "inet", "filter", "input",
                "{", "type", "filter", "hook", "input", "priority", "0", ";", "}"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

    def _nft_rule_exists(self, ip: str) -> bool:
        try:
            result = self._run(["nft", "list", "ruleset"])
            return f"ip saddr {ip} drop" in result.stdout
        except Exception:
            return False

    def _block_nft(self, ip: str) -> None:
        try:
            self._ensure_nft_table_chain()

            if self._nft_rule_exists(ip):
                print(f"[SKIP] NFT already blocked: {ip}")
                return

            subprocess.run(
                [
                    "nft", "add", "rule",
                    "inet", "filter", "input",
                    "ip", "saddr", ip, "drop"
                ],
                check=True
            )

            print(f"[ACTION] NFT block {ip}")

        except Exception as e:
            print(f"[!] NFT error: {e}")

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