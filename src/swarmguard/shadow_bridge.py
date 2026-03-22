from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone

from .audit import AuditEntry, BlockchainAuditLog
from .shadow_policy import get_policy
from .shadow_window import DecisionWindowState


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def phenomenal_to_shadow_metrics(
    *,
    integrity: float,
    stress: float,
    resonance: float,
    trauma_memory: float = 0.0,
    flourishing: float = 0.0,
) -> dict[str, float]:
    integrity_n = _clamp(integrity)
    stress_n = _clamp(stress)
    resonance_n = _clamp(resonance)
    trauma_n = _clamp(trauma_memory)
    flourishing_n = _clamp(flourishing)

    sleep_debt_proxy = _clamp(stress_n * (1.0 - integrity_n))
    canonical_readiness = _clamp((integrity_n * (1.0 - stress_n)) + (0.25 * flourishing_n) - (0.20 * trauma_n))
    exploratory_bias = _clamp((resonance_n * 0.55) + (stress_n * 0.30) + ((1.0 - integrity_n) * 0.15))
    risk_index = _clamp((sleep_debt_proxy * 0.45) + (stress_n * 0.35) + (trauma_n * 0.20))

    return {
        "integrity": round(integrity_n, 4),
        "stress": round(stress_n, 4),
        "resonance": round(resonance_n, 4),
        "sleep_debt_proxy": round(sleep_debt_proxy, 4),
        "canonical_readiness": round(canonical_readiness, 4),
        "exploratory_bias": round(exploratory_bias, 4),
        "risk_index": round(risk_index, 4),
    }


class ShadowDecisionBridge:
    def __init__(
        self,
        *,
        source: str = "shadow-bridge",
        audit_log: BlockchainAuditLog | None = None,
        policy_name: str = "balanced",
        window_state: DecisionWindowState | None = None,
    ) -> None:
        self.source = source
        self.audit_log = audit_log or BlockchainAuditLog()
        self.policy_name = policy_name
        self.window_state = window_state

    def recommend_action(self, metrics: dict[str, float]) -> tuple[str, str, float]:
        policy = get_policy(self.policy_name)
        risk = metrics.get("risk_index", 0.0)
        readiness = metrics.get("canonical_readiness", 0.0)
        exploratory = metrics.get("exploratory_bias", 0.0)

        if risk >= policy.risk_stabilize_threshold:
            return ("stabilize", "risk_index high", round(min(1.0, risk + 0.10), 4))
        if readiness >= policy.canonical_readiness_threshold and risk <= policy.canonical_max_risk:
            return ("promote_canonical", "readiness high and risk controlled", round(min(1.0, readiness + 0.08), 4))
        if exploratory >= policy.exploratory_bias_threshold and risk <= policy.exploratory_max_risk:
            return ("promote_exploratory", "exploratory bias high", round(min(1.0, exploratory + 0.05), 4))
        return ("observe", "insufficient confidence for promotion", 0.55)

    def record_decision(
        self,
        *,
        run_id: str,
        cycle: int,
        metrics: dict[str, float],
        action: str,
        reason: str,
        confidence: float,
    ) -> AuditEntry:
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = {
            "type": "shadow_decision",
            "source": self.source,
            "policy": self.policy_name,
            "run_id": run_id,
            "cycle": cycle,
            "action": action,
            "reason": reason,
            "confidence": round(_clamp(confidence), 4),
            "metrics": metrics,
        }

        entry = AuditEntry(
            timestamp=timestamp,
            agent_id=self.source,
            action=json.dumps(payload, ensure_ascii=True, sort_keys=True),
            proof_hash="0" * 64,
            prev_hash=self.audit_log.get_last_hash(),
        )
        self.audit_log.append_entry(entry)
        return entry

    def build_decision_payload(self, *, run_id: str, cycle: int, metrics: dict[str, float]) -> dict[str, object]:
        action, reason, confidence = self.recommend_action(metrics)
        return {
            "run_id": run_id,
            "cycle": cycle,
            "policy": self.policy_name,
            "action": action,
            "reason": reason,
            "confidence": confidence,
            "metrics": metrics,
        }

    def recommend_action_for_cycle(self, *, run_id: str, cycle: int, metrics: dict[str, float]) -> tuple[str, str, float]:
        action, reason, confidence = self.recommend_action(metrics)
        if not self.window_state:
            return (action, reason, confidence)

        allowed, gate_reason = self.window_state.allow(run_id=run_id, cycle=cycle, action=action)
        if not allowed:
            return ("observe", f"window-gate:{gate_reason}", min(confidence, 0.60))

        self.window_state.record(run_id=run_id, cycle=cycle, action=action)
        return (action, reason, confidence)
