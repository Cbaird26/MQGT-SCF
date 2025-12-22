# Operational Constraints on Ethically-Weighted Quantum Measurement: A Multi-Channel Effective Field Theory Analysis

**Author:** Christopher Michael Baird  
**GitHub:** https://github.com/Cbaird26/MQGT-SCF  
**Zenodo DOI:** 10.5281/zenodo.18012506  
**License:** CC-BY-4.0

---

## Abstract

We investigate a class of effective modifications to quantum measurement in which outcome probabilities are weakly biased by an auxiliary scalar label that encodes "ethical" or valence-like structure. We formulate the proposal in an explicitly operational way, and embed it within a conservative effective field theory (EFT) extension of the Standard Model and General Relativity that admits a clean decoupling limit. We derive likelihood-level predictions for three experimentally independent channels: (i) quantum random number generators (QRNGs), (ii) invisible Higgs decays via a Higgs-portal coupling, and (iii) short-range tests of Newtonian gravity parameterized by Yukawa deviations. Using published results for Higgs invisible branching fractions and short-range inverse-square-law tests, we obtain conservative constraints on the corresponding EFT couplings and force ranges. We emphasize transparent statistical assumptions and provide a reproducibility package (hash manifests and verification scripts) suitable for preregistration and third-party audit.

---

## 1. Introduction

The Born rule is the central probabilistic postulate of quantum mechanics: given a state expanded in an orthonormal measurement basis $\{ |i\rangle \}$ as $|\psi\rangle=\sum_i c_i |i\rangle$, the probability of outcome $i$ is $P(i)=|c_i|^2$. While extraordinarily successful, the Born rule is, operationally, an empirical law. A broad research program asks whether small deviations from standard measurement statistics might be detectable, or at least bounded, by experiments. Examples include dynamical collapse models and phenomenological tests of non-standard measurement rules.

This work considers a specific *operational* deformation of the Born rule motivated by the hypothesis that outcomes can be weakly biased by a scalar "valence" label $E_i$ assigned to each outcome. The interpretation of $E_i$ is deliberately left minimal: it is a real number that can encode, in principle, any externally specified classification of outcomes. The central question is then straightforward and testable:

> Do measured frequencies exhibit deviations consistent with a fixed outcome-label bias parameter?

We proceed in three steps. First, we define an ethically-weighted measurement rule and derive the corresponding inference problem for QRNG data. Second, we embed the bias within a conservative EFT framework by coupling a real scalar $S$ to the Higgs sector (a standard portal construction) and constrain the portal coupling with invisible Higgs decay limits. Third, we connect a light mediator to the standard Yukawa parameterization of short-range gravity tests and incorporate laboratory constraints.

---

## 2. Ethically-Weighted Measurement Rule

We define the ethically-weighted Born rule:

$$P(i) = \frac{|c_i|^2 e^{\eta E_i}}{\sum_j |c_j|^2 e^{\eta E_j}}$$

where $\eta$ is a real coupling parameter and $E_i \in \mathbb{R}$ is a pre-assigned outcome label. The standard Born rule is recovered for $\eta \to 0$.

For a two-outcome experiment with labels $E_1, E_0$ and baseline amplitudes $|c_1|^2=|c_0|^2=\frac{1}{2}$:

$$\log\frac{P(1)}{P(0)} = \eta (E_1-E_0)$$

In the small-$\eta$ regime, $P(1)\approx \frac{1}{2} + \eta\Delta E/4$ with $\Delta E=E_1-E_0$.

### 2.1 QRNG Likelihood and Sensitivity Scaling

Given $N$ independent trials with $N_1$ outcomes labeled "1", the likelihood is binomial:

$$\mathcal{L}(\eta \mid N_1,N) \propto P(1)^{N_1} [1-P(1)]^{N-N_1}$$

with $P(1)$ computed from the ethically-weighted Born rule above. A convenient estimator in the balanced-amplitude case is:

$$\hat{\eta} \approx \frac{2(N_1-N_0)}{N \Delta E}$$

and the binomial (shot-noise) sensitivity scales as:

$$\sigma_\eta \approx \frac{2}{\sqrt{N}\,\Delta E}$$

---

## 3. EFT Embedding and Collider Constraint

We now embed the framework in a conservative EFT extension that supports collider constraints. Consider a real scalar $S$ with a Higgs-portal interaction:

$$\mathcal{L}_{\mathrm{portal}} = - g_\phi \, S^2 \, H^\dagger H$$

where $H$ is the Standard Model Higgs doublet and $g_\phi$ is dimensionless. After electroweak symmetry breaking, $H^\dagger H = (v+h)^2/2$ generates an $hS^2$ coupling with effective vertex $\lambda_{hSS}=2g_\phi v$.

For $m_S < m_h/2$, the Higgs partial width to invisible scalars is:

$$\Gamma(h\to SS)=\frac{g_\phi^2 v^2}{8\pi m_h}\sqrt{1-\frac{4m_S^2}{m_h^2}}$$

The invisible branching fraction is $B_{\mathrm{inv}}=\Gamma_{\mathrm{inv}}/(\Gamma_{\mathrm{SM}}+\Gamma_{\mathrm{inv}})$. We use $\Gamma_{\mathrm{SM}}\simeq 4.07~\mathrm{MeV}$ for the Standard Model Higgs total width.

### 3.1 CMS HIG-20-003 Constraint

CMS reports a combined 2012--2018 limit $B(H\to \mathrm{inv})<0.18$ at 95% CL (assuming Standard Model production) and a best-fit value $B(H\to \mathrm{inv})=0.086^{+0.054}_{-0.052}$. We approximate the published one-dimensional profile likelihood ratio with an asymmetric Gaussian in $B$.

### 3.2 Constraint on $g_\phi$

Assuming a uniform prior on $g_\phi\in[0,0.01]$ and a light scalar mass $m_S\ll m_h/2$, we map $g_\phi\mapsto B_{\mathrm{inv}}$ via the width formula above and form the posterior $p(g_\phi)\propto \exp[-q(B(g_\phi))/2]$. We obtain the conservative 95% (97.5%) credible upper bounds:

$$g_\phi < 6.5\times 10^{-3}\quad (6.9\times 10^{-3})$$

under the stated prior and likelihood approximation.

---

## 4. Short-Range Gravity: Yukawa Deviations

Laboratory tests of the inverse-square law constrain additional Yukawa contributions to the Newtonian potential:

$$V(r)=-\frac{Gm_1m_2}{r}\left[1+\alpha\,e^{-r/\lambda}\right]$$

where $\alpha$ is the strength relative to gravity and $\lambda$ is the force range (often $\lambda=\hbar c/m$ for a mediator of mass $m$).

Lee *et al.* performed a torsion-balance test down to $52~\mu$m and report that any *gravitational-strength* Yukawa interaction (i.e. $|\alpha|=1$) must satisfy $\lambda<38.6~\mu$m at 95% confidence. Translating $\lambda$ into a mediator mass gives:

$$m \gtrsim \frac{\hbar c}{\lambda} \approx 5.1~\mathrm{meV}\qquad (\alpha=1\ \text{case})$$

---

## 5. Results Summary

### Parameter Constraints

| Parameter | Symbol | 95% CL Bound | Channel |
|-----------|--------|--------------|---------|
| Ethics-collapse coupling | $\eta$ | — | QRNG (to be tested) |
| Higgs-portal coupling | $g_\phi$ | $< 6.5 \times 10^{-3}$ | CMS invisible decays |
| Scalar mass | $m_S$ | $> 5.1$ meV | Fifth-force tests |

### Key Equations

**Ethically-Weighted Born Rule:**
$$P(i) = \frac{|c_i|^2 e^{\eta E_i}}{\sum_j |c_j|^2 e^{\eta E_j}}$$

**Higgs Portal Lagrangian:**
$$\mathcal{L}_{\mathrm{portal}} = - g_\phi \, S^2 \, H^\dagger H$$

**Yukawa Potential:**
$$V(r)=-\frac{Gm_1m_2}{r}\left[1+\alpha\,e^{-r/\lambda}\right]$$

---

## 6. Falsifiable Predictions

1. **QRNG Channel:** Statistical deviations in quantum random number generators correlated with ethical context labels, with sensitivity $\sigma_\eta \approx 2/\sqrt{N}$ for $\Delta E = 1$.

2. **Higgs Channel:** Invisible Higgs decay branching fraction $B(H\to\mathrm{inv})$ constrained by CMS data, yielding $g_\phi < 6.5 \times 10^{-3}$.

3. **Fifth-Force Channel:** Short-range gravity tests constrain Yukawa deviations, requiring $\lambda < 38.6~\mu$m for gravitational-strength interactions.

---

## 7. Reproducibility

All numerical results can be reproduced using the provided inference harnesses, digitized experimental data, and analysis scripts. See `reproducibility/README.md` for detailed instructions.

**Quick Reproduce:**
```bash
git clone https://github.com/Cbaird26/MQGT-SCF.git
cd MQGT-SCF
pip install -r requirements.txt
cd code/inference
python mqgt_joint_harness.py run --config joint_config_template.json
```

---

## 8. Limitations and Assumptions

- **Small Parameter Regime:** $\eta \ll 1$, $g_\phi \ll 1$ (perturbative)
- **Decoupling Limit:** Standard physics recovered as couplings $\to 0$
- **Locality:** All interactions are local (no superluminal signaling)
- **EFT Framework:** Valid at accessible energy scales

---

## 9. Citation

```bibtex
@software{baird2025mqgt,
  author = {Baird, Christopher Michael},
  title = {MQGT-SCF: Operational Constraints on Ethically-Weighted Quantum Measurement},
  year = {2025},
  url = {https://github.com/Cbaird26/MQGT-SCF},
  doi = {10.5281/zenodo.18012506}
}
```

---

## 10. Full Paper Access

**PDF Downloads:**
- [Main Paper PDF](https://github.com/Cbaird26/MQGT-SCF/raw/main/paper/MQGT_paper_main_v2.pdf)
- [Supplement PDF](https://github.com/Cbaird26/MQGT-SCF/raw/main/paper/MQGT_paper_supplement_v2.pdf)

**Complete Theory of Everything (4,824+ pages):**
- [ToE + Experiment](https://github.com/Cbaird26/MQGT-SCF/raw/main/theory/ToE_papers/A%20Theory%20of%20Everything%20%2B%20Experiment%20-%20Baird.%2C%20Et%20al%20(2025).pdf)
- [ToE - C.M. Baird (4,824 pages)](https://github.com/Cbaird26/MQGT-SCF/raw/main/theory/ToE_papers/A%20Theory%20of%20Everything%20-%20C.M.%20Baird.%2C%20Et%20al%20(2025).pdf)

**LaTeX Source:**
- [Main Paper LaTeX](https://github.com/Cbaird26/MQGT-SCF/blob/main/paper/main.tex)
- [Supplement LaTeX](https://github.com/Cbaird26/MQGT-SCF/blob/main/paper/supplement.tex)

---

**For complete theoretical foundation, see `theory/ToE_papers/` directory.**

