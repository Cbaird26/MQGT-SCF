# Creating GitHub Release v1.0

Follow these steps to create the GitHub Release that makes everything easily accessible:

## Step 1: Create Release on GitHub

1. Go to: https://github.com/Cbaird26/MQGT-SCF/releases/new
2. **Tag version:** `v1.0`
3. **Release title:** `MQGT-SCF v1.0 - Initial Release`
4. **Description:** Copy from `RELEASE_NOTES.md` (or use template below)

## Step 2: Attach Files

Upload these files from `releases/v1.0/`:
- `MQGT_paper_main_v2.pdf`
- `MQGT_paper_supplement_v2.pdf`

Or attach from `paper/` directory:
- `MQGT_paper_main_v2.pdf`
- `MQGT_paper_supplement_v2.pdf`

## Step 3: Release Notes Template

```markdown
# MQGT-SCF v1.0 - Initial Release

**Canonical Citation:** DOI [10.5281/zenodo.18012506](https://zenodo.org/records/18012506)

## What's Included

- **Main Paper PDF** - Operational constraints on ethically-weighted quantum measurement
- **Supplement PDF** - Supplementary material and additional results
- **Complete Code** - All inference harnesses and simulation code
- **Full Data** - Digitized experimental constraints
- **Theory of Everything Papers** - Complete 4,824+ page theoretical foundation

## Quick Start

**Read the paper:**
- [Full text (Markdown)](https://github.com/Cbaird26/MQGT-SCF/blob/main/paper.md)
- [PDF Download](MQGT_paper_main_v2.pdf) (attached)

**Reproduce results:**
```bash
git clone https://github.com/Cbaird26/MQGT-SCF.git
cd MQGT-SCF
python reproduce_all.py
```

## Files

- `MQGT_paper_main_v2.pdf` - Main manuscript
- `MQGT_paper_supplement_v2.pdf` - Supplementary material

## Citation

```bibtex
@software{baird2025mqgt,
  author = {Baird, Christopher Michael},
  title = {MQGT-SCF: Operational Constraints on Ethically-Weighted Quantum Measurement},
  year = {2025},
  version = {1.0},
  url = {https://github.com/Cbaird26/MQGT-SCF},
  doi = {10.5281/zenodo.18012506}
}
```

## Links

- **Repository:** https://github.com/Cbaird26/MQGT-SCF
- **Zenodo:** https://zenodo.org/records/18012506
- **Full Theory:** See `theory/ToE_papers/` directory
```

## Step 4: Publish

Click "Publish release" - this creates a permanent, easily accessible release that automated tools can fetch reliably.

## Why This Works

- **Releases are easier to fetch** than browsing repo trees
- **Attached files are directly downloadable**
- **Stable URLs** that don't change
- **Works for automated readers** that struggle with GitHub's dynamic UI

---

After creating the release, update your README to link to it:
`[Latest Release](https://github.com/Cbaird26/MQGT-SCF/releases/latest)`

