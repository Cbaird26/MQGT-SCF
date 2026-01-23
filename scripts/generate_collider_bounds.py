#!/usr/bin/env python3
"""
Generate ToE parameter bounds from Higgs invisible decay limits.

Reads experimental BR(H → invisible) limits and generates bounds on
θ_hc and |κ_cH v_c| as functions of m_c.
"""

import sys
import csv
import math
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import directly from module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from code.inference.collider.higgs_invisible import (
    compute_theta_max_from_br_limit,
    compute_kappa_vc_max_from_br_limit
)


def generate_collider_bounds(
    br_limit: float,
    m_c_min: float = 0.001,  # GeV
    m_c_max: float = 200.0,  # GeV
    n_points: int = 1000,
    v_c: float = 246.0,
    output_path: str = "results/collider/higgs_invisible_bounds.csv"
):
    """
    Generate bounds on ToE parameters from Higgs invisible decay limit.
    
    Args:
        br_limit: Experimental upper limit on BR(H → invisible)
        m_c_min: Minimum m_c to scan (GeV)
        m_c_max: Maximum m_c to scan (GeV)
        n_points: Number of points in scan
        v_c: Scalar field VEV v_c (GeV)
        output_path: Output CSV path
    """
    # Generate m_c grid (log scale for better coverage)
    log_mc_min = math.log10(m_c_min)
    log_mc_max = math.log10(m_c_max)
    m_c_values = [10 ** (log_mc_min + (log_mc_max - log_mc_min) * i / (n_points - 1))
                  for i in range(n_points)]
    
    # Compute bounds
    theta_max_values = []
    kappa_vc_max_values = []
    
    for m_c in m_c_values:
        theta_max = compute_theta_max_from_br_limit(br_limit, m_c)
        kappa_vc_max = compute_kappa_vc_max_from_br_limit(br_limit, m_c, v_c)
        
        theta_max_values.append(theta_max)
        kappa_vc_max_values.append(kappa_vc_max)
    
    # Write CSV
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'm_c_GeV', 'theta_max', 'kappa_vc_max_GeV', 'br_limit', 'v_c_GeV'
        ])
        for m_c, theta_max, kappa_vc_max in zip(m_c_values, theta_max_values, kappa_vc_max_values):
            writer.writerow([
                f"{m_c:.12e}",
                f"{theta_max:.12e}",
                f"{kappa_vc_max:.12e}",
                f"{br_limit:.12e}",
                f"{v_c:.6f}"
            ])
    
    print(f"Generated collider bounds: {output_path}")
    print(f"  BR limit: {br_limit}")
    print(f"  m_c range: {m_c_min:.3e} - {m_c_max:.3e} GeV")
    print(f"  Points: {n_points}")
    
    return output_path


def main():
    """CLI for generating collider bounds."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate collider constraint bounds')
    parser.add_argument('--br-limit', type=float, default=0.11, 
                       help='BR(H → invisible) limit (default: 0.11 for combined)')
    parser.add_argument('--m-c-min', type=float, default=0.001, help='Minimum m_c (GeV)')
    parser.add_argument('--m-c-max', type=float, default=200.0, help='Maximum m_c (GeV)')
    parser.add_argument('--n-points', type=int, default=1000, help='Number of points')
    parser.add_argument('--v-c', type=float, default=246.0, help='Scalar VEV v_c (GeV)')
    parser.add_argument('--output', type=str, 
                       default='results/collider/higgs_invisible_bounds.csv',
                       help='Output CSV path')
    
    args = parser.parse_args()
    
    generate_collider_bounds(
        args.br_limit,
        args.m_c_min,
        args.m_c_max,
        args.n_points,
        args.v_c,
        args.output
    )


if __name__ == "__main__":
    main()
