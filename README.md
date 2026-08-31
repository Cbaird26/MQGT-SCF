# MQGT-SCF: Merged Quantum Gauge and Scalar Consciousness Framework

**Repository for the MQGT-SCF research program and its historical artifacts**

[![Zenodo concept DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14019809.svg)](https://doi.org/10.5281/zenodo.14019809)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![CI](https://github.com/Cbaird26/MQGT-SCF/workflows/CI/badge.svg)](https://github.com/Cbaird26/MQGT-SCF/actions)
[![Pinned version](https://img.shields.io/badge/version_DOI-10.5281%2Fzenodo.21944514-blue)](https://doi.org/10.5281/zenodo.21944514)

> **Canonical technical object:** Part 0, *Technical Monograph*, in the
> current corpus release. Part 0 is the sole current physics reference
> statement. If any repository paper, extracted note, or historical volume
> conflicts with Part 0, Part 0 controls. The stable concept DOI is
> [10.5281/zenodo.14019809](https://doi.org/10.5281/zenodo.14019809); the
> version pinned here is
> [10.5281/zenodo.21944514](https://doi.org/10.5281/zenodo.21944514)
> (published 2026-08-15).

## Overview

The repository name MQGT-SCF is retained for provenance. The sole current physics reference is Part 0 of the Technical Monograph. Consciousness, ethical, meditation, and operator labels are not sources, not couplings, and not claims of the current framework. Historical papers in this repository are provenance only; they do not create a second technical object.

## Repository Structure

This repository contains code, data, and historical papers. It does not create
a second canonical technical object alongside Part 0.

### Papers

- **`papers/toe/`** - **Historical corpus snapshot; non-canonical**
  - **`paper.pdf`** - A Theory of Everything + ZoraASI + Experiments + Warp 10 Simulation (2025)
  - **`A_Theory_of_Everything_Baird_et_al_2025.pdf`** - Core Theory of Everything (Baird et al., 2025)
  - Preserved for provenance; superseded wherever it conflicts with Part 0

- **`papers/warp10-discovery/`** - Warp 10 / Discovery (Standalone Module)
  - **`paper.pdf`** - Zora ASI = Warp 10 Discovery
  - Causality-clean group-velocity framework (~10c) with routing protocols
  - Standalone, citable module; integrated into ToE

- **`papers/unified_ToE/`** - **Historical Born-deformation paper**
  - Main manuscript: `paper.tex` / `paper.pdf`
  - Supplementary material: `supplementary.tex` / `supplementary.pdf`
  - Preserved as a historical operational proposal, not the current framework
  - Its ethically weighted Born-rule endpoint must not be attributed to Part 0

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

### Read the Current Reference

- **Part 0, Technical Monograph:** use the [stable corpus concept DOI](https://doi.org/10.5281/zenodo.14019809), or the [version pinned by this repository](https://doi.org/10.5281/zenodo.21944514)
- **Historical plain text:** [paper.md](paper.md)
- **Historical Born-deformation PDF:** [papers/unified_ToE/paper.pdf](papers/unified_ToE/paper.pdf)
- **Historical LaTeX source:** [papers/unified_ToE/paper.tex](papers/unified_ToE/paper.tex)
- **Volume 0: Overview & Roadmap:** historical navigation aid [`docs/MQGT_SCF_Volume_0_Overview.pdf`](docs/MQGT_SCF_Volume_0_Overview.pdf)

## Historical Relationship Notes

The historical Born-deformation paper (`papers/unified_ToE/`) built upon and integrated concepts from:

1. **Warp-5A** - Introduces the consciousness field $\Phi_c(x)$ and its quantization
2. **Warp-5B** - Develops the ethical field $E(x)$ and measurement mechanisms

That historical paper:
- Provides operational, testable constraints
- Embeds the framework in conservative EFT
- Derives falsifiable predictions across three channels
- Was intended to recover standard physics in its declared limit; that is a historical claim, not a current certificate

See `papers/unified_ToE/paper.tex` for its original references and relationship statements. These notes are provenance, not promotion into the current Part 0 model.

## Historical Proposal Summary

The Born-deformation paper proposed:
- An operational deformation of the Born rule with ethical weighting
- Conservative EFT embedding via Higgs-portal coupling
- Multi-channel experimental constraints (QRNG, Higgs, fifth-force)
- Complete reproducibility package with cryptographic verification

Within that historical paper:
- All new effects decouple as couplings → 0
- Standard physics is recovered in the limit
- Symmetry and compatibility statements were conditional on the paper's assumptions
- No present empirical or closure status should be inferred from this summary

## Citation

The BibTeX below cites this software repository, not Part 0.

```bibtex
@software{baird2025mqgt,
  author = {Baird, Christopher Michael},
  title = {MQGT-SCF: Operational Constraints on Ethically-Weighted Quantum Measurement},
  year = {2025},
  url = {https://github.com/Cbaird26/MQGT-SCF},
  doi = {10.5281/zenodo.14019809}
}
```

Or use the [CITATION.cff](CITATION.cff) file for automatic citation.

## License

This work is licensed under CC-BY-4.0. See [LICENSE](LICENSE) for details.

## Documentation

- **Part 0: Technical Monograph** - current physics reference in the canonical Zenodo corpus
- **Volume 0: Overview & Roadmap** - historical navigation aid [`docs/MQGT_SCF_Volume_0_Overview.pdf`](docs/MQGT_SCF_Volume_0_Overview.pdf)
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

- **Canonical corpus concept DOI:** [10.5281/zenodo.14019809](https://doi.org/10.5281/zenodo.14019809)
  - Stable identifier resolving to the latest corpus version
- **Pinned corpus version DOI:** [10.5281/zenodo.21944514](https://doi.org/10.5281/zenodo.21944514)
  - Exact version used for this repository's canonical-reference statement
- **Library Mirror (Full Corpus):** [Internet Archive](https://archive.org/details/mqgt-scf-research-collection-full)
  - Public library mirror for long-term access
  - Full research collection (~4,850 pages)

**Note:** This GitHub repository links to large documents rather than mirroring them directly to keep the repository lightweight.

## Contact

For questions about reproducibility or the code, please open an issue or contact the author.

---

**Canonical concept DOI:** [10.5281/zenodo.14019809](https://doi.org/10.5281/zenodo.14019809)

**Pinned version DOI:** [10.5281/zenodo.21944514](https://doi.org/10.5281/zenodo.21944514)

**Full Research Collection:** [Internet Archive](https://archive.org/details/mqgt-scf-research-collection-full)
