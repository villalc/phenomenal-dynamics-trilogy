"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

import hashlib
import json
from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class AuditEntry:
    timestamp: str
    agent_id: str
    action: str
    proof_hash: str
    prev_hash: str

class BlockchainAuditLog:
    def __init__(self):
        self.chain: List[AuditEntry] = []
        # Genesis block
        self._append_genesis()

    def _calculate_hash(self, entry: AuditEntry) -> str:
        entry_str = f"{entry.timestamp}{entry.agent_id}{entry.action}{entry.proof_hash}{entry.prev_hash}"
        return hashlib.sha256(entry_str.encode()).hexdigest()

    def _append_genesis(self):
        genesis = AuditEntry(
            timestamp="1970-01-01T00:00:00",
            agent_id="SYSTEM",
            action="GENESIS",
            proof_hash="0"*64,
            prev_hash="0"*64
        )
        self.chain.append(genesis)

    def get_last_hash(self) -> str:
        if not self.chain:
            return "0"*64
        return self._calculate_hash(self.chain[-1])

    def append_entry(self, entry: AuditEntry) -> bool:
        """Appends an entry after validating its prev_hash."""
        expected_prev = self.get_last_hash()
        if entry.prev_hash != expected_prev:
            raise ValueError(f"Integrity Error: Entry prev_hash {entry.prev_hash} != chain tip {expected_prev}")

        self.chain.append(entry)
        return True

    def verify_chain(self) -> bool:
        """Verifies the entire chain integrity."""
        for i in range(1, len(self.chain)):
            prev = self.chain[i-1]
            curr = self.chain[i]
            if curr.prev_hash != self._calculate_hash(prev):
                return False
        return True

    def export_chain(self) -> List[Dict]:
        return [asdict(e) for e in self.chain]
