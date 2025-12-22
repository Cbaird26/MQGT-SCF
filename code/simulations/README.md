# Simulation Code

This directory contains field dynamics simulations for MQGT-SCF.

## Files

- `mqgt_simulation.py`: Original simulation code
- `mqgt_scf_simulation.py`: Enhanced simulator with Canon-A/B support
- `mqgt_scf_inference.py`: Bayesian inference for simulations

## Usage

```python
from mqgt_scf_simulation import MQGT_SCF_Simulator

# Initialize
sim = MQGT_SCF_Simulator(variant='A', eta=1e-6)

# Run QRNG forward model
result = sim.qrng_forward_model(N_trials=1000000, E_0=0.0, E_1=1.0)
print(f"Test statistic: {result['T']:.6f}")
```

## Theory

See `../../theory/` for theoretical background and assumptions.

