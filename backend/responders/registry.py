from responders.iptables_blocker import IPTablesBlocker
from responders.logger import LoggerResponder


def get_responders(config=None):
    responders = []

    responders.append(LoggerResponder())

    if config and config.get("enable_blocking"):
        responders.append(IPTablesBlocker())

    return responders