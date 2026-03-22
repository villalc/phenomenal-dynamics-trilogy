from src.swarmguard.audit import BlockchainAuditLog
from src.swarmguard.shadow_bridge import ShadowDecisionBridge, phenomenal_to_shadow_metrics


def test_phenomenal_to_shadow_metrics_bounds() -> None:
    metrics = phenomenal_to_shadow_metrics(
        integrity=0.82,
        stress=0.35,
        resonance=0.61,
        trauma_memory=0.2,
        flourishing=0.3,
    )

    assert 0.0 <= metrics["sleep_debt_proxy"] <= 1.0
    assert 0.0 <= metrics["canonical_readiness"] <= 1.0
    assert 0.0 <= metrics["exploratory_bias"] <= 1.0
    assert 0.0 <= metrics["risk_index"] <= 1.0


def test_shadow_decision_bridge_records_chain() -> None:
    bridge = ShadowDecisionBridge(source="shadow-test", audit_log=BlockchainAuditLog())
    metrics = phenomenal_to_shadow_metrics(integrity=0.9, stress=0.2, resonance=0.5)
    action, reason, confidence = bridge.recommend_action(metrics)

    entry = bridge.record_decision(
        run_id="run-001",
        cycle=10,
        metrics=metrics,
        action=action,
        reason=reason,
        confidence=confidence,
    )

    assert "shadow_decision" in entry.action
    assert bridge.audit_log.verify_chain() is True
    assert len(bridge.audit_log.chain) == 2
