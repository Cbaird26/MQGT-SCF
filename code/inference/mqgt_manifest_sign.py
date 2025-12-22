#!/usr/bin/env python3
import argparse, hashlib, json
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
            files.append({"path": rel, "sha256": sha256_file(p), "bytes": p.stat().st_size})
    return {"run_dir": str(run_dir), "created_utc": datetime.utcnow().isoformat()+"Z", "files": files}

def manifest_hash(manifest: dict) -> str:
    blob = json.dumps(manifest, sort_keys=True, separators=(",",":")).encode("utf-8")
    return sha256_bytes(blob)

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
        "signature_model": "none"
    }
    if secret:
        receipt["secret_fingerprint"] = sha256_bytes(secret.encode("utf-8"))[:16]
        receipt["signature_sha256"] = sha256_bytes(secret.encode("utf-8")+mhash.encode("utf-8"))
        receipt["signature_model"] = "sha256(secret || manifest_sha256)"
    (out/"receipt.json").write_text(json.dumps(receipt, indent=2))
    txt = [
        "MQGT Reproducibility Receipt (v9)",
        f"Created (UTC): {receipt['created_utc']}",
        f"Run directory: {receipt['run_dir']}",
        f"Files hashed:  {receipt['n_files']}",
        f"Total bytes:   {receipt['total_bytes']}",
        f"Manifest SHA256: {receipt['manifest_sha256']}",
        f"Signature model: {receipt['signature_model']}",
    ]
    if secret:
        txt += [f"Secret fingerprint: {receipt['secret_fingerprint']}",
                f"Signature SHA256:   {receipt['signature_sha256']}"]
    (out/"receipt.txt").write_text("\n".join(txt))
    return receipt

def verify(run_dir: Path, manifest_path: Path) -> int:
    manifest = json.loads(manifest_path.read_text())
    bad=[]
    for f in manifest["files"]:
        p = run_dir/Path(f["path"])
        if not p.exists():
            bad.append((f["path"], "missing")); continue
        if sha256_file(p) != f["sha256"]:
            bad.append((f["path"], "hash_mismatch"))
    if bad:
        print("FAILED")
        for path,why in bad: print("-",path,why)
        return 2
    print("OK")
    return 0

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd", required=True)
    mk=sub.add_parser("make")
    mk.add_argument("--run_dir", required=True)
    mk.add_argument("--out", required=True)
    mk.add_argument("--secret", default=None)
    vf=sub.add_parser("verify")
    vf.add_argument("--run_dir", required=True)
    vf.add_argument("--manifest", required=True)
    a=ap.parse_args()
    if a.cmd=="make":
        make_receipt(Path(a.run_dir), Path(a.out), a.secret)
        print("Wrote receipt to", a.out)
    else:
        raise SystemExit(verify(Path(a.run_dir), Path(a.manifest)))
if __name__=="__main__":
    main()
