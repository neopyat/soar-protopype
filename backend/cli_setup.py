import json
from typing import Dict, Any


# -------------------------
# Helpers
# -------------------------

def ask_yes_no(question: str, default: bool = False) -> bool:
    default_str = "y" if default else "n"

    while True:
        user_input = input(f"{question} (y/n) [default: {default_str}]: ").strip().lower()

        if user_input == "":
            return default

        if user_input in ("y", "yes"):
            return True

        if user_input in ("n", "no"):
            return False

        print("[!] Invalid input. Please enter y/n.")


def ask_siem() -> str:
    print("\n[?] Select SIEM system:")
    print("1. Wazuh")
    print("2. Splunk")
    print("3. Other")
    print("4. None")

    mapping = {
        "1": "wazuh",
        "2": "splunk",
        "3": "other",
        "4": "none"
    }

    while True:
        choice = input("Select option [default: 4]: ").strip()

        if choice == "":
            return "none"

        if choice in mapping:
            return mapping[choice]

        print("[!] Invalid selection. Choose 1-4.")


def ask_int(question: str, default: int) -> int:
    while True:
        user_input = input(f"{question} [default: {default}]: ").strip()

        if user_input == "":
            return default

        if user_input.isdigit():
            return int(user_input)

        print("[!] Please enter a valid number.")


# -------------------------
# Main config generator
# -------------------------

def generate_config() -> None:
    print("\n==============================")
    print("      SOAR Configuration      ")
    print("==============================")

    # Основные параметры
    loop_interval = ask_int("[?] Loop interval (seconds)", 2)
    debug = ask_yes_no("[?] Enable debug mode?", True)
    use_ml = ask_yes_no("[?] Enable ML module?", False)
    enable_blocking = ask_yes_no("[?] Enable automatic blocking (iptables)?", False)
    siem = ask_siem()

    # Формирование конфигурации
    config: Dict[str, Any] = {
        "loop_interval": loop_interval,
        "debug": debug,
        "use_ml": use_ml,
        "enable_blocking": enable_blocking,
        "siem": siem
    }

    # Сохранение
    try:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        print("\n[*] Configuration saved to config.json")

    except Exception as e:
        print(f"[!] Error saving config: {e}")


# -------------------------
# Entry point
# -------------------------

if __name__ == "__main__":
    generate_config()

# import json
# from typing import Dict, Any

# def ask_siem():
#     print("\n[?] Does your organization use SIEM?")
#     print("1. Wazuh")
#     print("2. Splunk")
#     print("3. Other")
#     print("4. No SIEM")

#     choice = input("Select option: ")

#     mapping = {
#         "1": "wazuh",
#         "2": "splunk",
#         "3": "other",
#         "4": "none"
#     }

#     return mapping.get(choice, "none")


# def ask_ml():
#     return input("\n[?] Enable ML module? (y/n): ").lower() == "y"


# def ask_blocking():
#     return input("\n[?] Enable automatic blocking (iptables)? (y/n): ").lower() == "y"


# def generate_config():
#     config: Dict[str, Any] = {
#         "loop_interval": 2,
#         "debug": True,
#         "use_ml": ask_ml(),
#         "enable_blocking": ask_blocking(),
#         "siem": ask_siem()
#     }

#     with open("config.json", "w") as f:
#         json.dump(config, f, indent=4)

#     print("\n[*] Config saved to config.json")


# if __name__ == "__main__":
#     generate_config()