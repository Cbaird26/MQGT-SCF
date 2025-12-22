# MQGT-SCF: Merged Quantum Gauge and Scalar Consciousness Framework

**Operational Constraints on Ethically-Weighted Quantum Measurement: A Multi-Channel Effective Field Theory Analysis**

[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.18012506.svg)](https://doi.org/10.5281/zenodo.18012506)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Canonical Citation:** DOI [10.5281/zenodo.18012506](https://zenodo.org/records/18012506)  
**Read the Paper:** [paper.md](paper.md) (full text) | [PDF Download](https://github.com/Cbaird26/MQGT-SCF/raw/main/paper/MQGT_paper_main_v2.pdf)  
**Reproduce Results:** `python reproduce_all.py` (one command)

## Abstract

We investigate a class of effective modifications to quantum measurement in which outcome probabilities are weakly biased by an auxiliary scalar label that encodes "ethical" or valence-like structure. We formulate the proposal in an explicitly operational way, and embed it within a conservative effective field theory (EFT) extension of the Standard Model and General Relativity that admits a clean decoupling limit. We derive likelihood-level predictions for three experimentally independent channels: (i) quantum random number generators (QRNGs), (ii) invisible Higgs decays via a Higgs-portal coupling, and (iii) short-range tests of Newtonian gravity parameterized by Yukawa deviations.

## 🔍 HOW TO ACCESS ALL FILES (For Reviewers)

**⚠️ IMPORTANT: GitHub doesn't render PDFs inline. You must download them using the links below or click "Download" on any PDF file.**

### Direct Download Links to Key Files:

**📄 Main Paper (Operational MQGT-SCF):**
- **[Download Main Paper PDF (665 KB)](https://github.com/Cbaird26/MQGT-SCF/raw/main/paper/MQGT_paper_main_v2.pdf)** - Operational constraints paper
- **[Download Supplement PDF (159 KB)](https://github.com/Cbaird26/MQGT-SCF/raw/main/paper/MQGT_paper_supplement_v2.pdf)** - Supplementary material
- **[View LaTeX Source](https://github.com/Cbaird26/MQGT-SCF/blob/main/paper/main.tex)** - Complete LaTeX source code

**📚 Complete Theory of Everything Papers (Full Theoretical Foundation):**
- **[ToE + Experiment (24 MB, 4,800+ pages)](https://github.com/Cbaird26/MQGT-SCF/raw/main/theory/ToE_papers/A%20Theory%20of%20Everything%20%2B%20Experiment%20-%20Baird.%2C%20Et%20al%20(2025).pdf)** - Complete theory with experimental proposals
- **[ToE - Baird et al (48 MB)](https://github.com/Cbaird26/MQGT-SCF/raw/main/theory/ToE_papers/A%20Theory%20of%20Everything%20-%20Baird%2C%20et%20al%20(2025).pdf)** - Core theoretical framework
- **[ToE - C.M. Baird (24 MB, 4,824 pages)](https://github.com/Cbaird26/MQGT-SCF/raw/main/theory/ToE_papers/A%20Theory%20of%20Everything%20-%20C.M.%20Baird.%2C%20Et%20al%20(2025).pdf)** - Complete 2025 version with full derivations

**💻 Code and Data:**
- **[All Inference Code](https://github.com/Cbaird26/MQGT-SCF/tree/main/code/inference)** - Bayesian inference harnesses
- **[Simulation Code](https://github.com/Cbaird26/MQGT-SCF/tree/main/code/simulations)** - Field dynamics simulations
- **[Digitized Experimental Data](https://github.com/Cbaird26/MQGT-SCF/tree/main/data/processed)** - CMS, fifth-force constraints

**📊 Figures:**
- **[All Publication Figures](https://github.com/Cbaird26/MQGT-SCF/tree/main/paper/figures)** - All 10+ figures from the paper

**📦 Zenodo Archive:**
- **[Zenodo DOI: 10.5281/zenodo.18012506](https://zenodo.org/records/18012506)** - Complete archive with all files

### How to Access Files on GitHub:

1. **For PDFs:** Click any PDF link above, or navigate to the file and click the "Download" button (top right)
2. **For LaTeX:** Click the file to view, or click "Raw" to download
3. **For directories:** Click folder names to browse, then click individual files

**All equations, derivations, and complete theory are in the PDFs above. The LaTeX source contains all mathematical formulations.**

## Repository Structure

```
MQGT-SCF/
├── paper/              # Main manuscript and supplement
├── theory/             # Theoretical derivations and assumptions
│   └── ToE_papers/    # Complete Theory of Everything papers
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

