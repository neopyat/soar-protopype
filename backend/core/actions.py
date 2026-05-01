from typing import Dict, Any


class Action:
    def __init__(
        self,
        action_type: str,
        target: str,
        metadata: Dict[str, Any]
    ):
        self.type = action_type
        self.target = target
        self.metadata = metadata

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        return cls(
            action_type=str(data.get("action", "")),
            target=str(data.get("ip", "") or data.get("target", "")),
            metadata=data
        )

    def __repr__(self) -> str:
        return f"<Action type={self.type} target={self.target}>"