# Data Directory

This directory contains all experimental data and processed constraints used in the analysis.

## Structure

```
data/
├── raw/              # Original data sources (if available)
└── processed/        # Digitized constraints and run outputs
    ├── cms_hig_20_003.json
    ├── lee_2020_isl.json
    └── runs/         # Inference run outputs
```

## Data Sources

### CMS HIG-20-003
- **Source**: CMS Collaboration, HIG-20-003
- **Content**: Invisible Higgs decay limits
- **Format**: JSON with profile likelihood approximation
- **Digitization**: Asymmetric Gaussian approximation to published profile likelihood
- **File**: `processed/cms_hig_20_003.json`

### Lee et al. (2020)
- **Source**: Lee et al., Phys. Rev. Lett. 124, 101101 (2020)
- **Content**: Short-range gravity exclusion envelope
- **Format**: JSON with $\alpha_{\max}(\lambda)$ curve
- **Digitization**: Exclusion envelope digitized from published figure
- **File**: `processed/lee_2020_isl.json`

## Run Outputs

Inference run outputs are stored in `processed/runs/run_YYYY-MM-DD/`:
- `joint_samples.csv`: MCMC parameter samples
- `joint_summary.json`: Summary statistics
- `manifest.json`: Cryptographic manifest
- `receipt.json`: Attestation receipt
- `plots/`: Diagnostic plots

## Usage

To use digitized constraints in your analysis:
```python
import json

with open('data/processed/cms_hig_20_003.json') as f:
    cms_data = json.load(f)
```

## Citation

When using this data, please cite the original experimental papers:
- CMS Collaboration, HIG-20-003
- Lee et al., Phys. Rev. Lett. 124, 101101 (2020)

