from typing import List, Dict, Any


class LogAdapter:
    def log(self, actions: List[Dict[str, Any]]) -> None:
        for action in actions:
            message = action.get("message")

            if isinstance(message, str):
                print(f"[LOG] {message}")