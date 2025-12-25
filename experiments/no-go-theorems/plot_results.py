import csv
import matplotlib.pyplot as plt
import numpy as np

def mean(lst):
    return sum(lst) / len(lst) if lst else float("nan")

def plot(csv_file: str, prefix: str):
    modes = ["aligned", "misaligned", "neutral", "shuffled"]
    metrics = ["PCI", "gross_advantage", "net_work"]

    data = {m: {} for m in modes}

    with open(csv_file) as f:
        r = csv.DictReader(f)
        for row in r:
            m = row["mode"]
            e = int(row["epoch"])
            data[m].setdefault(e, {k: [] for k in metrics})
            for k in metrics:
                data[m][e][k].append(float(row[k]))

    for metric in metrics:
        plt.figure(figsize=(8,5))
        for m in modes:
            epochs = sorted(data[m].keys())
            ys = [mean(data[m][e][metric]) for e in epochs]
            plt.plot(epochs, ys, label=m.capitalize())
        plt.xlabel("Epoch")
        plt.ylabel(metric)
        plt.title(f"{prefix}: {metric} vs Epoch")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        out = f"{prefix}_{metric}.png"
        plt.savefig(out, dpi=180)
        plt.close()
        print("Wrote", out)

if __name__ == "__main__":
    plot("results_intuitive.csv", "Intuitive_Scaling")
    plot("results_normalized.csv", "Normalized_Scaling")
