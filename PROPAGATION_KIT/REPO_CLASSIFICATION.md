# Repository Classification Guide

Classify each repo into one of three categories before applying standards.

## Category A: Active / Matters

**Gets:** Full "MQGT-SCF-lite" treatment
- Status banner
- Cursor rules
- Policies (or "see canonical" versions)
- CI (if has runnable code)
- Issue templates (optional)
- Makefile (if has workflows)

**Examples:**
- ZoraAPI (active API/library)
- zora-theory-of-everything (active application)
- Theory-of-Everything (if still maintained)
- toe-studio / quantum-lab (if actively developed)

## Category B: Mirror / Archive

**Gets:** Status banner only
- Clear "Archived" or "Mirror" status
- Link to canonical
- One-sentence purpose
- What it's NOT for

**Examples:**
- Old ToE mirrors
- Historical snapshots
- Deprecated versions

## Category C: Empty / Placeholder

**Gets:** Archive or delete
- Either delete if truly empty
- Or archive with minimal README: "This repository is archived. See [canonical]."

**Examples:**
- Repos with only LICENSE
- Placeholder repos
- Abandoned experiments

## Classification Checklist

For each repo, answer:

1. **Is it actively maintained?** → Category A
2. **Is it a historical snapshot?** → Category B
3. **Is it empty/abandoned?** → Category C

## Decision Matrix

| Has Code? | Actively Used? | Purpose? | Category |
|-----------|----------------|----------|----------|
| Yes | Yes | Clear | A (Active) |
| Yes | No | Historical | B (Archive) |
| No | No | None | C (Delete/Archive) |
| No | Yes | Docs only | A (but no CI) |

## Perfection Definition

A repo is "perfect" when:
- ✅ Clear identity (one word: Canonical/App/Library/Legacy)
- ✅ Clear pointer (if not canonical: link to MQGT-SCF)
- ✅ Minimal quality floor:
  - LICENSE (correct)
  - README (non-empty, has quick start or says "archived")
  - Security + CoC policy link
  - CI only if runnable code
  - Issue templates (optional for small repos)

**That's it. Everything else is bonus.**

