"""
Casimir Effect Channel for MQGT-SCF

Maps ToE parameters to Casimir force modifications and generates bounds
from experimental Casimir force measurements.

References:
- Lamoreaux (1997), Phys. Rev. Lett. 78, 5
- Bressi et al. (2002), Phys. Rev. Lett. 88, 041804
"""

import math
from typing import Tuple


# Physical constants
HBAR_C_GEV_M = 1.973269804e-16  # ħc in GeV·m
PI = math.pi


def compute_casimir_force_deviation(
    theta_hc: float,
    separation_m: float,
    m_c_GeV: float
) -> float:
    """
    Compute fractional deviation in Casimir force due to scalar field.
    
    Args:
        theta_hc: Mixing angle θ_hc
        separation_m: Plate separation in meters
        m_c_GeV: Scalar field mass m_c in GeV
        
    Returns:
        Fractional deviation δF/F
    """
    # Convert m_c to inverse length scale
    lambda_m = HBAR_C_GEV_M / m_c_GeV  # Compton wavelength in meters
    
    # Scalar field contribution to Casimir force
    # For small mixing: δF/F ≈ (θ_hc²) × exp(-2×separation/λ)
    if separation_m > 0 and lambda_m > 0:
        suppression = math.exp(-2.0 * separation_m / lambda_m)
        deviation = (theta_hc ** 2) * suppression
    else:
        deviation = 0.0
    
    return deviation


def compute_theta_max_from_casimir_limit(
    deviation_limit: float,
    separation_m: float,
    m_c_GeV: float
) -> float:
    """
    Inverse mapping: Casimir deviation limit → maximum allowed θ_hc.
    
    Args:
        deviation_limit: Experimental upper limit on |δF/F|
        separation_m: Plate separation in meters
        m_c_GeV: Scalar field mass m_c in GeV
        
    Returns:
        Maximum allowed |θ_hc|
    """
    if deviation_limit <= 0:
        return float('inf')
    
    lambda_m = HBAR_C_GEV_M / m_c_GeV if m_c_GeV > 0 else float('inf')
    
    if separation_m > 0 and lambda_m > 0:
        suppression = math.exp(-2.0 * separation_m / lambda_m)
        if suppression > 0:
            theta_sq = deviation_limit / suppression
            return math.sqrt(abs(theta_sq))
    
    return float('inf')


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c_GeV: float,
    separation_m: float,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Forward mapping: ToE parameters → Casimir deviation, θ_hc.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c_GeV: Scalar field mass m_c (GeV)
        separation_m: Plate separation (m)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (deviation, theta_hc)
    """
    # Compute θ_hc (simplified, ignoring m_c dependence for now)
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    
    deviation = compute_casimir_force_deviation(theta_hc, separation_m, m_c_GeV)
    return deviation, theta_hc


def inverse_mapping(
    deviation_limit: float,
    separation_m: float,
    m_c_GeV: float,
    v_c: float = 246.0,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Inverse mapping: Casimir limit → bounds on ToE parameters.
    
    Args:
        deviation_limit: Experimental upper limit on |δF/F|
        separation_m: Plate separation (m)
        m_c_GeV: Scalar field mass m_c (GeV)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    theta_max = compute_theta_max_from_casimir_limit(deviation_limit, separation_m, m_c_GeV)
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    return theta_max, kappa_vc_max
