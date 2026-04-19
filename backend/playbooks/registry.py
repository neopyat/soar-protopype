from typing import List, Optional, Dict, Any
from playbooks.base import BasePlaybook
from playbooks.rules import BruteForcePlaybook


def get_playbooks(config: Optional[Dict[str, Any]] = None) -> List[BasePlaybook]:
    playbooks: List[BasePlaybook] = []

    playbooks.append(BruteForcePlaybook())

    return playbooks