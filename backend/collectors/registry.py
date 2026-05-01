from collectors.auth_log import AuthLogCollector


def get_collectors(config=None):
    return [AuthLogCollector()]

# from typing import List, Optional, Dict, Any

# from collectors.base import BaseCollector
# from collectors.auth_log import AuthLogCollector


# def get_collectors(config: Optional[Dict[str, Any]] = None) -> List[BaseCollector]:
#     collectors: List[BaseCollector] = []

#     collectors.append(AuthLogCollector())

#     return collectors