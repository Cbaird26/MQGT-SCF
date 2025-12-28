"""Constraints module - attempts to import digitized constraints with graceful fallback."""

try:
    # Try importing from digitized package (if it exists)
    from digitized.constraints import *
except ImportError:
    # Fallback: try importing from data/processed/constraints
    import sys
    from pathlib import Path
    
    # Add data/processed to path if not already there
    data_constraints = Path(__file__).parent.parent.parent / "data" / "processed" / "constraints.py"
    if data_constraints.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("data_constraints", data_constraints)
        if spec and spec.loader:
            data_constraints_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(data_constraints_module)
            # Import the functions we need
            alpha_limit = getattr(data_constraints_module, 'alpha_limit', None)
            q_hinv = getattr(data_constraints_module, 'q_hinv', None)
            if alpha_limit is None or q_hinv is None:
                raise ImportError("digitized.constraints not available and data/processed/constraints.py missing required functions")
    else:
        raise ImportError(
            "digitized.constraints not available. "
            "For full reproduction, ensure data/processed/constraints.py exists or install digitized package. "
            "Some features may be limited without digitized constraints."
        )
