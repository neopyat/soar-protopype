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

# import json
# import os
# import time
# from collections import defaultdict
# from typing import List, Dict, DefaultDict, Optional

# from analyzers.base import BaseAnalyzer
# from models.event import Event
# from models.incident import Incident


# BASELINE_PATH = "ml_baseline.json"


# class MLAnalyzer(BaseAnalyzer):
#     def __init__(self, alpha: float = 0.3):
#         self.alpha = alpha
#         self.last_seen: Dict[str, float] = {}

#     # -------------------------
#     # FIX: строго под BaseAnalyzer
#     # -------------------------
#     def analyze(self, event: Event) -> Optional[Incident]:
#         results = self._analyze_batch([event])
#         return results[0] if results else None

#     # -------------------------
#     # ТВОЙ ОРИГИНАЛЬНЫЙ КОД (1 в 1)
#     # -------------------------
#     def _analyze_batch(self, events: List[Event]) -> List[Incident]:
#         incidents: List[Incident] = []

#         if not events:
#             return incidents

#         baseline = self._load_baseline()
#         ip_events = self._group_by_ip(events)

#         new_baseline: Dict[str, float] = {}

#         now = time.time()

#         for ip, ev_list in ip_events.items():
#             count = len(ev_list)

#             # =========================
#             # 1. RATE
#             # =========================
#             timestamps = [e.timestamp for e in ev_list if e.timestamp]
#             duration = max((max(timestamps) - min(timestamps)), 1) if timestamps else 1
#             rate = count / duration

#             rate_score = min(rate / 5.0, 1.0)

#             # =========================
#             # 2. BASELINE
#             # =========================
#             base = baseline.get(ip, 1.0)
#             anomaly = count / base
#             anomaly_score = min(anomaly / 10.0, 1.0)

#             # =========================
#             # 3. THREAT
#             # =========================
#             threat_score = self._calc_threat(ev_list)

#             # =========================
#             # 4. IMPACT
#             # =========================
#             impact_score = self._calc_impact(ev_list)

#             # =========================
#             # 5. TEMPORAL BOOST
#             # =========================
#             last = self.last_seen.get(ip, now)
#             delta = now - last

#             temporal_boost = 1.5 if delta < 10 else 1.0
#             self.last_seen[ip] = now

#             # =========================
#             # 6. FINAL RISK
#             # =========================
#             risk = (
#                 anomaly_score *
#                 threat_score *
#                 impact_score *
#                 (1 + rate_score)
#             ) * temporal_boost

#             risk = min(risk, 1.0)

#             # =========================
#             # 7. DECISION
#             # =========================
#             if risk < 0.25:
#                 new_baseline[ip] = self._update_baseline(base, count)
#                 continue

#             severity = self._risk_to_severity(risk)

#             inc = Incident(
#                 type="anomaly",
#                 ip=ip,
#                 severity=severity,
#                 events=ev_list
#             )

#             inc.meta.update({
#                 "risk": round(risk, 3),
#                 "rate": round(rate, 3),
#                 "anomaly": round(anomaly_score, 3),
#                 "threat": round(threat_score, 3),
#                 "impact": round(impact_score, 3),
#                 "events": count
#             })

#             incidents.append(inc)

#             new_baseline[ip] = self._update_baseline(base, count)

#         self._save_baseline(new_baseline)

#         return incidents

#     # -------------------------
#     # FEATURE ENGINEERING
#     # -------------------------

#     def _group_by_ip(self, events: List[Event]) -> Dict[str, List[Event]]:
#         grouped: DefaultDict[str, List[Event]] = defaultdict(list)

#         for e in events:
#             if e.ip:
#                 grouped[e.ip].append(e)

#         return dict(grouped)

#     def _calc_threat(self, events: List[Event]) -> float:
#         weight = 1.0

#         for e in events:
#             if e.type == "failed_login":
#                 weight += 0.4
#             elif e.type == "port_scan":
#                 weight += 0.2

#             if e.raw and "error" in e.raw.lower():
#                 weight += 0.2

#         return min(weight, 2.0)

#     def _calc_impact(self, events: List[Event]) -> float:
#         types = {e.type for e in events}

#         if "failed_login" in types:
#             return 0.9

#         if "port_scan" in types:
#             return 0.6

#         return 0.4

#     # -------------------------
#     # BASELINE
#     # -------------------------

#     def _load_baseline(self) -> Dict[str, float]:
#         if not os.path.exists(BASELINE_PATH):
#             return {}

#         try:
#             with open(BASELINE_PATH, "r") as f:
#                 return json.load(f)
#         except Exception:
#             return {}

#     def _save_baseline(self, baseline: Dict[str, float]) -> None:
#         try:
#             with open(BASELINE_PATH, "w") as f:
#                 json.dump(baseline, f, indent=4)
#         except Exception as e:
#             print(f"[ML] Save error: {e}")

#     def _update_baseline(self, old: float, new: float) -> float:
#         return self.alpha * new + (1 - self.alpha) * old

#     # -------------------------
#     # UTILS
#     # -------------------------

#     def _risk_to_severity(self, risk: float) -> str:
#         if risk > 0.75:
#             return "high"
#         if risk > 0.45:
#             return "medium"
#         return "low"

# import json
# import os
# import time
# from collections import defaultdict
# from typing import List, Dict, DefaultDict, Union

# from analyzers.base import BaseAnalyzer
# from models.event import Event
# from models.incident import Incident


# BASELINE_PATH = "ml_baseline.json"


# class MLAnalyzer(BaseAnalyzer):
#     def __init__(self, alpha: float = 0.3):
#         self.alpha = alpha
#         self.last_seen: Dict[str, float] = {}

#     # -------------------------
#     # MAIN (FIXED)
#     # -------------------------
#     def analyze(self, events: Union[Event, List[Event]]) -> List[Incident]:
#         # адаптация под pipeline (event -> [event])
#         if isinstance(events, list):
#             events_list = events
#         else:
#             events_list = [events]

#         incidents: List[Incident] = []

#         if not events_list:
#             return incidents

#         baseline = self._load_baseline()
#         ip_events = self._group_by_ip(events_list)

#         new_baseline: Dict[str, float] = {}

#         now = time.time()

#         for ip, ev_list in ip_events.items():
#             count = len(ev_list)

#             # =========================
#             # 1. RATE
#             # =========================
#             timestamps = [e.timestamp for e in ev_list if e.timestamp]
#             duration = max((max(timestamps) - min(timestamps)), 1) if timestamps else 1
#             rate = count / duration

#             rate_score = min(rate / 5.0, 1.0)

#             # =========================
#             # 2. BASELINE
#             # =========================
#             base = baseline.get(ip, 1.0)
#             anomaly = count / base
#             anomaly_score = min(anomaly / 10.0, 1.0)

#             # =========================
#             # 3. THREAT
#             # =========================
#             threat_score = self._calc_threat(ev_list)

#             # =========================
#             # 4. IMPACT
#             # =========================
#             impact_score = self._calc_impact(ev_list)

#             # =========================
#             # 5. TEMPORAL BOOST
#             # =========================
#             last = self.last_seen.get(ip, now)
#             delta = now - last

#             temporal_boost = 1.5 if delta < 10 else 1.0
#             self.last_seen[ip] = now

#             # =========================
#             # 6. FINAL RISK
#             # =========================
#             risk = (
#                 anomaly_score *
#                 threat_score *
#                 impact_score *
#                 (1 + rate_score)
#             ) * temporal_boost

#             risk = min(risk, 1.0)

#             # =========================
#             # 7. DECISION
#             # =========================
#             if risk < 0.25:
#                 new_baseline[ip] = self._update_baseline(base, count)
#                 continue

#             severity = self._risk_to_severity(risk)

#             inc = Incident(
#                 type="anomaly",
#                 ip=ip,
#                 severity=severity,
#                 events=ev_list
#             )

#             inc.meta.update({
#                 "risk": round(risk, 3),
#                 "rate": round(rate, 3),
#                 "anomaly": round(anomaly_score, 3),
#                 "threat": round(threat_score, 3),
#                 "impact": round(impact_score, 3),
#                 "events": count
#             })

#             incidents.append(inc)

#             new_baseline[ip] = self._update_baseline(base, count)

#         self._save_baseline(new_baseline)

#         return incidents

#     # -------------------------
#     # FEATURE ENGINEERING
#     # -------------------------

#     def _group_by_ip(self, events: List[Event]) -> Dict[str, List[Event]]:
#         grouped: DefaultDict[str, List[Event]] = defaultdict(list)

#         for e in events:
#             if e.ip:
#                 grouped[e.ip].append(e)

#         return dict(grouped)

#     def _calc_threat(self, events: List[Event]) -> float:
#         weight = 1.0

#         for e in events:
#             if e.type == "failed_login":
#                 weight += 0.4
#             elif e.type == "port_scan":
#                 weight += 0.2

#             if e.raw and "error" in e.raw.lower():
#                 weight += 0.2

#         return min(weight, 2.0)

#     def _calc_impact(self, events: List[Event]) -> float:
#         types = {e.type for e in events}

#         if "failed_login" in types:
#             return 0.9

#         if "port_scan" in types:
#             return 0.6

#         return 0.4

#     # -------------------------
#     # BASELINE
#     # -------------------------

#     def _load_baseline(self) -> Dict[str, float]:
#         if not os.path.exists(BASELINE_PATH):
#             return {}

#         try:
#             with open(BASELINE_PATH, "r") as f:
#                 return json.load(f)
#         except Exception:
#             return {}

#     def _save_baseline(self, baseline: Dict[str, float]) -> None:
#         try:
#             with open(BASELINE_PATH, "w") as f:
#                 json.dump(baseline, f, indent=4)
#         except Exception as e:
#             print(f"[ML] Save error: {e}")

#     def _update_baseline(self, old: float, new: float) -> float:
#         return self.alpha * new + (1 - self.alpha) * old

#     # -------------------------
#     # UTILS
#     # -------------------------

#     def _risk_to_severity(self, risk: float) -> str:
#         if risk > 0.75:
#             return "high"
#         if risk > 0.45:
#             return "medium"
#         return "low"


# import json
# import os
# import time
# from collections import defaultdict
# from typing import List, Dict, DefaultDict

# from analyzers.base import BaseAnalyzer
# from models.event import Event
# from models.incident import Incident


# BASELINE_PATH = "ml_baseline.json"


# class MLAnalyzer(BaseAnalyzer):
#     def __init__(self, alpha: float = 0.3):
#         self.alpha = alpha
#         self.last_seen: Dict[str, float] = {}

#     # -------------------------
#     # MAIN
#     # -------------------------
#     def analyze(self, events: List[Event]) -> List[Incident]:
#         incidents: List[Incident] = []

#         if not events:
#             return incidents

#         baseline = self._load_baseline()
#         ip_events = self._group_by_ip(events)

#         new_baseline: Dict[str, float] = {}

#         now = time.time()

#         for ip, ev_list in ip_events.items():
#             count = len(ev_list)

#             # =========================
#             # 1. RATE (скорость атак)
#             # =========================
#             timestamps = [e.timestamp for e in ev_list if e.timestamp]
#             duration = max((max(timestamps) - min(timestamps)), 1) if timestamps else 1
#             rate = count / duration

#             rate_score = min(rate / 5.0, 1.0)

#             # =========================
#             # 2. BASELINE (норма)
#             # =========================
#             base = baseline.get(ip, 1.0)
#             anomaly = count / base
#             anomaly_score = min(anomaly / 10.0, 1.0)

#             # =========================
#             # 3. THREAT (тип атаки)
#             # =========================
#             threat_score = self._calc_threat(ev_list)

#             # =========================
#             # 4. IMPACT
#             # =========================
#             impact_score = self._calc_impact(ev_list)

#             # =========================
#             # 5. TEMPORAL BOOST
#             # =========================
#             last = self.last_seen.get(ip, now)
#             delta = now - last

#             if delta < 10:
#                 temporal_boost = 1.5
#             else:
#                 temporal_boost = 1.0

#             self.last_seen[ip] = now

#             # =========================
#             # 6. FINAL RISK
#             # =========================
#             risk = (
#                 anomaly_score *
#                 threat_score *
#                 impact_score *
#                 (1 + rate_score)
#             ) * temporal_boost

#             risk = min(risk, 1.0)

#             # =========================
#             # 7. DECISION
#             # =========================
#             if risk < 0.25:
#                 new_baseline[ip] = self._update_baseline(base, count)
#                 continue

#             severity = self._risk_to_severity(risk)

#             inc = Incident(
#                 type="anomaly",
#                 ip=ip,
#                 severity=severity,
#                 events=ev_list
#             )

#             inc.meta.update({
#                 "risk": round(risk, 3),
#                 "rate": round(rate, 3),
#                 "anomaly": round(anomaly_score, 3),
#                 "threat": round(threat_score, 3),
#                 "impact": round(impact_score, 3),
#                 "events": count
#             })

#             incidents.append(inc)

#             new_baseline[ip] = self._update_baseline(base, count)

#         self._save_baseline(new_baseline)

#         return incidents

#     # -------------------------
#     # FEATURE ENGINEERING
#     # -------------------------

#     def _group_by_ip(self, events: List[Event]) -> Dict[str, List[Event]]:
#         grouped: DefaultDict[str, List[Event]] = defaultdict(list)

#         for e in events:
#             if e.ip:
#                 grouped[e.ip].append(e)

#         return dict(grouped)

#     def _calc_threat(self, events: List[Event]) -> float:
#         weight = 1.0

#         for e in events:
#             if e.type == "failed_login":
#                 weight += 0.4
#             elif e.type == "port_scan":
#                 weight += 0.2

#             if e.raw and "error" in e.raw.lower():
#                 weight += 0.2

#         return min(weight, 2.0)

#     def _calc_impact(self, events: List[Event]) -> float:
#         types = {e.type for e in events}

#         if "failed_login" in types:
#             return 0.9

#         if "port_scan" in types:
#             return 0.6

#         return 0.4

#     # -------------------------
#     # BASELINE
#     # -------------------------

#     def _load_baseline(self) -> Dict[str, float]:
#         if not os.path.exists(BASELINE_PATH):
#             return {}

#         try:
#             with open(BASELINE_PATH, "r") as f:
#                 return json.load(f)
#         except Exception:
#             return {}

#     def _save_baseline(self, baseline: Dict[str, float]) -> None:
#         try:
#             with open(BASELINE_PATH, "w") as f:
#                 json.dump(baseline, f, indent=4)
#         except Exception as e:
#             print(f"[ML] Save error: {e}")

#     def _update_baseline(self, old: float, new: float) -> float:
#         return self.alpha * new + (1 - self.alpha) * old

#     # -------------------------
#     # UTILS
#     # -------------------------

#     def _risk_to_severity(self, risk: float) -> str:
#         if risk > 0.75:
#             return "high"
#         if risk > 0.45:
#             return "medium"
#         return "low"

# import json
# import os
# from collections import defaultdict
# from typing import List, Dict, DefaultDict

# from analyzers.base import BaseAnalyzer
# from models.event import Event
# from models.incident import Incident


# BASELINE_PATH = "ml_baseline.json"


# class MLAnalyzer(BaseAnalyzer):
#     """
#     Risk-based adaptive analyzer.

#     Реализует модель:
#         Risk = Likelihood × Threat × Impact

#     Соответствует:
#     - ISO 27005 (оценка риска)
#     - NIST SP 800-30 (расчёт риска)
#     """

#     def __init__(self, alpha: float = 0.3):
#         # коэффициент для экспоненциального сглаживания
#         self.alpha = alpha

#     # -------------------------
#     # MAIN
#     # -------------------------
#     def analyze(self, events: List[Event]) -> List[Incident]:
#         incidents: List[Incident] = []

#         if not events:
#             return incidents

#         baseline = self._load_baseline()
#         ip_events = self._group_by_ip(events)

#         new_baseline: Dict[str, float] = {}

#         for ip, ev_list in ip_events.items():
#             count = len(ev_list)

#             # -------------------------
#             # 1. LIKELIHOOD (аномальность)
#             # -------------------------
#             base = baseline.get(ip, 1.0)
#             likelihood_raw = count / base
#             likelihood_score = min(likelihood_raw / 10.0, 1.0)

#             # -------------------------
#             # 2. THREAT
#             # -------------------------
#             threat_weight = self._calc_threat(ev_list)

#             # -------------------------
#             # 3. IMPACT
#             # -------------------------
#             impact_weight = self._calc_impact(ev_list)

#             # -------------------------
#             # 4. RISK
#             # -------------------------
#             risk_score = likelihood_score * threat_weight * impact_weight

#             # -------------------------
#             # 5. DECISION
#             # -------------------------
#             if risk_score < 0.2:
#                 new_baseline[ip] = self._update_baseline(base, count)
#                 continue

#             severity = self._risk_to_severity(risk_score)

#             inc = Incident(
#                 type="anomaly",
#                 ip=ip,
#                 severity=severity,
#                 events=ev_list
#             )

#             # -------------------------
#             # META (для диплома)
#             # -------------------------
#             inc.meta.update({
#                 "risk_score": round(risk_score, 3),
#                 "likelihood": round(likelihood_score, 3),
#                 "threat_weight": round(threat_weight, 3),
#                 "impact": round(impact_weight, 3),
#                 "events_count": count
#             })

#             incidents.append(inc)

#             new_baseline[ip] = self._update_baseline(base, count)

#         self._save_baseline(new_baseline)

#         return incidents

#     # -------------------------
#     # FEATURE ENGINEERING
#     # -------------------------

#     def _group_by_ip(self, events: List[Event]) -> Dict[str, List[Event]]:
#         grouped: DefaultDict[str, List[Event]] = defaultdict(list)

#         for e in events:
#             if e.ip:
#                 grouped[e.ip].append(e)

#         return dict(grouped)

#     def _calc_threat(self, events: List[Event]) -> float:
#         """
#         Оценка уровня угрозы.
#         """
#         weight = 1.0

#         for e in events:
#             if e.type == "failed_login":
#                 weight += 0.3

#             if "error" in e.raw.lower():
#                 weight += 0.2

#         return min(weight, 2.0)

#     def _calc_impact(self, events: List[Event]) -> float:
#         """
#         Оценка потенциального воздействия.
#         """
#         types = {e.type for e in events}

#         if "failed_login" in types:
#             return 0.8

#         if "port_scan" in types:
#             return 0.5

#         return 0.4

#     # -------------------------
#     # BASELINE (обучение)
#     # -------------------------

#     def _load_baseline(self) -> Dict[str, float]:
#         if not os.path.exists(BASELINE_PATH):
#             return {}

#         try:
#             with open(BASELINE_PATH, "r") as f:
#                 return json.load(f)
#         except Exception:
#             return {}

#     def _save_baseline(self, baseline: Dict[str, float]) -> None:
#         try:
#             with open(BASELINE_PATH, "w") as f:
#                 json.dump(baseline, f, indent=4)
#         except Exception as e:
#             print(f"[!] Baseline save error: {e}")

#     def _update_baseline(self, old: float, new: float) -> float:
#         """
#         Экспоненциальное сглаживание:
#         new = alpha * new_value + (1 - alpha) * old_value
#         """
#         return self.alpha * new + (1 - self.alpha) * old

#     # -------------------------
#     # UTILS
#     # -------------------------

#     def _risk_to_severity(self, risk: float) -> str:
#         if risk > 0.7:
#             return "high"
#         if risk > 0.4:
#             return "medium"
#         return "low"