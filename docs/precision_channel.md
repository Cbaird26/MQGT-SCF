# Precision Measurement Channel Documentation

## Overview

Tests scalar fields via Casimir effect, EP tests, and atomic clock comparisons.

## Methodology

- **Casimir**: Force deviation δF/F
- **EP**: Violation parameter η
- **Clocks**: Frequency shift δν/ν

## Implementation

- Modules: `code/inference/precision/casimir_effect.py`, `equivalence_principle.py`, `atomic_clocks.py`
- Data: `data/constraints/precision/`

## Sensitivity

- Casimir: λ ~ 100 nm - 10 μm
- EP: λ ~ 1 m - 1 km
- Clocks: m_c ~ 10⁻¹⁵ - 10⁻¹² eV
