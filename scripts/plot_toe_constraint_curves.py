#!/usr/bin/env python3
"""
Generate publication-ready plots of ToE constraint curves.
"""

import sys
import os
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def load_csv(filename):
    """Load CSV file and return arrays."""
    x_vals = []
    y_vals = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                x_vals.append(float(row[0]))
                y_vals.append(float(row[1]))
    return np.array(x_vals), np.array(y_vals)


def plot_theta_max_vs_lambda(csv_path, output_path):
    """Plot θ_max vs λ."""
    lambda_m, theta_max = load_csv(csv_path)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(lambda_m, theta_max, 'b-', linewidth=2, label='θ_max(λ)')
    ax.set_xlabel('λ (m)', fontsize=12)
    ax.set_ylabel('θ_max (rad)', fontsize=12)
    ax.set_title('Maximum Mixing Angle vs Yukawa Range', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_kappa_vc_max_vs_lambda(csv_path, output_path):
    """Plot |κ_cH v_c|_max vs λ."""
    lambda_m, kappa_vc_max = load_csv(csv_path)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(lambda_m, kappa_vc_max, 'r-', linewidth=2, label='|κ_cH v_c|_max(λ)')
    ax.set_xlabel('λ (m)', fontsize=12)
    ax.set_ylabel('|κ_cH v_c|_max (GeV)', fontsize=12)
    ax.set_title('Maximum |κ_cH v_c| vs Yukawa Range', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_kappa_vc_max_vs_m_c(csv_path, output_path):
    """Plot |κ_cH v_c|_max vs m_c."""
    m_c_GeV, kappa_vc_max = load_csv(csv_path)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(m_c_GeV, kappa_vc_max, 'g-', linewidth=2, label='|κ_cH v_c|_max(m_c)')
    ax.set_xlabel('m_c (GeV)', fontsize=12)
    ax.set_ylabel('|κ_cH v_c|_max (GeV)', fontsize=12)
    ax.set_title('Maximum |κ_cH v_c| vs Mediator Mass', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def main():
    """Generate all plots."""
    project_root = Path(__file__).parent.parent
    results_dir = project_root / "results/toe_constraints"
    plots_dir = results_dir
    plots_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating publication-ready plots...")
    
    # Plot theta_max vs lambda
    theta_csv = results_dir / "theta_max_vs_lambda.csv"
    if theta_csv.exists():
        plot_theta_max_vs_lambda(theta_csv, plots_dir / "theta_max_vs_lambda.png")
    
    # Plot kappa_vc_max vs lambda
    kappa_lambda_csv = results_dir / "kappa_vc_max_vs_lambda.csv"
    if kappa_lambda_csv.exists():
        plot_kappa_vc_max_vs_lambda(kappa_lambda_csv, plots_dir / "kappa_vc_max_vs_lambda.png")
    
    # Plot kappa_vc_max vs m_c
    kappa_mc_csv = results_dir / "kappa_vc_max_vs_m_c.csv"
    if kappa_mc_csv.exists():
        plot_kappa_vc_max_vs_m_c(kappa_mc_csv, plots_dir / "kappa_vc_max_vs_m_c.png")
    
    print("\n✅ All plots generated successfully!")


if __name__ == "__main__":
    main()
