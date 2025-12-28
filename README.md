# MQGT-SCF: Merged Quantum Gauge and Scalar Consciousness Framework

**Operational Constraints on Ethically-Weighted Quantum Measurement: A Multi-Channel Effective Field Theory Analysis**

[![Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.18012506.svg)](https://zenodo.org/records/18050570)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![CI](https://github.com/Cbaird26/MQGT-SCF/workflows/CI/badge.svg)](https://github.com/Cbaird26/MQGT-SCF/actions)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18012506-blue)](https://zenodo.org/records/18050570)

## Overview

The Merged Quantum Gauge and Scalar Consciousness Framework (MQGT-SCF) is an effective field theory extension of the Standard Model and General Relativity that incorporates scalar fields encoding consciousness-like and ethical structures. The framework is formulated operationally, with testable predictions across multiple experimental channels.

## Repository Structure

This repository contains multiple related papers and supporting materials:

### Papers

- **`papers/toe/`** - Theory of Everything (Master Paper)
  - **`paper.pdf`** - A Theory of Everything + ZoraASI + Experiments + Warp 10 Simulation (2025)
  - **`A_Theory_of_Everything_Baird_et_al_2025.pdf`** - Core Theory of Everything (Baird et al., 2025)
  - Master paper integrating theory, experiments, and applied modules
  - This is the **source of truth** for the unified framework

- **`papers/warp10-discovery/`** - Warp 10 / Discovery (Standalone Module)
  - **`paper.pdf`** - Zora ASI = Warp 10 Discovery
  - Causality-clean group-velocity framework (~10c) with routing protocols
  - Standalone, citable module; integrated into ToE

- **`papers/unified_ToE/`** - Unified Theory of Everything (operational constraints paper)
  - Main manuscript: `paper.tex` / `paper.pdf`
  - Supplementary material: `supplementary.tex` / `supplementary.pdf`
  - Primary, testable framework with experimental constraints

- **`papers/warp5A/`** - Warp-5A (precursor paper)
  - Early formulation of consciousness field dynamics
  - Provides foundational concepts for the unified framework

- **`papers/warp5B/`** - Warp-5B (precursor paper)
  - Extended treatment of ethical field and measurement mechanisms
  - Complements Warp-5A and feeds into unified framework

### Theory Documentation

- **`theory/`** - Extracted theoretical content
  - `lagrangian.md` - Unified Lagrangian formulation
  - `field_equations.md` - Field equations and dynamics
  - `collapse_mechanism.md` - Consciousness-induced collapse mechanism
  - `teleology.md` - Teleological term and implications
  - `glossary.md` - Notation and terminology

### Code and Data

- **`code/`** - Computational implementations
  - `inference/` - Bayesian inference harnesses
  - `simulations/` - Field dynamics simulations
  - `notebooks/` - Reproducibility notebooks

- **`data/`** - Experimental data and constraints
  - `raw/` - Original data sources
  - `processed/` - Digitized experimental constraints

- **`experiments/`** - Experimental proposals
  - `rng_bias/` - Quantum random number generator tests
  - `lattice_simulations/` - Lattice field theory simulations
  - `neural_coherence/` - Neural coherence measurements

## Quick Start

### Installation

**For reproducibility (exact versions):**
```bash
git clone https://github.com/Cbaird26/MQGT-SCF.git
cd MQGT-SCF
pip install -r requirements-lock.txt
```

> **Note:** `requirements-lock.txt` is generated from Python 3.11 on 2025-12-28. For exact reproduction, use the lockfile. To regenerate: `pip freeze > requirements-lock.txt` (from a clean environment with `requirements.txt` installed).

**For development (latest compatible versions):**
```bash
git clone https://github.com/Cbaird26/MQGT-SCF.git
cd MQGT-SCF
pip install -r requirements.txt

# Or install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Quick Start (Makefile)

```bash
# Install dependencies (reproducible)
make install

# Run tests
make test

# Reproduce results
make reproduce

# See all commands
make help
```

### Run Tests (Manual)

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Or with coverage
pytest tests/ --cov=code --cov-report=html
```

### Reproduce Results

```bash
python reproduce_all.py
```

### Read the Paper

- **Plain text (automated readers):** [paper.md](paper.md)
- **PDF:** [papers/unified_ToE/paper.pdf](papers/unified_ToE/paper.pdf)
- **LaTeX source:** [papers/unified_ToE/paper.tex](papers/unified_ToE/paper.tex)
- **Volume 0: Overview & Roadmap** - Start here for the complete research collection: [`docs/MQGT_SCF_Volume_0_Overview.pdf`](docs/MQGT_SCF_Volume_0_Overview.pdf)

## Relationship to Prior Work

The unified ToE paper (`papers/unified_ToE/`) builds upon and integrates concepts from:

1. **Warp-5A** - Introduces the consciousness field $\Phi_c(x)$ and its quantization
2. **Warp-5B** - Develops the ethical field $E(x)$ and measurement mechanisms

The unified framework:
- Provides operational, testable constraints
- Embeds the framework in conservative EFT
- Derives falsifiable predictions across three channels
- Maintains consistency with all known physics

See `papers/unified_ToE/paper.tex` for explicit references and relationship statements.

## Novelty Claims

This work introduces:
- An operational deformation of the Born rule with ethical weighting
- Conservative EFT embedding via Higgs-portal coupling
- Multi-channel experimental constraints (QRNG, Higgs, fifth-force)
- Complete reproducibility package with cryptographic verification

The framework is conservative in that:
- All new effects decouple as couplings → 0
- Standard physics is recovered in the limit
- No violations of known symmetries (except minuscule teleological term)
- Compatible with all current experimental bounds

## Citation

```bibtex
@software{baird2025mqgt,
  author = {Baird, Christopher Michael},
  title = {MQGT-SCF: Operational Constraints on Ethically-Weighted Quantum Measurement},
  year = {2025},
  url = {https://github.com/Cbaird26/MQGT-SCF},
  doi = {10.5281/zenodo.18012506}
}
```

Or use the [CITATION.cff](CITATION.cff) file for automatic citation.

## License

This work is licensed under CC-BY-4.0. See [LICENSE](LICENSE) for details.

## Documentation

- **Volume 0: Overview & Roadmap** - [`docs/MQGT_SCF_Volume_0_Overview.pdf`](docs/MQGT_SCF_Volume_0_Overview.pdf)
  - Navigational front door to the complete research collection
  - Volume map, reading pathways, and structural index
  - Entry point for the three-volume corpus (~4,824 pages)
  - **Recommended starting point** for accessing the full research collection
- **Theory:** See `theory/` directory for extracted equations and derivations
- **Experiments:** See `experiments/` for proposed tests
- **Reproducibility:** See `code/` and `notebooks/` for reproduction guides
- **Roadmap:** See `docs/roadmap.md` for future directions
- **FAQ:** See `docs/faq.md` for common questions

## Authoritative Archives

- **Canonical Archive (DOI):** [Zenodo Record 18050570](https://zenodo.org/records/18050570)
  - Versioned, persistent identifier
  - Complete research corpus with metadata
- **Library Mirror (Full Corpus):** [Internet Archive](https://archive.org/details/mqgt-scf-research-collection-full)
  - Public library mirror for long-term access
  - Full research collection (~4,850 pages)

**Note:** This GitHub repository links to large documents rather than mirroring them directly to keep the repository lightweight.

## Contact

For questions about reproducibility or the code, please open an issue or contact the author.

---

**Canonical DOI:** [10.5281/zenodo.18012506](https://zenodo.org/records/18050570)  
**Full Research Collection:** [Internet Archive](https://archive.org/details/mqgt-scf-research-collection-full)
