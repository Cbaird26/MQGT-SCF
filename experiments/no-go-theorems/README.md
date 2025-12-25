# No-Go Theorems Simulation Module

This directory contains the simulation code and results for the no-go theorems paper.

## Files

- `configs.py` - Simulation configuration (intuitive and normalized scaling)
- `theorem4_policy_continuity.py` - Main simulation script
- `plot_results.py` - Plotting script for results
- `THEOREM5_no_ethical_demon.md` - Theorem 5 documentation

## Running Simulations

```bash
# Generate CSV results
python theorem4_policy_continuity.py

# Generate plots
python plot_results.py
```

## Output Files

**CSVs:**
- `results_intuitive.csv` - Results with intuitive scaling
- `results_normalized.csv` - Results with normalized scaling

**PNGs (6 plots):**
- `Intuitive_Scaling_PCI.png`
- `Intuitive_Scaling_gross_advantage.png`
- `Intuitive_Scaling_net_work.png`
- `Normalized_Scaling_PCI.png`
- `Normalized_Scaling_gross_advantage.png`
- `Normalized_Scaling_net_work.png`

## Dependencies

- numpy
- matplotlib
- csv (standard library)

## Reproducibility

All results are deterministic given the seed offsets in the code. See the paper for full reproducibility manifest.

