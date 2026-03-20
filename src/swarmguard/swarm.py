"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
import time
import uuid
import json
from .agent import SwarmAgent, Vote
from .audit import BlockchainAuditLog, AuditEntry

try:  # pragma: no cover - optional dependency
    from prometheus_client import Counter as PromCounter, Histogram as PromHistogram
    CounterType: Optional[type] = PromCounter
    HistogramType: Optional[type] = PromHistogram
except ImportError:  # pragma: no cover - optional dependency
    CounterType = None  # type: ignore[assignment]
    HistogramType = None  # type: ignore[assignment]


def _build_counter(name: str, description: str, labelnames: List[str], registry: Optional[Any]):
    if CounterType is None:
        class _Dummy:
            def labels(self, *args, **kwargs):
                return self
            def inc(self, *args, **kwargs):
                return None
        return _Dummy()
    # registry=None registers on the global registry (can collide when multiple coordinators are created);
    # pass a CollectorRegistry in tests/services to avoid duplicate metric names.
    reg = registry
    return CounterType(name, description, labelnames=labelnames, registry=reg)  # type: ignore[call-arg]


def _build_histogram(name: str, description: str, labelnames: List[str], registry: Optional[Any]):
    if HistogramType is None:
        class _Dummy:
            def labels(self, *args, **kwargs):
                return self
            def observe(self, *args, **kwargs):
                return None
        return _Dummy()
    reg = registry
    return HistogramType(name, description, labelnames=labelnames, registry=reg)  # type: ignore[call-arg]

@dataclass
class Proposal:
    id: str
    action: str
    created_at: datetime
    votes: List[Vote] = field(default_factory=list)
    status: str = "pending"  # pending, approved, rejected

class SwarmCoordinator:
    def __init__(self, blockchain_path: Optional[str] = None, metrics_registry: Optional[Any] = None):
        self.agents: Dict[str, SwarmAgent] = {}
        self.audit_trail: List[Dict[str, Any]] = [] # Detailed internal log
        self.blockchain_log = BlockchainAuditLog(persistence_path=blockchain_path) # Immutable ledger
        self.proposals: Dict[str, Proposal] = {}
        self._consensus_counter = _build_counter(
            "swarm_consensus_total",
            "Total consensus decisions by status",
            ["status"],
            metrics_registry,
        )
        self._consensus_latency = _build_histogram(
            "swarm_consensus_latency_seconds",
            "Time taken to complete consensus evaluation",
            ["status"],
            metrics_registry,
        )

    def register_agent(self, agent: SwarmAgent):
        self.agents[agent.agent_id] = agent

    def remove_agent(self, agent_id: str):
        if agent_id in self.agents:
            del self.agents[agent_id]

    def propose_action(self, action: str) -> Proposal:
        proposal_id = str(uuid.uuid4())
        proposal = Proposal(
            id=proposal_id,
            action=action,
            created_at=datetime.now(timezone.utc)
        )
        self.proposals[proposal_id] = proposal

        # Collect votes from all agents
        for agent in self.agents.values():
            vote = agent.consensus_vote({"id": proposal_id, "action": action})
            proposal.votes.append(vote)

        return proposal

    def execute_if_consensus(self, proposal: Proposal) -> str:
        start = time.perf_counter()
        if proposal.status != "pending":
            return f"Proposal already {proposal.status}"

        total_agents = len(self.agents)
        if total_agents == 0:
            proposal.status = "rejected"
            return "No agents to vote"

        approvals = sum(1 for v in proposal.votes if v.approval)
        consensus_ratio = approvals / total_agents

        # 51% consensus threshold
        if consensus_ratio >= 0.51:
            proposal.status = "approved"
            result = f"Action '{proposal.action}' executed with {consensus_ratio:.2%} consensus"
        else:
            proposal.status = "rejected"
            result = f"Action '{proposal.action}' rejected with {consensus_ratio:.2%} consensus"

        timestamp = datetime.now(timezone.utc).isoformat()

        # Log to internal audit trail
        self.audit_trail.append({
            "timestamp": timestamp,
            "proposal_id": proposal.id,
            "action": proposal.action,
            "result": result,
            "consensus_ratio": consensus_ratio
        })

        # Log to blockchain audit log
        # We include the consensus result in the action field for the ledger
        ledger_action = {
            "action": proposal.action,
            "result": result,
            "consensus_ratio": consensus_ratio
        }

        entry = AuditEntry(
            timestamp=timestamp,
            agent_id="COORDINATOR",
            action=json.dumps(ledger_action),
            proof_hash="0"*64,
            prev_hash=self.blockchain_log.get_last_hash()
        )
        self.blockchain_log.append_entry(entry)

        duration = time.perf_counter() - start
        self._consensus_counter.labels(status=proposal.status).inc()
        self._consensus_latency.labels(status=proposal.status).observe(duration)
        return result
