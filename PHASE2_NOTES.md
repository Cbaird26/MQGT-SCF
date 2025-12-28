# Phase 2 Notes & Quality Checks

## ✅ Completed

1. **pyproject.toml** - Standard Python project structure
2. **Makefile** - Frictionless workflows
3. **Docs landing improvements** - Concise "Start Here" map
4. **Symbol index** - Reviewer-friendly reference

## ⚠️ Quality Checks to Address

### 1. Dev Dependencies Determinism

**Issue:** `make install-dev` installs from `requirements.txt` + `pyproject.toml` dev deps, but these can drift.

**Options:**
- Maintain `requirements-dev-lock.txt` (exact dev deps)
- Standardize on `pip-tools` later (generate from `requirements.in`)
- Document current approach in CONTRIBUTING.md

**Status:** Not urgent, but should be addressed to prevent "mystery meat" dev environment.

**Action:** Add note to CONTRIBUTING.md about dev deps, consider `requirements-dev-lock.txt` in future.

### 2. Golden Test Verification

**Test:** Fresh venv → `make install` → `make test` → `make reproduce`

**Status:** Needs end-to-end verification on clean environment.

**Action:** Should be tested before marking Phase 2 complete.

## 📊 Phase 2 Progress

- ✅ pyproject.toml (tooling standard)
- ✅ Makefile (muscle memory)
- ✅ Docs landing (human navigation)
- ✅ Symbol index (reviewer support)
- ⏳ Type hints (long-term safety - incremental)

## 🎯 Remaining: Type Hints

**Approach:** Incremental, start with public functions and hot paths.

**Priority:**
1. Public API functions in `code/inference/`
2. Public API functions in `code/simulations/`
3. Key functions in `reproduce_all.py`

**Tooling:** Can add mypy/pyright later (warn-first, gradual adoption).

---

**Status:** Phase 2 is 80% complete. Docs and symbol index dramatically improve comprehension.

