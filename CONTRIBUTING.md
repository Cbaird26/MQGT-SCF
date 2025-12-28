# Contributing to MQGT-SCF

Thank you for your interest in contributing to the MQGT-SCF research program!

## How to Contribute

### Reporting Issues

- **Bug reports:** Use GitHub Issues with clear description and reproduction steps
- **Theoretical questions:** Use GitHub Discussions
- **Experimental proposals:** See `experiments/` directory structure

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Environment

**Installing dependencies:**
- For reproducible builds: `make install` (uses `requirements-lock.txt`)
- For development: `make install-dev` (uses `requirements.txt` + dev deps from `pyproject.toml`)

**Note on dev dependencies:** Dev dependencies are currently specified in `pyproject.toml` under `[project.optional-dependencies]`. For exact reproducibility of dev environment, consider maintaining a `requirements-dev-lock.txt` in the future.

### Code Style

- Follow PEP 8 for Python code
- Use type hints where helpful
- Add docstrings to functions
- Include unit tests for new functionality

### Test Philosophy

Tests in this repository follow strict guidelines to keep the test suite fast and reliable:

- **Fast execution**: Tests must complete in seconds, not minutes. No long-running computations.
- **Fixed seeds**: Use deterministic random seeds (e.g., `seed=42`) for reproducibility.
- **No network calls**: Tests must not require internet access or external services.
- **No large data**: Avoid downloading or generating large datasets. Use minimal synthetic data.
- **Basic invariants**: Focus on checking that outputs are valid (no NaNs, correct types, reasonable bounds) rather than exact numerical values.
- **Isolated**: Each test should be independent and not rely on state from other tests.

**Anti-patterns to avoid:**
- ❌ Tests that train models or run full simulations
- ❌ Tests that download data from the internet
- ❌ Tests that take more than a few seconds
- ❌ Tests without fixed seeds (non-deterministic)
- ❌ Tests that modify global state

**Good test examples:**
- ✅ Import verification
- ✅ Function signature checks
- ✅ Output type and shape validation
- ✅ Basic mathematical invariants
- ✅ Small synthetic data with fixed seeds

### Documentation

- Update README.md if adding major features
- Add to CHANGELOG.md for user-facing changes
- Update theory documentation if adding new equations
- Keep FAQ updated with common questions

### Paper Contributions

- Maintain LaTeX formatting consistency
- Use consistent notation (see `theory/glossary.md`)
- Reference prior work appropriately
- Keep speculative language minimal

## Areas for Contribution

### Experimental

- QRNG experimental protocols
- Microtubule coherence measurement designs
- Neural entanglement detection methods
- Gravitational wave analysis

### Theoretical

- Additional field equation solutions
- Cosmological implications
- Dark matter/dark energy connections
- QCD embedding details

### Computational

- Performance optimizations
- Additional inference methods
- Extended simulation capabilities
- Visualization tools

### Documentation

- Tutorial notebooks
- Video walkthroughs
- Educational materials
- Reviewer guides

## Code of Conduct

- Be respectful and professional
- Focus on scientific merit
- Welcome diverse perspectives
- Maintain constructive dialogue

## License

By contributing, you agree that your contributions will be licensed under CC-BY-4.0, the same license as the project.

## Questions?

Open an issue or contact the author. We're happy to help!

---

**Thank you for contributing to open science!**

