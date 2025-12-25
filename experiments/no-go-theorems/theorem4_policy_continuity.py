import csv
import numpy as np
from configs import CFG_INTUITIVE, CFG_NORMALIZED, SimConfig

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))

def survival_prob(G: float, cfg: SimConfig) -> float:
    if cfg.use_T_scaling:
        return float(np.exp(-G / (cfg.C * cfg.T)))
    return float(np.exp(-G / cfg.C))

def run_agent(seed: int, mode: str, cfg: SimConfig):
    rng = np.random.default_rng(seed)
    theta = float(rng.normal(0, 0.1))
    theta0 = float(theta)

    rows = []

    for k in range(cfg.epochs):
        debt_for_a0 = cfg.debt_misaligned
        debt_for_a1 = cfg.debt_aligned
        if mode == "shuffled":
            if rng.random() < 0.5:
                debt_for_a0, debt_for_a1 = debt_for_a1, debt_for_a0

        G = 0.0
        work_extracted = 0.0
        temptation_payoff = 0.0

        for _ in range(cfg.T):
            p1 = sigmoid(theta)
            a = 1 if rng.random() < p1 else 0

            g = debt_for_a1 if a == 1 else debt_for_a0
            G += g

            if a == 0:
                temptation_payoff += cfg.temptation_bonus

            predicted = 1 if p1 >= 0.5 else 0
            if predicted == a:
                work_extracted += cfg.work_gain
            else:
                work_extracted -= cfg.work_loss

            if mode == "aligned":
                grad = (1 - p1) if a == 1 else (-p1)
                theta += cfg.lr * grad
            elif mode == "misaligned":
                grad = (-p1) if a == 0 else (-(1 - p1))
                theta += cfg.lr * grad
            elif mode in ("neutral", "shuffled"):
                pass
            else:
                raise ValueError("mode must be aligned/misaligned/neutral/shuffled")

        P_survive = survival_prob(G, cfg)
        survive = (rng.random() < P_survive)
        if not survive:
            theta += float(rng.normal(0.0, cfg.sigma_fracture))

        drift = abs(theta - theta0)
        pci = float(np.exp(-drift))

        gross_advantage = float(work_extracted + temptation_payoff)
        net_work = float(gross_advantage - cfg.debt_cost_lambda * G)

        rows.append({
            "epoch": k,
            "mode": mode,
            "seed": seed,
            "theta": theta,
            "theta0": theta0,
            "drift": drift,
            "PCI": pci,
            "G_debt": G,
            "P_survive": P_survive,
            "survive": int(survive),
            "temptation_payoff": temptation_payoff,
            "work_extracted": work_extracted,
            "gross_advantage": gross_advantage,
            "net_work": net_work,
        })

    return rows

def run_experiment(cfg: SimConfig, out_csv: str):
    mode_offset = {"aligned": 100000, "misaligned": 200000, "neutral": 300000, "shuffled": 400000}
    modes = ["aligned", "misaligned", "neutral", "shuffled"]

    all_rows = []
    for mode in modes:
        for s in range(cfg.seeds):
            seed = s + mode_offset[mode]
            all_rows.extend(run_agent(seed=seed, mode=mode, cfg=cfg))

    fieldnames = list(all_rows[0].keys())
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Wrote {out_csv}")

if __name__ == "__main__":
    run_experiment(CFG_INTUITIVE, "results_intuitive.csv")
    run_experiment(CFG_NORMALIZED, "results_normalized.csv")
