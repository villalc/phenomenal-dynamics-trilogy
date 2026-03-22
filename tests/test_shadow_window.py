from src.swarmguard.shadow_bridge import ShadowDecisionBridge
from src.swarmguard.shadow_window import DecisionWindowPolicy, DecisionWindowState


def test_window_blocks_canonical_by_cooldown() -> None:
    state = DecisionWindowState(
        policy=DecisionWindowPolicy(
            canonical_window_cycles=100,
            exploratory_window_cycles=100,
            canonical_limit_in_window=2,
            exploratory_limit_in_window=2,
            canonical_cooldown_cycles=50,
        )
    )
    bridge = ShadowDecisionBridge(policy_name="frontier", window_state=state)

    metrics = {
        "risk_index": 0.2,
        "canonical_readiness": 0.9,
        "exploratory_bias": 0.4,
    }

    action_1, _, _ = bridge.recommend_action_for_cycle(run_id="run-1", cycle=10, metrics=metrics)
    action_2, reason_2, _ = bridge.recommend_action_for_cycle(run_id="run-1", cycle=20, metrics=metrics)

    assert action_1 == "promote_canonical"
    assert action_2 == "observe"
    assert reason_2.startswith("window-gate:")


def test_window_limits_exploratory_promotions() -> None:
    state = DecisionWindowState(
        policy=DecisionWindowPolicy(
            canonical_window_cycles=200,
            exploratory_window_cycles=100,
            canonical_limit_in_window=1,
            exploratory_limit_in_window=1,
            canonical_cooldown_cycles=200,
        )
    )
    bridge = ShadowDecisionBridge(policy_name="frontier", window_state=state)

    metrics = {
        "risk_index": 0.2,
        "canonical_readiness": 0.2,
        "exploratory_bias": 0.9,
    }

    action_1, _, _ = bridge.recommend_action_for_cycle(run_id="run-2", cycle=5, metrics=metrics)
    action_2, reason_2, _ = bridge.recommend_action_for_cycle(run_id="run-2", cycle=10, metrics=metrics)

    assert action_1 == "promote_exploratory"
    assert action_2 == "observe"
    assert reason_2.startswith("window-gate:")
