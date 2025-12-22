# Inference Code

This directory contains the Bayesian inference harnesses for multi-channel analysis.

## Files

- `mqgt_qrng_harness.py`: QRNG channel inference
- `mqgt_joint_harness.py`: Joint multi-channel inference
- `mqgt_manifest_sign.py`: Manifest signing and verification
- `mqgt_prereg_pack.py`: Pre-registration utilities
- `constraints.py`: Likelihood functions for all channels

## Usage

### QRNG Channel Only

```bash
python mqgt_qrng_harness.py run --qrng_N1 5000123 --qrng_N0 4999877 --out ../../data/processed/runs/qrng_run/
```

### Joint Multi-Channel

```bash
python mqgt_joint_harness.py run --config joint_config_template.json --out ../../data/processed/runs/joint_run/
```

### Verify Results

```bash
python mqgt_manifest_sign.py --verify --run-dir ../../data/processed/runs/joint_run/
```

## Configuration

See `joint_config_template.json` for configuration options:
- Priors
- Sampling parameters
- Channel selection
- Output options

## Dependencies

See `../../requirements.txt` for full list. Key dependencies:
- numpy
- scipy
- pandas
- matplotlib

