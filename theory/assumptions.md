# Theoretical Assumptions

This document explicitly lists all theoretical assumptions underlying the MQGT-SCF framework.

## Core Assumptions

### 1. Effective Field Theory Framework
- **Assumption**: The Standard Model and General Relativity are valid effective field theories at accessible energy scales.
- **Justification**: Empirical success of SM and GR.
- **Decoupling Limit**: New fields decouple as couplings → 0.

### 2. Ethically-Weighted Born Rule
- **Assumption**: Quantum measurement probabilities can be modified by a scalar label $E_i$:
  $$P(i) = \frac{|c_i|^2 e^{\eta E_i}}{\sum_j |c_j|^2 e^{\eta E_j}}$$
- **Justification**: Operational deformation, testable.
- **Limits**: Standard Born rule recovered for $\eta \to 0$.

### 3. Higgs Portal Coupling
- **Assumption**: Real scalar $S$ couples via $\mathcal{L}_{\mathrm{portal}} = -g_\phi S^2 H^\dagger H$.
- **Justification**: Standard portal construction, renormalizable.
- **Constraints**: Must satisfy collider bounds.

### 4. Locality
- **Assumption**: All interactions are local (no superluminal signaling).
- **Justification**: Consistency with special relativity.

### 5. Small Parameter Regime
- **Assumption**: $\eta \ll 1$, $g_\phi \ll 1$ (perturbative regime).
- **Justification**: Empirical bounds require small couplings.

## Statistical Assumptions

### 1. Priors
- **Uniform prior** on $g_\phi \in [0, 0.01]$
- **Conservative bounds** on $\eta$ and $m_S$ (see config files)

### 2. Likelihood Approximations
- **CMS likelihood**: Asymmetric Gaussian approximation to profile likelihood
- **Fifth-force**: Exclusion-based likelihood from digitized envelope
- **QRNG**: Binomial likelihood (exact)

### 3. Sampling
- **MCMC method**: Metropolis-Hastings
- **Convergence**: Assessed via effective sample size and trace plots

## Experimental Assumptions

### 1. Digitized Data
- CMS HIG-20-003: Profile likelihood approximated as asymmetric Gaussian
- Lee et al. (2020): Exclusion envelope digitized from published figure

### 2. Systematic Uncertainties
- Assumed negligible compared to statistical uncertainties
- See original experimental papers for full systematics

## Dependencies

Each assumption depends on:
- **Theory**: Lagrangian structure, field content
- **Statistics**: Prior choices, likelihood forms
- **Experiment**: Published constraints, digitization methods

See individual files in `theory/` for detailed derivations.

