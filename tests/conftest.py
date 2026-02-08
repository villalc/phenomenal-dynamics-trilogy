"""
© 2025-2026 AHI 3.0 · AHI Governance Labs
Registro IMPI: EXP-3495968
License: MIT
"""
import pytest
from src.swarmguard.agent import SwarmAgent
from src.swarmguard.swarm import SwarmCoordinator

@pytest.fixture
def coordinator():
    return SwarmCoordinator()

@pytest.fixture
def agent_alpha():
    return SwarmAgent("alpha", "defense", 0.9)

@pytest.fixture
def agent_beta():
    return SwarmAgent("beta", "defense", 0.4)
