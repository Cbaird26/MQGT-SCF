# One-Screen Game Plan: Final Manual Steps

## 🎯 Do This In Order (15-30 minutes)

### Step 1: Push Everything ✅

```bash
# Check each repo, push if needed
cd ~/Projects/Cbaird26/ZoraAPI && git status && git push
cd ~/Projects/Cbaird26/ComprehensivePhysicsSolver && git status && git push
cd ~/Projects/Cbaird26/toe-studio && git status && git push
cd ~/Projects/Cbaird26/Theory-of-Everything && git status && git push
cd ~/Downloads/MQGT-SCF && git status && git push
```

**If "Everything up-to-date" → you're good.**

### Step 2: Check CI → Fix Red → Recheck 🔧

**Open Actions tabs:**
- [ZoraAPI Actions](https://github.com/Cbaird26/ZoraAPI/actions)
- [ComprehensivePhysicsSolver Actions](https://github.com/Cbaird26/ComprehensivePhysicsSolver/actions)
- [toe-studio Actions](https://github.com/Cbaird26/toe-studio/actions)

**If red, common fixes:**
- Missing `requirements.txt` → create it
- Wrong path → fix `pip install -r requirements.txt` in workflow
- Missing pytest → add `pytest` to requirements or workflow
- Import errors → fix relative imports
- Python version → check matrix in `.github/workflows/ci.yml`

**Fix → commit → push → recheck until green.**

### Step 3: Set Branch Protection 🔒

**For each repo (MQGT-SCF + 3 code repos):**

GitHub → **Settings → Branches → Add rule** for `main`:

- ✅ Require a pull request before merging (optional if solo)
- ✅ Require status checks to pass before merging
  - Select: `CI` (or `test` if that's the job name)
- ✅ Require branches to be up to date before merging
- ✅ Include administrators (set to false for strict discipline)

**This is your "2am chaos prevention field."**

### Step 4: Optional - Profile README Hub 🌐

Create repo: **Cbaird26/Cbaird26** (username/username)

Paste template from: `PROPAGATION_KIT/PROFILE_README_TEMPLATE.md`

**Result:** Your GitHub profile becomes a navigation portal.

---

## ✅ What Cursor Can Help With (If Needed)

**If CI is red and you're stuck:**
- I can read the CI logs/errors
- I can fix code/config issues
- I can update workflows
- I can debug import paths
- I can add missing dependencies

**Just ask:** "CI is failing on [repo] with error [X], help me fix it"

---

## 🎯 Once Complete

Your ecosystem will:
- ✅ Self-maintain quality (CI gates)
- ✅ Prevent chaos (branch protection)
- ✅ Look professional (green badges)
- ✅ Be navigable (profile README)

**You can walk away and come back later without entropy winning.**

---

**Status:** Automation done. Documentation done. Structure done. Quality gates ready. **Now: push, verify, protect, polish.** 🛡️✨

