# MQGT-SCF: Merged Quantum Gauge and Scalar Consciousness Framework

**Operational Constraints on Ethically-Weighted Quantum Measurement: A Multi-Channel Effective Field Theory Analysis**

[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![Zenodo](https://zenodo.org/badge/DOI/XXXX.XXXXX.svg)](https://doi.org/XXXX.XXXXX)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Abstract

We investigate a class of effective modifications to quantum measurement in which outcome probabilities are weakly biased by an auxiliary scalar label that encodes "ethical" or valence-like structure. We formulate the proposal in an explicitly operational way, and embed it within a conservative effective field theory (EFT) extension of the Standard Model and General Relativity that admits a clean decoupling limit. We derive likelihood-level predictions for three experimentally independent channels: (i) quantum random number generators (QRNGs), (ii) invisible Higgs decays via a Higgs-portal coupling, and (iii) short-range tests of Newtonian gravity parameterized by Yukawa deviations.

## Repository Structure

```
MQGT-SCF/
├── paper/              # Main manuscript and supplement
├── theory/             # Theoretical derivations and assumptions
├── code/               # All computational code
│   ├── inference/      # Bayesian inference harnesses
│   └── simulations/    # Field dynamics simulations
├── data/               # Experimental data and constraints
│   ├── raw/           # Original data sources
│   └── processed/     # Digitized constraints
├── figures/            # All publication figures
├── notebooks/          # Reproducibility notebooks
└── README.md          # This file
```

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Cbaird26/MQGT-SCF.git
cd MQGT-SCF

# Create conda environment
conda env create -f environment.yml
conda activate mqgt-scf

# Or use pip
pip install -r requirements.txt
```

### Reproducing Results

**Reproduce main inference:**
```bash
cd code/inference
python mqgt_joint_harness.py run --config joint_config_template.json --out ../../data/processed/runs/
```

**Reproduce figures:**
```bash
# See notebooks/ for step-by-step figure reproduction
jupyter notebook notebooks/reproduce_fig2.ipynb
```

**Verify integrity:**
```bash
cd code/inference
python mqgt_manifest_sign.py --verify --run-dir ../../data/processed/runs/run_YYYY-MM-DD/
```

## Documentation

- **Theory**: See `theory/` for derivations and assumptions
- **Code**: See `code/` README files for implementation details
- **Reproducibility**: See `notebooks/` for step-by-step guides
- **Data**: See `data/README.md` for data sources and processing

## Citation

If you use this work, please cite:

```bibtex
@article{baird2025mqgt,
  title={Operational Constraints on Ethically-Weighted Quantum Measurement: A Multi-Channel Effective Field Theory Analysis},
  author={Baird, Christopher Michael},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025},
  doi={10.5281/zenodo.XXXXXXX}
}
```

## Computational Assistance Disclosure

Computational assistance (including large language models) was used for code refactoring, documentation, and verification of algebraic consistency. All theoretical assumptions, model structure, and interpretive claims are the author's own and independently verifiable through the provided derivations and code.

## License

This work is licensed under CC-BY-4.0. See LICENSE file for details.

## Contact

For questions about reproducibility or the code, please open an issue or contact the author.

