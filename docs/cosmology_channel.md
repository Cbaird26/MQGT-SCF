# Cosmology Channel Documentation

## Overview

The cosmology channel tests scalar fields via BBN and CMB constraints.

## Methodology

- **BBN**: Maps to ΔN_eff (effective neutrino number)
- **CMB**: Maps to dark energy equation of state w
- **Data Sources**: PDG BBN, Planck CMB

## Implementation

- Modules: `code/inference/cosmology/bbn_constraints.py`, `cmb_constraints.py`
- Data: `data/constraints/cosmology/`

## Sensitivity

- BBN: m_c < 1 MeV (early universe)
- CMB: m_c < 10⁻³ eV (late-time expansion)
