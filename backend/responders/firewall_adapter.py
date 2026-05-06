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
