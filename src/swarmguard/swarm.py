"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid
import json
from .agent import SwarmAgent, Vote
from .audit import BlockchainAuditLog, AuditEntry

@dataclass
class Proposal:
    id: str
    action: str
    created_at: datetime
    votes: List[Vote] = field(default_factory=list)
    status: str = "pending"  # pending, approved, rejected

class SwarmCoordinator:
    def __init__(self):
        self.agents: Dict[str, SwarmAgent] = {}
        self.audit_trail: List[Dict[str, Any]] = [] # Detailed internal log
        self.blockchain_log = BlockchainAuditLog() # Immutable ledger
        self.proposals: Dict[str, Proposal] = {}

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

        return result
