class LoggerResponder:

    def respond(self, actions):
        for action in actions:
            if action.get("type") == "log":
                print(f"[LOG] {action.get('message')}")