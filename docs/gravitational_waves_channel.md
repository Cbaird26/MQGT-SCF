# Gravitational Wave Channel Documentation

## Overview

Tests scalar fields via GW propagation modifications and black hole shadow constraints.

## Methodology

- **GW Propagation**: Maps to speed modifications (v_gw - c)/c
- **BH Shadow**: Maps to shadow size modifications from ultralight scalars
- **Data Sources**: GW170817, EHT M87*/Sgr A*

## Implementation

- Modules: `code/inference/gravitational_waves/gw_propagation.py`, `bh_shadow.py`
- Scripts: `scripts/generate_gw_bounds.py`, `generate_bh_shadow_bounds.py`
- Data: `data/constraints/gravitational_waves/`

## Sensitivity

- GW propagation: All m_c (affects GW propagation)
- BH shadow: m_c < 10⁻¹⁰ eV (ultralight scalars)
