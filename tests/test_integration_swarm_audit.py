"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

import json
import pytest
from src.swarmguard.swarm import SwarmCoordinator
from src.swarmguard.agent import SwarmAgent
from src.swarmguard.audit import BlockchainAuditLog, AuditIntegrityError, AuditEntry


def test_consensus_persists_audit_and_detects_tamper(tmp_path):
    path = tmp_path / "audit_log.json"
    coord = SwarmCoordinator(blockchain_path=str(path))

    a1 = SwarmAgent("a1", "node", 0.9)
    a2 = SwarmAgent("a2", "node", 0.9)
    a3 = SwarmAgent("a3", "node", 0.1)
    coord.register_agent(a1)
    coord.register_agent(a2)
    coord.register_agent(a3)

    proposal = coord.propose_action("activate_shield")
    result = coord.execute_if_consensus(proposal)

    assert "executed" in result
    assert coord.blockchain_log.verify_chain() is True

    reloaded = BlockchainAuditLog(persistence_path=str(path))
    assert reloaded.verify_chain() is True
    assert len(reloaded.chain) == 2

    # Deliberately tamper with action to test integrity verification
    reloaded.chain[1].action = "tampered"
    assert reloaded.verify_chain() is False

    data = json.loads(path.read_text())
    data[1]["action"] = "tampered"
    path.write_text(json.dumps(data))

    manual = BlockchainAuditLog.__new__(BlockchainAuditLog)
    manual._persistence_path = None  # type: ignore[attr-defined]
    manual.chain = [AuditEntry(**item) for item in data]  # type: ignore[attr-defined]
    assert manual.verify_chain() is False

    with pytest.raises(AuditIntegrityError):
        BlockchainAuditLog(persistence_path=str(path))
