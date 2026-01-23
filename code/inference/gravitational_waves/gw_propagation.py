"""
Gravitational Wave Propagation Constraints Channel for MQGT-SCF

Maps ToE parameters to GW speed modifications and generates bounds
from LIGO/Virgo observations (GW170817 speed constraint).

References:
- GW170817: Speed of gravity = c within 10⁻¹⁵
- LIGO/Virgo public data releases
"""

import math
from typing import Tuple


# Physical constants
C = 299792458.0  # m/s, speed of light
HBAR_C_GEV_M = 1.973269804e-16


def compute_gw_speed_modification(
    m_c_GeV: float,
    coupling: float
) -> float:
    """
    Compute modification to gravitational wave speed from scalar field.
    
    Args:
        m_c_GeV: Scalar field mass m_c (GeV)
        coupling: Scalar-gravity coupling strength
        
    Returns:
        Speed modification (v_gw - c) / c
    """
    # For scalar-tensor theories: v_gw/c ≈ 1 - (coupling²) × (m_c² / ω²)
    # For GW170817: ω ~ 100 Hz, so m_c² / ω² is tiny unless m_c is ultralight
    
    # Simplified: v_gw/c = 1 - coupling² × suppression_factor
    # Suppression is large for m_c >> ω_GW, small for m_c << ω_GW
    omega_gw_hz = 100.0  # Typical GW frequency
    omega_gw_GeV = omega_gw_hz * 6.626e-34 * 1e9 / 1.602e-19  # Convert to GeV
    
    if m_c_GeV > 0:
        suppression = (m_c_GeV / omega_gw_GeV) ** 2 if omega_gw_GeV > 0 else 1.0
    else:
        suppression = 0.0
    
    delta_v_c = -(coupling ** 2) * suppression
    return delta_v_c


def compute_gw_dispersion(
    m_c_GeV: float,
    frequency_hz: float,
    coupling: float
) -> float:
    """
    Compute GW dispersion from scalar field.
    
    Args:
        m_c_GeV: Scalar field mass m_c (GeV)
        frequency_hz: GW frequency (Hz)
        coupling: Scalar-gravity coupling
        
    Returns:
        Dispersion parameter
    """
    # Modified dispersion: ω² = k² + m_eff²
    # m_eff ≈ coupling × m_c
    m_eff = coupling * m_c_GeV
    
    # Convert frequency to energy
    omega_GeV = frequency_hz * 6.626e-34 * 1e9 / 1.602e-19
    
    if omega_GeV > 0:
        dispersion = (m_eff / omega_GeV) ** 2
    else:
        dispersion = 0.0
    
    return dispersion


def compute_coupling_bound_from_gw_speed(
    speed_limit: float,
    m_c_GeV: float
) -> float:
    """
    Inverse mapping: GW speed limit → maximum allowed coupling.
    
    Args:
        speed_limit: Maximum allowed |v_gw - c|/c
        m_c_GeV: Scalar field mass m_c (GeV)
        
    Returns:
        Maximum allowed coupling
    """
    if speed_limit <= 0:
        return float('inf')
    
    omega_gw_hz = 100.0
    omega_gw_GeV = omega_gw_hz * 6.626e-34 * 1e9 / 1.602e-19
    
    if m_c_GeV > 0 and omega_gw_GeV > 0:
        suppression = (m_c_GeV / omega_gw_GeV) ** 2
    else:
        suppression = 1.0
    
    if suppression > 0:
        coupling_sq = abs(speed_limit) / suppression
        return math.sqrt(coupling_sq)
    
    return float('inf')


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c_GeV: float,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Forward mapping: ToE parameters → speed mod, coupling.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c_GeV: Scalar field mass m_c (GeV)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (delta_v_c, coupling)
    """
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    # Rough estimate: scalar-gravity coupling ≈ θ_hc
    coupling = abs(theta_hc)
    delta_v_c = compute_gw_speed_modification(m_c_GeV, coupling)
    return delta_v_c, coupling


def inverse_mapping(
    speed_limit: float,
    m_c_GeV: float,
    v_c: float = 246.0,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Inverse mapping: GW speed limit → bounds on ToE parameters.
    
    Args:
        speed_limit: Maximum allowed |v_gw - c|/c
        m_c_GeV: Scalar field mass m_c (GeV)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    coupling_max = compute_coupling_bound_from_gw_speed(speed_limit, m_c_GeV)
    
    if coupling_max == float('inf'):
        return float('inf'), float('inf')
    
    # Convert coupling back to θ_hc
    theta_max = coupling_max
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    
    return theta_max, kappa_vc_max
