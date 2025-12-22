
"""Constraints and likelihood utilities (digitized from published plots).

- Fifth-force envelope digitized from Lee et al. (2020) ISL test figure (ar5iv 2002.11761, Fig. 5 bottom)
- Higgs invisible profile likelihood digitized from CMS HIG-20-003 public results (Fig. 12)

These are intended as drop-in replacements for proxy/envelope placeholders.
"""

import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

# Load digitized data
_ff = pd.read_csv(DATA_DIR/'fifth_force_alpha_lambda_envelope.csv').sort_values('lambda_m')
_hinv = pd.read_csv(DATA_DIR/'cms_hinv_profilelik_digitized_unique.csv').sort_values('B')

def alpha_limit(lambda_m: np.ndarray) -> np.ndarray:
    """Return interpolated 95% CL upper limit alpha_max(lambda) from digitized envelope."""
    x = np.log10(_ff['lambda_m'].values)
    y = np.log10(_ff['alpha_limit_env'].values)
    lam = np.log10(np.asarray(lambda_m))
    yint = np.interp(lam, x, y, left=y[0], right=y[-1])
    return 10**yint

def q_hinv(B: np.ndarray) -> np.ndarray:
    """Return interpolated q(B) = -2ΔlnL for CMS combined observed scan."""
    x = _hinv['B'].values
    y = _hinv['q'].values
    b = np.asarray(B)
    return np.interp(b, x, y, left=y[0], right=y[-1])

def loglik_hinv(B: float) -> float:
    """Log-likelihood up to a constant from q(B)."""
    q = float(q_hinv(np.array([B]))[0])
    return -0.5*q

def loglik_fifth_force(alpha: float, lambda_m: float) -> float:
    """Soft constraint log-likelihood from envelope (alpha <= alpha_max)."""
    amax = float(alpha_limit(np.array([lambda_m]))[0])
    if alpha <= amax:
        return 0.0
    # quadratic penalty in log-space
    return -0.5*((np.log10(alpha)-np.log10(amax))/0.5)**2
