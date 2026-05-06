from __future__ import annotations

import time
from typing import List, Dict, Any

from core.actions import Action
from responders.firewall_adapter import FirewallAdapter
from responders.log_adapter import LogAdapter
from storage.db import Database


class ActionExecutor:
    def __init__(self) -> None:
        self.firewall: FirewallAdapter = FirewallAdapter()
        self.logger: LogAdapter = LogAdapter()
        self.db: Database = Database()

    def execute(self, actions: List[Dict[str, Any]]) -> None:
        if not actions:
            return

        parsed_actions: List[Action] = [
            Action.from_dict(a) for a in actions
        ]

        for action in parsed_actions:
            try:
                if action.type == "block_ip":

                    if self.db.is_ip_blocked(action.target):
                        print(f"[SKIP] IP already blocked: {action.target}")
                        continue

                    self.firewall.block_ip(action.target)

                    self.db.insert_action(
                        incident_id=action.incident_id,
                        action_type="block_ip",
                        target=action.target,
                        timestamp=time.time()
                    )

                    if action.incident_id:
                        self.db.update_incident_status(
                            action.incident_id,
                            "mitigated"
                        )

                elif action.type == "log":
                    self.logger.log([action.metadata])

                    message: str = str(
                        action.metadata.get("message", "")
                    )

                    self.db.insert_action(
                        incident_id=action.incident_id,
                        action_type="log",
                        target=message,
                        timestamp=time.time()
                    )

                else:
                    print(f"[!] Unknown action: {action.type}")

            except Exception as e:
                print(f"[!] Executor error ({action.type}): {e}")
