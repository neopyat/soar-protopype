import subprocess


class IPTablesBlocker:

    def respond(self, actions):
        for action in actions:
            if action.get("type") != "block_ip":
                continue

            ip = action.get("ip")
            if not ip:
                continue

            try:
                print(f"[RESPONDER] Blocking IP: {ip}")

                subprocess.run(
                    ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
                    check=True
                )

            except Exception as e:
                print(f"[ERROR] Failed to block IP {ip}: {e}")