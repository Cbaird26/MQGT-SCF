"""
Equivalence Principle (EP) Test Channel for MQGT-SCF

Maps ToE parameters to EP violation parameter η and generates bounds
from Eöt-Wash and MICROSCOPE measurements.

References:
- Eöt-Wash EP tests
- MICROSCOPE satellite experiment
"""

import math
from typing import Tuple


# Physical constants
HBAR_C_GEV_M = 1.973269804e-16  # ħc in GeV·m


def compute_ep_violation_eta(
    theta_hc: float,
    lambda_m: float
) -> float:
    """
    Compute EP violation parameter η from scalar field.
    
    η = (a_A - a_B) / ((a_A + a_B) / 2) for test masses A and B
    
    Args:
        theta_hc: Mixing angle θ_hc
        lambda_m: Scalar field range λ in meters
        
    Returns:
        EP violation parameter η (dimensionless)
    """
    # For Yukawa-type scalar field: η ≈ (θ_hc²) × (composition-dependent factor)
    # Simplified: η ≈ θ_hc² × f_composition × exp(-r/λ)
    # For long-range (r << λ): η ≈ θ_hc² × f_composition
    composition_factor = 1e-3  # Rough estimate, depends on test mass composition
    eta = (theta_hc ** 2) * composition_factor
    return eta


def compute_theta_max_from_ep_limit(
    eta_limit: float,
    lambda_m: float
) -> float:
    """
    Inverse mapping: EP violation limit → maximum allowed θ_hc.
    
    Args:
        eta_limit: Experimental upper limit on |η|
        lambda_m: Scalar field range λ in meters
        
    Returns:
        Maximum allowed |θ_hc|
    """
    if eta_limit <= 0:
        return float('inf')
    
    composition_factor = 1e-3
    theta_sq = eta_limit / composition_factor
    return math.sqrt(abs(theta_sq))


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c_GeV: float,
    m_h: float = 125.0
) -> Tuple[float, float, float]:
    """
    Forward mapping: ToE parameters → η, θ_hc, λ.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c_GeV: Scalar field mass m_c (GeV)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (eta, theta_hc, lambda_m)
    """
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    lambda_m = HBAR_C_GEV_M / m_c_GeV if m_c_GeV > 0 else float('inf')
    eta = compute_ep_violation_eta(theta_hc, lambda_m)
    return eta, theta_hc, lambda_m


def inverse_mapping(
    eta_limit: float,
    m_c_GeV: float,
    v_c: float = 246.0,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Inverse mapping: EP limit → bounds on ToE parameters.
    
    Args:
        eta_limit: Experimental upper limit on |η|
        m_c_GeV: Scalar field mass m_c (GeV)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    lambda_m = HBAR_C_GEV_M / m_c_GeV if m_c_GeV > 0 else float('inf')
    theta_max = compute_theta_max_from_ep_limit(eta_limit, lambda_m)
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    return theta_max, kappa_vc_max
