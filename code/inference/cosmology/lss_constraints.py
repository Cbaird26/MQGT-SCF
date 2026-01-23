"""
Large-Scale Structure (LSS) Constraints Channel for MQGT-SCF

Maps ToE parameters to matter power spectrum modifications and generates bounds
from galaxy surveys (SDSS, DES, Euclid).

References:
- SDSS matter power spectrum
- DES clustering measurements
- Euclid (future)
"""

import math
from typing import Tuple


def compute_power_spectrum_modification(
    m_c_GeV: float,
    coupling: float,
    z: float,
    k_h_Mpc: float
) -> float:
    """
    Compute modification to matter power spectrum from scalar field.
    
    Args:
        m_c_GeV: Scalar field mass m_c (GeV)
        coupling: Scalar-matter coupling
        z: Redshift
        k_h_Mpc: Wavenumber (h/Mpc)
        
    Returns:
        Fractional power spectrum modification ΔP/P
    """
    m_c_eV = m_c_GeV * 1e9
    
    # Only affects if m_c < 10⁻³ eV (affects structure formation)
    if m_c_eV > 1e-3:
        return 0.0
    
    # Modified growth factor
    # Rough estimate: δ(k,z) = f(m_c, coupling) × δ_ΛCDM(k,z)
    # For light scalars: f ≈ 1 + coupling² × suppression
    
    # Suppression factor (depends on k and m_c)
    k_GeV = k_h_Mpc * 1e-6  # Rough conversion
    if m_c_GeV > 0 and k_GeV > 0:
        suppression = (m_c_GeV / k_GeV) ** 2
    else:
        suppression = 0.0
    
    # Power spectrum modification
    delta_P_P = (coupling ** 2) * suppression * (1.0 + z) ** (-1.0)
    
    return delta_P_P


def compute_coupling_bound_from_lss(
    observed_spectrum: float,
    predicted_spectrum: float,
    m_c_GeV: float,
    z: float,
    k_h_Mpc: float
) -> float:
    """
    Inverse mapping: LSS power spectrum limit → maximum allowed coupling.
    
    Args:
        observed_spectrum: Observed power spectrum P(k)
        predicted_spectrum: Predicted spectrum without scalars P_ΛCDM(k)
        m_c_GeV: Scalar field mass m_c (GeV)
        z: Redshift
        k_h_Mpc: Wavenumber (h/Mpc)
        
    Returns:
        Maximum allowed coupling
    """
    if observed_spectrum <= 0 or predicted_spectrum <= 0:
        return float('inf')
    
    # Spectrum difference
    delta_P_P = abs(observed_spectrum - predicted_spectrum) / predicted_spectrum
    
    if delta_P_P <= 0:
        return float('inf')
    
    m_c_eV = m_c_GeV * 1e9
    if m_c_eV > 1e-3:
        return float('inf')
    
    k_GeV = k_h_Mpc * 1e-6
    if m_c_GeV > 0 and k_GeV > 0:
        suppression = (m_c_GeV / k_GeV) ** 2
    else:
        suppression = 1.0
    
    if suppression > 0:
        coupling_sq = delta_P_P / (suppression * (1.0 + z) ** (-1.0))
        return math.sqrt(abs(coupling_sq))
    
    return float('inf')


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c_GeV: float,
    z: float = 0.0,
    k_h_Mpc: float = 0.1,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Forward mapping: ToE parameters → power spectrum mod, coupling.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c_GeV: Scalar field mass m_c (GeV)
        z: Redshift
        k_h_Mpc: Wavenumber (h/Mpc)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (delta_P_P, coupling)
    """
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    coupling = abs(theta_hc)
    delta_P_P = compute_power_spectrum_modification(m_c_GeV, coupling, z, k_h_Mpc)
    return delta_P_P, coupling


def inverse_mapping(
    spectrum_limit: float,
    m_c_GeV: float,
    z: float = 0.0,
    k_h_Mpc: float = 0.1,
    v_c: float = 246.0,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Inverse mapping: LSS limit → bounds on ToE parameters.
    
    Args:
        spectrum_limit: Maximum allowed power spectrum modification
        m_c_GeV: Scalar field mass m_c (GeV)
        z: Redshift
        k_h_Mpc: Wavenumber (h/Mpc)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    predicted_spectrum = 1.0  # Normalized
    coupling_max = compute_coupling_bound_from_lss(
        predicted_spectrum * (1.0 + spectrum_limit), predicted_spectrum, m_c_GeV, z, k_h_Mpc
    )
    
    if coupling_max == float('inf'):
        return float('inf'), float('inf')
    
    theta_max = coupling_max
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    
    return theta_max, kappa_vc_max
