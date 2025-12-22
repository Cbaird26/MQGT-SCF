    #!/usr/bin/env python3
    """MQGT-SCF QRNG Experiment Harness (v7)

    Goals:
    - Run QRNG test (or simulate) under preregistered settings
    - Freeze analysis code hash
    - Ingest counts (N1, N0) or raw bitstream
    - Compute frequentist test + Bayesian posterior bound on eta
    - Output reproducible bundle (report, plots, JSON, code hash)

    Usage:
      python mqgt_qrng_harness.py simulate --N 10000000 --eta 1e-6 --seed 7 --out results/
      python mqgt_qrng_harness.py analyze --N1 5000123 --N0 4999877 --E1 1 --E0 0 --out results/
      python mqgt_qrng_harness.py analyze --bits bits.csv --col bit --E1 1 --E0 0 --out results/

    Notes:
    - This harness assumes Canon-A: P(1)/P(0) = exp(eta*(E1-E0)) when base log-odds is 0.
      If you need a nonzero base log-odds, pass --base_logodds.
    """

    import argparse, json, math, hashlib, os
    from pathlib import Path
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.stats import norm

    HBARC_EVM = 1.973269804e-7  # (not used here; kept for consistency across project)

    def sha256_of_file(path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1<<20), b""):
                h.update(chunk)
        return h.hexdigest()

    def sigmoid(x: float) -> float:
        return 1.0/(1.0+math.exp(-x))

    def simulate_counts(N: int, eta: float, E0: float, E1: float, base_logodds: float, seed: int):
        rng = np.random.default_rng(seed)
        logit = base_logodds + eta*(E1-E0)
        p1 = 1/(1+np.exp(-logit))
        N1 = int(rng.binomial(N, p1))
        N0 = int(N - N1)
        return N1, N0, float(p1)

    def ingest_bits(bits_path: Path, col: str):
        df = pd.read_csv(bits_path)
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in {bits_path}")
        bits = df[col].astype(int).values
        N1 = int(np.sum(bits==1))
        N0 = int(np.sum(bits==0))
        return N1, N0, int(len(bits))

    def posterior_grid(N1, N0, E0, E1, base_logodds, prior_mu, prior_sigma, eta_min, eta_max, n_grid):
        dE = (E1-E0)
        etas = np.linspace(eta_min, eta_max, n_grid)
        logits = base_logodds + etas*dE
        p1 = 1/(1+np.exp(-logits))
        loglik = N1*np.log(p1+1e-300) + N0*np.log(1-p1+1e-300)
        logprior = -0.5*((etas-prior_mu)/prior_sigma)**2 - math.log(prior_sigma*math.sqrt(2*math.pi))
        logpost = loglik + logprior
        logpost -= np.max(logpost)
        post = np.exp(logpost)
        # normalize
        post /= np.trapz(post, etas)
        # CDF
        cdf = np.concatenate([[0.0], np.cumsum((post[:-1]+post[1:])*(etas[1:]-etas[:-1])/2)])
        mean = float(np.trapz(etas*post, etas))
        var = float(np.trapz((etas-mean)**2*post, etas))
        median = float(np.interp(0.5, cdf, etas))
        lo = float(np.interp(0.025, cdf, etas))
        hi = float(np.interp(0.975, cdf, etas))
        map_eta = float(etas[np.argmax(post)])
        return {
            "etas": etas, "post": post, "cdf": cdf,
            "mean": mean, "sd": math.sqrt(var),
            "median": median, "ci95": [lo, hi], "map": map_eta
        }

    def frequentist_test(N1, N0, E0, E1, alpha=0.05):
        # Statistic T = log(N1/N0). Approx var(T) ≈ 1/N1 + 1/N0
        # Under H0: mean 0.
        T = math.log((N1+1e-12)/(N0+1e-12))
        se = math.sqrt(1.0/max(N1,1) + 1.0/max(N0,1))
        z = T/se if se>0 else 0.0
        p = 2*(1-norm.cdf(abs(z)))
        zcrit = norm.ppf(1-alpha/2)
        reject = abs(z) > zcrit
        return {"T": T, "se": se, "z": z, "p_value": p, "alpha": alpha, "reject_H0": reject}

    def write_bundle(outdir: Path, meta: dict, posterior: dict, freq: dict, code_hash: str):
        outdir.mkdir(parents=True, exist_ok=True)
        # Save arrays
        np.savetxt(outdir/"eta_grid.csv", np.c_[posterior["etas"], posterior["post"]], delimiter=",",
                   header="eta,posterior_density", comments="")
        # Plot posterior
        plt.figure()
        plt.plot(posterior["etas"], posterior["post"])
        plt.xlabel("eta")
        plt.ylabel("posterior density")
        plt.title("Posterior for eta (grid)")
        plt.savefig(outdir/"eta_posterior.png", dpi=200, bbox_inches="tight")
        plt.close()
        # Report
        report = {
            "meta": meta,
            "code_sha256": code_hash,
            "frequentist": freq,
            "posterior_summary": {k: posterior[k] for k in ["mean","sd","median","map","ci95"]},
        }
        (outdir/"report.json").write_text(json.dumps(report, indent=2))
        # Friendly markdown
        md = f"""# MQGT-SCF QRNG Report (v7)

**Code hash (sha256):** `{code_hash}`

## Data
- N1 = {meta['N1']:,}
- N0 = {meta['N0']:,}
- N  = {meta['N']:,}
- Labels: E1={meta['E1']}, E0={meta['E0']}
- base_logodds = {meta['base_logodds']}

## Frequentist test (two-sided)
- T = log(N1/N0) = {freq['T']:.6e}
- z = {freq['z']:.3f}
- p = {freq['p_value']:.3e}
- Reject H0 at alpha={freq['alpha']}? **{freq['reject_H0']}**

## Bayesian posterior for eta
- MAP: {posterior['map']:.3e}
- Median: {posterior['median']:.3e}
- Mean ± SD: {posterior['mean']:.3e} ± {posterior['sd']:.3e}
- 95% CrI: [{posterior['ci95'][0]:.3e}, {posterior['ci95'][1]:.3e}]

"""
        (outdir/"REPORT.md").write_text(md)

    def main():
        ap = argparse.ArgumentParser()
        sub = ap.add_subparsers(dest="cmd", required=True)

        ap_sim = sub.add_parser("simulate")
        ap_sim.add_argument("--N", type=int, required=True)
        ap_sim.add_argument("--eta", type=float, required=True)
        ap_sim.add_argument("--E1", type=float, default=1.0)
        ap_sim.add_argument("--E0", type=float, default=0.0)
        ap_sim.add_argument("--base_logodds", type=float, default=0.0)
        ap_sim.add_argument("--seed", type=int, default=7)
        ap_sim.add_argument("--out", type=str, required=True)

        ap_an = sub.add_parser("analyze")
        ap_an.add_argument("--N1", type=int, default=None)
        ap_an.add_argument("--N0", type=int, default=None)
        ap_an.add_argument("--bits", type=str, default=None)
        ap_an.add_argument("--col", type=str, default="bit")
        ap_an.add_argument("--E1", type=float, default=1.0)
        ap_an.add_argument("--E0", type=float, default=0.0)
        ap_an.add_argument("--base_logodds", type=float, default=0.0)
        ap_an.add_argument("--prior_mu", type=float, default=0.0)
        ap_an.add_argument("--prior_sigma", type=float, default=1e-5)
        ap_an.add_argument("--eta_min", type=float, default=-2e-5)
        ap_an.add_argument("--eta_max", type=float, default=2e-5)
        ap_an.add_argument("--n_grid", type=int, default=20001)
        ap_an.add_argument("--alpha", type=float, default=0.05)
        ap_an.add_argument("--out", type=str, required=True)

        args = ap.parse_args()
        outdir = Path(args.out)

        code_hash = sha256_of_file(Path(__file__))

        if args.cmd == "simulate":
            N1, N0, p1 = simulate_counts(args.N, args.eta, args.E0, args.E1, args.base_logodds, args.seed)
            meta = {
                "mode": "simulate",
                "N": args.N, "N1": N1, "N0": N0,
                "eta_true": args.eta, "p1": p1,
                "E1": args.E1, "E0": args.E0,
                "base_logodds": args.base_logodds,
                "seed": args.seed
            }
            # Analyze simulated counts
            freq = frequentist_test(N1, N0, args.E0, args.E1)
            post = posterior_grid(N1, N0, args.E0, args.E1, args.base_logodds,
                                  prior_mu=0.0, prior_sigma=1e-5,
                                  eta_min=-2e-5, eta_max=2e-5, n_grid=20001)
            write_bundle(outdir, meta, post, freq, code_hash)
            print(f"Wrote bundle to {outdir}")

        if args.cmd == "analyze":
            if args.bits:
                N1, N0, N = ingest_bits(Path(args.bits), args.col)
            else:
                if args.N1 is None or args.N0 is None:
                    raise SystemExit("Provide --N1 and --N0 or provide --bits")
                N1, N0 = int(args.N1), int(args.N0)
                N = N1 + N0
            meta = {
                "mode": "analyze",
                "N": int(N), "N1": int(N1), "N0": int(N0),
                "E1": float(args.E1), "E0": float(args.E0),
                "base_logodds": float(args.base_logodds),
                "prior_mu": float(args.prior_mu),
                "prior_sigma": float(args.prior_sigma),
                "eta_grid": [float(args.eta_min), float(args.eta_max), int(args.n_grid)]
            }
            freq = frequentist_test(N1, N0, args.E0, args.E1, alpha=args.alpha)
            post = posterior_grid(N1, N0, args.E0, args.E1, args.base_logodds,
                                  prior_mu=args.prior_mu, prior_sigma=args.prior_sigma,
                                  eta_min=args.eta_min, eta_max=args.eta_max, n_grid=args.n_grid)
            write_bundle(outdir, meta, post, freq, code_hash)
            print(f"Wrote bundle to {outdir}")

    if __name__ == "__main__":
        main()
