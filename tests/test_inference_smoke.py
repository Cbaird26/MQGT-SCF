"""Smoke test for inference code - minimal inference step."""

import sys
import numpy as np
from pathlib import Path

# Add code directory to path
code_dir = Path(__file__).parent.parent / "code"
sys.path.insert(0, str(code_dir))


def test_posterior_grid_basic():
    """Test posterior grid computation with minimal inputs."""
    import inference.mqgt_qrng_harness as qrng
    
    # Minimal test case
    N1 = 510
    N0 = 490
    E0 = 0.0
    E1 = 1.0
    base_logodds = 0.0
    prior_mu = 0.0
    prior_sigma = 1e-5
    eta_min = -1e-5
    eta_max = 1e-5
    n_grid = 101  # Small grid for speed
    
    result = qrng.posterior_grid(
        N1, N0, E0, E1, base_logodds,
        prior_mu, prior_sigma,
        eta_min, eta_max, n_grid
    )
    
    # Check output structure
    assert isinstance(result, dict)
    assert 'etas' in result
    assert 'post' in result
    assert 'mean' in result
    assert 'sd' in result
    assert 'median' in result
    assert 'ci95' in result
    assert 'map' in result
    
    # Check types
    assert isinstance(result['etas'], np.ndarray)
    assert isinstance(result['post'], np.ndarray)
    assert isinstance(result['mean'], float)
    assert isinstance(result['sd'], float)
    assert isinstance(result['median'], float)
    assert isinstance(result['map'], float)
    assert isinstance(result['ci95'], list)
    assert len(result['ci95']) == 2
    
    # Check shapes
    assert result['etas'].shape == (n_grid,)
    assert result['post'].shape == (n_grid,)
    
    # Check invariants
    assert np.all(np.isfinite(result['etas']))
    assert np.all(np.isfinite(result['post']))
    assert np.all(result['post'] >= 0)  # Probabilities non-negative
    assert not np.isnan(result['mean'])
    assert not np.isnan(result['sd'])
    assert not np.isnan(result['median'])
    assert not np.isnan(result['map'])
    assert result['sd'] >= 0  # Standard deviation non-negative
    assert result['ci95'][0] <= result['ci95'][1]  # CI bounds ordered


def test_sha256_function():
    """Test SHA256 hash function."""
    import inference.mqgt_prereg_pack as prereg
    from pathlib import Path
    import tempfile
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_path = Path(f.name)
    
    try:
        # Test hash function
        hash_result = prereg.sha256(temp_path)
        
        # Check output
        assert isinstance(hash_result, str)
        assert len(hash_result) == 64  # SHA256 hex string length
        assert all(c in '0123456789abcdef' for c in hash_result)
    finally:
        # Clean up
        temp_path.unlink()

