"""
Stellar Cooling Constraints Channel for MQGT-SCF

Maps ToE parameters to stellar energy loss via scalar emission and generates bounds
from stellar luminosity observations.

References:
- Red giant branch: Gaia/HST luminosity data
- White dwarfs: Cooling age measurements
- Solar neutrinos: Constrain scalar emission from Sun
"""

import math
from typing import Tuple


# Physical constants
HBAR_C_GEV_M = 1.973269804e-16  # ħc in GeV·m
ALPHA_EM = 1.0 / 137.036  # Fine structure constant


def compute_scalar_emission_rate(
    m_c_GeV: float,
    g_phi_e: float,
    T_stellar_MeV: float,
    rho_stellar_g_cm3: float
) -> float:
    """
    Compute scalar emission rate from stellar plasma.
    
    For m_c < T_stellar, scalars can be produced via electron-photon interactions.
    
    Args:
        m_c_GeV: Scalar field mass m_c (GeV)
        g_phi_e: Scalar-electron coupling
        T_stellar_MeV: Stellar temperature (MeV)
        rho_stellar_g_cm3: Stellar density (g/cm³)
        
    Returns:
        Energy loss rate ε_φ (erg/g/s)
    """
    m_c_MeV = m_c_GeV * 1000.0
    
    # Only emit if m_c < T_stellar (kinematically allowed)
    if m_c_MeV >= T_stellar_MeV:
        return 0.0
    
    # Rough estimate: ε_φ ≈ (g_φe² / m_e²) × (T⁴ / ρ) × phase_space
    # For stellar interiors: T ~ 0.1-1 MeV, ρ ~ 10²-10⁶ g/cm³
    m_e_MeV = 0.511  # Electron mass
    
    # Phase space factor
    phase_space = (1.0 - (m_c_MeV / T_stellar_MeV) ** 2) ** (3.0 / 2.0)
    
    # Emission rate (simplified)
    epsilon_phi = (g_phi_e ** 2) * (T_stellar_MeV ** 4) / (rho_stellar_g_cm3 * m_e_MeV ** 2) * phase_space
    epsilon_phi *= 1e20  # Rough conversion to erg/g/s
    
    return epsilon_phi


def compute_luminosity_modification(
    emission_rate: float,
    stellar_mass_g: float
) -> float:
    """
    Compute fractional luminosity modification from scalar emission.
    
    Args:
        emission_rate: Scalar emission rate ε_φ (erg/g/s)
        stellar_mass_g: Stellar mass (g)
        
    Returns:
        Fractional luminosity increase ΔL/L
    """
    # Total scalar luminosity
    L_scalar = emission_rate * stellar_mass_g
    
    # Typical stellar luminosity (solar: L_sun ≈ 3.8×10³³ erg/s)
    L_sun_erg_s = 3.8e33
    
    # Rough estimate: assume solar-like star
    L_stellar = L_sun_erg_s
    
    delta_L_L = L_scalar / L_stellar if L_stellar > 0 else 0.0
    return delta_L_L


def compute_g_phi_e_from_theta(theta_hc: float, m_c_GeV: float) -> float:
    """
    Map ToE mixing angle to scalar-electron coupling.
    
    Simplified: assume g_φe ≈ θ_hc × (electron Yukawa coupling)
    
    Args:
        theta_hc: Mixing angle θ_hc
        m_c_GeV: Scalar field mass m_c (GeV)
        
    Returns:
        Scalar-electron coupling g_φe
    """
    # Rough estimate: g_φe ≈ θ_hc × y_e where y_e ~ 10⁻⁶ (electron Yukawa)
    y_e = 1e-6
    g_phi_e = abs(theta_hc) * y_e
    return g_phi_e


def compute_coupling_bound_from_cooling(
    observed_luminosity: float,
    predicted_luminosity: float,
    m_c_GeV: float,
    T_stellar_MeV: float,
    rho_stellar_g_cm3: float
) -> float:
    """
    Inverse mapping: stellar cooling limit → maximum allowed coupling.
    
    Args:
        observed_luminosity: Observed stellar luminosity
        predicted_luminosity: Predicted luminosity (without scalars)
        m_c_GeV: Scalar field mass m_c (GeV)
        T_stellar_MeV: Stellar temperature (MeV)
        rho_stellar_g_cm3: Stellar density (g/cm³)
        
    Returns:
        Maximum allowed g_φe
    """
    if observed_luminosity <= 0 or predicted_luminosity <= 0:
        return float('inf')
    
    # Observed excess cooling
    excess = (predicted_luminosity - observed_luminosity) / predicted_luminosity
    
    if excess <= 0:
        return float('inf')  # No constraint if no excess cooling
    
    # Invert emission rate formula
    m_c_MeV = m_c_GeV * 1000.0
    if m_c_MeV >= T_stellar_MeV:
        return float('inf')
    
    phase_space = (1.0 - (m_c_MeV / T_stellar_MeV) ** 2) ** (3.0 / 2.0)
    if phase_space <= 0:
        return float('inf')
    
    m_e_MeV = 0.511
    # Solve: excess ≈ (g_φe² / m_e²) × (T⁴ / ρ) × phase_space
    g_phi_e_sq = excess * rho_stellar_g_cm3 * m_e_MeV ** 2 / (T_stellar_MeV ** 4 * phase_space)
    g_phi_e_sq /= 1e20  # Conversion factor
    
    return math.sqrt(abs(g_phi_e_sq))


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c_GeV: float,
    T_stellar_MeV: float = 0.1,
    rho_stellar_g_cm3: float = 100.0,
    m_h: float = 125.0
) -> Tuple[float, float, float]:
    """
    Forward mapping: ToE parameters → emission rate, luminosity mod, g_φe.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c_GeV: Scalar field mass m_c (GeV)
        T_stellar_MeV: Stellar temperature (MeV)
        rho_stellar_g_cm3: Stellar density (g/cm³)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (emission_rate, delta_L_L, g_phi_e)
    """
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    g_phi_e = compute_g_phi_e_from_theta(theta_hc, m_c_GeV)
    emission_rate = compute_scalar_emission_rate(m_c_GeV, g_phi_e, T_stellar_MeV, rho_stellar_g_cm3)
    delta_L_L = compute_luminosity_modification(emission_rate, 2e33)  # Solar mass in g
    return emission_rate, delta_L_L, g_phi_e


def inverse_mapping(
    cooling_limit: float,
    m_c_GeV: float,
    T_stellar_MeV: float = 0.1,
    rho_stellar_g_cm3: float = 100.0,
    v_c: float = 246.0,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Inverse mapping: cooling limit → bounds on ToE parameters.
    
    Args:
        cooling_limit: Maximum allowed excess cooling
        m_c_GeV: Scalar field mass m_c (GeV)
        T_stellar_MeV: Stellar temperature (MeV)
        rho_stellar_g_cm3: Stellar density (g/cm³)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    g_phi_e_max = compute_coupling_bound_from_cooling(
        1.0 - cooling_limit, 1.0, m_c_GeV, T_stellar_MeV, rho_stellar_g_cm3
    )
    
    if g_phi_e_max == float('inf'):
        return float('inf'), float('inf')
    
    # Convert g_φe back to θ_hc
    y_e = 1e-6
    theta_max = g_phi_e_max / y_e if y_e > 0 else float('inf')
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    
    return theta_max, kappa_vc_max
