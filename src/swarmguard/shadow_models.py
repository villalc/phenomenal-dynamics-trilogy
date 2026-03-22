from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class ShadowSignal:
    run_id: str
    cycle: int
    integrity: float
    stress: float
    resonance: float
    sleep_debt: float
    canonical_promotions: int
    exploratory_promotions: int
    mode: str
    note: str = ""
    timestamp: str = field(default_factory=utc_now)


@dataclass(slots=True)
class ShadowDecision:
    run_id: str
    cycle: int
    action: str
    reason: str
    confidence: float
    timestamp: str = field(default_factory=utc_now)


@dataclass(slots=True)
class ShadowRunManifest:
    run_id: str
    profile: str
    experiment: str
    created_at: str = field(default_factory=utc_now)
    signals: list[ShadowSignal] = field(default_factory=list)
    decisions: list[ShadowDecision] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    def add_signal(self, signal: ShadowSignal) -> None:
        self.signals.append(signal)

    def add_decision(self, decision: ShadowDecision) -> None:
        self.decisions.append(decision)

    def summary(self) -> dict[str, Any]:
        if not self.signals:
            return {
                "run_id": self.run_id,
                "signals": 0,
                "decisions": len(self.decisions),
                "sleep_debt_mean": 0.0,
                "integrity_mean": 0.0,
            }

        sleep_debt_mean = sum(signal.sleep_debt for signal in self.signals) / len(self.signals)
        integrity_mean = sum(signal.integrity for signal in self.signals) / len(self.signals)
        return {
            "run_id": self.run_id,
            "signals": len(self.signals),
            "decisions": len(self.decisions),
            "sleep_debt_mean": round(sleep_debt_mean, 4),
            "integrity_mean": round(integrity_mean, 4),
        }

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["summary"] = self.summary()
        return payload
