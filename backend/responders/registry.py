from typing import List, Optional, Dict, Any

from responders.base import BaseResponder
from responders.logger import LoggerResponder
from responders.iptables_blocker import IPTablesBlocker


def get_responders(config: Optional[Dict[str, Any]] = None) -> List[BaseResponder]:
    responders: List[BaseResponder] = []

    responders.append(LoggerResponder())

    if config and config.get("enable_blocking"):
        responders.append(IPTablesBlocker())

    return responders