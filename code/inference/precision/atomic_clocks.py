"""
Atomic Clock Comparison Channel for MQGT-SCF

Maps ToE parameters to atomic clock frequency shifts.
"""
import math
from typing import Tuple

HBAR_C_GEV_M = 1.973269804e-16

def compute_frequency_shift(theta_hc: float, m_c_GeV: float) -> float:
    """Compute fractional frequency shift δν/ν from scalar field."""
    m_c_eV = m_c_GeV * 1e9
    if m_c_eV < 1e-12:  # Ultralight scalars
        # Frequency shift ≈ (θ_hc²) × small_factor
        delta_nu_nu = (theta_hc ** 2) * 1e-6
        return delta_nu_nu
    return 0.0

def compute_theta_max_from_clock_limit(delta_nu_limit: float, m_c_GeV: float) -> float:
    """Inverse mapping: clock limit → maximum allowed θ_hc."""
    if delta_nu_limit <= 0:
        return float('inf')
    m_c_eV = m_c_GeV * 1e9
    if m_c_eV < 1e-12:
        theta_sq = delta_nu_limit / 1e-6
        return math.sqrt(abs(theta_sq))
    return float('inf')

def forward_mapping(kappa_ch: float, v_c: float, m_c_GeV: float, m_h: float = 125.0) -> Tuple[float, float]:
    """Forward mapping: ToE parameters → δν/ν, θ_hc."""
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    delta_nu_nu = compute_frequency_shift(theta_hc, m_c_GeV)
    return delta_nu_nu, theta_hc

def inverse_mapping(delta_nu_limit: float, m_c_GeV: float, v_c: float = 246.0, m_h: float = 125.0) -> Tuple[float, float]:
    """Inverse mapping: clock limit → bounds on ToE parameters."""
    theta_max = compute_theta_max_from_clock_limit(delta_nu_limit, m_c_GeV)
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    return theta_max, kappa_vc_max
