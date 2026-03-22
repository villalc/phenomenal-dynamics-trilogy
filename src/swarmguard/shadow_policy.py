from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ShadowPolicy:
    name: str
    risk_stabilize_threshold: float
    canonical_readiness_threshold: float
    canonical_max_risk: float
    exploratory_bias_threshold: float
    exploratory_max_risk: float


POLICIES: dict[str, ShadowPolicy] = {
    "balanced": ShadowPolicy(
        name="balanced",
        risk_stabilize_threshold=0.70,
        canonical_readiness_threshold=0.68,
        canonical_max_risk=0.45,
        exploratory_bias_threshold=0.60,
        exploratory_max_risk=0.60,
    ),
    "conservative": ShadowPolicy(
        name="conservative",
        risk_stabilize_threshold=0.62,
        canonical_readiness_threshold=0.74,
        canonical_max_risk=0.38,
        exploratory_bias_threshold=0.70,
        exploratory_max_risk=0.48,
    ),
    "frontier": ShadowPolicy(
        name="frontier",
        risk_stabilize_threshold=0.78,
        canonical_readiness_threshold=0.64,
        canonical_max_risk=0.52,
        exploratory_bias_threshold=0.56,
        exploratory_max_risk=0.68,
    ),
    "recovery": ShadowPolicy(
        name="recovery",
        risk_stabilize_threshold=0.58,
        canonical_readiness_threshold=0.72,
        canonical_max_risk=0.34,
        exploratory_bias_threshold=0.65,
        exploratory_max_risk=0.42,
    ),
}


def get_policy(name: str) -> ShadowPolicy:
    return POLICIES.get(name, POLICIES["balanced"])
