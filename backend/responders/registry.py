from playbooks.engine import PlaybookEngine


def get_playbooks(config=None):
    return [PlaybookEngine()]