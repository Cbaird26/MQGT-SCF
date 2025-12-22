"""
MQGT-SCF / UTQOL Simulation Package
Canonical implementation for field dynamics and experimental predictions
"""

import numpy as np
import scipy.integrate as integrate
from scipy.special import erf
from typing import Tuple, Callable, Optional
import matplotlib.pyplot as plt

class MQGT_SCF_Simulator:
    """
    Simulator for MQGT-SCF field dynamics.
    Supports both Canon-A (minimal) and Canon-B (UTQOL) variants.
    """
    
    def __init__(self, variant: str = 'A', **params):
        """
        Initialize simulator.
        
        Parameters:
        -----------
        variant : str
            'A' for Canon-A (minimal), 'B' for Canon-B (UTQOL)
        params : dict
            Field parameters (masses, couplings, etc.)
        """
        self.variant = variant
        self.params = self._set_default_params(**params)
        
    def _set_default_params(self, **kwargs):
        """Set default parameters with user overrides."""
        defaults = {
            # Canon-A parameters
            'm_c': 1e-4,  # Consciousness field mass (eV)
            'm_E': 1e-4,  # Ethics field mass (eV)
            'lambda_c': 0.1,  # Self-coupling Φc
            'lambda_E': 0.1,  # Self-coupling E
            'lambda_int': 1e-6,  # Interaction coupling
            'eta': 1e-6,  # Ethics-collapse coupling
            
            # Canon-B additional parameters
            'm_omega': 1e-4,  # Oversoul mass (eV)
            'lambda_omega': 0.1,  # Oversoul self-coupling
            'alpha': 1e-6,  # Φc²E² coupling
            'beta': 1e-6,  # ΦcΨω coupling
            'gamma': 1e-6,  # EΨω coupling
            'kappa': 1e-6,  # Nonlocal kernel strength
            'ell_K': 1.0,  # Kernel coherence length (natural units)
            'epsilon': 1e-60,  # Teleology coupling
            
            # Numerical parameters
            'dt': 0.01,  # Time step
            'dx': 0.1,  # Spatial step
            'N': 100,  # Grid points
        }
        defaults.update(kwargs)
        return defaults
    
    def potential_phi_c(self, phi_c: np.ndarray) -> np.ndarray:
        """Potential V(Φc)."""
        m_c = self.params['m_c']
        lambda_c = self.params['lambda_c']
        return 0.5 * m_c**2 * phi_c**2 + 0.25 * lambda_c * phi_c**4
    
    def potential_E(self, E: np.ndarray) -> np.ndarray:
        """Potential V(E)."""
        m_E = self.params['m_E']
        lambda_E = self.params['lambda_E']
        return 0.5 * m_E**2 * E**2 + 0.25 * lambda_E * E**4
    
    def potential_omega(self, psi_omega: np.ndarray) -> np.ndarray:
        """Potential V_ω(|Ψω|²)."""
        m_omega = self.params['m_omega']
        lambda_omega = self.params['lambda_omega']
        psi_sq = np.abs(psi_omega)**2
        return 0.5 * m_omega**2 * psi_sq + 0.25 * lambda_omega * psi_sq**2
    
    def kernel_gaussian(self, x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
        """
        Gaussian kernel: K(x,x') = exp(-d²/2ℓ_K²)
        
        Parameters:
        -----------
        x1, x2 : array-like
            Spacetime coordinates
            
        Returns:
        --------
        K : array
            Kernel values
        """
        ell_K = self.params['ell_K']
        d_sq = np.sum((x1 - x2)**2, axis=-1)
        return np.exp(-d_sq / (2 * ell_K**2))
    
    def kernel_yukawa(self, x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
        """Yukawa kernel: K(x,x') = exp(-m_K d) / d"""
        m_K = self.params.get('m_K', 1.0)
        d = np.sqrt(np.sum((x1 - x2)**2, axis=-1))
        d = np.where(d > 1e-10, d, 1e-10)  # Avoid division by zero
        return np.exp(-m_K * d) / d
    
    def field_equations_canon_A(self, t: float, y: np.ndarray, 
                                x_grid: np.ndarray) -> np.ndarray:
        """
        Field equations for Canon-A.
        
        Returns time derivatives of (Φc, ∂Φc/∂t, E, ∂E/∂t)
        """
        N = len(x_grid)
        phi_c = y[:N]
        dphi_c_dt = y[N:2*N]
        E = y[2*N:3*N]
        dE_dt = y[3*N:]
        
        # Laplacian (1D for simplicity, extendable to 3D)
        dx = x_grid[1] - x_grid[0]
        laplacian_phi = np.gradient(np.gradient(phi_c, dx), dx)
        laplacian_E = np.gradient(np.gradient(E, dx), dx)
        
        # Potential derivatives
        dV_dphi = self.params['m_c']**2 * phi_c + self.params['lambda_c'] * phi_c**3
        dV_dE = self.params['m_E']**2 * E + self.params['lambda_E'] * E**3
        
        # Interaction terms
        lambda_int = self.params['lambda_int']
        
        # Equations of motion
        d2phi_dt2 = laplacian_phi - dV_dphi - lambda_int * E
        d2E_dt2 = laplacian_E - dV_dE - lambda_int * phi_c
        
        return np.concatenate([dphi_c_dt, d2phi_dt2, dE_dt, d2E_dt2])
    
    def ethically_weighted_born_rule(self, amplitudes: np.ndarray, 
                                     E_values: np.ndarray) -> np.ndarray:
        """
        Ethically weighted Born rule: P(i) ∝ |c_i|² exp(η E_i)
        
        Parameters:
        -----------
        amplitudes : array
            Quantum amplitudes |c_i|²
        E_values : array
            Ethical values E_i for each outcome
            
        Returns:
        --------
        probabilities : array
            Modified probabilities
        """
        eta = self.params['eta']
        unnormalized = amplitudes * np.exp(eta * E_values)
        return unnormalized / np.sum(unnormalized)
    
    def qrng_forward_model(self, N_trials: int, E_0: float, E_1: float) -> dict:
        """
        Forward model for QRNG experiment (Channel 1).
        
        Parameters:
        -----------
        N_trials : int
            Number of trials
        E_0, E_1 : float
            Ethical labels for outcomes 0 and 1
            
        Returns:
        --------
        result : dict
            Contains counts, test statistic, etc.
        """
        eta = self.params['eta']
        
        # Standard quantum probabilities (equal for QRNG)
        P_0_standard = 0.5
        P_1_standard = 0.5
        
        # Ethically weighted probabilities
        amplitudes = np.array([P_0_standard, P_1_standard])
        E_values = np.array([E_0, E_1])
        probs = self.ethically_weighted_born_rule(amplitudes, E_values)
        
        # Simulate trials
        outcomes = np.random.binomial(1, probs[1], N_trials)
        N_1 = np.sum(outcomes)
        N_0 = N_trials - N_1
        
        # Test statistic
        T = np.log(N_1 / N_0) if N_0 > 0 and N_1 > 0 else 0.0
        
        # Expected value
        E_T = eta * (E_1 - E_0)
        
        return {
            'N_0': N_0,
            'N_1': N_1,
            'N_total': N_trials,
            'T': T,
            'E_T': E_T,
            'P_0': probs[0],
            'P_1': probs[1],
            'eta': eta
        }
    
    def higgs_portal_forward_model(self, g_phi: float, theta: float) -> dict:
        """
        Forward model for Higgs portal mixing (Channel 2).
        
        Parameters:
        -----------
        g_phi : float
            Higgs-Φc coupling
        theta : float
            Mixing angle
            
        Returns:
        --------
        result : dict
            Contains invisible width, etc.
        """
        Gamma_SM = 4.07e-3  # Standard Model Higgs width (GeV)
        Gamma_0 = 1e-3  # Reference width
        
        Gamma_inv = Gamma_SM + g_phi**2 * np.sin(theta)**2 * Gamma_0
        
        return {
            'Gamma_inv': Gamma_inv,
            'Gamma_SM': Gamma_SM,
            'Gamma_excess': Gamma_inv - Gamma_SM,
            'g_phi': g_phi,
            'theta': theta
        }
    
    def fifth_force_potential(self, r: np.ndarray, alpha: float, 
                              m_phi: float) -> np.ndarray:
        """
        Fifth-force potential: V(r) = -GMm/r (1 + α exp(-m_φ r))
        
        Parameters:
        -----------
        r : array
            Distances
        alpha : float
            Coupling strength
        m_phi : float
            Scalar mass
            
        Returns:
        --------
        V : array
            Potential values
        """
        G = 6.674e-11  # Gravitational constant (SI)
        M = 1.0  # Test mass (normalized)
        m = 1.0  # Source mass (normalized)
        
        V_newton = -G * M * m / r
        V_yukawa = alpha * np.exp(-m_phi * r)
        
        return V_newton * (1 + V_yukawa)
    
    def solve_field_equations(self, t_span: Tuple[float, float], 
                             initial_conditions: np.ndarray,
                             x_grid: np.ndarray) -> dict:
        """
        Solve field equations numerically.
        
        Parameters:
        -----------
        t_span : tuple
            (t_start, t_end)
        initial_conditions : array
            Initial field values
        x_grid : array
            Spatial grid
            
        Returns:
        --------
        solution : dict
            Contains time evolution, etc.
        """
        def rhs(t, y):
            return self.field_equations_canon_A(t, y, x_grid)
        
        sol = integrate.solve_ivp(rhs, t_span, initial_conditions, 
                                 method='RK45', dense_output=True)
        
        return {
            't': sol.t,
            'y': sol.y,
            'success': sol.success,
            'message': sol.message
        }


# Example usage and testing
if __name__ == '__main__':
    # Initialize simulator (Canon-A)
    sim = MQGT_SCF_Simulator(variant='A', eta=1e-6)
    
    # QRNG experiment simulation
    print("QRNG Forward Model Test:")
    result = sim.qrng_forward_model(N_trials=1000000, E_0=0.0, E_1=1.0)
    print(f"N_0: {result['N_0']}, N_1: {result['N_1']}")
    print(f"Test statistic T: {result['T']:.6f}")
    print(f"Expected T: {result['E_T']:.6f}")
    print(f"Modified probabilities: P_0={result['P_0']:.6f}, P_1={result['P_1']:.6f}")
    
    # Higgs portal test
    print("\nHiggs Portal Forward Model Test:")
    h_result = sim.higgs_portal_forward_model(g_phi=1e-3, theta=0.1)
    print(f"Invisible width: {h_result['Gamma_inv']:.6e} GeV")
    print(f"Excess: {h_result['Gamma_excess']:.6e} GeV")
    
    print("\nSimulation package ready for use.")

