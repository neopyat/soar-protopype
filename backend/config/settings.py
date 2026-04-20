from typing import Dict, Any


def load_settings() -> Dict[str, Any]:
    return {
        "loop_interval": 2,
        "debug": True,
        "use_ml": True,
        "enable_blocking": False
    }