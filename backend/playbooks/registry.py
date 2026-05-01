from playbooks.engine import PlaybookEngine


def get_playbooks(config=None):
    return PlaybookEngine()

# from collectors.auth_log import AuthLogCollector


# def get_collectors(config=None):
#     return [AuthLogCollector()]

# from typing import List, Optional, Dict, Any

# from playbooks.base import BasePlaybook
# from playbooks.rules import (
#     BruteForcePlaybook,
#     SuspiciousActivityPlaybook
# )


# def get_playbooks(config: Optional[Dict[str, Any]] = None) -> List[BasePlaybook]:
#     playbooks: List[BasePlaybook] = []

#     # базовые правила
#     playbooks.append(BruteForcePlaybook())
#     playbooks.append(SuspiciousActivityPlaybook())

#     return playbooks