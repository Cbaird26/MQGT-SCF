"""
Dark Matter Direct Detection Constraints Channel for MQGT-SCF

Maps ToE parameters to dark matter scattering rates and generates bounds
from direct detection experiments (XENON, LUX, PandaX, LZ).

Note: Only relevant if Φ_c is a dark matter candidate.

References:
- XENON1T/nT limits
- LUX-ZEPLIN (LZ) limits
- PandaX limits
"""

import math
from typing import Tuple


# Physical constants
HBAR_C_GEV_M = 1.973269804e-16
M_PROTON_GEV = 0.938  # Proton mass


def compute_scattering_rate(
    m_c_GeV: float,
    coupling: float,
    target_nucleus_A: int = 131  # Xe-131
) -> float:
    """
    Compute dark matter-nucleus scattering rate.
    
    Args:
        m_c_GeV: Scalar field mass m_c (GeV) - DM mass
        coupling: Scalar-nucleon coupling
        target_nucleus_A: Target nucleus mass number
        
    Returns:
        Scattering rate (events/kg/year)
    """
    # Only relevant if m_c ~ 1 GeV - 1 TeV (DM mass range)
    if m_c_GeV < 0.1 or m_c_GeV > 1000.0:
        return 0.0
    
    # DM number density (local: ρ_DM ≈ 0.3 GeV/cm³)
    rho_dm_GeV_cm3 = 0.3
    n_dm_cm3 = rho_dm_GeV_cm3 / m_c_GeV
    
    # DM velocity (virial: v ~ 10⁻³ c)
    v_dm = 1e-3 * 299792458.0  # m/s
    
    # Cross section (simplified)
    # σ ≈ (coupling²) × (A²) × (m_n² / m_c²)
    m_n_GeV = target_nucleus_A * M_PROTON_GEV / 1.0  # Rough estimate
    sigma_cm2 = (coupling ** 2) * (target_nucleus_A ** 2) * (m_n_GeV ** 2) / (m_c_GeV ** 2)
    sigma_cm2 *= 1e-40  # Conversion factor
    
    # Scattering rate: R = n_DM × v × σ × N_target
    # For 1 kg target: N_target ≈ 10²⁶
    N_target = 1e26
    rate_per_kg_year = n_dm_cm3 * (v_dm / 100.0) * sigma_cm2 * N_target * 3.15e7  # Convert to /year
    
    return rate_per_kg_year


def compute_coupling_bound_from_detection(
    observed_rate: float,
    predicted_rate: float,
    m_c_GeV: float,
    target_nucleus_A: int = 131
) -> float:
    """
    Inverse mapping: detection rate limit → maximum allowed coupling.
    
    Args:
        observed_rate: Observed rate (events/kg/year)
        predicted_rate: Predicted rate without scalars (events/kg/year)
        m_c_GeV: Scalar field mass m_c (GeV)
        target_nucleus_A: Target nucleus mass number
        
    Returns:
        Maximum allowed coupling
    """
    if observed_rate <= 0:
        return float('inf')
    
    # Rate limit
    rate_limit = observed_rate
    
    if rate_limit <= 0:
        return float('inf')
    
    if m_c_GeV < 0.1 or m_c_GeV > 1000.0:
        return float('inf')
    
    # Invert scattering rate formula
    rho_dm_GeV_cm3 = 0.3
    n_dm_cm3 = rho_dm_GeV_cm3 / m_c_GeV
    v_dm = 1e-3 * 299792458.0
    N_target = 1e26
    m_n_GeV = target_nucleus_A * M_PROTON_GEV
    
    # Solve: rate_limit = n_DM × v × σ × N_target
    # σ = (coupling²) × (A²) × (m_n² / m_c²) × conversion
    sigma_cm2 = rate_limit / (n_dm_cm3 * (v_dm / 100.0) * N_target * 3.15e7)
    
    if sigma_cm2 > 0 and m_n_GeV > 0:
        coupling_sq = sigma_cm2 * (m_c_GeV ** 2) / ((target_nucleus_A ** 2) * (m_n_GeV ** 2) * 1e-40)
        return math.sqrt(abs(coupling_sq))
    
    return float('inf')


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c_GeV: float,
    target_nucleus_A: int = 131,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Forward mapping: ToE parameters → scattering rate, coupling.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c_GeV: Scalar field mass m_c (GeV) - DM mass
        target_nucleus_A: Target nucleus mass number
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (scattering_rate, coupling)
    """
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    coupling = abs(theta_hc)
    rate = compute_scattering_rate(m_c_GeV, coupling, target_nucleus_A)
    return rate, coupling


def inverse_mapping(
    rate_limit: float,
    m_c_GeV: float,
    target_nucleus_A: int = 131,
    v_c: float = 246.0,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Inverse mapping: detection limit → bounds on ToE parameters.
    
    Args:
        rate_limit: Maximum allowed scattering rate (events/kg/year)
        m_c_GeV: Scalar field mass m_c (GeV)
        target_nucleus_A: Target nucleus mass number
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    predicted_rate = 0.0  # No signal expected
    coupling_max = compute_coupling_bound_from_detection(
        rate_limit, predicted_rate, m_c_GeV, target_nucleus_A
    )
    
    if coupling_max == float('inf'):
        return float('inf'), float('inf')
    
    theta_max = coupling_max
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    
    return theta_max, kappa_vc_max
