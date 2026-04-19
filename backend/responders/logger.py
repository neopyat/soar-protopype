from typing import List, Dict, Any

from responders.base import BaseResponder


class LoggerResponder(BaseResponder):
    def respond(self, actions: List[Dict[str, Any]]) -> None:
        for action in actions:
            if action.get("action") == "log":
                message = action.get("message")

                if isinstance(message, str):
                    print(f"[LOG] {message}")