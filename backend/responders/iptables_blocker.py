import subprocess
from typing import List, Dict, Any

from responders.base import BaseResponder


class IPTablesBlocker(BaseResponder):
    def respond(self, actions: List[Dict[str, Any]]) -> None:
        for action in actions:
            if action.get("action") == "block_ip":
                ip = action.get("ip")

                if not isinstance(ip, str):
                    continue

                try:
                    subprocess.run(
                        ["sudo", "iptables", "-C", "INPUT", "-s", ip, "-j", "DROP"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except subprocess.CalledProcessError:
                    subprocess.run(
                        ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )