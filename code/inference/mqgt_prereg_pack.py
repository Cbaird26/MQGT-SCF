#!/usr/bin/env python3
"""Generate a preregistration bundle with code hashes and locked parameters."""
import argparse, hashlib, json
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--N", type=int, default=10_000_000)
    ap.add_argument("--E1", type=float, default=1.0)
    ap.add_argument("--E0", type=float, default=0.0)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--prior_sigma", type=float, default=1e-5)
    ap.add_argument("--eta_min", type=float, default=-2e-5)
    ap.add_argument("--eta_max", type=float, default=2e-5)
    ap.add_argument("--analysis_script", type=str, default="mqgt_qrng_harness.py")
    args=ap.parse_args()

    outdir=Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    script_path=Path(__file__).resolve().parent/args.analysis_script
    bundle={
        "title":"Testing Ethically Weighted Quantum Collapse via QRNG (MQGT-SCF)",
        "fixed_parameters":{
            "N": args.N,
            "E1": args.E1,
            "E0": args.E0,
            "alpha": args.alpha,
            "prior_sigma": args.prior_sigma,
            "eta_grid":[args.eta_min, args.eta_max, 20001],
        },
        "analysis_code":{
            "script": str(script_path.name),
            "sha256": sha256(script_path)
        },
        "stopping_rule":"Fixed N; no optional stopping; no midstream changes.",
        "blinding":"Condition labels hidden until analysis code hash recorded."
    }
    (outdir/"prereg_bundle.json").write_text(json.dumps(bundle, indent=2))
    md=f"""# Prereg Bundle (MQGT-SCF QRNG)

**Analysis script:** `{script_path.name}`  
**sha256:** `{bundle['analysis_code']['sha256']}`

## Fixed parameters
- N = {args.N:,}
- Labels: E1={args.E1}, E0={args.E0}
- alpha = {args.alpha}
- prior_sigma = {args.prior_sigma}
- eta grid = [{args.eta_min}, {args.eta_max}] (20001 points)

## Stopping rule
{bundle['stopping_rule']}

## Blinding
{bundle['blinding']}
"""
    (outdir/"PREREG.md").write_text(md)

if __name__=="__main__":
    main()
