"""Smoke test for simulation code - minimal simulation step."""

import sys
import numpy as np
from pathlib import Path

# Add code directory to path
code_dir = Path(__file__).parent.parent / "code"
sys.path.insert(0, str(code_dir))


def test_qrng_simulation_basic():
    """Test basic QRNG simulation with fixed seed."""
    import inference.mqgt_qrng_harness as qrng
    
    # Run minimal simulation
    N = 1000  # Small N for speed
    eta = 1e-6
    E0 = 0.0
    E1 = 1.0
    base_logodds = 0.0
    seed = 42  # Fixed seed for reproducibility
    
    N1, N0, p1 = qrng.simulate_counts(N, eta, E0, E1, base_logodds, seed)
    
    # Basic invariants
    assert isinstance(N1, int)
    assert isinstance(N0, int)
    assert isinstance(p1, float)
    assert N1 >= 0
    assert N0 >= 0
    assert N1 + N0 == N
    assert 0.0 <= p1 <= 1.0
    assert not np.isnan(p1)
    assert not np.isinf(p1)


def test_frequentist_test_basic():
    """Test frequentist test function with simple inputs."""
    import inference.mqgt_qrng_harness as qrng
    
    # Simple test case
    N1 = 510
    N0 = 490
    E0 = 0.0
    E1 = 1.0
    alpha = 0.05
    
    result = qrng.frequentist_test(N1, N0, E0, E1, alpha)
    
    # Check output structure
    assert isinstance(result, dict)
    assert 'T' in result
    assert 'se' in result
    assert 'z' in result
    assert 'p_value' in result
    assert 'alpha' in result
    assert 'reject_H0' in result
    
    # Check types
    assert isinstance(result['T'], float)
    assert isinstance(result['z'], float)
    assert isinstance(result['p_value'], float)
    assert isinstance(result['reject_H0'], bool)
    
    # Check invariants
    assert not np.isnan(result['T'])
    assert not np.isnan(result['z'])
    assert 0.0 <= result['p_value'] <= 1.0
    assert result['alpha'] == alpha

