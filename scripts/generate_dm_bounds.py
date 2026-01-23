#!/usr/bin/env python3
"""Generate dark matter direct detection constraint bounds."""
import sys
import csv
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from code.inference.dark_matter.direct_detection import inverse_mapping

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--rate-limit', type=float, default=1.0)
    parser.add_argument('--m-c-min', type=float, default=1.0)
    parser.add_argument('--m-c-max', type=float, default=1000.0)
    parser.add_argument('--n-points', type=int, default=100)
    parser.add_argument('--output', default='results/dark_matter/dm_bounds.csv')
    args = parser.parse_args()
    
    m_c_values = [10**(math.log10(args.m_c_min) + (math.log10(args.m_c_max) - math.log10(args.m_c_min)) * i / (args.n_points - 1)) for i in range(args.n_points)]
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['m_c_GeV', 'theta_max', 'kappa_vc_max_GeV', 'rate_limit'])
        for m_c in m_c_values:
            theta_max, kappa_vc_max = inverse_mapping(args.rate_limit, m_c)
            writer.writerow([f"{m_c:.12e}", f"{theta_max:.12e}", f"{kappa_vc_max:.12e}", f"{args.rate_limit:.6f}"])
    
    print(f"Generated DM bounds: {output_path}")

if __name__ == "__main__":
    main()
