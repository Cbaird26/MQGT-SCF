# TensorFlow Fix (Ready to Apply if CI Fails)

## If ComprehensivePhysicsSolver CI Fails on TensorFlow Install

**Apply this fix instantly:**

### Step 1: Split Requirements

**Create `requirements.txt` (core, light):**
```txt
streamlit
numpy
pandas
scikit-learn
matplotlib
scipy
```

**Create `requirements-optional-ml.txt` (heavy extras):**
```txt
tensorflow
qiskit
```

### Step 2: Update CI Workflow

**In `.github/workflows/ci.yml`, change:**
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    python -m pip install pytest pytest-cov streamlit
```

**To:**
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    python -m pip install pytest pytest-cov streamlit
    # Optional ML deps (install if file exists, but don't fail if missing)
    if [ -f "requirements-optional-ml.txt" ]; then
      python -m pip install -r requirements-optional-ml.txt || echo "Optional ML deps failed (non-critical)"
    fi
```

### Step 3: Commit & Push

```bash
cd ~/Projects/Cbaird26/ComprehensivePhysicsSolver
git add requirements.txt requirements-optional-ml.txt .github/workflows/ci.yml
git commit -m "chore: split TensorFlow into optional ML deps for lighter CI"
git push
```

---

**Status:** Fix ready. Only apply if CI actually fails on TensorFlow install. 🧯

