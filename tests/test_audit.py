"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

import pytest
from src.swarmguard.audit import BlockchainAuditLog, AuditEntry

def test_audit_log_append_and_verify():
    log = BlockchainAuditLog()
    assert len(log.chain) == 1  # Genesis block

    # Append valid entry
    entry1 = AuditEntry(
        timestamp="2025-01-01T12:00:00",
        agent_id="agent1",
        action="login",
        proof_hash="abc",
        prev_hash=log.get_last_hash()
    )
    log.append_entry(entry1)

    assert len(log.chain) == 2
    assert log.verify_chain() is True

def test_audit_log_tamper_detection():
    log = BlockchainAuditLog()

    entry1 = AuditEntry(
        timestamp="2025-01-01T12:00:00",
        agent_id="agent1",
        action="login",
        proof_hash="abc",
        prev_hash=log.get_last_hash()
    )
    log.append_entry(entry1)

    entry2 = AuditEntry(
        timestamp="2025-01-01T13:00:00",
        agent_id="agent1",
        action="logout",
        proof_hash="def",
        prev_hash=log.get_last_hash()
    )
    log.append_entry(entry2)

    assert log.verify_chain() is True

    # Now tamper with entry 1 (which is at index 1, index 0 is genesis)
    log.chain[1].action = "hacked_login"

    # Now entry 2's prev_hash (which points to hash of original entry 1)
    # won't match hash(modified entry 1)
    assert log.verify_chain() is False

def test_audit_log_append_invalid_prev_hash():
    log = BlockchainAuditLog()

    entry_invalid = AuditEntry(
        timestamp="2025-01-01T12:00:00",
        agent_id="agent1",
        action="login",
        proof_hash="abc",
        prev_hash="wrong_hash"
    )

    with pytest.raises(ValueError):
        log.append_entry(entry_invalid)

def test_audit_log_export_chain():
    from dataclasses import asdict
    log = BlockchainAuditLog()

    # Check genesis export
    exported = log.export_chain()
    assert len(exported) == 1
    assert exported[0] == asdict(log.chain[0])

    # Append an entry and check export again
    entry1 = AuditEntry(
        timestamp="2025-01-01T12:00:00",
        agent_id="agent1",
        action="login",
        proof_hash="abc",
        prev_hash=log.get_last_hash()
    )
    log.append_entry(entry1)

    exported = log.export_chain()
    assert len(exported) == 2
    assert exported[1] == asdict(entry1)
