import json
from typing import Dict, Any

def ask_siem():
    print("\n[?] Does your organization use SIEM?")
    print("1. Wazuh")
    print("2. Splunk")
    print("3. Other")
    print("4. No SIEM")

    choice = input("Select option: ")

    mapping = {
        "1": "wazuh",
        "2": "splunk",
        "3": "other",
        "4": "none"
    }

    return mapping.get(choice, "none")


def ask_ml():
    return input("\n[?] Enable ML module? (y/n): ").lower() == "y"


def ask_blocking():
    return input("\n[?] Enable automatic blocking (iptables)? (y/n): ").lower() == "y"


def generate_config():
    config: Dict[str, Any] = {
        "loop_interval": 2,
        "debug": True,
        "use_ml": ask_ml(),
        "enable_blocking": ask_blocking(),
        "siem": ask_siem()
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    print("\n[*] Config saved to config.json")


if __name__ == "__main__":
    generate_config()