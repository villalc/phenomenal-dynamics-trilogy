"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

from src.swarmguard.agent import SwarmAgent

def test_agent_creation():
    agent = SwarmAgent("test_agent", "observer", 0.8)
    assert agent.agent_id == "test_agent"
    assert agent.role == "observer"
    assert agent.trust_score == 0.8

def test_sign_and_verify():
    alice = SwarmAgent("alice", "admin", 1.0)
    bob = SwarmAgent("bob", "user", 0.5)

    action = "deploy_shield"
    signed_payload = alice.sign_action(action)

    # Bob verifies Alice's signature
    assert bob.verify_peer(alice, signed_payload) is True

    # Tamper with payload
    signed_payload["action"] = "disable_shield"
    assert bob.verify_peer(alice, signed_payload) is False

def test_consensus_vote():
    agent = SwarmAgent("voter", "node", 0.9)
    proposal = {"id": "prop-123", "action": "update"}

    vote = agent.consensus_vote(proposal)
    assert vote.agent_id == "voter"
    assert vote.proposal_id == "prop-123"
    assert vote.approval is True
    assert vote.signature is not None

def test_consensus_vote_low_trust():
    agent = SwarmAgent("untrusted", "node", 0.1)
    proposal = {"id": "prop-456", "action": "delete"}

    vote = agent.consensus_vote(proposal)
    assert vote.approval is False
