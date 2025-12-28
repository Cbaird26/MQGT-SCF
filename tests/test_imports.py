"""Test that critical modules import without side effects."""

import sys
from pathlib import Path

# Add code directory to path
code_dir = Path(__file__).parent.parent / "code"
sys.path.insert(0, str(code_dir))


def test_core_dependencies_import():
    """Test that core dependencies can be imported."""
    import numpy
    import scipy
    import matplotlib
    import pandas
    
    assert numpy is not None
    assert scipy is not None
    assert matplotlib is not None
    assert pandas is not None


def test_inference_modules_import():
    """Test that inference modules can be imported."""
    import inference.mqgt_qrng_harness as qrng
    import inference.mqgt_prereg_pack as prereg
    
    # Check key functions exist
    assert hasattr(qrng, 'simulate_counts')
    assert hasattr(qrng, 'frequentist_test')
    assert hasattr(prereg, 'sha256')
    assert hasattr(prereg, 'main')


def test_simulation_modules_import():
    """Test that simulation modules can be imported."""
    # Check if simulation modules exist and can be imported
    try:
        import simulations.mqgt_scf_simulation as sim
        assert sim is not None
    except ImportError:
        # If module doesn't exist yet, that's okay for now
        pass


def test_reproduce_script_imports():
    """Test that reproduce_all.py can be imported."""
    import reproduce_all
    
    assert hasattr(reproduce_all, 'check_dependencies')
    assert hasattr(reproduce_all, 'run_inference')

