#!/usr/bin/env python3
"""MQGT Reproducibility Receipt: manifest + signing + public attestation + appendix bundling (v10)

Commands:
  make   : create manifest.json + receipt.json + receipt.txt for a run directory
  verify : verify run directory matches a manifest.json
  attest : print a one-line attestation string to paste into OSF/arXiv (timestamp anchor)
  bundle : create a DOI-ready appendix zip (manifest + receipt + key outputs)

Signing model (optional):
  signature = sha256( secret || manifest_sha256 )
This is tamper-evident for your archive; public verifiability comes from publishing the manifest_sha256 (or attestation line).

Examples:
  python mqgt_manifest_sign.py make   --run_dir joint_run/ --out receipt_joint/
  python mqgt_manifest_sign.py attest --run_dir joint_run/ --manifest receipt_joint/manifest.json
  python mqgt_manifest_sign.py bundle --run_dir joint_run/ --manifest receipt_joint/manifest.json --out appendix_joint.zip --include "joint_summary.json,used_config.json"

"""

import argparse, hashlib, json, os
from pathlib import Path
from datetime import datetime

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def build_manifest(run_dir: Path) -> dict:
    files=[]
    for p in sorted(run_dir.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(run_dir))
            files.append({
                "path": rel,
                "sha256": sha256_file(p),
                "bytes": p.stat().st_size
            })
    return {
        "run_dir": str(run_dir),
        "created_utc": datetime.utcnow().isoformat()+"Z",
        "files": files
    }

def manifest_hash(manifest: dict) -> str:
    blob = json.dumps(manifest, sort_keys=True, separators=(",",":")).encode("utf-8")
    return sha256_bytes(blob)

def attestation_line(manifest_sha256: str, run_dir: str) -> str:
    # Short, copy-pasteable, platform-safe single line
    return f"MQGT-SCF/UTQOL RUN ATTESTATION | manifest_sha256={manifest_sha256} | run_dir={run_dir} | utc={datetime.utcnow().isoformat()}Z"

def make_receipt(run_dir: Path, out: Path, secret: str|None):
    out.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(run_dir)
    mhash = manifest_hash(manifest)
    (out/"manifest.json").write_text(json.dumps(manifest, indent=2))

    receipt = {
        "created_utc": datetime.utcnow().isoformat()+"Z",
        "run_dir": str(run_dir),
        "manifest_sha256": mhash,
        "n_files": len(manifest["files"]),
        "total_bytes": int(sum(f["bytes"] for f in manifest["files"])),
        "signature_model": "none",
        "attestation_line": attestation_line(mhash, str(run_dir)),
    }

    if secret:
        sec_hash = sha256_bytes(secret.encode("utf-8"))
        receipt["secret_fingerprint"] = sec_hash[:16]
        receipt["signature_sha256"] = sha256_bytes(secret.encode("utf-8")+mhash.encode("utf-8"))
        receipt["signature_model"] = "sha256(secret || manifest_sha256)"

    (out/"receipt.json").write_text(json.dumps(receipt, indent=2))

    txt = []
    txt.append("MQGT Reproducibility Receipt (v10)")
    txt.append(f"Created (UTC): {receipt['created_utc']}")
    txt.append(f"Run directory: {receipt['run_dir']}")
    txt.append(f"Files hashed:  {receipt['n_files']}")
    txt.append(f"Total bytes:   {receipt['total_bytes']}")
    txt.append(f"Manifest SHA256: {receipt['manifest_sha256']}")
    txt.append(f"Signature model: {receipt['signature_model']}")
    if secret:
        txt.append(f"Secret fingerprint: {receipt['secret_fingerprint']}")
        txt.append(f"Signature SHA256:   {receipt['signature_sha256']}")
    txt.append("")
    txt.append("Public attestation line (paste into OSF/arXiv/DOI notes):")
    txt.append(receipt["attestation_line"])
    (out/"receipt.txt").write_text("\n".join(txt))

    return receipt

def verify(run_dir: Path, manifest_path: Path) -> int:
    manifest = json.loads(manifest_path.read_text())
    bad=[]
    for f in manifest["files"]:
        p = run_dir/Path(f["path"])
        if not p.exists():
            bad.append((f["path"], "missing"))
            continue
        h = sha256_file(p)
        if h != f["sha256"]:
            bad.append((f["path"], "hash_mismatch"))
    if bad:
        print("Verification FAILED. Problems:")
        for path, why in bad:
            print(" -", path, why)
        return 2
    print("Verification OK.")
    return 0

def bundle_appendix(run_dir: Path, manifest_path: Path, out_zip: Path, include: list[str]|None):
    import zipfile
    manifest = json.loads(manifest_path.read_text())
    # Always include manifest + receipt if present alongside manifest
    receipt_path = manifest_path.parent/"receipt.json"
    receipt_txt  = manifest_path.parent/"receipt.txt"

    # Compute a default include set if not supplied: pick common outputs
    default = {"REPORT.md","report.json","joint_summary.json","used_config.json","joint_samples.csv","eta_grid.csv","eta_posterior.png"}
    include_set = set(default)
    if include:
        include_set |= set([s.strip() for s in include if s.strip()])

    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(manifest_path, arcname="manifest.json")
        if receipt_path.exists():
            z.write(receipt_path, arcname="receipt.json")
        if receipt_txt.exists():
            z.write(receipt_txt, arcname="receipt.txt")

        # Add selected files from run_dir (if present)
        for rel in sorted(include_set):
            p = run_dir/rel
            if p.exists() and p.is_file():
                z.write(p, arcname=f"run_outputs/{rel}")

        # Add a compact manifest hash file for DOI notes
        mhash = manifest_hash(manifest)
        z.writestr("MANIFEST_SHA256.txt", mhash + "\n")
        z.writestr("ATTESTATION.txt", attestation_line(mhash, str(run_dir)) + "\n")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    mk = sub.add_parser("make")
    mk.add_argument("--run_dir", required=True)
    mk.add_argument("--out", required=True)
    mk.add_argument("--secret", default=None)

    vf = sub.add_parser("verify")
    vf.add_argument("--run_dir", required=True)
    vf.add_argument("--manifest", required=True)

    at = sub.add_parser("attest")
    at.add_argument("--run_dir", required=True)
    at.add_argument("--manifest", required=True)

    bd = sub.add_parser("bundle")
    bd.add_argument("--run_dir", required=True)
    bd.add_argument("--manifest", required=True)
    bd.add_argument("--out", required=True)
    bd.add_argument("--include", default=None, help="comma-separated extra files to include from run_dir")

    args = ap.parse_args()

    if args.cmd == "make":
        make_receipt(Path(args.run_dir), Path(args.out), args.secret)
        print("Wrote manifest + receipt to", args.out)
        return

    if args.cmd == "verify":
        raise SystemExit(verify(Path(args.run_dir), Path(args.manifest)))

    if args.cmd == "attest":
        manifest = json.loads(Path(args.manifest).read_text())
        mhash = manifest_hash(manifest)
        print(attestation_line(mhash, args.run_dir))
        return

    if args.cmd == "bundle":
        include = None
        if args.include:
            include = args.include.split(",")
        bundle_appendix(Path(args.run_dir), Path(args.manifest), Path(args.out), include)
        print("Wrote appendix bundle to", args.out)
        return

if __name__ == "__main__":
    main()
