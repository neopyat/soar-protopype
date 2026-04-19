class SOAREngine:
    def __init__(self):
        self.collectors = []
        self.analyzers = []
        self.responders = []

    def register_collector(self, collector):
        self.collectors.append(collector)

    def register_analyzer(self, analyzer):
        self.analyzers.append(analyzer)

    def register_responder(self, responder):
        self.responders.append(responder)

    def run(self):
        print("[*] SOAR started")

        events = []
        for collector in self.collectors:
            events.extend(collector.collect())

        print(f"[*] Events: {len(events)}")

        incidents = []
        for analyzer in self.analyzers:
            incidents.extend(analyzer.analyze(events))

        print(f"[*] Incidents: {len(incidents)}")

        for responder in self.responders:
            responder.respond(incidents)