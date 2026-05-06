import json

from typing import Any, Dict


# -------------------------
# HELPERS
# -------------------------
def ask_string(
    question: str,
    default: str
) -> str:

    user_input = input(
        f"{question} [default: {default}]: "
    ).strip()

    if user_input == "":
        return default

    return user_input


def ask_int(
    question: str,
    default: int
) -> int:

    while True:

        user_input = input(
            f"{question} [default: {default}]: "
        ).strip()

        if user_input == "":
            return default

        if user_input.isdigit():
            return int(user_input)

        print("[!] Please enter a valid integer")


def ask_float(
    question: str,
    default: float
) -> float:

    while True:

        user_input = input(
            f"{question} [default: {default}]: "
        ).strip()

        if user_input == "":
            return default

        try:
            return float(user_input)

        except ValueError:
            print("[!] Please enter a valid number")


def ask_yes_no(
    question: str,
    default: bool
) -> bool:

    default_str = "y" if default else "n"

    while True:

        user_input = input(
            f"{question} (y/n) [default: {default_str}]: "
        ).strip().lower()

        if user_input == "":
            return default

        if user_input in ("y", "yes"):
            return True

        if user_input in ("n", "no"):
            return False

        print("[!] Please enter y or n")


def ask_siem() -> str:

    print("\n[?] Select SIEM integration:")
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

        choice = input(
            "Select option [default: 4]: "
        ).strip()

        if choice == "":
            return "none"

        if choice in mapping:
            return mapping[choice]

        print("[!] Invalid option")


# -------------------------
# MAIN CONFIG
# -------------------------
def generate_config() -> None:

    print("")
    print("======================================")
    print("         SOAR Configuration")
    print("======================================")

    # -------------------------
    # CORE
    # -------------------------
    loop_interval = ask_int(
        "\n[?] Event loop interval (seconds)",
        2
    )

    debug = ask_yes_no(
        "[?] Enable debug logging?",
        False
    )

    # -------------------------
    # ML
    # -------------------------
    use_ml = ask_yes_no(
        "[?] Enable ML anomaly module?",
        False
    )

    # -------------------------
    # BLOCKING
    # -------------------------
    enable_blocking = ask_yes_no(
        "[?] Enable automatic remote blocking?",
        True
    )

    # -------------------------
    # SSH COLLECTION
    # -------------------------
    ssh_host = ask_string(
        "\n[?] Target SSH host",
        "192.168.0.109"
    )

    ssh_user = ask_string(
        "[?] Target SSH user",
        "srvr"
    )

    ssh_log_path = ask_string(
        "[?] SSH log path",
        "/var/log/auth.log"
    )

    # -------------------------
    # NETWORK MONITORING
    # -------------------------
    enable_network_monitoring = ask_yes_no(
        "\n[?] Enable network monitoring?",
        True
    )

    ddos_threshold = ask_int(
        "[?] DDoS detection threshold",
        30
    )

    # -------------------------
    # SYSTEM METRICS
    # -------------------------
    enable_system_metrics = ask_yes_no(
        "\n[?] Enable system metrics monitoring?",
        True
    )

    cpu_threshold = ask_float(
        "[?] CPU alert threshold",
        80.0
    )

    # -------------------------
    # SIEM
    # -------------------------
    siem = ask_siem()

    # -------------------------
    # CONFIG
    # -------------------------
    config: Dict[str, Any] = {
        "loop_interval": loop_interval,
        "debug": debug,
        "use_ml": use_ml,
        "enable_blocking": enable_blocking,

        "ssh_host": ssh_host,
        "ssh_user": ssh_user,
        "ssh_log_path": ssh_log_path,

        "enable_network_monitoring": enable_network_monitoring,
        "enable_system_metrics": enable_system_metrics,

        "ddos_threshold": ddos_threshold,
        "cpu_threshold": cpu_threshold,

        "siem": siem
    }

    # -------------------------
    # SAVE
    # -------------------------
    try:

        with open(
            "config.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                config,
                file,
                indent=4
            )

        print("")
        print("[✓] Configuration saved to config.json")

    except Exception as exc:

        print("")
        print(f"[!] Failed to save config: {exc}")


# -------------------------
# ENTRYPOINT
# -------------------------
if __name__ == "__main__":
    generate_config()


# import json
# from typing import Dict, Any


# # -------------------------
# # Helpers
# # -------------------------

# def ask_yes_no(question: str, default: bool = False) -> bool:
#     default_str = "y" if default else "n"

#     while True:
#         user_input = input(f"{question} (y/n) [default: {default_str}]: ").strip().lower()

#         if user_input == "":
#             return default

#         if user_input in ("y", "yes"):
#             return True

#         if user_input in ("n", "no"):
#             return False

#         print("[!] Invalid input. Please enter y/n.")


# def ask_siem() -> str:
#     print("\n[?] Select SIEM system:")
#     print("1. Wazuh")
#     print("2. Splunk")
#     print("3. Other")
#     print("4. None")

#     mapping = {
#         "1": "wazuh",
#         "2": "splunk",
#         "3": "other",
#         "4": "none"
#     }

#     while True:
#         choice = input("Select option [default: 4]: ").strip()

#         if choice == "":
#             return "none"

#         if choice in mapping:
#             return mapping[choice]

#         print("[!] Invalid selection. Choose 1-4.")


# def ask_int(question: str, default: int) -> int:
#     while True:
#         user_input = input(f"{question} [default: {default}]: ").strip()

#         if user_input == "":
#             return default

#         if user_input.isdigit():
#             return int(user_input)

#         print("[!] Please enter a valid number.")


# # -------------------------
# # Main config generator
# # -------------------------

# def generate_config() -> None:
#     print("\n==============================")
#     print("      SOAR Configuration      ")
#     print("==============================")

#     # Основные параметры
#     loop_interval = ask_int("[?] Loop interval (seconds)", 2)
#     debug = ask_yes_no("[?] Enable debug mode?", True)
#     use_ml = ask_yes_no("[?] Enable ML module?", False)
#     enable_blocking = ask_yes_no("[?] Enable automatic blocking (iptables)?", False)
#     siem = ask_siem()

#     # Формирование конфигурации
#     config: Dict[str, Any] = {
#         "loop_interval": loop_interval,
#         "debug": debug,
#         "use_ml": use_ml,
#         "enable_blocking": enable_blocking,
#         "siem": siem
#     }

#     # Сохранение
#     try:
#         with open("config.json", "w") as f:
#             json.dump(config, f, indent=4)

#         print("\n[*] Configuration saved to config.json")

#     except Exception as e:
#         print(f"[!] Error saving config: {e}")


# # -------------------------
# # Entry point
# # -------------------------

# if __name__ == "__main__":
#     generate_config()
