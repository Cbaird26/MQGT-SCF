"""
Multi-Channel Joint Inference Pipeline for MQGT-SCF
Bayesian framework for parameter estimation across all experimental channels
"""

import numpy as np
import scipy.stats as stats
from scipy.optimize import minimize
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
from mqgt_scf_simulation import MQGT_SCF_Simulator

class MQGT_SCF_Inference:
    """
    Bayesian inference engine for MQGT-SCF parameters.
    Supports joint likelihood across multiple experimental channels.
    """
    
    def __init__(self, simulator: MQGT_SCF_Simulator):
        """
        Initialize inference engine.
        
        Parameters:
        -----------
        simulator : MQGT_SCF_Simulator
            Simulator instance for forward models
        """
        self.sim = simulator
        self.channels = []
        self.data = {}
        self.priors = {}
        
    def set_prior(self, param_name: str, prior_type: str, **kwargs):
        """
        Set prior distribution for a parameter.
        
        Parameters:
        -----------
        param_name : str
            Parameter name (e.g., 'eta', 'g_phi')
        prior_type : str
            'normal', 'uniform', 'log_normal'
        kwargs : dict
            Prior parameters (mean, std, bounds, etc.)
        """
        if prior_type == 'normal':
            self.priors[param_name] = {
                'type': 'normal',
                'mean': kwargs.get('mean', 0.0),
                'std': kwargs.get('std', 1.0)
            }
        elif prior_type == 'uniform':
            self.priors[param_name] = {
                'type': 'uniform',
                'low': kwargs.get('low', -np.inf),
                'high': kwargs.get('high', np.inf)
            }
        elif prior_type == 'log_normal':
            self.priors[param_name] = {
                'type': 'log_normal',
                'mean': kwargs.get('mean', 0.0),
                'std': kwargs.get('std', 1.0)
            }
    
    def set_default_priors(self):
        """Set conservative default priors based on theoretical constraints."""
        # Ethics-collapse coupling (very small)
        self.set_prior('eta', 'normal', mean=0.0, std=1e-5)
        
        # Higgs portal coupling (bounded by collider)
        self.set_prior('g_phi', 'uniform', low=0.0, high=1e-2)
        
        # Field masses (bounded by fifth-force tests)
        self.set_prior('m_c', 'log_normal', mean=np.log(1e-4), std=1.0)
        self.set_prior('m_E', 'log_normal', mean=np.log(1e-4), std=1.0)
        
        # Teleology coupling (extremely small)
        self.set_prior('epsilon', 'log_normal', mean=np.log(1e-60), std=10.0)
    
    def add_channel_data(self, channel_name: str, data: Dict):
        """
        Add experimental data for a channel.
        
        Parameters:
        -----------
        channel_name : str
            'qrng', 'higgs', 'fifth_force', 'cosmology'
        data : dict
            Experimental data (counts, measurements, etc.)
        """
        self.data[channel_name] = data
        if channel_name not in self.channels:
            self.channels.append(channel_name)
    
    def likelihood_qrng(self, eta: float, data: Dict) -> float:
        """
        Likelihood for QRNG channel (Channel 1).
        
        Parameters:
        -----------
        eta : float
            Ethics-collapse coupling
        data : dict
            Contains N_0, N_1, E_0, E_1
            
        Returns:
        --------
        log_likelihood : float
        """
        N_0 = data['N_0']
        N_1 = data['N_1']
        E_0 = data.get('E_0', 0.0)
        E_1 = data.get('E_1', 1.0)
        
        # Expected probabilities
        P_0_standard = 0.5
        P_1_standard = 0.5
        
        # Ethically weighted
        amplitudes = np.array([P_0_standard, P_1_standard])
        E_values = np.array([E_0, E_1])
        unnormalized = amplitudes * np.exp(eta * E_values)
        P_1 = unnormalized[1] / np.sum(unnormalized)
        P_0 = 1 - P_1
        
        # Binomial likelihood
        log_likelihood = stats.binom.logpmf(N_1, N_0 + N_1, P_1)
        
        return log_likelihood
    
    def likelihood_higgs(self, g_phi: float, theta: float, data: Dict) -> float:
        """
        Likelihood for Higgs portal channel (Channel 2).
        
        Parameters:
        -----------
        g_phi : float
            Higgs-Φc coupling
        theta : float
            Mixing angle
        data : dict
            Contains observed Gamma_inv, sigma_Gamma
            
        Returns:
        --------
        log_likelihood : float
        """
        Gamma_obs = data['Gamma_inv']
        sigma_Gamma = data.get('sigma_Gamma', 0.1 * Gamma_obs)
        
        # Forward model
        Gamma_SM = 4.07e-3
        Gamma_0 = 1e-3
        Gamma_pred = Gamma_SM + g_phi**2 * np.sin(theta)**2 * Gamma_0
        
        # Gaussian likelihood
        log_likelihood = stats.norm.logpdf(Gamma_obs, loc=Gamma_pred, scale=sigma_Gamma)
        
        return log_likelihood
    
    def likelihood_fifth_force(self, alpha: float, m_phi: float, 
                               data: Dict) -> float:
        """
        Likelihood for fifth-force channel (Channel 3).
        
        Parameters:
        -----------
        alpha : float
            Coupling strength
        m_phi : float
            Scalar mass
        data : dict
            Contains force measurements, distances
            
        Returns:
        --------
        log_likelihood : float
        """
        # Simplified: assume null result gives upper bound
        # More sophisticated: use actual force measurements
        alpha_bound = data.get('alpha_bound', 1e-10)
        m_phi_bound = data.get('m_phi_bound', 1e-4)
        
        # Truncated likelihood (penalize if exceeds bounds)
        if alpha > alpha_bound or m_phi < m_phi_bound:
            return -np.inf
        
        # Flat likelihood within bounds (null result)
        return 0.0
    
    def likelihood_cosmology(self, params: Dict, data: Dict) -> float:
        """
        Likelihood for cosmology channel (Channel 4).
        
        Parameters:
        -----------
        params : dict
            Cosmological parameters
        data : dict
            Contains w(z) measurements, etc.
            
        Returns:
        --------
        log_likelihood : float
        """
        # Simplified: compare predicted w(z) to observations
        # Full implementation would use actual survey data
        w_obs = data.get('w_obs', -1.0)
        sigma_w = data.get('sigma_w', 0.1)
        
        # Placeholder: would compute w(z) from field evolution
        w_pred = -1.0  # Dark energy-like
        
        log_likelihood = stats.norm.logpdf(w_obs, loc=w_pred, scale=sigma_w)
        
        return log_likelihood
    
    def log_prior(self, params: Dict) -> float:
        """
        Compute log-prior for parameters.
        
        Parameters:
        -----------
        params : dict
            Parameter values
            
        Returns:
        --------
        log_prior : float
        """
        log_prior = 0.0
        
        for param_name, value in params.items():
            if param_name not in self.priors:
                continue
            
            prior = self.priors[param_name]
            
            if prior['type'] == 'normal':
                log_prior += stats.norm.logpdf(
                    value, loc=prior['mean'], scale=prior['std']
                )
            elif prior['type'] == 'uniform':
                if value < prior['low'] or value > prior['high']:
                    return -np.inf
                log_prior += 0.0  # Uniform: constant
            elif prior['type'] == 'log_normal':
                if value <= 0:
                    return -np.inf
                log_prior += stats.lognorm.logpdf(
                    value, s=prior['std'], scale=np.exp(prior['mean'])
                )
        
        return log_prior
    
    def log_likelihood(self, params: Dict) -> float:
        """
        Compute joint log-likelihood across all channels.
        
        Parameters:
        -----------
        params : dict
            Parameter values
            
        Returns:
        --------
        log_likelihood : float
        """
        log_likelihood = 0.0
        
        # Channel 1: QRNG
        if 'qrng' in self.channels:
            eta = params.get('eta', 0.0)
            log_likelihood += self.likelihood_qrng(eta, self.data['qrng'])
        
        # Channel 2: Higgs portal
        if 'higgs' in self.channels:
            g_phi = params.get('g_phi', 0.0)
            theta = params.get('theta', 0.0)
            log_likelihood += self.likelihood_higgs(g_phi, theta, self.data['higgs'])
        
        # Channel 3: Fifth force
        if 'fifth_force' in self.channels:
            alpha = params.get('alpha', 0.0)
            m_phi = params.get('m_c', 1e-4)  # Use m_c as proxy
            log_likelihood += self.likelihood_fifth_force(alpha, m_phi, self.data['fifth_force'])
        
        # Channel 4: Cosmology
        if 'cosmology' in self.channels:
            log_likelihood += self.likelihood_cosmology(params, self.data['cosmology'])
        
        return log_likelihood
    
    def log_posterior(self, params: Dict) -> float:
        """
        Compute log-posterior (prior + likelihood).
        
        Parameters:
        -----------
        params : dict
            Parameter values
            
        Returns:
        --------
        log_posterior : float
        """
        log_prior = self.log_prior(params)
        if not np.isfinite(log_prior):
            return -np.inf
        
        log_likelihood = self.log_likelihood(params)
        if not np.isfinite(log_likelihood):
            return -np.inf
        
        return log_prior + log_likelihood
    
    def mcmc_sample(self, n_samples: int = 10000, n_warmup: int = 1000,
                    initial_params: Optional[Dict] = None) -> Dict:
        """
        MCMC sampling of posterior (simplified Metropolis-Hastings).
        
        Parameters:
        -----------
        n_samples : int
            Number of samples
        n_warmup : int
            Warmup samples to discard
        initial_params : dict, optional
            Starting point
            
        Returns:
        --------
        samples : dict
            Parameter samples
        """
        # Simplified implementation
        # Full version would use emcee, pymc3, or similar
        
        if initial_params is None:
            initial_params = {name: prior.get('mean', 0.0) 
                            for name, prior in self.priors.items()}
        
        samples = {name: [] for name in initial_params.keys()}
        current_params = initial_params.copy()
        current_log_post = self.log_posterior(current_params)
        
        # Proposal scale (would be adaptive in real implementation)
        proposal_scale = {name: 0.1 * abs(val) if abs(val) > 0 else 0.01
                          for name, val in initial_params.items()}
        
        accepted = 0
        
        for i in range(n_samples + n_warmup):
            # Propose new parameters
            proposed_params = {}
            for name, value in current_params.items():
                if name in self.priors:
                    scale = proposal_scale.get(name, 0.01)
                    proposed_params[name] = value + np.random.normal(0, scale)
                else:
                    proposed_params[name] = value
            
            # Evaluate posterior
            proposed_log_post = self.log_posterior(proposed_params)
            
            # Metropolis acceptance
            if np.random.rand() < np.exp(proposed_log_post - current_log_post):
                current_params = proposed_params
                current_log_post = proposed_log_post
                accepted += 1
            
            # Store sample (after warmup)
            if i >= n_warmup:
                for name, value in current_params.items():
                    samples[name].append(value)
        
        acceptance_rate = accepted / (n_samples + n_warmup)
        print(f"MCMC acceptance rate: {acceptance_rate:.2%}")
        
        return samples
    
    def compute_credible_intervals(self, samples: Dict, 
                                   confidence: float = 0.95) -> Dict:
        """
        Compute credible intervals from samples.
        
        Parameters:
        -----------
        samples : dict
            Parameter samples
        confidence : float
            Confidence level (e.g., 0.95 for 95% CI)
            
        Returns:
        --------
        intervals : dict
            Lower and upper bounds for each parameter
        """
        alpha = 1 - confidence
        intervals = {}
        
        for name, values in samples.items():
            lower = np.percentile(values, 100 * alpha / 2)
            upper = np.percentile(values, 100 * (1 - alpha / 2))
            median = np.median(values)
            
            intervals[name] = {
                'median': median,
                'lower': lower,
                'upper': upper,
                'confidence': confidence
            }
        
        return intervals


# Example usage
if __name__ == '__main__':
    # Initialize
    sim = MQGT_SCF_Simulator(variant='A')
    inference = MQGT_SCF_Inference(sim)
    inference.set_default_priors()
    
    # Add simulated QRNG data
    qrng_result = sim.qrng_forward_model(N_trials=1000000, E_0=0.0, E_1=1.0)
    inference.add_channel_data('qrng', {
        'N_0': qrng_result['N_0'],
        'N_1': qrng_result['N_1'],
        'E_0': 0.0,
        'E_1': 1.0
    })
    
    # Add Higgs portal data (null result)
    inference.add_channel_data('higgs', {
        'Gamma_inv': 4.07e-3,  # Standard Model value
        'sigma_Gamma': 0.1e-3
    })
    
    # Run MCMC
    print("Running MCMC...")
    samples = inference.mcmc_sample(n_samples=5000, n_warmup=500)
    
    # Compute credible intervals
    intervals = inference.compute_credible_intervals(samples)
    
    print("\n95% Credible Intervals:")
    for name, interval in intervals.items():
        print(f"{name}: {interval['median']:.6e} "
              f"[{interval['lower']:.6e}, {interval['upper']:.6e}]")
    
    print("\nInference pipeline ready for use.")

