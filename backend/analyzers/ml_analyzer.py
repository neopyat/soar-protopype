import json
import os
from collections import defaultdict
from typing import List, Dict, DefaultDict

from analyzers.base import BaseAnalyzer
from models.event import Event
from models.incident import Incident


BASELINE_PATH = "ml_baseline.json"


class MLAnalyzer(BaseAnalyzer):
    """
    Risk-based adaptive analyzer.

    Реализует модель:
        Risk = Likelihood × Threat × Impact

    Соответствует:
    - ISO 27005 (оценка риска)
    - NIST SP 800-30 (расчёт риска)
    """

    def __init__(self, alpha: float = 0.3):
        # коэффициент для экспоненциального сглаживания
        self.alpha = alpha

    # -------------------------
    # MAIN
    # -------------------------
    def analyze(self, events: List[Event]) -> List[Incident]:
        incidents: List[Incident] = []

        if not events:
            return incidents

        baseline = self._load_baseline()
        ip_events = self._group_by_ip(events)

        new_baseline: Dict[str, float] = {}

        for ip, ev_list in ip_events.items():
            count = len(ev_list)

            # -------------------------
            # 1. LIKELIHOOD (аномальность)
            # -------------------------
            base = baseline.get(ip, 1.0)
            likelihood_raw = count / base
            likelihood_score = min(likelihood_raw / 10.0, 1.0)

            # -------------------------
            # 2. THREAT
            # -------------------------
            threat_weight = self._calc_threat(ev_list)

            # -------------------------
            # 3. IMPACT
            # -------------------------
            impact_weight = self._calc_impact(ev_list)

            # -------------------------
            # 4. RISK
            # -------------------------
            risk_score = likelihood_score * threat_weight * impact_weight

            # -------------------------
            # 5. DECISION
            # -------------------------
            if risk_score < 0.2:
                new_baseline[ip] = self._update_baseline(base, count)
                continue

            severity = self._risk_to_severity(risk_score)

            inc = Incident(
                type="anomaly",
                ip=ip,
                severity=severity,
                events=ev_list
            )

            # -------------------------
            # META (для диплома)
            # -------------------------
            inc.meta.update({
                "risk_score": round(risk_score, 3),
                "likelihood": round(likelihood_score, 3),
                "threat_weight": round(threat_weight, 3),
                "impact": round(impact_weight, 3),
                "events_count": count
            })

            incidents.append(inc)

            new_baseline[ip] = self._update_baseline(base, count)

        self._save_baseline(new_baseline)

        return incidents

    # -------------------------
    # FEATURE ENGINEERING
    # -------------------------

    def _group_by_ip(self, events: List[Event]) -> Dict[str, List[Event]]:
        grouped: DefaultDict[str, List[Event]] = defaultdict(list)

        for e in events:
            if e.ip:
                grouped[e.ip].append(e)

        return dict(grouped)

    def _calc_threat(self, events: List[Event]) -> float:
        """
        Оценка уровня угрозы.
        """
        weight = 1.0

        for e in events:
            if e.type == "failed_login":
                weight += 0.3

            if "error" in e.raw.lower():
                weight += 0.2

        return min(weight, 2.0)

    def _calc_impact(self, events: List[Event]) -> float:
        """
        Оценка потенциального воздействия.
        """
        types = {e.type for e in events}

        if "failed_login" in types:
            return 0.8

        if "port_scan" in types:
            return 0.5

        return 0.4

    # -------------------------
    # BASELINE (обучение)
    # -------------------------

    def _load_baseline(self) -> Dict[str, float]:
        if not os.path.exists(BASELINE_PATH):
            return {}

        try:
            with open(BASELINE_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_baseline(self, baseline: Dict[str, float]) -> None:
        try:
            with open(BASELINE_PATH, "w") as f:
                json.dump(baseline, f, indent=4)
        except Exception as e:
            print(f"[!] Baseline save error: {e}")

    def _update_baseline(self, old: float, new: float) -> float:
        """
        Экспоненциальное сглаживание:
        new = alpha * new_value + (1 - alpha) * old_value
        """
        return self.alpha * new + (1 - self.alpha) * old

    # -------------------------
    # UTILS
    # -------------------------

    def _risk_to_severity(self, risk: float) -> str:
        if risk > 0.7:
            return "high"
        if risk > 0.4:
            return "medium"
        return "low"