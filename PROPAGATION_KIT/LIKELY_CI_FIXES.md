# Likely CI Fixes (Quick Reference)

## ComprehensivePhysicsSolver

### TensorFlow Install Failure
**Symptom:** CI fails during `pip install` with TensorFlow wheel/version errors

**Quick Fix:**
- Move TensorFlow to optional: `requirements-ml.txt`
- Keep `requirements.txt` light (streamlit, numpy, pandas, scikit-learn, matplotlib, scipy)
- Update CI workflow to install base deps only (or make ML deps optional)

**Or:** Pin TensorFlow version: `tensorflow==2.13.0` (or compatible version)

## toe-studio / ZoraAPI

### Missing Requirements File
**Symptom:** `ERROR: Could not open requirements file`

**Quick Fix:**
- Check workflow path: `pip install -r requirements.txt`
- Verify file exists at repo root
- Or update workflow to correct path

### Import Error (ModuleNotFoundError)
**Symptom:** `ModuleNotFoundError: No module named '...'`

**Quick Fix:**
- Add missing dependency to `requirements.txt`
- Or adjust import paths in workflow (add `PYTHONPATH`)

### Pytest Fails (No Tests)
**Symptom:** `pytest` fails because no tests directory exists

**Quick Fix:**
- Make workflow graceful: `pytest tests/ || echo "No tests yet"`
- Or create minimal `tests/__init__.py` and `tests/test_smoke.py`

## Quick Fix Commands

**If TensorFlow is the issue:**
```bash
# Split requirements
echo "tensorflow" > requirements-ml.txt
# Remove from requirements.txt
# Update CI to install base only
```

**If import path is the issue:**
```bash
# Add to workflow before imports:
- name: Set PYTHONPATH
  run: echo "PYTHONPATH=${{ github.workspace }}" >> $GITHUB_ENV
```

**If tests are the issue:**
```bash
# Make workflow graceful:
- name: Run tests
  run: |
    if [ -d "tests" ]; then
      pytest tests/ || exit 1
    else
      echo "No tests yet" && exit 0
    fi
```

---

**Ready to fix any failures you report.** Just paste the 3-line snippet and I'll provide the exact fix. 🛠️

