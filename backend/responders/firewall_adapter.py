import subprocess


class FirewallAdapter:
    def __init__(self):
        self.mode = self._detect_mode()

    def _detect_mode(self) -> str:
        try:
            result = subprocess.run(
                ["iptables", "--version"],
                capture_output=True,
                text=True
            )

            if "nf_tables" in result.stdout:
                return "nft"

            return "iptables"

        except Exception:
            return "unknown"

    def block_ip(self, ip: str) -> None:
        if not ip:
            return

        if self.mode == "iptables":
            self._block_iptables(ip)

        elif self.mode == "nft":
            self._block_nft(ip)

        else:
            print("[!] No firewall backend available")

    def _block_iptables(self, ip: str) -> None:
        subprocess.run(
            ["/usr/sbin/iptables", "-I", "INPUT", "1", "-s", ip, "-j", "DROP"]
        )
        print(f"[ACTION] IPTABLES block {ip}")

    def _block_nft(self, ip: str) -> None:
        try:
            subprocess.run(
                ["nft", "add", "rule", "inet", "filter", "input", "ip", "saddr", ip, "drop"],
                check=True
            )
            print(f"[ACTION] NFT block {ip}")

        except Exception as e:
            print(f"[!] NFT error: {e}")