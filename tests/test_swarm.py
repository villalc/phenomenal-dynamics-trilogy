"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

from src.swarmguard.swarm import SwarmCoordinator
from src.swarmguard.agent import SwarmAgent

def test_consensus_approval():
    coord = SwarmCoordinator()

    # Add agents
    # 2 out of 3 agents have high trust > 0.5 (66% approval)
    a1 = SwarmAgent("a1", "node", 0.9)
    a2 = SwarmAgent("a2", "node", 0.9)
    a3 = SwarmAgent("a3", "node", 0.1)

    coord.register_agent(a1)
    coord.register_agent(a2)
    coord.register_agent(a3)

    proposal = coord.propose_action("fire_lasers")
    assert proposal.status == "pending"
    assert len(proposal.votes) == 3

    result = coord.execute_if_consensus(proposal)
    assert proposal.status == "approved"
    assert "executed" in result
    assert len(coord.audit_trail) == 1
    assert coord.audit_trail[0]["consensus_ratio"] > 0.6

    # Check blockchain log
    assert len(coord.blockchain_log.chain) == 2 # Genesis + 1 entry
    assert "fire_lasers" in coord.blockchain_log.chain[1].action

def test_consensus_rejection():
    coord = SwarmCoordinator()

    # 1 out of 3 agents have high trust (33% approval)
    a1 = SwarmAgent("a1", "node", 0.9)
    a2 = SwarmAgent("a2", "node", 0.1)
    a3 = SwarmAgent("a3", "node", 0.1)

    coord.register_agent(a1)
    coord.register_agent(a2)
    coord.register_agent(a3)

    proposal = coord.propose_action("self_destruct")
    result = coord.execute_if_consensus(proposal)

    assert proposal.status == "rejected"
    assert "rejected" in result

    # Check blockchain log
    assert len(coord.blockchain_log.chain) == 2 # Genesis + 1 entry
    assert "self_destruct" in coord.blockchain_log.chain[1].action
