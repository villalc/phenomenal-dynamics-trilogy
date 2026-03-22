from src.swarmguard.shadow_validate import validate_manifest_payload


def test_validate_manifest_payload_ok() -> None:
    payload = {
        "run_id": "run-1",
        "profile": "frontier",
        "experiment": "exp",
        "created_at": "2026-01-01T00:00:00+00:00",
        "signals": [
            {
                "run_id": "run-1",
                "cycle": 1,
                "integrity": 0.9,
                "stress": 0.2,
                "resonance": 0.7,
                "sleep_debt": 0.03,
                "canonical_promotions": 1,
                "exploratory_promotions": 2,
                "mode": "FLOW",
                "timestamp": "2026-01-01T00:00:00+00:00",
            }
        ],
        "decisions": [
            {
                "run_id": "run-1",
                "cycle": 1,
                "action": "observe",
                "reason": "demo",
                "confidence": 0.7,
                "timestamp": "2026-01-01T00:00:00+00:00",
            }
        ],
        "metadata": {},
        "summary": {},
    }

    assert validate_manifest_payload(payload) == []


def test_validate_manifest_payload_detects_errors() -> None:
    payload = {
        "run_id": "run-1",
        "profile": "frontier",
        "signals": [
            {
                "run_id": "run-1",
                "cycle": 1,
                "integrity": 1.2,
                "stress": 0.2,
                "resonance": 0.7,
                "sleep_debt": 0.03,
                "canonical_promotions": 1,
                "exploratory_promotions": 2,
                "mode": "FLOW",
                "timestamp": "2026-01-01T00:00:00+00:00",
            }
        ],
        "decisions": [
            {
                "run_id": "run-1",
                "cycle": 1,
                "action": "observe",
                "reason": "demo",
                "confidence": 1.4,
                "timestamp": "2026-01-01T00:00:00+00:00",
            }
        ],
        "metadata": {},
        "summary": {},
    }

    errors = validate_manifest_payload(payload)
    assert any(error.startswith("missing_top_level") for error in errors)
    assert "signal[0]_integrity_out_of_range" in errors
    assert "decision[0]_confidence_out_of_range" in errors
