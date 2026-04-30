import time
import json
from pathlib import Path

from core.engine import SOAREngine
from collectors.auth_log import AuthLogCollector
from analyzers.bruteforce import BruteforceAnalyzer
from analyzers.anomaly import AnomalyAnalyzer

from responders.registry import get_responders
from playbooks.registry import get_playbooks

from web import create_app


def load_config() -> dict:
    config_path = Path("config.json")

    if not config_path.exists():
        print("[!] config.json not found, using defaults")
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            print("[*] Config loaded from config.json")
            return config
    except Exception as e:
        print(f"[!] Failed to load config: {e}")
        return {}


def main():
    config = load_config()

    engine = SOAREngine(config=config)

    # -------------------------
    # COLLECTORS
    # -------------------------
    engine.register_collector(AuthLogCollector())

    # -------------------------
    # ANALYZERS
    # -------------------------
    engine.register_analyzer(BruteforceAnalyzer())
    engine.register_analyzer(AnomalyAnalyzer())

    # -------------------------
    # RESPONDERS
    # -------------------------
    responders = get_responders(config)
    for responder in responders:
        engine.register_responder(responder)

    # -------------------------
    # PLAYBOOKS
    # -------------------------
    playbooks = get_playbooks(config)
    engine.register_playbooks(playbooks)

    print("[*] SOAR started")

    # -------------------------
    # LOOP
    # -------------------------
    while True:
        engine.run()
        time.sleep(config.get("loop_interval", 2))


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        main()

# import time
# import json
# from pathlib import Path

# from core.engine import SOAREngine
# from collectors.auth_log import AuthLogCollector
# from analyzers.bruteforce import BruteforceAnalyzer
# from analyzers.anomaly import AnomalyAnalyzer

# from responders.registry import get_responders
# from playbooks.registry import get_playbooks

# from web import create_app


# def load_config() -> dict:
#     config_path = Path("config.json")

#     if not config_path.exists():
#         print("[!] config.json not found, using defaults")
#         return {}

#     try:
#         with open(config_path, "r", encoding="utf-8") as f:
#             config = json.load(f)
#             print("[*] Config loaded from config.json")
#             return config
#     except Exception as e:
#         print(f"[!] Failed to load config: {e}")
#         return {}


# def main():
#     config = load_config()

#     engine = SOAREngine(config=config)

#     # collectors
#     engine.register_collector(AuthLogCollector())

#     # analyzers
#     engine.register_analyzer(BruteforceAnalyzer())
#     engine.register_analyzer(AnomalyAnalyzer())

#     # responders (через registry)
#     for responder in get_responders(config):
#         engine.register_responder(responder)

#     # playbooks (через registry)
#     engine.register_playbooks(get_playbooks(config))

#     print("[*] SOAR started")

#     while True:
#         engine.run()
#         time.sleep(config.get("interval", 2))


# if __name__ == "__main__":
#     app = create_app()

#     with app.app_context():
#         main()

# import time
# import json
# from pathlib import Path

# from core.engine import SOAREngine
# from collectors.auth_log import AuthLogCollector
# from analyzers.bruteforce import BruteforceAnalyzer
# from analyzers.anomaly import AnomalyAnalyzer
# from responders.block_ip import BlockIPResponder
# from responders.logger import LogResponder
# from playbooks.default import DefaultPlaybook

# from web import create_app


# def load_config() -> dict:
#     config_path = Path("config.json")

#     if not config_path.exists():
#         print("[!] config.json not found, using defaults")
#         return {}

#     try:
#         with open(config_path, "r", encoding="utf-8") as f:
#             config = json.load(f)
#             print("[*] Config loaded from config.json")
#             return config
#     except Exception as e:
#         print(f"[!] Failed to load config: {e}")
#         return {}


# def main():
#     config = load_config()

#     # -------------------------
#     # INIT ENGINE
#     # -------------------------
#     engine = SOAREngine(config=config)

#     # -------------------------
#     # COLLECTORS
#     # -------------------------
#     engine.register_collector(AuthLogCollector())

#     # -------------------------
#     # ANALYZERS
#     # -------------------------
#     engine.register_analyzer(BruteforceAnalyzer())
#     engine.register_analyzer(AnomalyAnalyzer())

#     # -------------------------
#     # RESPONDERS
#     # -------------------------
#     engine.register_responder(BlockIPResponder())
#     engine.register_responder(LogResponder())

#     # -------------------------
#     # PLAYBOOKS
#     # -------------------------
#     engine.register_playbooks([
#         DefaultPlaybook()
#     ])

#     print("[*] SOAR started (production mode)")

#     # -------------------------
#     # MAIN LOOP
#     # -------------------------
#     while True:
#         engine.run()
#         time.sleep(config.get("interval", 2))


# if __name__ == "__main__":
    
#     app = create_app()

#     with app.app_context():
#         main()

# import json
# import time
# from typing import Dict, Any

# from core.engine import SOAREngine

# from collectors.registry import get_collectors
# from analyzers.registry import get_analyzers
# from responders.registry import get_responders
# from playbooks.registry import get_playbooks


# # -------------------------
# # Config loader
# # -------------------------

# def load_config() -> Dict[str, Any]:
#     try:
#         with open("config.json", "r") as f:
#             config: Dict[str, Any] = json.load(f)
#             print("[*] Config loaded from config.json")
#             return config

#     except FileNotFoundError:
#         print("[!] config.json not found, using default config")

#         return {
#             "loop_interval": 2,
#             "debug": True,
#             "use_ml": False,
#             "enable_blocking": False,
#             "siem": "none"
#         }


# # -------------------------
# # Main
# # -------------------------

# def main() -> None:
#     config = load_config()

#     engine = SOAREngine(config)

#     # -------------------------
#     # Collectors
#     # -------------------------
#     for collector in get_collectors(config):
#         engine.register_collector(collector)

#     # -------------------------
#     # Analyzers
#     # -------------------------
#     for analyzer in get_analyzers(config):
#         engine.register_analyzer(analyzer)

#     # -------------------------
#     # Playbooks
#     # -------------------------
#     playbooks = get_playbooks(config)
#     engine.register_playbooks(playbooks)

#     # -------------------------
#     # Responders
#     # -------------------------
#     for responder in get_responders(config):
#         engine.register_responder(responder)

#     print("[*] SOAR started (production mode)")

#     # -------------------------
#     # Loop
#     # -------------------------
#     while True:
#         try:
#             engine.run()
#             time.sleep(config.get("loop_interval", 2))

#         except KeyboardInterrupt:
#             print("\n[*] SOAR stopped by user")
#             break

#         except Exception as e:
#             print(f"[!] Runtime error: {e}")
#             time.sleep(config.get("loop_interval", 2))


# if __name__ == "__main__":
#     main()

# import time
# from typing import Dict, Any

# from core.engine import SOAREngine

# from collectors.registry import get_collectors
# from analyzers.registry import get_analyzers
# from responders.registry import get_responders
# from playbooks.registry import get_playbooks


# # -------------------------
# # Config
# # -------------------------

# CONFIG: Dict[str, Any] = {
#     "loop_interval": 2,
#     "debug": True,
#     "use_ml": True,
#     "enable_blocking": False
# }


# # -------------------------
# # Main
# # -------------------------

# def main() -> None:
#     engine = SOAREngine(CONFIG)

#     # Collectors
#     for collector in get_collectors(CONFIG):
#         engine.register_collector(collector)

#     # Analyzers
#     for analyzer in get_analyzers(CONFIG):
#         engine.register_analyzer(analyzer)

#     # Playbooks
#     engine.register_playbooks(get_playbooks(CONFIG))

#     # Responders
#     for responder in get_responders(CONFIG):
#         engine.register_responder(responder)

#     print("[*] SOAR started (production mode)")

#     while True:
#         try:
#             engine.run()
#             time.sleep(CONFIG["loop_interval"])

#         except KeyboardInterrupt:
#             print("\n[*] SOAR stopped by user")
#             break

#         except Exception as e:
#             print(f"[!] Runtime error: {e}")
#             time.sleep(CONFIG["loop_interval"])


# if __name__ == "__main__":
#     main()
    
# import time
# from typing import TypedDict

# from core.engine import SOAREngine

# from collectors.registry import get_collectors
# from analyzers.registry import get_analyzers
# from responders.registry import get_responders
# from playbooks.registry import get_playbooks


# # -------------------------
# # Config schema (production-level)
# # -------------------------

# class Config(TypedDict):
#     loop_interval: int
#     debug: bool
#     use_ml: bool
#     enable_blocking: bool


# CONFIG: Config = {
#     "loop_interval": 2,
#     "debug": True,
#     "use_ml": False,
#     "enable_blocking": False  # ⚠️ сначала выключи iptables
# }


# # -------------------------
# # Main
# # -------------------------

# def main() -> None:
#     engine = SOAREngine(CONFIG)

#     # Collectors
#     for collector in get_collectors(CONFIG):
#         engine.register_collector(collector)

#     # Analyzers
#     for analyzer in get_analyzers(CONFIG):
#         engine.register_analyzer(analyzer)

#     # Playbooks
#     playbooks = get_playbooks(CONFIG)
#     engine.register_playbooks(playbooks)

#     # Responders
#     for responder in get_responders(CONFIG):
#         engine.register_responder(responder)

#     print("[*] SOAR started (production mode)")

#     while True:
#         try:
#             engine.run()
#             time.sleep(CONFIG["loop_interval"])

#         except KeyboardInterrupt:
#             print("\n[*] SOAR stopped by user")
#             break

#         except Exception as e:
#             print(f"[!] Runtime error: {e}")
#             time.sleep(CONFIG["loop_interval"])


# if __name__ == "__main__":
#     main()

# import time

# from core.engine import SOAREngine
# from collectors.registry import get_collectors
# from analyzers.registry import get_analyzers
# from responders.registry import get_responders
# from playbooks.registry import get_playbooks


# # базовая конфигурация
# CONFIG = {
#     "loop_interval": 2,
#     "use_ml": False,
#     "enable_blocking": True,
#     "debug": True
# }


# def main():
#     engine = SOAREngine(config=CONFIG)

#     # collectors
#     for collector in get_collectors(CONFIG):
#         engine.register_collector(collector)

#     # analyzers
#     for analyzer in get_analyzers(CONFIG):
#         engine.register_analyzer(analyzer)

#     # playbooks
#     playbooks = get_playbooks(CONFIG)
#     engine.register_playbooks(playbooks)

#     # responders
#     for responder in get_responders(CONFIG):
#         engine.register_responder(responder)

#     print("[*] SOAR started (production mode with playbooks)")

#     while True:
#         try:
#             engine.run()
#             time.sleep(CONFIG["loop_interval"])

#         except KeyboardInterrupt:
#             print("\n[*] SOAR stopped by user")
#             break

#         except Exception as e:
#             print(f"[!] Runtime error: {e}")
#             time.sleep(CONFIG["loop_interval"])


# if __name__ == "__main__":
#     main()

# import time
# версия 4
# from core.engine import SOAREngine
# from collectors.registry import get_collectors
# from analyzers.registry import get_analyzers
# from responders.registry import get_responders


# # базовая конфигурация (потом вынесем в файл)
# CONFIG = {
#     "loop_interval": 2,
#     "use_ml": False,
#     "enable_blocking": True
# }


# def main():
#     engine = SOAREngine()

#     # collectors
#     collectors = get_collectors(CONFIG)
#     for collector in collectors:
#         engine.register_collector(collector)

#     # analyzers
#     analyzers = get_analyzers(CONFIG)
#     for analyzer in analyzers:
#         engine.register_analyzer(analyzer)

#     # responders
#     responders = get_responders(CONFIG)
#     for responder in responders:
#         engine.register_responder(responder)

#     print("[*] SOAR started (production mode)")

#     while True:
#         try:
#             engine.run()
#             time.sleep(CONFIG["loop_interval"])

#         except KeyboardInterrupt:
#             print("\n[*] SOAR stopped by user")
#             break

#         except Exception as e:
#             print(f"[!] Runtime error: {e}")
#             time.sleep(CONFIG["loop_interval"])


# if __name__ == "__main__":
#     main()

# import time

# from core.engine import SOAREngine
# from collectors.registry import get_collectors
# from analyzers.registry import get_analyzers


# class ConsoleResponder:
#     def respond(self, incidents):
#         if not incidents:
#             return

#         for inc in incidents:
#             print(f"[!] Incident detected: {inc}")


# def main():
#     engine = SOAREngine()

#     # регистрируем collectors
#     for collector in get_collectors():
#         engine.register_collector(collector)

#     # регистрируем analyzers
#     for analyzer in get_analyzers():
#         engine.register_analyzer(analyzer)

#     # responder
#     engine.register_responder(ConsoleResponder())

#     print("[*] SOAR started (loop mode)")

#     while True:
#         try:
#             engine.run()
#             time.sleep(2)  # интервал (потом вынесем в config)

#         except KeyboardInterrupt:
#             print("\n[*] Stopped by user")
#             break

#         except Exception as e:
#             print(f"[!] Error: {e}")
#             time.sleep(2)


# if __name__ == "__main__":
#     main()
# from core.engine import SOAREngine
# from analyzers.registry import get_analyzers
#версия 2

# class DummyCollector:
#     def collect(self):
#         return []


# class DummyResponder:
#     def respond(self, incidents):
#         if not incidents:
#             print("[*] No incidents")
#         for inc in incidents:
#             print(f"[!] Incident detected: {inc}")


# if __name__ == "__main__":
#     engine = SOAREngine()

#     engine.register_collector(DummyCollector())

#     for analyzer in get_analyzers():
#         engine.register_analyzer(analyzer)

#     engine.register_responder(DummyResponder())

#     engine.run()
# from core.engine import SOAREngine

#версия 1
# class DummyCollector:
#     def collect(self):
#         return []


# class DummyAnalyzer:
#     def analyze(self, events):
#         return []


# class DummyResponder:
#     def respond(self, incidents):
#         print("[*] No incidents")


# if __name__ == "__main__":
#     engine = SOAREngine()

#     engine.register_collector(DummyCollector())
#     engine.register_analyzer(DummyAnalyzer())
#     engine.register_responder(DummyResponder())

#     engine.run()