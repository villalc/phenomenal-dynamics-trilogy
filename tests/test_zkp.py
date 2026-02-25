"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

from src.swarmguard.zkp import ZeroKnowledgeVerifier

def test_zk_proof_flow():
    verifier = ZeroKnowledgeVerifier()
    secret = "nuclear_launch_codes"
    statement = "I know the codes"

    # Generate commitment
    commitment = verifier.generate_commitment(secret)
    assert len(commitment) == 64  # SHA-256 hex digest length

    # Create proof
    proof = verifier.create_proof(secret, statement)
    assert proof.statement == statement
    assert proof.timestamp > 0

    # Verify proof
    is_valid = verifier.verify_proof(proof, commitment, statement)
    assert is_valid is True

def test_zk_proof_invalid_statement():
    verifier = ZeroKnowledgeVerifier()
    secret = "secret"
    proof = verifier.create_proof(secret, "statement A")

    # Verification fails if statement doesn't match
    is_valid = verifier.verify_proof(proof, "commitment", "statement B")
    assert is_valid is False
