import json
from typing import Dict, Any

from core.engine import SOAREngine
from core.pipeline import Pipeline

from collectors.registry import get_collectors
from analyzers.registry import get_analyzers
from responders.registry import get_responders
from playbooks.registry import get_playbooks

from playbooks.engine import PlaybookEngine
from storage.repository import IncidentRepository


# -------------------------
# CONFIG
# -------------------------
def load_config() -> Dict[str, Any]:
    try:
        with open("config.json", "r") as f:
            config: Dict[str, Any] = json.load(f)
            print("[*] Config loaded from config.json")
            return config

    except FileNotFoundError:
        print("[!] config.json not found, using default config")

        return {
            "loop_interval": 2,
            "debug": True,
            "use_ml": False,
            "enable_blocking": False,
        }


# -------------------------
# MAIN
# -------------------------
def main() -> None:
    config = load_config()

    # -------------------------
    # COMPONENTS
    # -------------------------
    collectors = get_collectors(config)
    analyzers = get_analyzers(config)
    responders = get_responders(config)
    playbooks = get_playbooks(config)

    # -------------------------
    # PLAYBOOK ENGINE
    # -------------------------
    playbook_engine = PlaybookEngine(playbooks)

    # -------------------------
    # STORAGE
    # -------------------------
    repository = IncidentRepository()

    # -------------------------
    # PIPELINE
    # -------------------------
    pipeline = Pipeline(
        analyzers=analyzers,
        playbook_engine=playbook_engine,
        responders=responders,
        storage=repository,
        debug=config.get("debug", False),
    )

    # -------------------------
    # ENGINE
    # -------------------------
    engine = SOAREngine(
        collectors=collectors,
        pipeline=pipeline,
        interval=config.get("loop_interval", 2),
        debug=config.get("debug", False),
    )

    print("[*] SOAR started (pipeline mode)")

    engine.start()


if __name__ == "__main__":
    main()

