"""
Falsification Dashboard Module

Standardized output format for ToE constraint analysis with coverage metrics,
mapping provenance, exclusion/detectability metrics, and robustness tracking.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime


def compute_coverage_metrics(
    lambda_sampled: np.ndarray,
    lambda_support_intervals: List[Tuple[float, float]]
) -> Dict:
    """
    Compute coverage fraction and support union.
    
    Args:
        lambda_sampled: Array of sampled λ values
        lambda_support_intervals: List of (λ_min, λ_max) tuples for each constraint source
        
    Returns:
        dict with coverage_fraction, lambda_support, lambda_support_union
    """
    if len(lambda_support_intervals) == 0:
        return {
            'coverage_fraction': 0.0,
            'lambda_support': [],
            'lambda_support_union': []
        }
    
    # Compute union of all support intervals
    sorted_intervals = sorted(lambda_support_intervals, key=lambda x: x[0])
    union_intervals = []
    current_start, current_end = sorted_intervals[0]
    
    for start, end in sorted_intervals[1:]:
        if start <= current_end:
            # Overlapping or adjacent: merge
            current_end = max(current_end, end)
        else:
            # Gap: save current, start new
            union_intervals.append((current_start, current_end))
            current_start, current_end = start, end
    union_intervals.append((current_start, current_end))
    
    # Count sampled points within union
    in_support = np.zeros(len(lambda_sampled), dtype=bool)
    for start, end in union_intervals:
        in_support |= (lambda_sampled >= start) & (lambda_sampled <= end)
    
    coverage_fraction = np.sum(in_support) / len(lambda_sampled) if len(lambda_sampled) > 0 else 0.0
    
    return {
        'coverage_fraction': float(coverage_fraction),
        'lambda_support': lambda_support_intervals,
        'lambda_support_union': union_intervals,
        'note': 'no extrapolation outside support; undefined r elsewhere'
    }


def compute_detectability_metrics(
    alpha_pred: np.ndarray,
    alpha_max: np.ndarray,
    lambda_values: np.ndarray
) -> Dict:
    """
    Compute r_max, quantiles, scale factors from α_pred and α_max.
    
    Args:
        alpha_pred: Predicted α values
        alpha_max: Experimental upper limits
        lambda_values: Corresponding λ values
        
    Returns:
        dict with r_max, r_quantiles, scale factors, etc.
    """
    # Compute ratio r(λ) = α_pred / α_max
    # Handle division by zero and NaN
    valid_mask = (alpha_max > 0) & np.isfinite(alpha_pred) & np.isfinite(alpha_max)
    r_values = np.full_like(alpha_pred, np.nan)
    r_values[valid_mask] = alpha_pred[valid_mask] / alpha_max[valid_mask]
    
    # Remove NaN for quantile computation
    r_valid = r_values[valid_mask]
    
    if len(r_valid) == 0:
        return {
            'r_max': np.nan,
            'lambda_at_r_max': np.nan,
            'r_quantiles': {'r_50': np.nan, 'r_90': np.nan, 'r_95': np.nan, 'r_99': np.nan},
            'fraction_r_gt_0_1': 0.0,
            'fraction_r_gt_1': 0.0,
            'scale_to_detectable': np.nan,
            'scale_to_exclude': np.nan,
            'closest_approach_sentence': 'No valid data points'
        }
    
    r_max = np.nanmax(r_values)
    lambda_at_r_max = lambda_values[valid_mask][np.nanargmax(r_values[valid_mask])]
    
    # Quantiles
    r_quantiles = {
        'r_50': float(np.nanpercentile(r_valid, 50)),
        'r_90': float(np.nanpercentile(r_valid, 90)),
        'r_95': float(np.nanpercentile(r_valid, 95)),
        'r_99': float(np.nanpercentile(r_valid, 99))
    }
    
    # Fractions above thresholds
    fraction_r_gt_0_1 = np.sum(r_valid > 0.1) / len(r_valid)
    fraction_r_gt_1 = np.sum(r_valid > 1.0) / len(r_valid)
    
    # Scale factors
    if r_max > 0:
        scale_to_detectable = 0.1 / r_max
        scale_to_exclude = 1.0 / r_max
        closest_approach_sentence = (
            f"Needs ×{scale_to_exclude:.2e} uplift to reach exclusion (r=1), "
            f"or ×{scale_to_detectable:.2e} to reach r=0.1."
        )
    else:
        scale_to_detectable = np.inf
        scale_to_exclude = np.inf
        closest_approach_sentence = "r_max is zero or negative"
    
    return {
        'r_max': float(r_max),
        'lambda_at_r_max': float(lambda_at_r_max),
        'r_quantiles': r_quantiles,
        'fraction_r_gt_0_1': float(fraction_r_gt_0_1),
        'fraction_r_gt_1': float(fraction_r_gt_1),
        'scale_to_detectable': float(scale_to_detectable),
        'scale_to_exclude': float(scale_to_exclude),
        'closest_approach_sentence': closest_approach_sentence
    }


def compute_dashboard(
    lambda_values: np.ndarray,
    alpha_pred_values: np.ndarray,
    alpha_max_envelope: np.ndarray,
    mapping_mode: str,
    mapping_params: Dict,
    envelope_variant: str,
    sampling_info: Dict,
    lambda_support_intervals: Optional[List[Tuple[float, float]]] = None
) -> Dict:
    """
    Compute complete falsification dashboard.
    
    Args:
        lambda_values: Sampled λ values
        alpha_pred_values: Predicted α values
        alpha_max_envelope: Experimental envelope α_max(λ)
        mapping_mode: e.g., "HIGGS_MIX", "DIRECT_YUKAWA"
        mapping_params: dict with f_N, κ, v_c, etc.
        envelope_variant: "canonical" / "monotone" / etc.
        sampling_info: dict with NPTS, method, seed
        lambda_support_intervals: List of (λ_min, λ_max) tuples for coverage
        
    Returns:
        Complete dashboard dict
    """
    # Domain discipline
    if lambda_support_intervals is None:
        lambda_support_intervals = []
    domain_metrics = compute_coverage_metrics(lambda_values, lambda_support_intervals)
    
    # Detectability metrics
    detectability_metrics = compute_detectability_metrics(
        alpha_pred_values, alpha_max_envelope, lambda_values
    )
    
    # Build complete dashboard
    dashboard = {
        'timestamp': datetime.now().isoformat(),
        'domain_discipline': domain_metrics,
        'mapping_provenance': {
            'mapping_mode': mapping_mode,
            'mapping_parameters': mapping_params,
            'convention_flags': {
                'planck_mass': 'reduced',  # M_Pl² = (8πG)⁻¹
                'sign_conventions': {
                    'alpha': 'always positive (depends on sin²θ)',
                    'kappa_vc': 'bounds on |κ_cH v_c| (absolute value)'
                }
            }
        },
        'exclusion_detectability': detectability_metrics,
        'robustness_knobs': {
            'envelope_variant': envelope_variant,
            'sampling': sampling_info
        }
    }
    
    return dashboard


def dashboard_to_markdown(dashboard: Dict) -> str:
    """
    Convert dashboard dict to human-readable Markdown.
    
    Args:
        dashboard: Dashboard dict from compute_dashboard()
        
    Returns:
        Markdown string
    """
    md = f"""# Falsification Dashboard

**Generated:** {dashboard['timestamp']}

## Domain Discipline (Real-Only)

- **Coverage Fraction:** {dashboard['domain_discipline']['coverage_fraction']:.6f}
- **λ Support Intervals:** {len(dashboard['domain_discipline']['lambda_support'])} sources
- **Union:** {dashboard['domain_discipline']['lambda_support_union']}
- **Note:** {dashboard['domain_discipline']['note']}

## Mapping Provenance

- **Mode:** {dashboard['mapping_provenance']['mapping_mode']}
- **Parameters:** {dashboard['mapping_provenance']['mapping_parameters']}
- **Conventions:** {dashboard['mapping_provenance']['convention_flags']}

## Exclusion / Detectability Metrics

- **r_max:** {dashboard['exclusion_detectability']['r_max']:.6e}
- **λ at r_max:** {dashboard['exclusion_detectability']['lambda_at_r_max']:.6e} m
- **r Quantiles:**
  - r_50: {dashboard['exclusion_detectability']['r_quantiles']['r_50']:.6e}
  - r_90: {dashboard['exclusion_detectability']['r_quantiles']['r_90']:.6e}
  - r_95: {dashboard['exclusion_detectability']['r_quantiles']['r_95']:.6e}
  - r_99: {dashboard['exclusion_detectability']['r_quantiles']['r_99']:.6e}
- **Fraction r > 0.1:** {dashboard['exclusion_detectability']['fraction_r_gt_0_1']:.6f}
- **Fraction r > 1:** {dashboard['exclusion_detectability']['fraction_r_gt_1']:.6f}
- **Scale to Detectable (r=0.1):** ×{dashboard['exclusion_detectability']['scale_to_detectable']:.6e}
- **Scale to Exclude (r=1):** ×{dashboard['exclusion_detectability']['scale_to_exclude']:.6e}

**Closest Approach:** {dashboard['exclusion_detectability']['closest_approach_sentence']}

## Robustness Knobs

- **Envelope Variant:** {dashboard['robustness_knobs']['envelope_variant']}
- **Sampling:** {dashboard['robustness_knobs']['sampling']}
"""
    return md


def add_emi_metrics_to_dashboard(dashboard: Dict, emi_report_path: str) -> Dict:
    """
    Add EMI red-team metrics to dashboard.
    
    Args:
        dashboard: Existing dashboard dict
        emi_report_path: Path to EMI red-team report JSON
        
    Returns:
        Updated dashboard dict
    """
    import json
    from pathlib import Path
    
    emi_path = Path(emi_report_path)
    if not emi_path.exists():
        dashboard['emi_redteam'] = {
            'status': 'not_run',
            'note': 'EMI red-team test not executed'
        }
        return dashboard
    
    with open(emi_path, 'r') as f:
        emi_report = json.load(f)
    
    correlation = emi_report.get('correlation_analysis', {})
    vulnerability = emi_report.get('vulnerability_assessment', {})
    
    dashboard['emi_redteam'] = {
        'status': 'completed',
        'correlation_coefficient': correlation.get('correlation_coefficient', 0.0),
        'p_value': correlation.get('p_value', 1.0),
        'significant': correlation.get('significant', False),
        'vulnerability_score': vulnerability.get('vulnerability_score', 0.0),
        'recommendation': vulnerability.get('recommendation', 'UNKNOWN'),
        'emi_amplitude_tested': emi_report.get('parameters', {}).get('emi_amplitude', 0.0),
        'report_path': str(emi_path)
    }
    
    # Add warning flag if EMI correlation is significant
    if correlation.get('significant', False):
        if 'warnings' not in dashboard:
            dashboard['warnings'] = []
        dashboard['warnings'].append(
            'EMI red-team test detected significant correlation. '
            'QRNG results may be confounded by electromagnetic interference.'
        )
    
    return dashboard


def add_collider_metrics_to_dashboard(dashboard: dict, collider_report_path: str) -> dict:
    """Add collider (Higgs invisible) metrics to dashboard."""
    import json
    from pathlib import Path
    
    collider_path = Path(collider_report_path)
    if not collider_path.exists():
        dashboard['collider'] = {'status': 'not_run', 'note': 'Collider test not executed'}
        return dashboard
    
    with open(collider_path, 'r') as f:
        collider_data = json.load(f) if collider_path.suffix == '.json' else {}
    
    dashboard['collider'] = {
        'status': 'completed',
        'br_limit': collider_data.get('br_limit', 0.11),
        'theta_max': collider_data.get('theta_max', 0.0),
        'kappa_vc_max': collider_data.get('kappa_vc_max', 0.0),
        'report_path': str(collider_path)
    }
    return dashboard


def add_cosmology_metrics_to_dashboard(dashboard: dict, cosmology_report_path: str) -> dict:
    """Add cosmology (BBN, CMB) metrics to dashboard."""
    import json
    from pathlib import Path
    
    cosmo_path = Path(cosmology_report_path)
    if not cosmo_path.exists():
        dashboard['cosmology'] = {'status': 'not_run', 'note': 'Cosmology test not executed'}
        return dashboard
    
    with open(cosmo_path, 'r') as f:
        cosmo_data = json.load(f) if cosmo_path.suffix == '.json' else {}
    
    dashboard['cosmology'] = {
        'status': 'completed',
        'bbn_delta_n_eff': cosmo_data.get('bbn_delta_n_eff', 0.0),
        'cmb_delta_w': cosmo_data.get('cmb_delta_w', 0.0),
        'theta_max': cosmo_data.get('theta_max', 0.0),
        'report_path': str(cosmo_path)
    }
    return dashboard


def add_precision_metrics_to_dashboard(dashboard: dict, precision_report_path: str) -> dict:
    """Add precision measurement (Casimir, EP, clocks) metrics to dashboard."""
    import json
    from pathlib import Path
    
    prec_path = Path(precision_report_path)
    if not prec_path.exists():
        dashboard['precision'] = {'status': 'not_run', 'note': 'Precision test not executed'}
        return dashboard
    
    with open(prec_path, 'r') as f:
        prec_data = json.load(f) if prec_path.suffix == '.json' else {}
    
    dashboard['precision'] = {
        'status': 'completed',
        'casimir_deviation': prec_data.get('casimir_deviation', 0.0),
        'ep_eta': prec_data.get('ep_eta', 0.0),
        'clock_shift': prec_data.get('clock_shift', 0.0),
        'theta_max': prec_data.get('theta_max', 0.0),
        'report_path': str(prec_path)
    }
    return dashboard


def add_quantum_optics_metrics_to_dashboard(dashboard: dict, qo_report_path: str) -> dict:
    """Add quantum optics (SPDC, HOM) metrics to dashboard."""
    import json
    from pathlib import Path
    
    qo_path = Path(qo_report_path)
    if not qo_path.exists():
        dashboard['quantum_optics'] = {'status': 'not_run', 'note': 'Quantum optics test not executed'}
        return dashboard
    
    with open(qo_path, 'r') as f:
        qo_data = json.load(f) if qo_path.suffix == '.json' else {}
    
    dashboard['quantum_optics'] = {
        'status': 'completed',
        'spdc_correlation_mod': qo_data.get('spdc_correlation_mod', 0.0),
        'hom_visibility_mod': qo_data.get('hom_visibility_mod', 0.0),
        'theta_hc': qo_data.get('theta_hc', 0.0),
        'report_path': str(qo_path)
    }
    return dashboard


def add_astrophysics_metrics_to_dashboard(dashboard: dict, astro_report_path: str) -> dict:
    """Add astrophysics (stellar cooling, SN1987A) metrics to dashboard."""
    import json
    from pathlib import Path
    
    astro_path = Path(astro_report_path)
    if not astro_path.exists():
        dashboard['astrophysics'] = {'status': 'not_run', 'note': 'Astrophysics test not executed'}
        return dashboard
    
    with open(astro_path, 'r') as f:
        astro_data = json.load(f) if astro_path.suffix == '.json' else {}
    
    dashboard['astrophysics'] = {
        'status': 'completed',
        'stellar_cooling_rate': astro_data.get('stellar_cooling_rate', 0.0),
        'sn1987a_energy_loss': astro_data.get('sn1987a_energy_loss', 0.0),
        'theta_max': astro_data.get('theta_max', 0.0),
        'report_path': str(astro_path)
    }
    return dashboard


def add_gravitational_wave_metrics_to_dashboard(dashboard: dict, gw_report_path: str) -> dict:
    """Add gravitational wave (GW propagation, BH shadow) metrics to dashboard."""
    import json
    from pathlib import Path
    
    gw_path = Path(gw_report_path)
    if not gw_path.exists():
        dashboard['gravitational_waves'] = {'status': 'not_run', 'note': 'GW test not executed'}
        return dashboard
    
    with open(gw_path, 'r') as f:
        gw_data = json.load(f) if gw_path.suffix == '.json' else {}
    
    dashboard['gravitational_waves'] = {
        'status': 'completed',
        'gw_speed_modification': gw_data.get('gw_speed_modification', 0.0),
        'bh_shadow_modification': gw_data.get('bh_shadow_modification', 0.0),
        'theta_max': gw_data.get('theta_max', 0.0),
        'report_path': str(gw_path)
    }
    return dashboard


def add_neutrino_metrics_to_dashboard(dashboard: dict, neutrino_report_path: str) -> dict:
    """Add neutrino oscillation metrics to dashboard."""
    import json
    from pathlib import Path
    
    nu_path = Path(neutrino_report_path)
    if not nu_path.exists():
        dashboard['neutrinos'] = {'status': 'not_run', 'note': 'Neutrino test not executed'}
        return dashboard
    
    with open(nu_path, 'r') as f:
        nu_data = json.load(f) if nu_path.suffix == '.json' else {}
    
    dashboard['neutrinos'] = {
        'status': 'completed',
        'oscillation_prob_modification': nu_data.get('oscillation_prob_modification', 0.0),
        'mass_matrix_modification': nu_data.get('mass_matrix_modification', 0.0),
        'theta_max': nu_data.get('theta_max', 0.0),
        'report_path': str(nu_path)
    }
    return dashboard


def add_dark_matter_metrics_to_dashboard(dashboard: dict, dm_report_path: str) -> dict:
    """Add dark matter direct detection metrics to dashboard."""
    import json
    from pathlib import Path
    
    dm_path = Path(dm_report_path)
    if not dm_path.exists():
        dashboard['dark_matter'] = {'status': 'not_run', 'note': 'DM test not executed'}
        return dashboard
    
    with open(dm_path, 'r') as f:
        dm_data = json.load(f) if dm_path.suffix == '.json' else {}
    
    dashboard['dark_matter'] = {
        'status': 'completed',
        'scattering_rate': dm_data.get('scattering_rate', 0.0),
        'theta_max': dm_data.get('theta_max', 0.0),
        'report_path': str(dm_path)
    }
    return dashboard


def add_theorem_metrics_to_dashboard(dashboard: dict, theorem_report_path: str) -> dict:
    """Add theorem-level consistency proof metrics to dashboard."""
    import json
    from pathlib import Path
    
    thm_path = Path(theorem_report_path)
    if not thm_path.exists():
        dashboard['theorems'] = {'status': 'not_run', 'note': 'Theorem proofs not executed'}
        return dashboard
    
    with open(thm_path, 'r') as f:
        thm_data = json.load(f) if thm_path.suffix == '.json' else {}
    
    dashboard['theorems'] = {
        'status': 'completed',
        'no_signaling': thm_data.get('no_signaling', {}),
        'stability': thm_data.get('stability', {}),
        'reduction_gr_sm': thm_data.get('reduction_gr_sm', {}),
        'report_path': str(thm_path)
    }
    return dashboard
