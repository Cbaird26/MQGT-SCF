# Zenodo Description Update

Copy this updated description to your Zenodo deposit at https://zenodo.org/records/18012506

---

## Description

This deposit contains the full reproducibility package for the associated manuscript "Operational Constraints on Ethically-Weighted Quantum Measurement: A Multi-Channel Effective Field Theory Analysis" (GitHub: https://github.com/Cbaird26/MQGT-SCF).

### ⚡ DIRECT ACCESS TO ALL FILES:

**Main Paper:**
- PDF: https://github.com/Cbaird26/MQGT-SCF/raw/main/paper/MQGT_paper_main_v2.pdf
- LaTeX: https://github.com/Cbaird26/MQGT-SCF/blob/main/paper/main.tex

**Complete Theory of Everything (4,824+ pages):**
- ToE + Experiment: https://github.com/Cbaird26/MQGT-SCF/raw/main/theory/ToE_papers/A%20Theory%20of%20Everything%20%2B%20Experiment%20-%20Baird.%2C%20Et%20al%20(2025).pdf
- ToE - C.M. Baird (4,824 pages): https://github.com/Cbaird26/MQGT-SCF/raw/main/theory/ToE_papers/A%20Theory%20of%20Everything%20-%20C.M.%20Baird.%2C%20Et%20al%20(2025).pdf

**Note:** GitHub doesn't render PDFs inline. Use the links above to download directly, or click "Download" on any PDF file in the repository.

### Contents

- **Inference Harnesses**: Complete Python scripts for QRNG, Higgs portal, and fifth-force channel analysis, plus joint multi-channel Bayesian inference
- **Digitized Experimental Data**: CMS HIG-20-003 invisible Higgs decay limits and Lee et al. (2020) short-range gravity constraints in machine-readable format
- **Run Outputs**: MCMC samples, summary statistics, and cryptographic manifests for published results
- **Manifest System**: Hash-based verification tools enabling third-party confirmation that published results match archived code and data
- **Complete Theory of Everything Papers**: Full 4,824+ page theoretical foundation (in `theory/ToE_papers/`)
- **Documentation**: Complete reproducibility guide with step-by-step instructions

### Reproducing Results

All numerical results can be reproduced by:

1. Installing dependencies: `pip install -r code/requirements.txt`
2. Running inference: `python code/inference/mqgt_joint_harness.py run --config joint_config_template.json`
3. Verifying integrity: `python code/inference/mqgt_manifest_sign.py --verify`

See `reproducibility/README.md` for detailed instructions.

### Attestation

The attestation string for the published results is in `reproducibility/ATTESTATION.txt`. This cryptographic signature enables verification that published results match the archived code and data.

### Citation

If you use this package, please cite:

Baird, C. M. (2025). Operational Constraints on Ethically-Weighted Quantum Measurement: A Multi-Channel Effective Field Theory Analysis. GitHub: https://github.com/Cbaird26/MQGT-SCF, Zenodo: 10.5281/zenodo.18012506

---

## Keywords

quantum measurement, effective field theory, Higgs portal, fifth force, reproducibility, Bayesian inference, manifest system, theory of everything, consciousness, scalar fields

## Related Identifiers

- **GitHub**: https://github.com/Cbaird26/MQGT-SCF
- **Related Publication**: [arXiv link when available]

## License

CC-BY-4.0

