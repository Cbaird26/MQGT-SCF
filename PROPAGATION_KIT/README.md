# MQGT-SCF Propagation Kit

Standardized assets for propagating quality standards across repositories.

## What This Is

A minimal, copy-paste set of files that establish:
- Clear identity and status
- Quality floor (LICENSE, README, policies)
- Cursor rules for maintainer discipline
- CI (only for code repos)
- Issue templates (optional)

## Usage

### Step 1: Classify Repo

Determine category:
- **Active** - Gets full "MQGT-SCF-lite" treatment
- **Mirror/Archive** - Gets status banner only
- **Empty/Placeholder** - Archive or delete

### Step 2: Apply Status Banner

Add to top of README.md:

```markdown
> **Status:** [Active / Archived / Mirror / Experimental]  
> **Canonical:** [MQGT-SCF link if not canonical]  
> **Purpose:** [One sentence]  
> **Not for:** [What it's not]
```

### Step 3: Copy Kit Files (Active repos only)

- `.cursor/rules/00-core.mdc` (always)
- `.cursor/rules/*` (full pack if desired)
- `SECURITY.md` (or "see canonical" version)
- `CODE_OF_CONDUCT.md` (or "see canonical" version)
- `.github/ISSUE_TEMPLATE/*` (optional)
- `.github/workflows/ci.yml` (only if repo has runnable code)
- `Makefile` (only if repo has runnable workflows)

## Files in This Kit

- `README_BANNER_TEMPLATE.md` - Status banner template
- `SECURITY_SHORT.md` - Short "see canonical" version
- `CODE_OF_CONDUCT_SHORT.md` - Short "see canonical" version
- `cursor_rules/` - Cursor rules pack
- `ci_workflow_minimal.yml` - Minimal CI for code repos

## Principles

1. **No CI for docs-only repos** - Avoid meaningless failures
2. **Banners first** - Clarity before features
3. **Minimal viable** - Don't over-engineer small repos
4. **Canonical pointer** - Always link to MQGT-SCF if not canonical

