"""
SPDC Simulation Channel for MQGT-SCF

Simulates Spontaneous Parametric Down-Conversion with scalar field modifications.
"""
import math
from typing import Tuple

def simulate_spdc_with_scalar(theta_hc: float, m_c_GeV: float) -> Tuple[float, float]:
    """Simulate SPDC biphoton correlations with scalar field effects."""
    m_c_eV = m_c_GeV * 1e9
    if 1e-3 < m_c_eV < 1e-1:  # Optical frequency range
        # Scalar field modifies correlation function
        correlation_modification = (theta_hc ** 2) * 1e-4
        return correlation_modification, theta_hc
    return 0.0, theta_hc

def forward_mapping(kappa_ch: float, v_c: float, m_c_GeV: float, m_h: float = 125.0) -> Tuple[float, float]:
    """Forward mapping: ToE parameters → correlation modification, θ_hc."""
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    corr_mod, _ = simulate_spdc_with_scalar(theta_hc, m_c_GeV)
    return corr_mod, theta_hc
