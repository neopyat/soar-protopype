import urllib.request
from typing import Set


class ThreatIntel:
    def __init__(self) -> None:
        self.blacklist: Set[str] = set()

    def load_feeds(self) -> None:
        urls = [
            "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
            "https://rules.emergingthreats.net/blockrules/compromised-ips.txt"
        ]

        for url in urls:
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    content = response.read().decode("utf-8", errors="ignore")

                    for line in content.splitlines():
                        line = line.strip()

                        if not line or line.startswith("#"):
                            continue

                        self.blacklist.add(line)

                print(f"[TI] Loaded feed: {url}")

            except Exception as e:
                print(f"[TI] Failed to load {url}: {e}")

    def is_malicious(self, ip: str) -> bool:
        return ip in self.blacklist