# Flip The Switches: Final Execution Checklist

## 🎯 Do This Now (In Order)

### Step 1: Push Remaining Commits

**For each repo:**

```bash
cd ~/Projects/Cbaird26/[REPO]
git status
git add -A  # only if status shows changes
git commit -m "chore: finalize propagation changes"  # only if needed
git push
```

**Repos to check:**
- [ ] ZoraAPI
- [ ] ComprehensivePhysicsSolver (has uncommitted `OMNISOLVE` - check it first)
- [ ] toe-studio
- [ ] Theory-of-Everything
- [ ] MQGT-SCF

**Note on `OMNISOLVE` file:**
- If it's legit project content → commit it
- If it's accidental/scratch → delete or add to `.gitignore`
- If unsure → open it and decide

### Step 2: Verify CI Goes Green

**Check Actions tabs:**
- [ ] [ZoraAPI Actions](https://github.com/Cbaird26/ZoraAPI/actions) - Latest run on `main`?
- [ ] [ComprehensivePhysicsSolver Actions](https://github.com/Cbaird26/ComprehensivePhysicsSolver/actions) - Latest run on `main`?
- [ ] [toe-studio Actions](https://github.com/Cbaird26/toe-studio/actions) - Latest run on `main`?

**If any are red:**
1. Open the failed job
2. Find the first real error (not cascade)
3. Tell Cursor: "CI is failing on [repo] with error [X], help me fix it"
4. Fix → commit → push → recheck

### Step 3: Set Branch Protection 🔒

**For each repo (MQGT-SCF + 3 code repos):**

GitHub → **Settings → Branches → Add rule** for `main`:

- [ ] ✅ Require status checks to pass before merging
  - Select: `CI` (or `test` if that's the job name)
- [ ] ✅ Require branches to be up to date before merging
- [ ] ✅ Require pull request before merging (optional but recommended)
- [ ] ✅ Include administrators (set to false for strict discipline)

**This is your "2am chaos prevention field."**

### Step 4: Optional - Profile README Hub 🌐

- [ ] Create repo: **Cbaird26/Cbaird26** (username/username)
- [ ] Paste template from: `PROPAGATION_KIT/PROFILE_README_TEMPLATE.md`

**Result:** Your GitHub profile becomes a navigation portal.

---

## ✅ What Cursor Can Help With

**If CI is red:**
- ✅ Read CI logs/errors
- ✅ Fix code/config issues
- ✅ Update workflows
- ✅ Debug import paths
- ✅ Add missing dependencies

**Just ask:** "CI is failing on [repo] with error [X], help me fix it"

---

## ❌ What Cursor Cannot Do

**GitHub governance (you must do):**
- ❌ Enable branch protection rules
- ❌ Change repo settings in GitHub UI
- ❌ Merge PRs "as you"
- ❌ Access secrets/tokens safely

**Cursor is your repo mechanic and CI firefighter.**
**You are the governor (branch rules + settings).**

---

## 🎯 Once Complete

Your ecosystem will:
- ✅ Self-maintain quality (CI gates)
- ✅ Prevent chaos (branch protection)
- ✅ Look professional (green badges)
- ✅ Be navigable (profile README)

**You can walk away and come back later without entropy winning.**

---

**Status:** Ready to flip the switches. Automation done. Documentation done. Structure done. **Now: push, verify, protect, polish.** 🛡️✨

