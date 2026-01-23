"""
Neutrino Oscillation Modification Constraints Channel for MQGT-SCF

Maps ToE parameters to neutrino mass matrix modifications and generates bounds
from oscillation experiments (Super-K, SNO, KamLAND, Daya Bay).

References:
- Super-Kamiokande atmospheric neutrinos
- SNO solar neutrinos
- KamLAND reactor neutrinos
- Daya Bay reactor neutrinos
"""

import math
from typing import Tuple


def compute_mass_matrix_modification(
    m_c_GeV: float,
    coupling: float
) -> float:
    """
    Compute modification to neutrino mass matrix from scalar field.
    
    Args:
        m_c_GeV: Scalar field mass m_c (GeV)
        coupling: Scalar-neutrino coupling
        
    Returns:
        Mass matrix modification (fractional)
    """
    m_c_eV = m_c_GeV * 1e9
    
    # Only affects if m_c ~ 10⁻³ - 10⁻¹ eV (neutrino mass scale)
    if m_c_eV < 1e-3 or m_c_eV > 1e-1:
        return 0.0
    
    # Mass matrix modification
    # Rough estimate: δm² ≈ coupling² × m_c²
    delta_m2 = (coupling ** 2) * (m_c_eV ** 2)
    
    return delta_m2


def compute_oscillation_probability_modification(
    mass_matrix_mod: float,
    L_km: float,
    E_MeV: float
) -> float:
    """
    Compute modification to oscillation probability from mass matrix change.
    
    Args:
        mass_matrix_mod: Mass matrix modification δm² (eV²)
        L_km: Baseline distance (km)
        E_MeV: Neutrino energy (MeV)
        
    Returns:
        Oscillation probability modification ΔP
    """
    # Standard oscillation: P ≈ sin²(1.27 × δm² × L / E)
    # Modification: ΔP ≈ (coupling²) × (δm² / δm²_standard) × oscillation_term
    
    if E_MeV <= 0:
        return 0.0
    
    # Standard δm² (atmospheric: ~2.5×10⁻³ eV²)
    delta_m2_standard = 2.5e-3
    
    if delta_m2_standard > 0:
        ratio = mass_matrix_mod / delta_m2_standard
        oscillation_arg = 1.27 * delta_m2_standard * L_km / E_MeV
        delta_P = ratio * math.sin(oscillation_arg) ** 2
    else:
        delta_P = 0.0
    
    return delta_P


def compute_coupling_bound_from_oscillations(
    observed_prob: float,
    predicted_prob: float,
    m_c_GeV: float,
    L_km: float,
    E_MeV: float
) -> float:
    """
    Inverse mapping: oscillation probability limit → maximum allowed coupling.
    
    Args:
        observed_prob: Observed oscillation probability
        predicted_prob: Predicted probability without scalars
        m_c_GeV: Scalar field mass m_c (GeV)
        L_km: Baseline (km)
        E_MeV: Energy (MeV)
        
    Returns:
        Maximum allowed coupling
    """
    if observed_prob < 0 or predicted_prob < 0:
        return float('inf')
    
    # Probability difference
    delta_P = abs(observed_prob - predicted_prob)
    
    if delta_P <= 0:
        return float('inf')
    
    m_c_eV = m_c_GeV * 1e9
    if m_c_eV < 1e-3 or m_c_eV > 1e-1:
        return float('inf')
    
    # Invert: delta_P ≈ (coupling²) × (m_c²) × oscillation_term
    delta_m2_standard = 2.5e-3
    if E_MeV > 0 and delta_m2_standard > 0:
        oscillation_arg = 1.27 * delta_m2_standard * L_km / E_MeV
        oscillation_term = math.sin(oscillation_arg) ** 2
        
        if oscillation_term > 0:
            coupling_sq = delta_P / ((m_c_eV ** 2) / delta_m2_standard * oscillation_term)
            return math.sqrt(abs(coupling_sq))
    
    return float('inf')


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c_GeV: float,
    L_km: float = 295.0,  # KamLAND baseline
    E_MeV: float = 3.0,
    m_h: float = 125.0
) -> Tuple[float, float, float]:
    """
    Forward mapping: ToE parameters → mass mod, prob mod, coupling.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c_GeV: Scalar field mass m_c (GeV)
        L_km: Baseline (km)
        E_MeV: Energy (MeV)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (mass_matrix_mod, delta_P, coupling)
    """
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    coupling = abs(theta_hc)
    mass_mod = compute_mass_matrix_modification(m_c_GeV, coupling)
    delta_P = compute_oscillation_probability_modification(mass_mod, L_km, E_MeV)
    return mass_mod, delta_P, coupling


def inverse_mapping(
    prob_limit: float,
    m_c_GeV: float,
    L_km: float = 295.0,
    E_MeV: float = 3.0,
    v_c: float = 246.0,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Inverse mapping: oscillation limit → bounds on ToE parameters.
    
    Args:
        prob_limit: Maximum allowed probability modification
        m_c_GeV: Scalar field mass m_c (GeV)
        L_km: Baseline (km)
        E_MeV: Energy (MeV)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    predicted_prob = 0.5  # Typical oscillation probability
    coupling_max = compute_coupling_bound_from_oscillations(
        predicted_prob + prob_limit, predicted_prob, m_c_GeV, L_km, E_MeV
    )
    
    if coupling_max == float('inf'):
        return float('inf'), float('inf')
    
    theta_max = coupling_max
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    
    return theta_max, kappa_vc_max
