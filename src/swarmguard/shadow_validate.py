from __future__ import annotations

from typing import Any


REQUIRED_TOP_LEVEL = {
    "run_id",
    "profile",
    "experiment",
    "created_at",
    "signals",
    "decisions",
    "metadata",
    "summary",
}


REQUIRED_SIGNAL = {
    "run_id",
    "cycle",
    "integrity",
    "stress",
    "resonance",
    "sleep_debt",
    "canonical_promotions",
    "exploratory_promotions",
    "mode",
    "timestamp",
}


REQUIRED_DECISION = {
    "run_id",
    "cycle",
    "action",
    "reason",
    "confidence",
    "timestamp",
}


def _as_dict(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return value
    return {}


def _as_list(value: object) -> list[object]:
    if isinstance(value, list):
        return value
    return []


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_manifest_payload(payload: dict[str, object]) -> list[str]:
    errors: list[str] = []

    missing = REQUIRED_TOP_LEVEL.difference(payload.keys())
    if missing:
        errors.append(f"missing_top_level:{','.join(sorted(missing))}")

    signals = _as_list(payload.get("signals"))
    decisions = _as_list(payload.get("decisions"))

    for index, row in enumerate(signals):
        signal = _as_dict(row)
        missing_signal = REQUIRED_SIGNAL.difference(signal.keys())
        if missing_signal:
            errors.append(f"signal[{index}]_missing:{','.join(sorted(missing_signal))}")
            continue

        for numeric_key in ["integrity", "stress", "resonance", "sleep_debt"]:
            value = signal.get(numeric_key)
            if not _is_number(value):
                errors.append(f"signal[{index}]_{numeric_key}_not_numeric")
            elif float(value) < 0.0 or float(value) > 1.0:
                errors.append(f"signal[{index}]_{numeric_key}_out_of_range")

    for index, row in enumerate(decisions):
        decision = _as_dict(row)
        missing_decision = REQUIRED_DECISION.difference(decision.keys())
        if missing_decision:
            errors.append(f"decision[{index}]_missing:{','.join(sorted(missing_decision))}")
            continue

        confidence = decision.get("confidence")
        if not _is_number(confidence):
            errors.append(f"decision[{index}]_confidence_not_numeric")
        elif float(confidence) < 0.0 or float(confidence) > 1.0:
            errors.append(f"decision[{index}]_confidence_out_of_range")

    return errors
