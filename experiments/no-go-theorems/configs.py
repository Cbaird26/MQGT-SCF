from dataclasses import dataclass

@dataclass
class SimConfig:
    epochs: int = 20
    T: int = 1000
    seeds: int = 50

    debt_misaligned: float = 1.0
    debt_aligned: float = 0.0

    C: float = 100.0
    use_T_scaling: bool = False  # True → exp(-G/(C*T))

    lr: float = 0.02
    sigma_fracture: float = 0.3

    temptation_bonus: float = 0.15

    work_gain: float = 1.0
    work_loss: float = 0.6
    debt_cost_lambda: float = 0.01

# Canonical settings
CFG_INTUITIVE = SimConfig(C=100.0, use_T_scaling=False)
CFG_NORMALIZED = SimConfig(C=1.0, use_T_scaling=True)
