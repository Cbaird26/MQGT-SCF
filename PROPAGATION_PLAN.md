# Propagation Plan: MQGT-SCF Standards → All Repos

## Goal

Propagate quality standards from MQGT-SCF to all repos without multiplying maintenance burden.

## 3-Pass Execution

### Pass 1: Classify Every Repo (15 minutes, zero code)

**Bucket A: Active / Matters** (gets real upgrades)
- [ ] ZoraAPI
- [ ] zora-theory-of-everything
- [ ] Theory-of-Everything (if still maintained)
- [ ] A-Theory-of-Everything (if still maintained)
- [ ] toe-studio / quantum-lab (if actively developed)

**Bucket B: Mirror / Archive** (gets redirect banner + archived)
- [ ] Old ToE mirrors
- [ ] Historical snapshots
- [ ] Deprecated versions

**Bucket C: Empty / Placeholder** (delete/merge or archive)
- [ ] Repos with only LICENSE
- [ ] Abandoned experiments

**Perfection = No repo is ambiguous**

### Pass 2: Apply Status Banner Everywhere (highest ROI)

For every non-canonical repo, add 10-line banner at top of README:

```markdown
> **Status:** [Active / Archived / Mirror / Experimental]
> **Canonical:** [MQGT-SCF link]
> **Purpose:** [One sentence]
> **Not for:** [One sentence - prevents misinterpretation]
```

**This alone makes GitHub "feel" coherent and professional.**

### Pass 3: Upgrade Only Active Repos to "MQGT-SCF-lite"

For Active repos, copy minimal version:

**Always add:**
- ✅ `.cursor/rules/00-core.mdc` (or full pack)
- ✅ `SECURITY.md` + `CODE_OF_CONDUCT.md` (or "see canonical" versions)
- ✅ `.github/ISSUE_TEMPLATE/` (optional but nice)

**Add only if applicable:**
- ✅ CI (only if repo has runnable code)
- ✅ Makefile (only if repo has runnable workflows)

## Propagation Kit Location

All assets ready in: `PROPAGATION_KIT/`

- `README_BANNER_TEMPLATE.md` - Banner template
- `SECURITY_SHORT.md` - "See canonical" version
- `CODE_OF_CONDUCT_SHORT.md` - "See canonical" version
- `cursor_rules/00-core.mdc` - Cursor rules
- `ci_workflow_minimal.yml` - Minimal CI
- `APPLY_BANNER.sh` - Quick banner application script
- `REPO_CLASSIFICATION.md` - Classification guide

## Execution Order

1. **Classify** - List all repos, assign categories
2. **Banners first** - Apply to all repos (fast, high impact)
3. **Upgrade active** - Copy kit files to Category A repos only

## What "Perfected cbaird26" Looks Like

✅ Clicking any repo, stranger immediately knows:
- Is this canonical?
- Is this alive?
- Where do I start?

✅ No "mystery repos" with no README
✅ No repo contradicts licensing/citation
✅ Only repos that benefit from CI have CI

## Next Steps

1. Identify all repos (GitHub + local)
2. Classify each (A/B/C)
3. Start with 5-8 repos you care about most
4. Apply banners first, then upgrades

---

**Status:** Ready to execute. Kit prepared. 🛠️✨

