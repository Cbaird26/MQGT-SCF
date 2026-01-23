#!/usr/bin/env python3
"""Generate SN1987A constraint bounds."""
import sys
import csv
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from code.inference.astrophysics.sn1987a_constraints import inverse_mapping

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration-limit', type=float, default=9.0)
    parser.add_argument('--m-c-min', type=float, default=1e-6)
    parser.add_argument('--m-c-max', type=float, default=0.1)
    parser.add_argument('--n-points', type=int, default=100)
    parser.add_argument('--output', default='results/astrophysics/sn1987a_bounds.csv')
    args = parser.parse_args()
    
    m_c_values = [10**(math.log10(args.m_c_min) + (math.log10(args.m_c_max) - math.log10(args.m_c_min)) * i / (args.n_points - 1)) for i in range(args.n_points)]
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['m_c_GeV', 'theta_max', 'kappa_vc_max_GeV', 'duration_limit_s'])
        for m_c in m_c_values:
            theta_max, kappa_vc_max = inverse_mapping(args.duration_limit, m_c)
            writer.writerow([f"{m_c:.12e}", f"{theta_max:.12e}", f"{kappa_vc_max:.12e}", f"{args.duration_limit:.6f}"])
    
    print(f"Generated SN1987A bounds: {output_path}")

if __name__ == "__main__":
    main()
