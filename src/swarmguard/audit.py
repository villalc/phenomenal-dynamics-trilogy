"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional

class AuditIntegrityError(ValueError):
    """Raised when audit log integrity verification fails."""

@dataclass
class AuditEntry:
    timestamp: str
    agent_id: str
    action: str
    proof_hash: str
    prev_hash: str
    entry_hash: str = ""

class BlockchainAuditLog:
    def __init__(self, persistence_path: Optional[str] = None):
        self.chain: List[AuditEntry] = []
        self._persistence_path = Path(persistence_path) if persistence_path else None
        if self._persistence_path and self._persistence_path.exists():
            self._load_chain()
        else:
            self._append_genesis()
            self._persist_chain()

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
        genesis.entry_hash = self._calculate_hash(genesis)
        self.chain.append(genesis)

    def _persist_chain(self):
        if not self._persistence_path:
            return
        self._persistence_path.parent.mkdir(parents=True, exist_ok=True)
        serialized = [asdict(e) for e in self.chain]
        self._persistence_path.write_text(json.dumps(serialized, ensure_ascii=False, indent=2))

    def _load_chain(self):
        if not self._persistence_path:
            return
        raw = json.loads(self._persistence_path.read_text())
        self.chain = [AuditEntry(**item) for item in raw]
        for i in range(len(self.chain)):
            current = self.chain[i]
            expected_hash = self._calculate_hash(current)
            if not current.entry_hash:
                raise AuditIntegrityError(f"Integrity Error: entry {i} missing entry_hash")
            if current.entry_hash != expected_hash:
                raise AuditIntegrityError(f"Integrity Error: entry {i} hash mismatch")
            if i == 0:
                continue
            prev_hash = self._calculate_hash(self.chain[i-1])
            if current.prev_hash != prev_hash:
                raise AuditIntegrityError(
                    f"Integrity Error: entry {i} prev_hash {current.prev_hash} != expected {prev_hash}"
                )

    def get_last_hash(self) -> str:
        if not self.chain:
            return "0"*64
        return self._calculate_hash(self.chain[-1])

    def append_entry(self, entry: AuditEntry) -> bool:
        """Appends an entry after validating its prev_hash."""
        expected_prev = self.get_last_hash()
        if entry.prev_hash != expected_prev:
            raise AuditIntegrityError(f"Integrity Error: Entry prev_hash {entry.prev_hash} != chain tip {expected_prev}")

        entry.entry_hash = self._calculate_hash(entry)
        self.chain.append(entry)
        self._persist_chain()
        return True

    def verify_chain(self) -> bool:
        """Verifies the entire chain integrity."""
        for i in range(len(self.chain)):
            current = self.chain[i]
            if current.entry_hash and current.entry_hash != self._calculate_hash(current):
                return False
            if i == 0:
                continue
            prev = self.chain[i-1]
            if current.prev_hash != self._calculate_hash(prev):
                return False
        return True

    def export_chain(self) -> List[Dict]:
        return [asdict(e) for e in self.chain]
