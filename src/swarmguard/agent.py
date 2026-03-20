"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    BestAvailableEncryption,
    Encoding,
    PrivateFormat,
    load_pem_private_key,
)

@dataclass
class Vote:
    agent_id: str
    proposal_id: str
    approval: bool
    signature: bytes

class SwarmAgent:
    def __init__(
        self,
        agent_id: str,
        role: str,
        trust_score: float = 1.0,
        private_key: Optional[ec.EllipticCurvePrivateKey] = None,
    ):
        self.agent_id = agent_id
        self.role = role
        self.trust_score = trust_score
        # Generate private key (simulated HSM) with secure RNG if not provided
        self._private_key: Optional[ec.EllipticCurvePrivateKey] = (
            private_key if private_key is not None else ec.generate_private_key(ec.SECP256R1())
        )
        self.public_key = self._private_key.public_key()

    def _require_private_key(self) -> ec.EllipticCurvePrivateKey:
        if self._private_key is None:
            raise ValueError("Private key is not available (destroyed or not loaded).")
        return self._private_key

    def sign_action(self, action: str) -> Dict[str, Any]:
        """Signs an action string and returns the payload."""
        private_key = self._require_private_key()
        signature = private_key.sign(
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
        vote_data = f"{self.agent_id}:{proposal.get('id')}:{approval}"
        private_key = self._require_private_key()
        signature = private_key.sign(
            vote_data.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return Vote(
            agent_id=self.agent_id,
            proposal_id=proposal.get('id', 'unknown'),
            approval=approval,
            signature=signature
        )

    def rotate_private_key(self) -> None:
        """Generates a new private key using a secure RNG and updates public key."""
        self._private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self._private_key.public_key()

    def destroy_private_key(self) -> None:
        """
        Best-effort removal of private key material from memory.
        Note: Python garbage collection is non-deterministic; material may stay
        in memory until the next GC cycle. For production-grade zeroization,
        use secure memory handling/zeroing primitives (e.g., ctypes.memset or
        secure-memory utilities) beyond pure Python.
        """
        self._private_key = None

    def export_private_key_encrypted(self, password: bytes) -> bytes:
        """
        Export the private key encrypted (at-rest encryption) for secure storage.
        """
        private_key = self._require_private_key()
        return private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=BestAvailableEncryption(password),
        )

    @classmethod
    def from_encrypted_private_key(
        cls,
        agent_id: str,
        role: str,
        trust_score: float,
        encrypted_pem: bytes,
        password: bytes,
    ) -> "SwarmAgent":
        """
        Restore an agent using an encrypted PEM private key.
        """
        private_key = load_pem_private_key(encrypted_pem, password=password)
        if not isinstance(private_key, ec.EllipticCurvePrivateKey):
            raise ValueError("Expected EC private key")
        return cls(agent_id, role, trust_score, private_key=private_key)
