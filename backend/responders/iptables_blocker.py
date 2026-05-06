from typing import List, Dict, Any

from responders.base import BaseResponder
from responders.firewall_adapter import FirewallAdapter


class IptablesBlocker(BaseResponder):
    def __init__(self) -> None:
        self.firewall: FirewallAdapter = FirewallAdapter()

    def respond(self, actions: List[Dict[str, Any]]) -> None:
        if not actions:
            return

        print(f"[DEBUG] Incoming actions: {actions}")

        for action in actions:
            try:
                action_type: str = action.get("action", "")

                if action_type != "block_ip":
                    continue

                ip: str = action.get("ip", "")

                if not ip:
                    continue

                self.firewall.block_ip(ip)

            except Exception as e:
                print(f"[Responder Error] {e}")

