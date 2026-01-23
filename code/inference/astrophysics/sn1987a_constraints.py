"""
Supernova 1987A Energy Loss Constraints Channel for MQGT-SCF

Maps ToE parameters to scalar energy loss in supernovae and generates bounds
from SN1987A neutrino burst duration.

References:
- SN1987A neutrino timing data (IMB, Kamiokande)
- Supernova simulation codes (PROMETHEUS, SNEC)
"""

import math
from typing import Tuple


# Physical constants
HBAR_C_GEV_M = 1.973269804e-16


def compute_scalar_energy_loss(
    m_c_GeV: float,
    g_phi_nu: float,
    T_sn_MeV: float = 30.0,
    rho_sn_g_cm3: float = 1e14
) -> float:
    """
    Compute scalar energy loss rate in supernova core.
    
    Args:
        m_c_GeV: Scalar field mass m_c (GeV)
        g_phi_nu: Scalar-neutrino coupling
        T_sn_MeV: Supernova core temperature (MeV), default 30
        rho_sn_g_cm3: Supernova core density (g/cm³), default 1e14
        
    Returns:
        Energy loss rate ε_φ (erg/g/s)
    """
    m_c_MeV = m_c_GeV * 1000.0
    
    # Only emit if m_c < T_sn
    if m_c_MeV >= T_sn_MeV:
        return 0.0
    
    # Phase space factor
    phase_space = (1.0 - (m_c_MeV / T_sn_MeV) ** 2) ** (3.0 / 2.0)
    
    # Emission rate (simplified)
    epsilon_phi = (g_phi_nu ** 2) * (T_sn_MeV ** 4) / rho_sn_g_cm3 * phase_space
    epsilon_phi *= 1e25  # Conversion to erg/g/s
    
    return epsilon_phi


def compute_neutrino_burst_modification(
    energy_loss_rate: float,
    burst_duration_s: float = 10.0
) -> float:
    """
    Compute modification to neutrino burst duration from scalar energy loss.
    
    Args:
        energy_loss_rate: Scalar emission rate ε_φ (erg/g/s)
        burst_duration_s: Standard burst duration (s), default 10
        
    Returns:
        Fractional duration reduction Δt/t
    """
    # Rough estimate: energy loss shortens burst
    # Typical supernova energy: E_sn ~ 10⁵³ erg
    E_sn_erg = 1e53
    M_sn_g = 1.4e33  # Solar mass
    
    # Total scalar energy loss
    E_scalar = energy_loss_rate * M_sn_g * burst_duration_s
    
    # Fractional energy loss
    delta_E_E = E_scalar / E_sn_erg if E_sn_erg > 0 else 0.0
    
    # Duration reduction (roughly proportional)
    delta_t_t = delta_E_E
    
    return delta_t_t


def compute_g_phi_nu_from_theta(theta_hc: float) -> float:
    """
    Map ToE mixing angle to scalar-neutrino coupling.
    
    Args:
        theta_hc: Mixing angle θ_hc
        
    Returns:
        Scalar-neutrino coupling g_φν
    """
    # Rough estimate: g_φν ≈ θ_hc × (neutrino Yukawa)
    y_nu = 1e-12  # Neutrino Yukawa (very small)
    g_phi_nu = abs(theta_hc) * y_nu
    return g_phi_nu


def compute_coupling_bound_from_burst_duration(
    observed_duration_s: float,
    predicted_duration_s: float,
    m_c_GeV: float,
    T_sn_MeV: float = 30.0,
    rho_sn_g_cm3: float = 1e14
) -> float:
    """
    Inverse mapping: burst duration limit → maximum allowed coupling.
    
    Args:
        observed_duration_s: Observed neutrino burst duration (s)
        predicted_duration_s: Predicted duration without scalars (s)
        m_c_GeV: Scalar field mass m_c (GeV)
        T_sn_MeV: Supernova temperature (MeV)
        rho_sn_g_cm3: Supernova density (g/cm³)
        
    Returns:
        Maximum allowed g_φν
    """
    if observed_duration_s <= 0 or predicted_duration_s <= 0:
        return float('inf')
    
    # Duration reduction
    delta_t_t = (predicted_duration_s - observed_duration_s) / predicted_duration_s
    
    if delta_t_t <= 0:
        return float('inf')
    
    m_c_MeV = m_c_GeV * 1000.0
    if m_c_MeV >= T_sn_MeV:
        return float('inf')
    
    phase_space = (1.0 - (m_c_MeV / T_sn_MeV) ** 2) ** (3.0 / 2.0)
    if phase_space <= 0:
        return float('inf')
    
    # Invert: delta_t_t ≈ (g_φν²) × (T⁴ / ρ) × phase_space × conversion
    g_phi_nu_sq = delta_t_t * rho_sn_g_cm3 / (T_sn_MeV ** 4 * phase_space)
    g_phi_nu_sq /= 1e25  # Conversion factor
    
    return math.sqrt(abs(g_phi_nu_sq))


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c_GeV: float,
    T_sn_MeV: float = 30.0,
    rho_sn_g_cm3: float = 1e14,
    m_h: float = 125.0
) -> Tuple[float, float, float]:
    """
    Forward mapping: ToE parameters → energy loss, burst mod, g_φν.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c_GeV: Scalar field mass m_c (GeV)
        T_sn_MeV: Supernova temperature (MeV)
        rho_sn_g_cm3: Supernova density (g/cm³)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (energy_loss, delta_t_t, g_phi_nu)
    """
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    g_phi_nu = compute_g_phi_nu_from_theta(theta_hc)
    energy_loss = compute_scalar_energy_loss(m_c_GeV, g_phi_nu, T_sn_MeV, rho_sn_g_cm3)
    delta_t_t = compute_neutrino_burst_modification(energy_loss)
    return energy_loss, delta_t_t, g_phi_nu


def inverse_mapping(
    duration_limit_s: float,
    m_c_GeV: float,
    T_sn_MeV: float = 30.0,
    rho_sn_g_cm3: float = 1e14,
    v_c: float = 246.0,
    m_h: float = 125.0
) -> Tuple[float, float]:
    """
    Inverse mapping: duration limit → bounds on ToE parameters.
    
    Args:
        duration_limit_s: Minimum allowed burst duration (s)
        m_c_GeV: Scalar field mass m_c (GeV)
        T_sn_MeV: Supernova temperature (MeV)
        rho_sn_g_cm3: Supernova density (g/cm³)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    predicted_duration = 10.0  # Standard SN burst duration
    g_phi_nu_max = compute_coupling_bound_from_burst_duration(
        duration_limit_s, predicted_duration, m_c_GeV, T_sn_MeV, rho_sn_g_cm3
    )
    
    if g_phi_nu_max == float('inf'):
        return float('inf'), float('inf')
    
    # Convert g_φν back to θ_hc
    y_nu = 1e-12
    theta_max = g_phi_nu_max / y_nu if y_nu > 0 else float('inf')
    kappa_vc_max = abs(theta_max) * (m_h ** 2) if theta_max != float('inf') else float('inf')
    
    return theta_max, kappa_vc_max
