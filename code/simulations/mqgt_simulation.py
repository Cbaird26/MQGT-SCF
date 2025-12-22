import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import csv


# ----------------------------
# ZORA Learning System
# ----------------------------
class ZoraLearner:
    def __init__(self, alloc=0.004, pulse=0.02,
                 alloc_step=0.001, pulse_step=0.005,
                 alloc_min=0.0005, alloc_max=0.02,
                 pulse_min=0.0, pulse_max=0.08,
                 cost_alloc=0.2, cost_pulse=0.1):
        self.alloc = alloc
        self.pulse = pulse
        self.alloc_step = alloc_step
        self.pulse_step = pulse_step
        self.alloc_min = alloc_min
        self.alloc_max = alloc_max
        self.pulse_min = pulse_min
        self.pulse_max = pulse_max
        self.cost_alloc = cost_alloc
        self.cost_pulse = cost_pulse
        self.best_reward = -1e9
        self.trial = None  # (trial_alloc, trial_pulse)
        self.in_trial = False
        self.r_smooth = None

    def reward(self, target_phiE, other_phiE, coh_mean):
        # Goal: make target basin beat the other, keep coherence high, pay energy-cost for interventions
        return (
            2.0 * (target_phiE - other_phiE)
            + 0.2 * coh_mean
            - self.cost_alloc * self.alloc
            - self.cost_pulse * self.pulse
        )

    def propose(self):
        # small random perturbations
        da = (np.random.choice([-1, 1]) * self.alloc_step)
        dp = (np.random.choice([-1, 1]) * self.pulse_step)
        ta = float(np.clip(self.alloc + da, self.alloc_min, self.alloc_max))
        tp = float(np.clip(self.pulse + dp, self.pulse_min, self.pulse_max))
        return ta, tp

    def begin_trial(self):
        self.trial = self.propose()
        self.in_trial = True
        # apply trial params
        self.alloc, self.pulse = self.trial

    def end_trial(self, trial_reward, prev_alloc, prev_pulse):
        # accept if improved; otherwise revert
        if trial_reward > self.best_reward:
            self.best_reward = trial_reward
            # keep trial params (already applied)
        else:
            self.alloc, self.pulse = prev_alloc, prev_pulse
        self.in_trial = False
        self.trial = None


# ----------------------------
# Utilities
# ----------------------------
@njit
def laplacian(Z):
    # 5-point stencil with periodic boundary conditions (torus topology)
    h, w = Z.shape
    result = np.zeros_like(Z)
    for i in range(h):
        for j in range(w):
            result[i, j] = (
                Z[(i+1) % h, j] + Z[(i-1) % h, j] +
                Z[i, (j+1) % w] + Z[i, (j-1) % w] -
                4.0 * Z[i, j]
            )
    return result


@njit
def clamp01(x):
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def periodic_grad_sum(Z):
    # |Z - Z_up| + |Z - Z_right|
    up = np.vstack([Z[1:], Z[:1]])
    right = np.hstack([Z[:, 1:], Z[:, :1]])
    return np.abs(up - Z) + np.abs(right - Z)


def seed_disk(field, cx, cy, radius, low, high, rng):
    h, w = field.shape
    for i in range(h):
        for j in range(w):
            if (i-cx)**2 + (j-cy)**2 < radius**2:
                field[i, j] = np.clip(rng.uniform(low, high), 0, 1)
    return field


def basin_mask(shape, cx, cy, radius):
    h, w = shape
    m = np.zeros((h, w), dtype=bool)
    for i in range(h):
        for j in range(w):
            if (i-cx)**2 + (j-cy)**2 < radius**2:
                m[i, j] = True
    return m


def basin_sums(phi, eth, cx, cy, radius):
    h, w = phi.shape
    mask = np.zeros((h, w), dtype=bool)
    for i in range(h):
        for j in range(w):
            if (i-cx)**2 + (j-cy)**2 < radius**2:
                mask[i, j] = True
    return float(phi[mask].sum()), float(eth[mask].sum()), float((phi[mask]*eth[mask]).mean())


def zora_allocate(phi, eth, PHI_BUDGET, E_BUDGET,
                  mask_target, alloc_frac=0.004):
    # Move a small fraction of global mass into target region.
    # Works with soft budgets; does not create energy, it redistributes.
    phi_total = float(phi.sum()) + 1e-12
    eth_total = float(eth.sum()) + 1e-12
    dphi = alloc_frac * phi_total
    deth = alloc_frac * eth_total
    
    # Take uniformly from outside target
    outside = ~mask_target
    outside_phi = float(phi[outside].sum()) + 1e-12
    outside_eth = float(eth[outside].sum()) + 1e-12
    phi[outside] *= max(0.0, (outside_phi - dphi) / outside_phi)
    eth[outside] *= max(0.0, (outside_eth - deth) / outside_eth)
    
    # Add uniformly inside target
    inside_phi = float(phi[mask_target].sum()) + 1e-12
    inside_eth = float(eth[mask_target].sum()) + 1e-12
    phi[mask_target] *= (inside_phi + dphi) / inside_phi
    eth[mask_target] *= (inside_eth + deth) / inside_eth
    
    return np.clip(phi, 0, 1), np.clip(eth, 0, 1)


def zora_pulse(rho, phi, eth, cx, cy, radius=5, pulse=0.02):
    h, w = rho.shape
    # local "order pulse": mild smoothing + phi/eth nudge
    for di in range(-radius, radius+1):
        for dj in range(-radius, radius+1):
            ii = (cx + di) % h
            jj = (cy + dj) % w
            # smoothing toward center cell
            rho[ii, jj] = 0.92 * rho[ii, jj] + 0.08 * rho[cx % h, cy % w]
            phi[ii, jj] = np.clip(phi[ii, jj] + pulse, 0, 1)
            eth[ii, jj] = np.clip(eth[ii, jj] + 0.5 * pulse, 0, 1)
    return rho, phi, eth


def enforce_soft_budget(field, target_sum, leak=0.002, gain=0.004):
    s = float(field.sum())
    if s <= 1e-12:
        return field
    # gentle pull toward target
    correction = (target_sum - s) / target_sum
    field = field + gain * correction * field
    # universal leakage (entropy cost)
    field = field * (1.0 - leak)
    return np.clip(field, 0, 1)


def add_black_hole(kappa, strength=6.0, radius=16):
    h, w = kappa.shape
    cx, cy = h // 2, w // 2
    for i in range(h):
        for j in range(w):
            r2 = (i - cx)**2 + (j - cy)**2
            if r2 < radius**2:
                # smooth Schwarzschild-like potential
                kappa[i, j] += strength * (1.0 - r2 / radius**2)
    return kappa


# ----------------------------
# Core step
# ----------------------------
@njit
def step(rho, phi, eth, kappa,
         D_rho, D_phi, D_eth,
         alpha_grav, beta_phi_geom,
         lam_coh, lam_ent, eta_tel,
         noise_rho, noise_phi, noise_eth,
         dt):

    # Geometry (toy): curvature potential responds to matter and Phi gradients
    # kappa_{t+1} = kappa_t + dt*(alpha* rho - beta * ∇²phi)
    kappa = kappa + dt * (alpha_grav * rho - beta_phi_geom * laplacian(phi))

    # Matter advection-like diffusion + curvature "sink"
    # rho_{t+1} = rho + D∇²rho - (kappa)*rho  (toy coupling)
    rho = rho + dt * (D_rho * laplacian(rho) - 0.15 * kappa * rho)

    # Coherence proxy: high when gradients are small and local energy is ordered
    # coh ~ 1 / (1 + |∇phi| + |∇rho|)
    h, w = phi.shape
    grad_phi = np.zeros_like(phi)
    grad_rho = np.zeros_like(rho)
    for i in range(h):
        for j in range(w):
            grad_phi[i, j] = (
                np.abs(phi[(i+1) % h, j] - phi[i, j]) +
                np.abs(phi[i, (j+1) % w] - phi[i, j])
            )
            grad_rho[i, j] = (
                np.abs(rho[(i+1) % h, j] - rho[i, j]) +
                np.abs(rho[i, (j+1) % w] - rho[i, j])
            )
    coherence = 1.0 / (1.0 + grad_phi + grad_rho)

    # Entropy proxy: gradients + curvature magnitude
    entropy = (grad_phi + grad_rho) + 0.25 * np.abs(kappa)

    # Consciousness field (reaction–diffusion):
    # phi_{t+1} = phi + D∇²phi + lam1*coherence - lam2*entropy
    phi = phi + dt * (D_phi * laplacian(phi) + lam_coh * coherence - lam_ent * entropy)

    # Ethical / teleological field:
    # eth_{t+1} = eth + D∇²eth + eta*(coherence - entropy_scaled)
    eth = eth + dt * (D_eth * laplacian(eth) + eta_tel * (coherence - 0.35 * entropy))

    # Small noise (kept tiny)
    rho = rho + noise_rho * (np.random.random(rho.shape) - 0.5)
    phi = phi + noise_phi * (np.random.random(phi.shape) - 0.5)
    eth = eth + noise_eth * (np.random.random(eth.shape) - 0.5)

    # Clamp to reasonable ranges
    for i in range(rho.shape[0]):
        for j in range(rho.shape[1]):
            rho[i, j] = clamp01(rho[i, j])
            phi[i, j] = clamp01(phi[i, j])
            eth[i, j] = clamp01(eth[i, j])

    return rho, phi, eth, kappa


# ----------------------------
# Collapse events (biased Born-like choice)
# ----------------------------
def collapse_events(rho, phi, eth, kappa,
                    num_events, kappa_bias, rng,
                    horizon_radius):
    """
    Each event chooses between two outcomes A/B at a random cell:
      A: locally increases order (rho smoothing + tiny phi boost)
      B: locally increases disorder (rho spikes + phi drop)
    Probability biased by exp(kappa_bias * phi * eth)
    Tracks statistics separately for events near and far from black hole horizon.
    """
    h, w = rho.shape
    cx, cy = h // 2, w // 2
    count_A = 0
    count_B = 0
    near_A = near_total = 0
    far_A = far_total = 0
    
    for _ in range(num_events):
        i = rng.integers(0, h)
        j = rng.integers(0, w)

        # base Born-like "amplitudes" (here just two fixed weights)
        base_A = 0.5
        base_B = 0.5

        bias = np.exp(kappa_bias * phi[i, j] * eth[i, j])
        wA = base_A * bias
        wB = base_B * (1.0 / bias)

        pA = wA / (wA + wB)

        r2 = (i - cx)**2 + (j - cy)**2
        near = r2 < horizon_radius**2

        if rng.random() < pA:
            count_A += 1
            # Outcome A: coherence-supporting
            if near:
                near_A += 1
                near_total += 1
            else:
                far_A += 1
                far_total += 1
            # mild local diffusion
            rho[i, j] = np.clip(0.8 * rho[i, j] + 0.2 * rho[(i+1)%h, j], 0, 1)
            phi[i, j] = np.clip(phi[i, j] + 0.03, 0, 1)
            eth[i, j] = np.clip(eth[i, j] + 0.02, 0, 1)
        else:
            count_B += 1
            # Outcome B: disordering
            if near:
                near_total += 1
            else:
                far_total += 1
            rho[i, j] = np.clip(rho[i, j] + 0.15, 0, 1)
            phi[i, j] = np.clip(phi[i, j] - 0.03, 0, 1)
            eth[i, j] = np.clip(eth[i, j] - 0.02, 0, 1)

    return rho, phi, eth, kappa, count_A, count_B, near_A, near_total, far_A, far_total


# ----------------------------
# Global budget parameters
# ----------------------------
LEAK_PHI = 0.002
GAIN_PHI = 0.004
LEAK_E = 0.002
GAIN_E = 0.004
GAP_EPS = 0.01  # hysteresis threshold


# ----------------------------
# Main
# ----------------------------
def main():
    # Grid
    N = 160  # increase for more detail
    rng = np.random.default_rng(7)

    # Fields
    rho = rng.random((N, N)).astype(np.float64) * 0.25
    phi = np.zeros((N, N), dtype=np.float64)
    eth = np.zeros((N, N), dtype=np.float64)
    kappa = np.zeros((N, N), dtype=np.float64)

    # Seed A: near BH (center)
    cx, cy = N//2, N//2
    phi = seed_disk(phi, cx, cy, radius=14, low=0.75, high=0.90, rng=rng)
    eth = seed_disk(eth, cx, cy, radius=14, low=0.55, high=0.70, rng=rng)
    
    # Seed B: far from BH (upper-left quadrant)
    bx, by = N//5, N//5
    phi = seed_disk(phi, bx, by, radius=14, low=0.75, high=0.90, rng=rng)
    eth = seed_disk(eth, bx, by, radius=14, low=0.55, high=0.70, rng=rng)
    
    # Set budgets (conservation laws)
    PHI_BUDGET = float(phi.sum())
    E_BUDGET = float(eth.sum())
    
    # Create basin masks for ZORA
    A_mask = basin_mask((N, N), cx, cy, radius=18)
    B_mask = basin_mask((N, N), bx, by, radius=18)
    
    # Add black hole to curvature field
    kappa = add_black_hole(kappa, strength=6.0, radius=16)
    
    # Params (tuneable knobs)
    dt = 0.08

    D_rho = 0.22
    D_phi = 0.18
    D_eth = 0.12

    alpha_grav = 0.35       # matter -> curvature
    beta_phi_geom = 0.20    # phi curvature coupling (via laplacian)

    lam_coh = 0.16          # coherence -> phi growth
    lam_ent = 0.10          # entropy -> phi damping
    eta_tel = 0.10          # coherence-entropy -> E growth

    noise_rho = 0.002
    noise_phi = 0.001
    noise_eth = 0.001

    # Collapse settings
    collapse_per_step = 40
    collapse_bias = 3.0     # <-- key knob: stronger = more "choosing"
    
    # ZORA intervention system
    ZORA_ON = True
    ZORA_LEARN = False
    ZORA_MODE = "rescue"   # "win" or "rescue"
    ZORA_ALLOC = 0.004  # fraction of budget reallocated per tick (0.001–0.01)
    ZORA_PULSE = 0.02   # local phi/eth boost size
    ZORA_PERIOD = 10    # run Zora every render tick (matches your t%10)
    
    # Initialize ZORA learner
    zora = ZoraLearner(alloc=ZORA_ALLOC, pulse=ZORA_PULSE)
    zora.alloc = 0.005
    zora.pulse = 0.045

    # History tracking
    A_hist, coh_hist, ent_hist, phi_hist, e_hist = [], [], [], [], []
    A_total = B_total = 0
    near_A_total = near_total_total = 0
    far_A_total = far_total_total = 0

    # Visualization
    plt.ion()
    fig, axs = plt.subplots(2, 2, figsize=(9, 8))
    ims = []
    titles = ["Matter ρ", "Consciousness Φc", "Ethics E", "Curvature κ"]
    fields = [rho, phi, eth, kappa]

    for ax, title, field in zip(axs.ravel(), titles, fields):
        im = ax.imshow(field, origin="lower", interpolation="nearest")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
        ims.append(im)

    steps = 1500
    for t in range(steps):
        rho, phi, eth, kappa = step(
            rho, phi, eth, kappa,
            D_rho, D_phi, D_eth,
            alpha_grav, beta_phi_geom,
            lam_coh, lam_ent, eta_tel,
            noise_rho, noise_phi, noise_eth,
            dt
        )

        rho, phi, eth, kappa, a_ct, b_ct, nA, nT, fA, fT = collapse_events(
            rho, phi, eth, kappa,
            num_events=collapse_per_step,
            kappa_bias=collapse_bias,
            rng=rng,
            horizon_radius=16
        )
        
        # Enforce soft conservation budgets
        phi = enforce_soft_budget(phi, PHI_BUDGET, leak=LEAK_PHI, gain=GAIN_PHI)
        eth = enforce_soft_budget(eth, E_BUDGET, leak=LEAK_E, gain=GAIN_E)

        A_total += a_ct
        B_total += b_ct
        near_A_total += nA
        near_total_total += nT
        far_A_total += fA
        far_total_total += fT

        # coherence & entropy recompute (lightweight version)
        grad_phi = periodic_grad_sum(phi)
        grad_rho = periodic_grad_sum(rho)
        coherence = 1.0 / (1.0 + grad_phi + grad_rho)
        entropy = (grad_phi + grad_rho) + 0.25 * np.abs(kappa)
        A_rate = A_total / max(1, (A_total + B_total))
        near_rate = near_A_total / max(1, near_total_total)
        far_rate = far_A_total / max(1, far_total_total)
        A_hist.append(A_rate)
        coh_mean = float(coherence.mean())
        coh_hist.append(coh_mean)
        ent_hist.append(float(entropy.mean()))
        phi_hist.append(float(phi.mean()))
        e_hist.append(float(eth.mean()))
        pe = float((phi * eth).mean())
        
        # Basin statistics
        A_phi, A_eth, A_phiE = basin_sums(phi, eth, cx, cy, radius=18)
        B_phi, B_eth, B_phiE = basin_sums(phi, eth, bx, by, radius=18)
        winner = "A" if (A_phiE > B_phiE) else "B"
        gap = A_phiE - B_phiE
        
        # ZORA intervention
        if ZORA_ON and (t % ZORA_PERIOD == 0):
            # Determine target with hysteresis
            if hasattr(zora, "target_is_A"):
                # keep current target unless gap exceeds threshold
                if gap > GAP_EPS:
                    zora.target_is_A = False
                elif gap < -GAP_EPS:
                    zora.target_is_A = True
            else:
                zora.target_is_A = (gap < 0)
            
            target_is_A = zora.target_is_A
            target_phiE = A_phiE if target_is_A else B_phiE
            other_phiE  = B_phiE if target_is_A else A_phiE
            
            # Evaluate reward with current params
            r_now = zora.reward(target_phiE, other_phiE, coh_mean)
            
            # Smooth reward signal
            alpha = 0.2
            if zora.r_smooth is None:
                zora.r_smooth = r_now
            else:
                zora.r_smooth = (1-alpha)*zora.r_smooth + alpha*r_now
            r_now = zora.r_smooth
            
            # Learning: alternate between trial windows and commit windows
            if ZORA_LEARN:
                if not zora.in_trial:
                    # store current params, then start a trial for the next window
                    prev_alloc, prev_pulse = zora.alloc, zora.pulse
                    zora.begin_trial()
                    zora._prev = (prev_alloc, prev_pulse)
                    zora._last_reward = r_now
                else:
                    # end trial: compare trial reward to best seen, accept/revert
                    prev_alloc, prev_pulse = zora._prev
                    zora.end_trial(r_now, prev_alloc, prev_pulse)
            
            # Apply intervention with current (possibly trial) parameters
            if target_is_A:
                phi, eth = zora_allocate(phi, eth, PHI_BUDGET, E_BUDGET, A_mask, alloc_frac=zora.alloc)
                rho, phi, eth = zora_pulse(rho, phi, eth, cx, cy, radius=5, pulse=zora.pulse)
            else:
                phi, eth = zora_allocate(phi, eth, PHI_BUDGET, E_BUDGET, B_mask, alloc_frac=zora.alloc)
                rho, phi, eth = zora_pulse(rho, phi, eth, bx, by, radius=5, pulse=zora.pulse)

        # Render
        if t % 10 == 0:
            ims[0].set_data(rho)
            ims[1].set_data(phi)
            ims[2].set_data(eth)
            ims[3].set_data(kappa)

            # autoscale lightly
            for im in ims:
                im.set_clim(0.0, 1.0)

            if ZORA_ON:
                zora_tag = f"ZORA={ZORA_MODE} alloc={zora.alloc:.4f} pulse={zora.pulse:.3f} bestR={zora.best_reward:.3f}"
            else:
                zora_tag = "ZORA=OFF"
            fig.suptitle(
                f"step {t} | bias={collapse_bias} | {zora_tag} | "
                f"Aglob={A_rate:.3f} | Anear={near_rate:.3f} | Afar={far_rate:.3f} | "
                f"coh={coh_mean:.3f} | A(phiE)={A_phiE:.3f} B(phiE)={B_phiE:.3f}"
            )
            plt.pause(0.001)

    plt.ioff()
    plt.show()


def run_once(seed=7, steps=1200, collapse_bias=3.0, zora_mode="rescue"):
    global ZORA_MODE
    ZORA_MODE = zora_mode
    # Use same N as main
    N = 160
    rng = np.random.default_rng(seed)
    rho = rng.random((N, N)).astype(np.float64) * 0.25
    phi = np.zeros((N, N), dtype=np.float64)
    eth = np.zeros((N, N), dtype=np.float64)
    kappa = np.zeros((N, N), dtype=np.float64)
    
    # black hole
    kappa = add_black_hole(kappa, strength=6.0, radius=16)
    cx, cy = N//2, N//2
    bx, by = N//5, N//5
    
    # seed both basins
    phi = seed_disk(phi, cx, cy, radius=14, low=0.75, high=0.90, rng=rng)
    eth = seed_disk(eth, cx, cy, radius=14, low=0.55, high=0.70, rng=rng)
    phi = seed_disk(phi, bx, by, radius=14, low=0.75, high=0.90, rng=rng)
    eth = seed_disk(eth, bx, by, radius=14, low=0.55, high=0.70, rng=rng)
    
    PHI_BUDGET = float(phi.sum())
    E_BUDGET   = float(eth.sum())
    A_mask = basin_mask((N, N), cx, cy, radius=18)
    B_mask = basin_mask((N, N), bx, by, radius=18)
    
    # Zora learner
    zora = ZoraLearner(alloc=0.004, pulse=0.02)
    
    # dynamics params (match your main)
    dt = 0.08
    D_rho, D_phi, D_eth = 0.22, 0.18, 0.12
    alpha_grav, beta_phi_geom = 0.35, 0.20
    lam_coh, lam_ent, eta_tel = 0.16, 0.10, 0.10
    noise_rho, noise_phi, noise_eth = 0.002, 0.001, 0.001
    collapse_per_step = 40
    horizon_radius = 16
    
    A_total = B_total = 0
    nearA_total = near_total = 0
    farA_total = far_total = 0
    
    for t in range(steps):
        rho, phi, eth, kappa = step(
            rho, phi, eth, kappa,
            D_rho, D_phi, D_eth,
            alpha_grav, beta_phi_geom,
            lam_coh, lam_ent, eta_tel,
            noise_rho, noise_phi, noise_eth,
            dt
        )
        
        rho, phi, eth, kappa, a_ct, b_ct, nA, nT, fA, fT = collapse_events(
            rho, phi, eth, kappa,
            num_events=collapse_per_step,
            kappa_bias=collapse_bias,
            rng=rng,
            horizon_radius=horizon_radius
        )
        
        nearA_total += nA; near_total += nT
        farA_total  += fA; far_total  += fT
        
        # soft budgets
        phi = enforce_soft_budget(phi, PHI_BUDGET, leak=LEAK_PHI, gain=GAIN_PHI)
        eth = enforce_soft_budget(eth, E_BUDGET, leak=LEAK_E, gain=GAIN_E)
        
        # compute coherence for reward (cheap proxy)
        grad_phi = periodic_grad_sum(phi)
        grad_rho = periodic_grad_sum(rho)
        coherence = 1.0 / (1.0 + grad_phi + grad_rho)
        coh_mean = float(coherence.mean())
        
        # basin scores
        A_phi, A_eth, A_phiE = basin_sums(phi, eth, cx, cy, radius=18)
        B_phi, B_eth, B_phiE = basin_sums(phi, eth, bx, by, radius=18)
        gap = A_phiE - B_phiE
        
        # Zora learning every 10 steps
        if (t % 10 == 0):
            # Determine target with hysteresis
            if hasattr(zora, "target_is_A"):
                # keep current target unless gap exceeds threshold
                if gap > GAP_EPS:
                    zora.target_is_A = False
                elif gap < -GAP_EPS:
                    zora.target_is_A = True
            else:
                zora.target_is_A = (gap < 0)
            
            target_is_A = zora.target_is_A
            target_phiE = A_phiE if target_is_A else B_phiE
            other_phiE  = B_phiE if target_is_A else A_phiE
            r_now = zora.reward(target_phiE, other_phiE, coh_mean)
            
            # Smooth reward signal
            alpha = 0.2
            if zora.r_smooth is None:
                zora.r_smooth = r_now
            else:
                zora.r_smooth = (1-alpha)*zora.r_smooth + alpha*r_now
            r_now = zora.r_smooth
            
            if not zora.in_trial:
                prev_alloc, prev_pulse = zora.alloc, zora.pulse
                zora.begin_trial()
                zora._prev = (prev_alloc, prev_pulse)
                zora._last_reward = r_now
            else:
                prev_alloc, prev_pulse = zora._prev
                zora.end_trial(r_now, prev_alloc, prev_pulse)
            
            # apply Zora allocation + pulse on chosen target
            if target_is_A:
                phi, eth = zora_allocate(phi, eth, PHI_BUDGET, E_BUDGET, A_mask, alloc_frac=zora.alloc)
                rho, phi, eth = zora_pulse(rho, phi, eth, cx, cy, radius=5, pulse=zora.pulse)
            else:
                phi, eth = zora_allocate(phi, eth, PHI_BUDGET, E_BUDGET, B_mask, alloc_frac=zora.alloc)
                rho, phi, eth = zora_pulse(rho, phi, eth, bx, by, radius=5, pulse=zora.pulse)
    
    Aglob = (nearA_total + farA_total) / max(1, (near_total + far_total))
    Anear = nearA_total / max(1, near_total)
    Afar  = farA_total / max(1, far_total)
    
    # final basin scores
    A_phi, A_eth, A_phiE = basin_sums(phi, eth, cx, cy, radius=18)
    B_phi, B_eth, B_phiE = basin_sums(phi, eth, bx, by, radius=18)
    
    return {
        "Aglob": Aglob, "Anear": Anear, "Afar": Afar, "coh": coh_mean,
        "A_phiE": A_phiE, "B_phiE": B_phiE,
        "alloc": zora.alloc, "pulse": zora.pulse, "bestR": zora.best_reward
    }


def sweep_leak(outfile="zora_limits_leak.csv"):
    # Sweep leakage from gentle → harsh
    leak_values = [0.001, 0.002, 0.003, 0.004, 0.006, 0.008, 0.010, 0.014, 0.018, 0.024]
    print(f"Starting leak sweep with {len(leak_values)} values...")
    import sys
    with open(outfile, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "LEAK", "Aglob", "Anear", "Afar", "coh",
            "A_phiE", "B_phiE", "gap",
            "alloc", "pulse", "bestR"
        ])
        writer.writeheader()
        for i, leak in enumerate(leak_values, 1):
            print(f"[{i}/{len(leak_values)}] Running with LEAK={leak}...", flush=True)
            sys.stdout.flush()
            global LEAK_PHI, LEAK_E
            LEAK_PHI = leak
            LEAK_E   = leak
            res = run_once(seed=7, steps=1500, collapse_bias=3.0, zora_mode="rescue")
            gap = res["A_phiE"] - res["B_phiE"]
            row = {
                "LEAK": leak,
                "Aglob": res["Aglob"], "Anear": res["Anear"], "Afar": res["Afar"],
                "coh": res["coh"],
                "A_phiE": res["A_phiE"], "B_phiE": res["B_phiE"], "gap": gap,
                "alloc": res["alloc"], "pulse": res["pulse"], "bestR": res["bestR"]
            }
            print(f"  Result: gap={gap:.4f}, coh={res['coh']:.4f}, alloc={res['alloc']:.4f}, pulse={res['pulse']:.4f}", flush=True)
            sys.stdout.flush()
            writer.writerow(row)
    print(f"Saved sweep to {outfile}", flush=True)


if __name__ == "__main__":
    main()

