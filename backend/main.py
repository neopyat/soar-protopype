from core.engine import SOAREngine
from analyzers.registry import get_analyzers


class DummyCollector:
    def collect(self):
        return []


class DummyResponder:
    def respond(self, incidents):
        if not incidents:
            print("[*] No incidents")
        for inc in incidents:
            print(f"[!] Incident detected: {inc}")


if __name__ == "__main__":
    engine = SOAREngine()

    engine.register_collector(DummyCollector())

    for analyzer in get_analyzers():
        engine.register_analyzer(analyzer)

    engine.register_responder(DummyResponder())

    engine.run()
# from core.engine import SOAREngine

#версия 1
# class DummyCollector:
#     def collect(self):
#         return []


# class DummyAnalyzer:
#     def analyze(self, events):
#         return []


# class DummyResponder:
#     def respond(self, incidents):
#         print("[*] No incidents")


# if __name__ == "__main__":
#     engine = SOAREngine()

#     engine.register_collector(DummyCollector())
#     engine.register_analyzer(DummyAnalyzer())
#     engine.register_responder(DummyResponder())

#     engine.run()