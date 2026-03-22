from src.swarmguard.shadow_bridge import ShadowDecisionBridge
from src.swarmguard.shadow_policy import get_policy


def test_get_policy_fallback_balanced() -> None:
    fallback = get_policy("unknown-profile")
    assert fallback.name == "balanced"


def test_conservative_is_stricter_than_frontier() -> None:
    conservative = get_policy("conservative")
    frontier = get_policy("frontier")

    assert conservative.canonical_readiness_threshold > frontier.canonical_readiness_threshold
    assert conservative.canonical_max_risk < frontier.canonical_max_risk


def test_policy_changes_decision_outcome() -> None:
    metrics = {
        "risk_index": 0.49,
        "canonical_readiness": 0.70,
        "exploratory_bias": 0.58,
    }

    conservative = ShadowDecisionBridge(policy_name="conservative")
    frontier = ShadowDecisionBridge(policy_name="frontier")

    action_cons, _, _ = conservative.recommend_action(metrics)
    action_front, _, _ = frontier.recommend_action(metrics)

    assert action_cons in {"observe", "stabilize", "promote_exploratory", "promote_canonical"}
    assert action_front in {"observe", "stabilize", "promote_exploratory", "promote_canonical"}
    assert action_cons != action_front
