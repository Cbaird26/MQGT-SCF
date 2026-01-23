# Comprehensive Empirical Test Channel Catalog for MQGT-SCF

## Overview

This document catalogs ALL empirical test channels for scalar fields (Φ_c) in MQGT-SCF, organized by test type, sensitivity range, data sources, and implementation status. All tests are concrete, implementable via simulation or experiment, and exclude human-influenced RNG.

**Last Updated**: 2026-01-22  
**Status**: Active catalog, continuously updated as channels are implemented

## Test Channel Summary Table

| Channel | Category | Status | Sensitivity Range | Data Source | Priority |
|---------|----------|--------|-------------------|-------------|----------|
| Fifth-Force Torsion Balance | Direct Force | ✅ Implemented | λ ~ 10 μm - 1 mm | Eöt-Wash 2016, Lee 2020 | N/A |
| Casimir Effect | Direct Force | 🔄 Planned | λ ~ 100 nm - 10 μm | Lamoreaux 1997, Bressi 2002 | High |
| Higgs Invisible Decay | Collider | 🔄 Planned | m_c < m_h/2 | ATLAS, CMS | High |
| Big Bang Nucleosynthesis | Cosmology | 🔄 Planned | m_c < 1 MeV | PDG, Planck | High |
| Equivalence Principle | Precision | 🔄 Planned | λ ~ 1 m - 1 km | Eöt-Wash, MICROSCOPE | High |
| Atomic Clock Comparisons | Precision | 🔄 Planned | m_c ~ 10⁻¹⁵ - 10⁻¹² eV | NIST, PTB | Medium |
| CMB Constraints | Cosmology | 🔄 Planned | m_c < 10⁻³ eV | Planck 2018 | Medium |
| Quantum Optics (SPDC/HOM) | Quantum Optics | 🔄 Planned | m_c ~ 10⁻³ - 10⁻¹ eV | Simulation | Medium |

**Legend:**
- ✅ Implemented: Fully functional with data ingestion and constraint generation
- 🔄 Planned: Design complete, implementation in progress
- 📋 Design: Concept defined, design phase

## Category 1: Direct Force Tests (Short-Range)

### 1.1 Fifth-Force Torsion Balance ✅ IMPLEMENTED

**Status**: Fully implemented and operational

**Principle**: Scalar fields produce Yukawa-type deviations from inverse-square gravity at short ranges.

**Implementation**:
- **Data**: Eöt-Wash 2016 (Kapner et al.), Lee 2020 (Lee et al.)
- **Constraint Format**: α_max(λ) for λ ~ 10 μm - 1 mm
- **Mapping**: ToE parameters (κ_cH, v_c, m_c) → θ_hc → α(λ)
- **Files**: 
  - `code/inference/fifth_force/toe_mapping.py`
  - `code/inference/fifth_force/toe_bounds.py`
  - `data/raw/fifth_force/lee2020/`
  - `results/toe_constraints/theta_max_vs_lambda.csv`

**Sensitivity**: λ ~ 10 μm - 1 mm (m_c ~ 0.2 meV - 20 meV)

### 1.2 Casimir Effect Modifications 🔄 PLANNED

**Principle**: Scalar fields modify vacuum fluctuations, changing the Casimir force between parallel plates.

**Data Sources**: Lamoreaux (1997), Bressi et al. (2002)

**Sensitivity**: λ ~ 100 nm - 10 μm (m_c ~ 0.02 meV - 2 meV)

## Category 2: Higgs Portal Tests (Collider)

### 2.1 Higgs Invisible Decay Width 🔄 PLANNED (HIGH PRIORITY)

**Principle**: Scalar-Higgs mixing (θ_hc) → invisible Higgs decays H → Φ_c Φ_c

**Data Sources**:
- ATLAS: BR(H → invisible) < 0.15 (95% CL)
- CMS: BR(H → invisible) < 0.19 (95% CL)

**Sensitivity**: 
- On-shell: m_c < m_h/2 ≈ 62.5 GeV
- Off-shell: All m_c (contributes to total width)

**Priority**: HIGH (direct collider constraint, well-defined)

## Category 3: Cosmological Tests

### 3.1 Big Bang Nucleosynthesis (BBN) 🔄 PLANNED (HIGH PRIORITY)

**Principle**: Scalar fields modify expansion rate → change light element abundances

**Data Sources**: PDG BBN constraints, Planck CMB

**Sensitivity**: m_c < 1 MeV (affects early universe, T ~ 1 MeV)

**Priority**: HIGH (early universe, well-measured)

### 3.2 Cosmic Microwave Background (CMB) 🔄 PLANNED

**Principle**: Scalar fields modify expansion history → change CMB power spectrum

**Data Sources**: Planck 2018 CMB data

**Sensitivity**: m_c < 10⁻³ eV (affects late-time expansion)

## Category 4: Precision Measurement Tests

### 4.1 Equivalence Principle (EP) Tests 🔄 PLANNED (HIGH PRIORITY)

**Principle**: Scalar fields violate weak equivalence principle (WEP)

**Data Sources**: Eöt-Wash EP tests, MICROSCOPE

**Sensitivity**: λ ~ 1 m - 1 km (long-range tests)

**Priority**: HIGH (long-range complement to short-range tests)

### 4.2 Atomic Clock Comparisons 🔄 PLANNED

**Principle**: Scalar fields shift atomic transition frequencies

**Data Sources**: NIST, PTB clock comparisons

**Sensitivity**: m_c ~ 10⁻¹⁵ - 10⁻¹² eV (ultralight scalars)

## Category 5: Quantum Optics Tests (Non-Human)

### 5.1 Spontaneous Parametric Down-Conversion (SPDC) 🔄 PLANNED

**Principle**: Scalar fields modify biphoton correlations

**Test Method**: Simulate SPDC with scalar field modifications

**Sensitivity**: m_c ~ 10⁻³ - 10⁻¹ eV (optical frequencies)

**Note**: All quantum optics tests are simulation-based, not human-influenced

### 5.2 Hong-Ou-Mandel (HOM) Interference 🔄 PLANNED

**Principle**: Scalar fields modify photon indistinguishability

**Test Method**: Simulate HOM with scalar field effects

**Sensitivity**: m_c ~ 10⁻³ - 10⁻¹ eV



## Category 7: Astrophysical Constraints

### 7.1 Stellar Cooling Constraints ✅ IMPLEMENTED

**Status**: Fully implemented

**Principle**: Light scalars coupled to electrons/photons carry energy from stellar cores.

**Data Sources**: Red giant branch (Gaia/HST), white dwarfs, solar neutrinos

**Sensitivity**: m_c < 1 MeV (affects stellar interiors)

**Files**:
- `code/inference/astrophysics/stellar_cooling.py`
- `scripts/generate_stellar_cooling_bounds.py`
- `data/constraints/astrophysics/`

### 7.2 Supernova 1987A Energy Loss ✅ IMPLEMENTED

**Status**: Fully implemented

**Principle**: Scalars modify neutrino burst duration by carrying away energy.

**Data Sources**: SN1987A neutrino timing (IMB, Kamiokande)

**Sensitivity**: m_c < 100 MeV (affects supernova core)

**Files**:
- `code/inference/astrophysics/sn1987a_constraints.py`
- `scripts/generate_sn1987a_bounds.py`

## Category 8: Gravitational Wave Constraints

### 8.1 GW Propagation Modifications ✅ IMPLEMENTED

**Status**: Fully implemented

**Principle**: Scalars modify GW speed, polarization, or dispersion.

**Data Sources**: GW170817 (speed of gravity = c within 10⁻¹⁵)

**Sensitivity**: All m_c (affects GW propagation)

**Files**:
- `code/inference/gravitational_waves/gw_propagation.py`
- `scripts/generate_gw_bounds.py`

### 8.2 Black Hole Shadow Constraints ✅ IMPLEMENTED

**Status**: Fully implemented

**Principle**: Ultralight scalars modify black hole metrics, changing shadow size.

**Data Sources**: Event Horizon Telescope (M87*, Sgr A*)

**Sensitivity**: m_c < 10⁻¹⁰ eV (ultralight scalars)

**Files**:
- `code/inference/gravitational_waves/bh_shadow.py`
- `scripts/generate_bh_shadow_bounds.py`

## Category 9: Large-Scale Structure (LSS)

### 9.1 Matter Power Spectrum Constraints ✅ IMPLEMENTED

**Status**: Fully implemented

**Principle**: Scalars modify structure formation, changing matter clustering.

**Data Sources**: SDSS, DES, Euclid

**Sensitivity**: m_c < 10⁻³ eV (affects structure formation)

**Files**:
- `code/inference/cosmology/lss_constraints.py`
- `scripts/generate_lss_bounds.py`

## Category 10: Neutrino Oscillation Modifications

### 10.1 Neutrino Mass Matrix Modifications ✅ IMPLEMENTED

**Status**: Fully implemented

**Principle**: Scalars modify neutrino mass matrix, changing oscillation probabilities.

**Data Sources**: Super-K, SNO, KamLAND, Daya Bay

**Sensitivity**: m_c ~ 10⁻³ - 10⁻¹ eV (neutrino mass scale)

**Files**:
- `code/inference/neutrinos/oscillation_modifications.py`
- `scripts/generate_neutrino_bounds.py`

## Category 11: Dark Matter Direct Detection

### 11.1 Scalar Dark Matter Scattering ✅ IMPLEMENTED

**Status**: Fully implemented (conditional on Φ_c being DM)

**Principle**: If Φ_c is dark matter, it scatters off nuclei.

**Data Sources**: XENON, LUX, PandaX, LZ

**Sensitivity**: m_c ~ 1 GeV - 1 TeV (if dark matter)

**Files**:
- `code/inference/dark_matter/direct_detection.py`
- `scripts/generate_dm_bounds.py`

## Category 12: Theorem-Level Consistency Proofs

### 12.1 No-Signaling Proofs ✅ IMPLEMENTED

**Status**: Framework implemented (requires formal verification)

**Principle**: Verify modified Born rule preserves causality.

**Files**:
- `code/inference/theorems/no_signaling.py`

### 12.2 Stability Proofs ✅ IMPLEMENTED

**Status**: Framework implemented

**Principle**: Prove bounded energy and absence of ghosts.

**Files**:
- `code/inference/theorems/stability.py`

### 12.3 Reduction to GR+SM ✅ IMPLEMENTED

**Status**: Framework implemented

**Principle**: Prove exact recovery of GR+SM in low-energy limits.

**Files**:
- `code/inference/theorems/reduction.py`


## Implementation Roadmap

### Phase 1: High-Priority, High-Impact (Weeks 1-4)
1. ✅ Fifth-Force Torsion Balance (DONE)
2. 🔄 Higgs Invisible Decay (IN PROGRESS)
3. 🔄 Casimir Effect (NEXT)
4. 🔄 BBN Constraints (NEXT)
5. 🔄 EP Tests (NEXT)

### Phase 2: Medium-Priority (Weeks 5-8)
6. CMB Constraints
7. Atomic Clock Comparisons
8. Quantum Optics Simulations (SPDC, HOM)

## Technical Notes

### Mapping Strategy

For each channel, implement:
1. **Forward Mapping**: ToE parameters → observable prediction
2. **Inverse Mapping**: Experimental constraint → bounds on ToE parameters
3. **Validation**: Round-trip closure tests

### Data Management

- All experimental constraints stored in `data/constraints/{channel}/`
- Canonical CSV files with provenance metadata
- SHA256 hashes for reproducibility
- Constraint ledger tracks all sources

### Integration

- All channels integrated into unified falsification dashboard
- Consistent parameter bounds format
- Cross-channel consistency checks
