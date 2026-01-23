# Astrophysics Channel Documentation

## Overview

The astrophysics channel tests scalar fields via stellar cooling and supernova energy loss constraints.

## Methodology

- **Stellar Cooling**: Maps to energy loss rate ε_φ from stellar cores
- **SN1987A**: Maps to neutrino burst duration modifications
- **Data Sources**: Red giants, white dwarfs, solar neutrinos, SN1987A timing

## Implementation

- Modules: `code/inference/astrophysics/stellar_cooling.py`, `sn1987a_constraints.py`
- Scripts: `scripts/generate_stellar_cooling_bounds.py`, `generate_sn1987a_bounds.py`
- Data: `data/constraints/astrophysics/`

## Sensitivity

- Stellar cooling: m_c < 1 MeV (affects stellar interiors)
- SN1987A: m_c < 100 MeV (affects supernova core)
