from typing import List, Dict, Any

from core.actions import Action
from responders.firewall_adapter import FirewallAdapter
from responders.log_adapter import LogAdapter


class ActionExecutor:
    def __init__(self):
        self.firewall = FirewallAdapter()
        self.logger = LogAdapter()

    def execute(self, actions: List[Dict[str, Any]]) -> None:
        if not actions:
            return

        parsed_actions: List[Action] = [
            Action.from_dict(a) for a in actions
        ]

        for action in parsed_actions:
            try:
                if action.type == "block_ip":
                    self.firewall.block_ip(action.target)

                elif action.type == "log":
                    self.logger.log([action.metadata])

                else:
                    print(f"[!] Unknown action: {action.type}")

            except Exception as e:
                print(f"[!] Executor error ({action.type}): {e}")