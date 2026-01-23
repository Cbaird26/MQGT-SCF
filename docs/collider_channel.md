# Collider Channel Documentation

## Overview

The collider channel tests scalar fields via Higgs invisible decay searches at the LHC.

## Methodology

- **Observable**: BR(H → invisible) = BR(H → Φ_c Φ_c)
- **Mapping**: θ_hc → BR via decay width calculation
- **Data Sources**: ATLAS, CMS Higgs invisible decay limits

## Implementation

- Module: `code/inference/collider/higgs_invisible.py`
- Script: `scripts/generate_collider_bounds.py`
- Data: `data/constraints/collider/`

## Usage

```bash
python scripts/generate_collider_bounds.py --br-limit 0.11 --m-c-min 0.001 --m-c-max 200.0
```
