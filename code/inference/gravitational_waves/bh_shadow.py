"""
Black Hole Shadow Constraints Channel for MQGT-SCF

Maps ToE parameters to black hole shadow modifications and generates bounds
from Event Horizon Telescope (EHT) measurements.

References:
- EHT M87* shadow data
- EHT Sgr A* shadow data
"""

import math
from typing import Tuple


# Physical constants
G = 6.67430e-11  # m³/kg/s², gravitational constant
C = 299792458.0  # m/s
HBAR_C_GEV_M = 1.973269804e-16


def compute_shadow_modification(
    m_c_GeV: float,
    coupling: float,
    M_bh_solar_masses: float
) -> float:
    """
    Compute modification to black hole shadow size from scalar field.
    
    Args:
        m_c_GeV: Scalar field mass m_c (GeV)
        coupling: Scalar-gravity coupling
        M_bh_solar_masses: Black hole mass (solar masses)
        
    Returns:
        Fractional shadow size modification ΔR/R
    """
    # For ultralight scalars (m_c < 10⁻¹⁰ eV), scalar hair can modify metric
    m_c_eV = m_c_GeV * 1e9
    
    if m_c_eV > 1e-10:
        return 0.0  # Too heavy to affect BH metric
    
    # Schwarzschild radius
    R_s_m = 2 * G * M_bh_solar_masses * 1.989e30 / (C ** 2)
    
    # Scalar field range
    lambda_m = HBAR_C_GEV_M / m_c_GeV if m_c_GeV > 0 else float('inf')
    
    # Modification scales with coupling and range
    # Rough estimate: ΔR/R ≈ coupling² × (R_s / λ)
    if lambda_m > 0:
        delta_R_R = (coupling ** 2) * (R_s_m / lambda_m)
    else:
        delta_R_R = 0.0
    
    return delta_R_R


def compute_coupling_bound_from_shadow(
    observed_size: float,
    predicted_size: float,
    m_c_GeV: float,
    M_bh_solar_masses: float
) -> float:
    """
    Inverse mapping: shadow size limit → maximum allowed coupling.
    
    Args:
        observed_size: Observed shadow size (angular diameter, μas)
        predicted_size: Predicted size without scalars (μas)
        m_c_GeV: Scalar field mass m_c (GeV)
        M_bh_solar_masses: Black hole mass (solar masses)
        
    Returns:
        Maximum allowed coupling
    """
    if observed_size <= 0 or predicted_size <= 0:
        return float('inf')
    
    # Size difference
    delta_size = abs(observed_size - predicted_size) / predicted_size
    
    if delta_size <= 0:
        return float('inf')
    
    m_c_eV = m_c_GeV * 1e9
    if m_c_eV > 1e-10:
        return float('inf')  # No constraint for heavy scalars
    
    R_s_m = 2 * G * M_bh_solar_masses * 1.989e30 / (C ** 2)
    lambda_m = HBAR_C_GEV_M / m_c_GeV if m_c_GeV > 0 else float('inf')
    
    if lambda_m > 0:
        coupling_sq = delta_size * lambda_m / R_s_m
        return math.sqrt(abs(coupling_sq))
    
    return float('inf')


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c_GeV: float,
    M_bh_solar_masses: float = 6.5e9,  # M87* mass
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Forward mapping: ToE parameters → shadow mod, coupling.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c_GeV: Scalar field mass m_c (GeV)
        M_bh_solar_masses: Black hole mass (solar masses)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (delta_R_R, coupling)
    """
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    coupling = abs(theta_hc)
    delta_R_R = compute_shadow_modification(m_c_GeV, coupling, M_bh_solar_masses)
    return delta_R_R, coupling


def inverse_mapping(
    shadow_limit: float,
    m_c_GeV: float,
    M_bh_solar_masses: float = 6.5e9,
    v_c: float = 246.0,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Inverse mapping: shadow limit → bounds on ToE parameters.
    
    Args:
        shadow_limit: Maximum allowed shadow size modification
        m_c_GeV: Scalar field mass m_c (GeV)
        M_bh_solar_masses: Black hole mass (solar masses)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    predicted_size = 42.0  # Standard Schwarzschild shadow (μas for M87*)
    coupling_max = compute_coupling_bound_from_shadow(
        predicted_size * (1.0 + shadow_limit), predicted_size, m_c_GeV, M_bh_solar_masses
    )
    
    if coupling_max == float('inf'):
        return float('inf'), float('inf')
    
    theta_max = coupling_max
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    
    return theta_max, kappa_vc_max
