from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DecisionWindowPolicy:
    canonical_window_cycles: int = 500
    exploratory_window_cycles: int = 250
    canonical_limit_in_window: int = 1
    exploratory_limit_in_window: int = 2
    canonical_cooldown_cycles: int = 600


@dataclass(slots=True)
class DecisionWindowState:
    policy: DecisionWindowPolicy = field(default_factory=DecisionWindowPolicy)
    _canonical_cycles: dict[str, list[int]] = field(default_factory=dict)
    _exploratory_cycles: dict[str, list[int]] = field(default_factory=dict)

    def _prune(self, run_id: str, current_cycle: int) -> None:
        canonical_min = current_cycle - self.policy.canonical_window_cycles
        exploratory_min = current_cycle - self.policy.exploratory_window_cycles
        self._canonical_cycles[run_id] = [
            cycle for cycle in self._canonical_cycles.get(run_id, []) if cycle >= canonical_min
        ]
        self._exploratory_cycles[run_id] = [
            cycle for cycle in self._exploratory_cycles.get(run_id, []) if cycle >= exploratory_min
        ]

    def allow(self, *, run_id: str, cycle: int, action: str) -> tuple[bool, str]:
        if action not in {"promote_canonical", "promote_exploratory"}:
            return (True, "no-window-required")

        self._prune(run_id, cycle)

        if action == "promote_canonical":
            history = self._canonical_cycles.get(run_id, [])
            if len(history) >= self.policy.canonical_limit_in_window:
                return (False, "canonical-window-limit")
            if history and (cycle - history[-1]) < self.policy.canonical_cooldown_cycles:
                return (False, "canonical-cooldown")
            return (True, "canonical-window-ok")

        history = self._exploratory_cycles.get(run_id, [])
        if len(history) >= self.policy.exploratory_limit_in_window:
            return (False, "exploratory-window-limit")
        return (True, "exploratory-window-ok")

    def record(self, *, run_id: str, cycle: int, action: str) -> None:
        if action == "promote_canonical":
            self._canonical_cycles.setdefault(run_id, []).append(cycle)
        elif action == "promote_exploratory":
            self._exploratory_cycles.setdefault(run_id, []).append(cycle)
