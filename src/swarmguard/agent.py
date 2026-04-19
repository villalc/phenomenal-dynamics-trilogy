"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

import json
from dataclasses import dataclass
from typing import Any, Dict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


@dataclass
class Vote:
    agent_id: str
    proposal_id: str
    approval: bool
    signature: bytes


class SwarmAgent:
    def __init__(self, agent_id: str, role: str, trust_score: float = 1.0):
        self.agent_id = agent_id
        self.role = role
        self.trust_score = trust_score
        # Generate private key (simulated HSM)
        self._private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self._private_key.public_key()

    def sign_action(self, action: str) -> Dict[str, Any]:
        """Signs an action string and returns the payload."""
        signature = self._private_key.sign(
            action.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return {
            "agent_id": self.agent_id,
            "action": action,
            "signature": signature
        }

    def verify_peer(self, peer_agent: 'SwarmAgent', signed_payload: Dict[str, Any]) -> bool:
        """Verifies that the payload was signed by the peer agent."""
        if signed_payload.get("agent_id") != peer_agent.agent_id:
            return False

        try:
            peer_agent.public_key.verify(
                signed_payload["signature"],
                signed_payload["action"].encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False

    def consensus_vote(self, proposal: Dict[str, Any]) -> Vote:
        """
        Cast a vote on a proposal.
        Voting logic: Approve if trust_score >= 0.5.
        """
        approval = self.trust_score >= 0.5
        # The vote itself should be signed
        # Use canonical JSON serialization to prevent signature forgery
        vote_payload = {
            "agent_id": self.agent_id,
            "proposal_id": proposal.get('id'),
            "approval": approval
        }
        vote_data = json.dumps(vote_payload, sort_keys=True, separators=(',', ':'))
        signature = self._private_key.sign(
            vote_data.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return Vote(
            agent_id=self.agent_id,
            proposal_id=proposal.get('id', 'unknown'),
            approval=approval,
            signature=signature
        )
