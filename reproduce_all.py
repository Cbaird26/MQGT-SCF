#!/usr/bin/env python3
"""Fail-closed one-command reproduction for the historical analysis bundle.

Usage:
    python reproduce_all.py
    python reproduce_all.py --ci

The CI mode uses a smaller deterministic MCMC configuration, but it executes
the same digitized-input, inference, manifest-generation, and verification
stages as a full run.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parent
CODE_DIR = REPO_ROOT / "code" / "inference"
DATA_DIR = REPO_ROOT / "data" / "processed"
RUN_DIR = DATA_DIR / "runs" / "reproduced"
RECEIPT_DIR = DATA_DIR / "runs" / "reproduced_receipt"


def check_dependencies() -> bool:
    """Return false when any runtime dependency is unavailable."""
    required = ["numpy", "scipy", "matplotlib", "pandas"]
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print(f"Install with: {sys.executable} -m pip install {' '.join(missing)}")
        return False

    print("✅ All dependencies installed")
    return True


def check_digitized_data(data_dir: Path = DATA_DIR) -> tuple[bool, str | None]:
    """Require every digitized input consumed by the joint harness."""
    required = (
        "constraints.py",
        "fifth_force_alpha_lambda_envelope.csv",
        "cms_hinv_profilelik_digitized_unique.csv",
        "cosmo_cov_w0_wa.json",
    )
    missing = [name for name in required if not (data_dir / name).is_file()]
    if missing:
        return False, f"missing digitized inputs: {', '.join(missing)}"
    return True, None


def run_command(command: Sequence[str], cwd: Path) -> bool:
    """Run a pipeline command and preserve diagnostic output on failure."""
    try:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"❌ Command failed: {' '.join(command)}")
        if isinstance(error, subprocess.CalledProcessError):
            if error.stdout:
                print(error.stdout.rstrip())
            if error.stderr:
                print(error.stderr.rstrip(), file=sys.stderr)
        else:
            print(str(error), file=sys.stderr)
        return False

    if completed.stdout:
        print(completed.stdout.rstrip())
    return True


def run_inference(ci_mode: bool = False, run_dir: Path = RUN_DIR) -> bool:
    """Run the joint inference harness; never downgrade a failure to success."""
    print("\n📊 Running joint inference...")
    command = [
        sys.executable,
        str(CODE_DIR / "mqgt_joint_harness.py"),
        "run",
        "--qrng_N1",
        "5000123",
        "--qrng_N0",
        "4999877",
        "--out",
        str(run_dir),
    ]
    if ci_mode:
        command.extend(["--config", str(CODE_DIR / "joint_config_ci.json")])

    if not run_command(command, CODE_DIR):
        return False

    required_outputs = ("used_config.json", "joint_summary.json", "joint_samples.csv")
    missing = [name for name in required_outputs if not (run_dir / name).is_file()]
    if missing:
        print(f"❌ Inference returned without required outputs: {', '.join(missing)}")
        return False

    print(f"✅ Inference completed; results saved to {run_dir}")
    return True


def create_manifest(
    run_dir: Path = RUN_DIR, receipt_dir: Path = RECEIPT_DIR
) -> bool:
    """Create a manifest in a directory separate from the hashed run."""
    print("\n🧾 Creating reproduction manifest...")
    command = [
        sys.executable,
        str(CODE_DIR / "mqgt_manifest_sign.py"),
        "make",
        "--run_dir",
        str(run_dir),
        "--out",
        str(receipt_dir),
    ]
    if not run_command(command, CODE_DIR):
        return False

    manifest = receipt_dir / "manifest.json"
    if not manifest.is_file():
        print(f"❌ Manifest generation returned without {manifest}")
        return False
    return True


def verify_results(
    run_dir: Path = RUN_DIR, receipt_dir: Path = RECEIPT_DIR
) -> bool:
    """Fail when the manifest is absent or any manifest verification fails."""
    print("\n🔍 Verifying results...")
    manifest = receipt_dir / "manifest.json"
    if not manifest.is_file():
        print(f"❌ Required manifest is missing: {manifest}")
        return False

    command = [
        sys.executable,
        str(CODE_DIR / "mqgt_manifest_sign.py"),
        "verify",
        "--run_dir",
        str(run_dir),
        "--manifest",
        str(manifest),
    ]
    if not run_command(command, CODE_DIR):
        return False

    print("✅ Manifest verification passed")
    return True


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ci",
        action="store_true",
        help="use a smaller deterministic MCMC run while exercising every stage",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    print("=" * 60)
    print("MQGT-SCF Reproduction Pipeline (historical analysis)")
    print("=" * 60)

    if not check_dependencies():
        return 1

    has_data, data_error = check_digitized_data()
    if not has_data:
        print(f"❌ {data_error}")
        return 2
    print("✅ Required digitized inputs are present")

    if not run_inference(ci_mode=args.ci):
        return 3
    if not create_manifest():
        return 4
    if not verify_results():
        return 5

    print("\n" + "=" * 60)
    print("✅ Reproduction and verification complete")
    print("=" * 60)
    print(f"Results: {RUN_DIR}")
    print(f"Manifest: {RECEIPT_DIR / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
