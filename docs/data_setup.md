# Data Setup Guide

This guide explains how to set up the digitized experimental constraints required for full reproduction of MQGT-SCF results.

## Overview

The MQGT-SCF inference harness uses digitized experimental constraints from published experimental results:

- **Fifth-force constraints**: Digitized from Lee et al. (2020) ISL test figure
- **Higgs invisible decay**: Digitized from CMS HIG-20-003 public results
- **Cosmology constraints**: Correlated Gaussian (w0, wa) from digitized contour

## Required Files

The following files should be present in `data/processed/`:

1. **`constraints.py`** - Main constraints module with interpolation functions
2. **`fifth_force_alpha_lambda_envelope.csv`** - Fifth-force exclusion envelope
3. **`cms_hinv_profilelik_digitized_unique.csv`** - CMS Higgs invisible profile likelihood
4. **`cosmo_cov_w0_wa.json`** - Cosmology covariance matrix (if using cosmology channel)

## Setup Options

### Option A: Use Existing Data (If Available)

If the repository includes these files in `data/processed/`, no setup is needed. The reproduction script will use them automatically.

### Option B: Generate from Sources

If you need to regenerate the digitized data:

1. **Fifth-force envelope**: Digitize from Lee et al. (2020) Figure 5 (bottom panel)
   - Source: ar5iv:2002.11761
   - Format: CSV with columns `lambda_m`, `alpha_limit_env`

2. **CMS Higgs invisible**: Digitize from CMS HIG-20-003 Figure 12
   - Format: CSV with columns `B`, `q` (profile likelihood)

3. **Cosmology**: Extract from published (w0, wa) contour
   - Format: JSON with covariance matrix

### Option C: Minimal Reproduction (QRNG Only)

For testing core functionality without full data setup:

- QRNG tests work independently (no digitized data required)
- Use `code/inference/mqgt_qrng_harness.py` directly
- Full joint inference requires digitized constraints

## Verification

Check that data is set up correctly:

```bash
# Check for required files
ls data/processed/constraints.py
ls data/processed/*.csv
ls data/processed/*.json  # if using cosmology

# Test import
python -c "import sys; sys.path.insert(0, 'data/processed'); from constraints import alpha_limit; print('OK')"
```

## Expected File Structure

```
data/
└── processed/
    ├── constraints.py
    ├── fifth_force_alpha_lambda_envelope.csv
    ├── cms_hinv_profilelik_digitized_unique.csv
    └── cosmo_cov_w0_wa.json  # optional
```

## Troubleshooting

**Error: "ModuleNotFoundError: No module named 'digitized'"**

- This means `data/processed/constraints.py` is not accessible
- Ensure the file exists and is in the correct location
- The reproduction script will degrade gracefully if data is missing

**Error: "Missing CSV files"**

- Ensure all required CSV files are in `data/processed/`
- Check file names match exactly (case-sensitive)

## Notes

- Digitized data is derived from published experimental results
- For exact reproduction, use the same digitization method as the original paper
- See paper supplementary materials for digitization details

