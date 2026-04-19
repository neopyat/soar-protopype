from core.engine import SOAREngine


class DummyCollector:
    def collect(self):
        return []


class DummyAnalyzer:
    def analyze(self, events):
        return []


class DummyResponder:
    def respond(self, incidents):
        print("[*] No incidents")


if __name__ == "__main__":
    engine = SOAREngine()

    engine.register_collector(DummyCollector())
    engine.register_analyzer(DummyAnalyzer())
    engine.register_responder(DummyResponder())

    engine.run()