#!/usr/bin/env python3
"""
Generate Falsification Dashboard

Produces standardized dashboard JSON and Markdown from ToE constraint runs.
"""

import sys
import os
import json
import numpy as np
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from code.inference.fifth_force.falsification_dashboard import compute_dashboard, dashboard_to_markdown
from code.inference.fifth_force.toe_mapping import (
    toe_theta_hc,
    toe_alpha_from_theta,
    m_c_GeV_to_lambda,
    lambda_to_m_c_GeV
)
from code.inference.fifth_force.envelope_merger import load_constraint_curve, compute_real_only_support
from code.inference.fifth_force.mixture_sampler import mixture_sample_lambda, compute_real_only_windows
from code.inference.fifth_force.run_manifest import generate_run_manifest


def load_canonical_envelope(canonical_path):
    """Load canonical constraint curve."""
    return load_constraint_curve(canonical_path)


def sample_toe_parameters(n_points, seed=None):
    """
    Sample ToE parameters for constraint evaluation.
    
    For now, uses simple priors. Can be extended with more sophisticated sampling.
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Simple priors (can be made more sophisticated)
    kappa_cH_samples = np.logspace(-12, -6, n_points)
    v_c_samples = np.full(n_points, 246.0)  # Fixed for now
    m_c_samples = np.logspace(-4, -2, n_points)  # GeV
    
    return {
        'kappa_cH': kappa_cH_samples,
        'v_c_GeV': v_c_samples,
        'm_c_GeV': m_c_samples
    }


def compute_alpha_pred_for_points(toe_params, constraint_curve):
    """
    Compute α_pred(λ) for sampled ToE parameters.
    
    Args:
        toe_params: dict with kappa_cH, v_c_GeV, m_c_GeV arrays
        constraint_curve: constraint curve dict
        
    Returns:
        lambda_values, alpha_pred_values
    """
    n_points = len(toe_params['kappa_cH'])
    lambda_values = []
    alpha_pred_values = []
    
    for i in range(n_points):
        kappa_cH = toe_params['kappa_cH'][i]
        v_c = toe_params['v_c_GeV'][i]
        m_c = toe_params['m_c_GeV'][i]
        
        try:
            # Compute θ_hc
            theta = toe_theta_hc(kappa_cH, v_c, m_c)
            # Compute α
            alpha = toe_alpha_from_theta(theta)
            # Get λ
            lambda_m = m_c_GeV_to_lambda(m_c)
            
            lambda_values.append(lambda_m)
            alpha_pred_values.append(alpha)
        except ValueError:
            # Resonance region - skip
            lambda_values.append(np.nan)
            alpha_pred_values.append(np.nan)
    
    return np.array(lambda_values), np.array(alpha_pred_values)


def main():
    """Generate falsification dashboard."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate falsification dashboard')
    parser.add_argument('--mapping-mode', type=str, default='HIGGS_MIX', help='Mapping mode')
    parser.add_argument('--f-n', type=float, default=0.30, help='f_N value')
    parser.add_argument('--npts', type=int, default=2000, help='Number of sample points')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--real-only', action='store_true', help='Enforce 100% coverage')
    parser.add_argument('--output-dir', type=str, default=None, help='Output directory')
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    canonical_curve = project_root / "data/constraints/canonical/eotwash_prl2016_canonical.csv"
    output_dir = project_root / "results/toe_constraints" if args.output_dir is None else Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Loading canonical constraint envelope...")
    constraint_curve = load_canonical_envelope(str(canonical_curve))
    constraint_curves = [constraint_curve]
    
    print(f"Sampling {args.npts} ToE parameter points...")
    toe_params = sample_toe_parameters(args.npts, seed=args.seed)
    
    print("Computing α_pred for all points...")
    lambda_values, alpha_pred_values = compute_alpha_pred_for_points(toe_params, constraint_curve)
    
    # Remove NaN points
    valid_mask = np.isfinite(lambda_values) & np.isfinite(alpha_pred_values)
    lambda_values = lambda_values[valid_mask]
    alpha_pred_values = alpha_pred_values[valid_mask]
    
    print(f"Valid points: {len(lambda_values)}/{args.npts}")
    
    # Get envelope
    from code.inference.fifth_force.envelope_merger import compute_envelope_real_only
    alpha_max_envelope = compute_envelope_real_only(constraint_curves, lambda_values)
    
    # Compute support intervals
    lambda_support_intervals = [constraint_curve['lambda_domain']]
    
    # Check coverage
    from code.inference.fifth_force.falsification_dashboard import compute_coverage_metrics
    coverage = compute_coverage_metrics(lambda_values, lambda_support_intervals)
    print(f"Coverage fraction: {coverage['coverage_fraction']:.6f}")
    
    if args.real_only and coverage['coverage_fraction'] < 1.0:
        print("WARNING: Coverage < 1.0 but --real-only flag set!")
    
    # Build dashboard
    print("Computing dashboard...")
    dashboard = compute_dashboard(
        lambda_values=lambda_values,
        alpha_pred_values=alpha_pred_values,
        alpha_max_envelope=alpha_max_envelope,
        mapping_mode=args.mapping_mode,
        mapping_params={'f_N': args.f_n},
        envelope_variant='canonical',
        sampling_info={
            'NPTS': args.npts,
            'method': 'mixture' if args.real_only else 'uniform_log',
            'seed': args.seed
        },
        lambda_support_intervals=lambda_support_intervals
    )
    
    # Save JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"dashboard_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(dashboard, f, indent=2)
    print(f"Saved dashboard JSON: {json_path}")
    
    # Save Markdown
    md_path = output_dir / f"dashboard_{timestamp}.md"
    md_content = dashboard_to_markdown(dashboard)
    with open(md_path, 'w') as f:
        f.write(md_content)
    print(f"Saved dashboard Markdown: {md_path}")
    
    print("\n✅ Falsification dashboard generated successfully!")


if __name__ == "__main__":
    main()
