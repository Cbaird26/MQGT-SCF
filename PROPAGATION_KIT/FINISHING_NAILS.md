# Finishing Nails: CI Verification & Branch Protection

## 1. Verify CI is Green ✅

**Action Required:** Check GitHub Actions for these 3 repos:

- [ ] [ZoraAPI Actions](https://github.com/Cbaird26/ZoraAPI/actions)
- [ ] [ComprehensivePhysicsSolver Actions](https://github.com/Cbaird26/ComprehensivePhysicsSolver/actions)
- [ ] [toe-studio Actions](https://github.com/Cbaird26/toe-studio/actions)

**If CI fails:**
- Fix missing dependencies in `requirements.txt`
- Fix import path issues
- Fix syntax errors caught by `compileall`
- **Do not merge until green** - early CI failures create "broken window" effect

**CI badges added to READMEs** - they will show red until first successful run.

## 2. CI Badges Added ✅

CI badges have been added to all 3 code repo READMEs:
- ZoraAPI
- ComprehensivePhysicsSolver
- toe-studio

**Note:** Badges will show red until CI runs successfully. Verify CI is green before considering this complete.

## 3. Branch Protection Setup (Recommended)

### Manual Setup (GitHub Web UI)

For each of the 3 code repos, go to:
**Settings → Branches → Add rule**

**Rule for `main` branch:**
- ✅ Require a pull request before merging
- ✅ Require approvals: 0 (or 1 if you want extra discipline)
- ✅ Require status checks to pass before merging
  - Select: `CI` (or `test` if that's the job name)
- ✅ Require branches to be up to date before merging
- ✅ Include administrators (optional - set to false for strict discipline)

**Rule for `develop` branch (if used):**
- Same as above, or less strict (status checks optional)

### Via GitHub CLI (if `gh` is available)

```bash
# For each repo
gh api repos/Cbaird26/ZoraAPI/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["CI"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":0}' \
  --field restrictions=null
```

### Why This Matters

- **Prevents broken main** - CI must pass before merge
- **Enforces PR discipline** - Even solo, PRs create reviewable history
- **Prevents force-push accidents** - Protected branches can't be force-pushed
- **Creates "civilized under pressure"** - System enforces quality even when you're rushing

## 4. Optional: GitHub Profile README (Tier Higher)

Create a repository named exactly: `Cbaird26/Cbaird26` (username/username)

This becomes your GitHub profile README that shows on your profile page.

**Template:**

```markdown
# Theory of Everything Research & Engineering

> **Canonical Repository:** [MQGT-SCF](https://github.com/Cbaird26/MQGT-SCF)

## Start Here

- **[MQGT-SCF](https://github.com/Cbaird26/MQGT-SCF)** - Core theory, experiments, and reproducibility

## Active Projects

- **[ZoraAPI](https://github.com/Cbaird26/ZoraAPI)** - API library for Zora consciousness system
- **[ComprehensivePhysicsSolver](https://github.com/Cbaird26/ComprehensivePhysicsSolver)** - Unified physics solver
- **[toe-studio](https://github.com/Cbaird26/toe-studio)** - Interactive ToE visualization studio

## Theory & Papers

- **[Theory-of-Everything](https://github.com/Cbaird26/Theory-of-Everything)** - Papers and documentation

## Archive

- Legacy simulations and experimental repos (see individual repos for status)

---

**All repos follow MQGT-SCF standards:** CI gates, reproducible builds, clear canonical pointers.
```

This turns your GitHub into an **intentional public artifact** rather than a list of repositories.

## Status Checklist

- [x] CI workflows added to 3 code repos
- [x] CI badges added to READMEs
- [ ] **Verify CI is green** (manual check required)
- [ ] **Set branch protection** (manual setup recommended)
- [ ] **Create profile README** (optional tier-higher move)

## Result

Once CI is green and branch protection is set:
- ✅ **Machine-reliable** - CI gates prevent broken code
- ✅ **Disciplined** - PRs required, status checks enforced
- ✅ **Professional** - Green badges signal trust
- ✅ **Legible** - Profile README provides navigation

**This is "civilized under pressure" - the system enforces quality even when you're rushing.** 🛡️✨

