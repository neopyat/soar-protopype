import json
import os
import time
from typing import Dict, List, Optional, DefaultDict
from collections import defaultdict

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


BASELINE_PATH = "ml_baseline.json"


class MLAnalyzer(BaseAnalyzer):
    def __init__(self, alpha: float = 0.3, window: int = 60) -> None:
        self.alpha: float = alpha
        self.window: int = window

        # история событий по IP
        self.ip_events: DefaultDict[str, List[Event]] = defaultdict(list)

        # baseline
        self.baseline: Dict[str, float] = self._load_baseline()

        # для temporal анализа
        self.last_seen: Dict[str, float] = {}

    # -------------------------
    # MAIN (совместим с pipeline)
    # -------------------------
    def analyze(self, event: Event) -> Optional[Incident]:
        if not event.ip:
            return None

        now: float = time.time()

        # добавляем событие в историю
        self.ip_events[event.ip].append(event)

        # очищаем окно
        self.ip_events[event.ip] = [
            e for e in self.ip_events[event.ip]
            if now - e.timestamp <= self.window
        ]

        ev_list: List[Event] = self.ip_events[event.ip]
        count: int = len(ev_list)

        # -------------------------
        # FEATURE 1: RATE
        # -------------------------
        timestamps: List[float] = [e.timestamp for e in ev_list if e.timestamp]
        duration: float = max((max(timestamps) - min(timestamps)), 1.0) if timestamps else 1.0
        rate: float = count / duration
        rate_score: float = min(rate / 5.0, 1.0)

        # -------------------------
        # FEATURE 2: BASELINE
        # -------------------------
        base: float = self.baseline.get(event.ip, 1.0)
        anomaly: float = count / base
        anomaly_score: float = min(anomaly / 10.0, 1.0)

        # -------------------------
        # FEATURE 3: THREAT
        # -------------------------
        threat_score: float = self._calc_threat(ev_list)

        # -------------------------
        # FEATURE 4: IMPACT
        # -------------------------
        impact_score: float = self._calc_impact(ev_list)

        # -------------------------
        # FEATURE 5: TEMPORAL
        # -------------------------
        last: float = self.last_seen.get(event.ip, now)
        delta: float = now - last

        temporal_boost: float = 1.5 if delta < 10 else 1.0
        self.last_seen[event.ip] = now

        # -------------------------
        # FINAL RISK
        # -------------------------
        risk: float = (
            anomaly_score *
            threat_score *
            impact_score *
            (1 + rate_score)
        ) * temporal_boost

        risk = min(risk, 1.0)

        # -------------------------
        # DECISION
        # -------------------------
        if risk < 0.3:
            self._update_baseline(event.ip, count)
            return None

        severity: str = self._risk_to_severity(risk)

        inc = Incident(
            type="anomaly",
            ip=event.ip,
            severity=severity
        )

        inc.add_event(event)

        inc.meta.update({
            "risk": round(risk, 3),
            "rate": round(rate, 3),
            "anomaly": round(anomaly_score, 3),
            "threat": round(threat_score, 3),
            "impact": round(impact_score, 3),
            "events": count
        })

        self._update_baseline(event.ip, count)

        return inc

    # -------------------------
    # FEATURE ENGINEERING
    # -------------------------

    def _calc_threat(self, events: List[Event]) -> float:
        weight: float = 1.0

        for e in events:
            if e.type == "failed_login":
                weight += 0.4
            elif e.type == "port_scan":
                weight += 0.3
            elif e.type == "connection":
                weight += 0.2

            if e.raw and "error" in e.raw.lower():
                weight += 0.2

        return min(weight, 2.0)

    def _calc_impact(self, events: List[Event]) -> float:
        types = {e.type for e in events}

        if "failed_login" in types:
            return 0.9

        if "port_scan" in types:
            return 0.7

        if "connection" in types:
            return 0.6

        return 0.4

    # -------------------------
    # BASELINE
    # -------------------------

    def _load_baseline(self) -> Dict[str, float]:
        if not os.path.exists(BASELINE_PATH):
            return {}

        try:
            with open(BASELINE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_baseline(self) -> None:
        try:
            with open(BASELINE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.baseline, f, indent=4)
        except Exception as e:
            print(f"[ML] Save error: {e}")

    def _update_baseline(self, ip: str, value: float) -> None:
        old: float = self.baseline.get(ip, 1.0)
        new: float = self.alpha * value + (1 - self.alpha) * old

        self.baseline[ip] = new
        self._save_baseline()

    # -------------------------
    # UTILS
    # -------------------------

    def _risk_to_severity(self, risk: float) -> str:
        if risk > 0.75:
            return "high"
        if risk > 0.45:
            return "medium"
        return "low"
