"""
Higgs Invisible Decay Channel for MQGT-SCF

Maps ToE parameters to Higgs invisible decay branching ratio and generates bounds
from LHC experimental limits.

References:
- ATLAS: BR(H → invisible) < 0.15 (95% CL)
- CMS: BR(H → invisible) < 0.19 (95% CL)
"""

import math
from typing import Tuple, Optional


# Physical constants
M_H = 125.0  # GeV, Higgs mass
GAMMA_H_SM = 4.07e-3  # GeV, Standard Model Higgs width


def compute_theta_hc(kappa_ch: float, v_c: float, m_h: float = M_H) -> float:
    """
    Compute Higgs-portal mixing angle θ_hc from ToE parameters.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Mixing angle θ_hc (dimensionless)
    """
    if abs(v_c) < 1e-10:
        return 0.0
    
    # Small-angle approximation: θ_hc ≈ -κ_cH v_c / m_h²
    theta_hc = -kappa_ch * v_c / (m_h ** 2)
    return theta_hc


def compute_br_invisible_onshell(theta_hc: float, m_c: float, m_h: float = M_H) -> float:
    """
    Compute branching ratio BR(H → Φ_c Φ_c) for on-shell decay.
    
    Valid for m_c < m_h/2.
    
    Args:
        theta_hc: Mixing angle θ_hc
        m_c: Scalar field mass m_c (GeV)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Branching ratio (0 to 1)
    """
    if m_c >= m_h / 2.0:
        # Off-shell decay, use approximate formula
        return compute_br_invisible_offshell(theta_hc, m_c, m_h)
    
    # Phase space factor for H → Φ_c Φ_c
    beta = math.sqrt(1.0 - (4.0 * m_c ** 2) / (m_h ** 2))
    
    # Decay width: Γ(H → Φ_c Φ_c) = (θ_hc² m_h³) / (32π) × phase_space
    # Normalized by total width
    gamma_invisible = (theta_hc ** 2) * (m_h ** 3) / (32.0 * math.pi) * beta
    gamma_total = GAMMA_H_SM + gamma_invisible
    
    br = gamma_invisible / gamma_total if gamma_total > 0 else 0.0
    return min(br, 1.0)  # Clamp to [0, 1]


def compute_br_invisible_offshell(theta_hc: float, m_c: float, m_h: float = M_H) -> float:
    """
    Compute branching ratio for off-shell decay (m_c > m_h/2).
    
    Uses effective field theory approximation.
    
    Args:
        theta_hc: Mixing angle θ_hc
        m_c: Scalar field mass m_c (GeV)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Branching ratio (0 to 1)
    """
    # Off-shell contribution is suppressed by (m_h/m_c)⁴
    suppression = (m_h / m_c) ** 4 if m_c > m_h else 1.0
    
    # Approximate: BR ≈ (θ_hc² / suppression) × small_factor
    br_approx = (theta_hc ** 2) * suppression * 1e-3  # Rough estimate
    return min(br_approx, 1.0)


def compute_br_invisible(theta_hc: float, m_c: float, m_h: float = M_H) -> float:
    """
    Compute total invisible branching ratio.
    
    Args:
        theta_hc: Mixing angle θ_hc
        m_c: Scalar field mass m_c (GeV)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Branching ratio (0 to 1)
    """
    if m_c < m_h / 2.0:
        return compute_br_invisible_onshell(theta_hc, m_c, m_h)
    else:
        return compute_br_invisible_offshell(theta_hc, m_c, m_h)


def compute_theta_max_from_br_limit(br_limit: float, m_c: float, m_h: float = M_H) -> float:
    """
    Inverse mapping: experimental BR limit → maximum allowed θ_hc.
    
    Args:
        br_limit: Experimental upper limit on BR(H → invisible)
        m_c: Scalar field mass m_c (GeV)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Maximum allowed |θ_hc|
    """
    if br_limit <= 0 or br_limit >= 1:
        return float('inf')
    
    if m_c < m_h / 2.0:
        # On-shell: invert the on-shell formula
        beta = math.sqrt(1.0 - (4.0 * m_c ** 2) / (m_h ** 2))
        if beta <= 0:
            return float('inf')
        
        # Solve: br_limit = gamma_invisible / (gamma_SM + gamma_invisible)
        # gamma_invisible = (theta² m_h³) / (32π) × beta
        # This gives: theta² = (br_limit × gamma_SM) / ((1 - br_limit) × m_h³ / (32π) × beta)
        denominator = (1.0 - br_limit) * (m_h ** 3) / (32.0 * math.pi) * beta
        if denominator <= 0:
            return float('inf')
        
        theta_sq = (br_limit * GAMMA_H_SM) / denominator
        return math.sqrt(abs(theta_sq))
    else:
        # Off-shell: approximate inversion
        suppression = (m_h / m_c) ** 4 if m_c > m_h else 1.0
        theta_sq = br_limit / (suppression * 1e-3)
        return math.sqrt(abs(theta_sq))


def compute_kappa_vc_max_from_br_limit(
    br_limit: float, 
    m_c: float, 
    v_c: float = 246.0,
    m_h: float = M_H
) -> float:
    """
    Compute maximum allowed |κ_cH v_c| from BR limit.
    
    Args:
        br_limit: Experimental upper limit on BR(H → invisible)
        m_c: Scalar field mass m_c (GeV)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Maximum allowed |κ_cH v_c| (GeV)
    """
    theta_max = compute_theta_max_from_br_limit(br_limit, m_c, m_h)
    if theta_max == float('inf'):
        return float('inf')
    
    # From θ_hc ≈ -κ_cH v_c / m_h², we get |κ_cH v_c| = |θ_hc| m_h²
    kappa_vc_max = abs(theta_max) * (m_h ** 2)
    return kappa_vc_max


def forward_mapping(
    kappa_ch: float,
    v_c: float,
    m_c: float,
    m_h: float = M_H
) -> Tuple[float, float]:
    """
    Forward mapping: ToE parameters → BR(H → invisible), θ_hc.
    
    Args:
        kappa_ch: Coupling constant κ_cH
        v_c: Scalar field VEV v_c (GeV)
        m_c: Scalar field mass m_c (GeV)
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (BR_invisible, theta_hc)
    """
    theta_hc = compute_theta_hc(kappa_ch, v_c, m_h)
    br_invisible = compute_br_invisible(theta_hc, m_c, m_h)
    return br_invisible, theta_hc


def inverse_mapping(
    br_limit: float,
    m_c: float,
    v_c: float = 246.0,
    m_h: float = M_H
) -> Tuple[float, float]:
    """
    Inverse mapping: BR limit → bounds on ToE parameters.
    
    Args:
        br_limit: Experimental upper limit on BR(H → invisible)
        m_c: Scalar field mass m_c (GeV)
        v_c: Scalar field VEV v_c (GeV), default 246.0
        m_h: Higgs mass (GeV), default 125.0
        
    Returns:
        Tuple of (theta_max, kappa_vc_max)
    """
    theta_max = compute_theta_max_from_br_limit(br_limit, m_c, m_h)
    kappa_vc_max = compute_kappa_vc_max_from_br_limit(br_limit, m_c, v_c, m_h)
    return theta_max, kappa_vc_max
