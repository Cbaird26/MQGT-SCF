"""Fail-closed contract tests for reproduce_all.py."""

import sys
from pathlib import Path

# Add code directory to path
code_dir = Path(__file__).parent.parent / "code"
sys.path.insert(0, str(code_dir))


def test_dependency_check():
    """Test that dependency check function works."""
    import reproduce_all
    
    result = reproduce_all.check_dependencies()
    assert isinstance(result, bool)


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


def test_missing_digitized_input_is_an_error(tmp_path):
    import reproduce_all

    data_dir = tmp_path / "processed"
    data_dir.mkdir()
    ok, message = reproduce_all.check_digitized_data(data_dir)
    assert ok is False
    assert "missing digitized inputs" in message


def test_main_stops_nonzero_on_missing_digitized_input(monkeypatch):
    import reproduce_all

    monkeypatch.setattr(reproduce_all, "check_dependencies", lambda: True)
    monkeypatch.setattr(
        reproduce_all,
        "check_digitized_data",
        lambda: (False, "missing digitized inputs: constraints.py"),
    )
    monkeypatch.setattr(
        reproduce_all,
        "run_inference",
        lambda ci_mode=False: (_ for _ in ()).throw(
            AssertionError("inference must not run without digitized data")
        ),
    )

    assert reproduce_all.main([]) == 2


def test_missing_manifest_is_an_error(tmp_path):
    import reproduce_all

    assert reproduce_all.verify_results(tmp_path / "run", tmp_path / "receipt") is False


def test_manifest_verification_failure_is_an_error(tmp_path, monkeypatch):
    import reproduce_all

    run_dir = tmp_path / "run"
    receipt_dir = tmp_path / "receipt"
    run_dir.mkdir()
    receipt_dir.mkdir()
    (receipt_dir / "manifest.json").write_text("{}")
    monkeypatch.setattr(reproduce_all, "run_command", lambda command, cwd: False)

    assert reproduce_all.verify_results(run_dir, receipt_dir) is False


def test_inference_command_failure_is_not_downgraded(monkeypatch, tmp_path):
    import reproduce_all

    monkeypatch.setattr(reproduce_all, "run_command", lambda command, cwd: False)
    assert reproduce_all.run_inference(run_dir=tmp_path / "run") is False
