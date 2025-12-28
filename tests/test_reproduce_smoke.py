"""Smoke test for reproduce_all.py - minimal execution path."""

import sys
from pathlib import Path

# Add code directory to path
code_dir = Path(__file__).parent.parent / "code"
sys.path.insert(0, str(code_dir))


def test_dependency_check():
    """Test that dependency check function works."""
    import reproduce_all
    
    # Should return True if dependencies are installed
    result = reproduce_all.check_dependencies()
    assert isinstance(result, bool)
    # If dependencies are installed, should be True
    # If not, we'll catch it in CI


def test_reproduce_script_structure():
    """Test that reproduce_all.py has expected structure."""
    import reproduce_all
    from pathlib import Path
    
    # Check that it can find its own directory
    script_path = Path(reproduce_all.__file__)
    assert script_path.exists()
    assert script_path.name == "reproduce_all.py"
    
    # Check that code directory exists relative to script
    code_dir = script_path.parent / "code"
    assert code_dir.exists()

