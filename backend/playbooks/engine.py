from playbooks.rules import RulesEngine


class PlaybookEngine:

    def __init__(self):
        self.rules = RulesEngine()

    def run(self, incidents):
        if not incidents:
            return []

        actions = self.rules.process(incidents)

        print(f"[PLAYBOOK] Generated actions: {actions}")

        return actions