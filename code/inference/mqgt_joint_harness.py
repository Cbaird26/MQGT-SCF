#!/usr/bin/env python3
"""MQGT-SCF Joint Constraint Harness (v8)

One command to produce:
- QRNG η bound (from counts or bitstream)
- Higgs invisible likelihood via digitized CMS q(B) curve
- Fifth-force likelihood via digitized alpha_max(lambda) envelope
- Cosmology likelihood via correlated Gaussian (w0, wa) from digitized contour
- Joint posterior samples (simple Metropolis) + plots + summary JSON

Usage:
  python mqgt_joint_harness.py run --qrng_N1 5000123 --qrng_N0 4999877 --out results_joint/
  python mqgt_joint_harness.py run --qrng_bits bits.csv --qrng_col bit --out results_joint/
  python mqgt_joint_harness.py run --config joint_config.json --out results_joint/

Notes:
- Higgs mapping uses EFT portal-width formula (as in v5), feeding CMS q(B).
- Fifth-force uses confidence-mapped penalty above digitized envelope boundary.
"""

import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from constraints import alpha_limit  # Higgs uses analytic q(B) in v11

HBARC_EVM = 1.973269804e-7  # eV*m
MH_GEV = 125.25
V_GEV = 246.0
GAMMA_SM_GEV = 4.07e-6  # 4.07 MeV = 4.07e-3 GeV? actually 4.07 MeV = 4.07e-3 GeV; width is 4.07 MeV => 4.07e-3 GeV.
# In earlier runs we used 4.07e-6 by mistake for MeV->GeV; correct is 4.07e-3.
# We'll set correct value here:
GAMMA_SM_GEV = 4.07e-3

# ---- Higgs invisible likelihood (analytic approximation; publication-grade) ----
# CMS HIG-20-003 combined 2012-2018 reports best-fit and asymmetric uncertainties:
#   Bhat = 0.086, sigma_plus = 0.054, sigma_minus = 0.052
# We approximate q(B) = -2ΔlnL as an asymmetric Gaussian:
#   q(B)=((B-Bhat)/sigma_-)^2 for B<Bhat, else ((B-Bhat)/sigma_+)^2
B_HAT = 0.086
SIGMA_PLUS = 0.054
SIGMA_MINUS = 0.052

def q_hinv_analytic(B: float) -> float:
    if B >= B_HAT:
        return ((B - B_HAT) / SIGMA_PLUS) ** 2
    return ((B - B_HAT) / SIGMA_MINUS) ** 2

def loglik_hinv_analytic(B: float) -> float:
    return -0.5 * q_hinv_analytic(B)


def ingest_bits(bits_path: Path, col: str):
    df = pd.read_csv(bits_path)
    bits = df[col].astype(int).values
    N1 = int(np.sum(bits==1)); N0 = int(np.sum(bits==0))
    return N1, N0

def br_inv_from_portal(g_phi: float, m_c_eV: float) -> float:
    mS = m_c_eV * 1e-9  # eV -> GeV
    if mS >= MH_GEV/2:
        return 0.0
    lam = g_phi
    phase = math.sqrt(max(0.0, 1.0 - 4.0*(mS**2)/(MH_GEV**2)))
    Gamma = (lam**2 * V_GEV**2)/(8.0*math.pi*MH_GEV) * phase
    return float(Gamma/(GAMMA_SM_GEV + Gamma))

def loglik_qrng(eta: float, N1: int, N0: int, E1: float, E0: float, base_logodds: float=0.0) -> float:
    dE = (E1-E0)
    logit = base_logodds + eta*dE
    p1 = 1/(1+math.exp(-logit))
    return N1*math.log(p1+1e-300) + N0*math.log(1-p1+1e-300)

def loglik_higgs(g_phi: float, m_c: float) -> float:
        B = br_inv_from_portal(g_phi, m_c)
        B = float(np.clip(B, 0.0, 0.6))
        return float(loglik_hinv_analytic(B))

def loglik_fifth(alpha: float, m_c: float, delta95_decades: float=0.3) -> float:
    lam = float(np.clip(HBARC_EVM/max(m_c,1e-30), 2e-5, 1e-3))
    amax = float(alpha_limit(np.array([lam]))[0])
    if alpha <= amax:
        return 0.0
    q95 = 2.71  # one-sided 95% threshold
    d = (math.log10(alpha/amax))/delta95_decades
    q = q95*(d**2)
    return -0.5*q

def load_cosmo_cov(digitized_dir: Path):
    j = json.loads((digitized_dir/"cosmo_cov_w0_wa.json").read_text())
    mu = np.array([j["mu"]["w0"], j["mu"]["wa"]], dtype=float)
    Sigma = np.array(j["Sigma"], dtype=float)
    Sinv = np.linalg.inv(Sigma)
    return mu, Sigma, Sinv, j

def loglik_cosmo(w0: float, wa: float, mu: np.ndarray, Sinv: np.ndarray) -> float:
    x = np.array([w0, wa]) - mu
    q = float(x.T @ Sinv @ x)
    return -0.5*q

def log_normal(x, mu, sigma):
    return -0.5*((x-mu)/sigma)**2 - math.log(sigma*math.sqrt(2*math.pi))

def log_uniform(x, low, high):
    return 0.0 if (low <= x <= high) else -math.inf

def log_loguniform(x, low, high):
    if x<=0 or x<low or x>high:
        return -math.inf
    return -math.log(x) - math.log(math.log(high/low))

def mcmc_joint(cfg: dict, N1: int, N0: int, outdir: Path):
    rng = np.random.default_rng(cfg.get("seed", 123))
    mu_cos, Sigma, Sinv, cos_json = load_cosmo_cov(Path(cfg["digitized_dir"]))

    # Priors
    pri = cfg["priors"]
    def log_prior(th):
        lp = 0.0
        lp += log_normal(th["eta"], pri["eta"]["mu"], pri["eta"]["sigma"])
        lp += log_uniform(th["g_phi"], pri["g_phi"]["low"], pri["g_phi"]["high"])
        lp += log_loguniform(th["m_c"], pri["m_c"]["low"], pri["m_c"]["high"])
        lp += log_loguniform(th["alpha_ff"], pri["alpha_ff"]["low"], pri["alpha_ff"]["high"])
        lp += log_normal(th["w0"], pri["w0"]["mu"], pri["w0"]["sigma"])
        lp += log_normal(th["wa"], pri["wa"]["mu"], pri["wa"]["sigma"])
        return lp

    def log_post(th):
        lp = log_prior(th)
        if not np.isfinite(lp):
            return -math.inf
        ll = 0.0
        ll += loglik_qrng(th["eta"], N1, N0, cfg["qrng"]["E1"], cfg["qrng"]["E0"], cfg["qrng"].get("base_logodds",0.0))
        ll += loglik_higgs(th["g_phi"], th["m_c"])
        ll += loglik_fifth(th["alpha_ff"], th["m_c"], cfg["fifth_force"]["delta95_decades"])
        ll += loglik_cosmo(th["w0"], th["wa"], mu_cos, Sinv)
        return lp + ll

    # init
    th = {
        "eta": 0.0,
        "g_phi": 1e-3,
        "m_c": 1e-4,
        "alpha_ff": 1e-12,
        "w0": float(mu_cos[0]),
        "wa": float(mu_cos[1]),
    }
    cur = log_post(th)
    prop = cfg["proposal_scales"]

    samples=[]
    acc=0
    n_steps=cfg["mcmc"]["n_steps"]; burn=cfg["mcmc"]["burn"]; thin=cfg["mcmc"]["thin"]

    for i in range(n_steps):
        cand = dict(th)
        cand["eta"] = th["eta"] + rng.normal(0, prop["eta"])
        cand["g_phi"] = max(0.0, th["g_phi"] + rng.normal(0, prop["g_phi"]))
        cand["w0"] = th["w0"] + rng.normal(0, prop["w0"])
        cand["wa"] = th["wa"] + rng.normal(0, prop["wa"])
        cand["m_c"] = float(th["m_c"]*math.exp(rng.normal(0, prop["log_m_c"])))
        cand["alpha_ff"] = float(th["alpha_ff"]*math.exp(rng.normal(0, prop["log_alpha"])))
        new = log_post(cand)
        if math.log(rng.random()) < (new-cur):
            th, cur = cand, new
            acc += 1
        if i>=burn and ((i-burn)%thin==0):
            br = br_inv_from_portal(th["g_phi"], th["m_c"])
            samples.append({**th, "BRinv": br, "logpost": cur})

    df = pd.DataFrame(samples)
    outdir.mkdir(parents=True, exist_ok=True)
    df.to_csv(outdir/"joint_samples.csv", index=False)

    # summary
    def q(x, p): return float(np.quantile(x, p))
    summ = {}
    for c in ["eta","g_phi","m_c","alpha_ff","w0","wa","BRinv"]:
        arr=df[c].values
        summ[c]={"median": float(np.median(arr)), "ci95":[q(arr,0.025), q(arr,0.975)], "mean": float(np.mean(arr))}
    meta = {
        "accept_rate": acc/n_steps,
        "n_samples": len(df),
        "N1": N1, "N0": N0,
        "config": cfg,
        "cosmo": cos_json,
        "posterior_summary": summ
    }
    (outdir/"joint_summary.json").write_text(json.dumps(meta, indent=2))

    # plots
    for c in ["eta","g_phi","m_c","alpha_ff","w0","wa","BRinv"]:
        plt.figure()
        plt.hist(df[c].values, bins=80)
        plt.xlabel(c); plt.ylabel("count")
        plt.title(f"Joint posterior marginal: {c}")
        plt.savefig(outdir/f"posterior_{c}.png", dpi=200, bbox_inches="tight")
        plt.close()

    plt.figure()
    plt.hist2d(df["w0"], df["wa"], bins=80)
    plt.xlabel("w0"); plt.ylabel("wa")
    plt.title("Joint posterior density: (w0, wa)")
    plt.colorbar(label="count")
    plt.savefig(outdir/"posterior_w0_wa.png", dpi=200, bbox_inches="tight")
    plt.close()

    return meta

def default_config(digitized_dir: str) -> dict:
    return {
        "seed": 123,
        "digitized_dir": digitized_dir,
        "qrng": {"E1": 1.0, "E0": 0.0, "base_logodds": 0.0},
        "fifth_force": {"delta95_decades": 0.3},
        "mcmc": {"n_steps": 180000, "burn": 40000, "thin": 25},
        "proposal_scales": {"eta": 5e-7, "g_phi": 1.2e-4, "w0": 0.012, "wa": 0.03, "log_m_c": 0.12, "log_alpha": 0.35},
        "priors": {
            "eta": {"mu": 0.0, "sigma": 1e-5},
            "g_phi": {"low": 0.0, "high": 1e-2},
            "m_c": {"low": 1e-8, "high": 1e-1},
            "alpha_ff": {"low": 1e-20, "high": 1e-2},
            "w0": {"mu": -1.0, "sigma": 0.3},
            "wa": {"mu": 0.0, "sigma": 1.0},
        }
    }

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run")
    run.add_argument("--out", required=True)
    run.add_argument("--config", default=None)
    run.add_argument("--qrng_N1", type=int, default=None)
    run.add_argument("--qrng_N0", type=int, default=None)
    run.add_argument("--qrng_bits", type=str, default=None)
    run.add_argument("--qrng_col", type=str, default="bit")
    args = ap.parse_args()

    outdir = Path(args.out)
    digitized_dir = str((Path(__file__).resolve().parent/"digitized").resolve())

    cfg = default_config(digitized_dir)
    if args.config:
        cfg.update(json.loads(Path(args.config).read_text()))
        cfg["digitized_dir"] = digitized_dir

    if args.qrng_bits:
        N1, N0 = ingest_bits(Path(args.qrng_bits), args.qrng_col)
    else:
        if args.qrng_N1 is None or args.qrng_N0 is None:
            raise SystemExit("Provide --qrng_N1 and --qrng_N0 OR --qrng_bits")
        N1, N0 = args.qrng_N1, args.qrng_N0

    (outdir/"used_config.json").write_text(json.dumps(cfg, indent=2))
    meta = mcmc_joint(cfg, N1, N0, outdir)
    print("Wrote joint bundle to", outdir)
    print("Acceptance rate:", meta["accept_rate"])

if __name__=="__main__":
    main()
