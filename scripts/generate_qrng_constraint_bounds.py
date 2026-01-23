#!/usr/bin/env python3
"""
Generate QRNG Constraint Bounds

Converts QRNG null results into bounds on η ΔE, compatible with the constraint pipeline.
"""

import sys
import csv
import json
import math
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))


def compute_eta_bound_from_null_result(N1, N0, N, E1, E0, confidence_level=0.95):
    """
    Compute bound on η from null QRNG result.
    
    Args:
        N1: Count of outcome 1
        N0: Count of outcome 0
        N: Total count (N1 + N0)
        E1: Ethical energy for outcome 1
        E0: Ethical energy for outcome 0
        confidence_level: Confidence level for bound (default 0.95)
        
    Returns:
        dict with eta_max, epsilon_obs, statistical_info
    """
    if N == 0:
        return {
            'eta_max': float('inf'),
            'epsilon_obs': 0.0,
            'statistical_info': {'error': 'No data'}
        }
    
    # Observed bias
    epsilon_obs = (N1 - N0) / N
    
    # Statistical uncertainty (binomial)
    # For large N, standard error ≈ sqrt(p(1-p)/N) where p ≈ 0.5
    p_est = N1 / N if N > 0 else 0.5
    se_epsilon = math.sqrt(p_est * (1 - p_est) / N)
    
    # Z-score for confidence level
    z_score = 1.96 if confidence_level == 0.95 else 2.58  # 95% or 99%
    
    # Upper bound on epsilon (one-sided)
    epsilon_max = epsilon_obs + z_score * se_epsilon
    
    # Bound on η: ε ≈ (η ΔE) / 4, so η_max ≈ 4 ε_max / ΔE
    DeltaE = E1 - E0
    if abs(DeltaE) < 1e-10:
        eta_max = float('inf')
    else:
        eta_max = 4.0 * abs(epsilon_max) / abs(DeltaE)
    
    return {
        'eta_max': eta_max,
        'epsilon_obs': epsilon_obs,
        'epsilon_max': epsilon_max,
        'statistical_info': {
            'N': N,
            'N1': N1,
            'N0': N0,
            'se_epsilon': se_epsilon,
            'z_score': z_score,
            'confidence_level': confidence_level
        }
    }


def load_qrng_results(results_path):
    """
    Load QRNG results from JSON or CSV.
    
    Expected formats:
    - JSON: {"N1": int, "N0": int, "E1": float, "E0": float, ...}
    - CSV: columns N1, N0, E1, E0
    """
    results_path = Path(results_path)
    
    if results_path.suffix == '.json':
        with open(results_path, 'r') as f:
            data = json.load(f)
        return data
    elif results_path.suffix == '.csv':
        with open(results_path, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)[0]  # Assume single row for now
    else:
        raise ValueError(f"Unsupported file format: {results_path.suffix}")


def generate_qrng_bounds_csv(results_path, output_path, protocol_id="qrng_protocol_v1"):
    """
    Generate QRNG constraint bounds CSV compatible with constraint ledger.
    
    Args:
        results_path: Path to QRNG results (JSON or CSV)
        output_path: Output CSV path
        protocol_id: Protocol identifier
    """
    results = load_qrng_results(results_path)
    
    # Extract values
    N1 = int(results.get('N1', results.get('N_1', 0)))
    N0 = int(results.get('N0', results.get('N_0', 0)))
    N = N1 + N0
    E1 = float(results.get('E1', results.get('E_1', 1.0)))
    E0 = float(results.get('E0', results.get('E_0', 0.0)))
    
    # Compute bounds
    bounds_95 = compute_eta_bound_from_null_result(N1, N0, N, E1, E0, 0.95)
    bounds_99 = compute_eta_bound_from_null_result(N1, N0, N, E1, E0, 0.99)
    
    # Write CSV
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'protocol_id', 'N', 'N1', 'N0', 'E1', 'E0', 'DeltaE',
            'epsilon_obs', 'epsilon_max_95cl', 'epsilon_max_99cl',
            'eta_max_95cl', 'eta_max_99cl', 'timestamp'
        ])
        writer.writerow([
            protocol_id, N, N1, N0, E1, E0, E1 - E0,
            f"{bounds_95['epsilon_obs']:.12e}",
            f"{bounds_95['epsilon_max']:.12e}",
            f"{bounds_99['epsilon_max']:.12e}",
            f"{bounds_95['eta_max']:.12e}",
            f"{bounds_99['eta_max']:.12e}",
            datetime.utcnow().isoformat() + "Z"
        ])
    
    print(f"Generated QRNG bounds CSV: {output_path}")
    print(f"  N = {N}, ε_obs = {bounds_95['epsilon_obs']:.6e}")
    print(f"  η_max (95% CL) = {bounds_95['eta_max']:.6e}")
    
    return bounds_95


def main():
    """CLI for generating QRNG bounds."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate QRNG constraint bounds')
    parser.add_argument('--results', required=True, help='Path to QRNG results (JSON or CSV)')
    parser.add_argument('--output', required=True, help='Output CSV path')
    parser.add_argument('--protocol-id', default='qrng_protocol_v1', help='Protocol identifier')
    
    args = parser.parse_args()
    
    generate_qrng_bounds_csv(args.results, args.output, args.protocol_id)


if __name__ == "__main__":
    main()
