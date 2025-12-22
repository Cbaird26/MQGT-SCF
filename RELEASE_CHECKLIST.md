# GitHub Release v1.0 Checklist

## ✅ Files Ready

All files are committed and pushed:
- ✅ `paper.md` - Full text at repo root
- ✅ `reproduce_all.py` - One-command reproduction script
- ✅ `theory/ToE_key_equations.md` - All equations in text format
- ✅ `theory/ToE_canonical_variants.md` - Canon-A vs Canon-B
- ✅ `theory/ToE_summary.md` - Executive summary
- ✅ `README.md` - Updated with front-door links

## 📦 Create Release

**Go to:** https://github.com/Cbaird26/MQGT-SCF/releases/new

### Release Details

**Tag version:** `v1.0`  
**Release title:** `MQGT-SCF v1.0 - Initial Release`

### Description

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
- [Full text (Markdown)](https://github.com/Cbaird26/MQGT-SCF/blob/main/paper.md) - Readable by all tools
- [PDF Download](MQGT_paper_main_v2.pdf) (attached below)

**Reproduce results:**
```bash
git clone https://github.com/Cbaird26/MQGT-SCF.git
cd MQGT-SCF
python reproduce_all.py
```

## Key Equations (Text Format)

All key equations are available in readable markdown:
- [ToE Key Equations](https://github.com/Cbaird26/MQGT-SCF/blob/main/theory/ToE_key_equations.md)
- [Canonical Variants](https://github.com/Cbaird26/MQGT-SCF/blob/main/theory/ToE_canonical_variants.md)
- [Executive Summary](https://github.com/Cbaird26/MQGT-SCF/blob/main/theory/ToE_summary.md)

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

### Attach Files

Upload these PDFs from `paper/` directory:
- `MQGT_paper_main_v2.pdf`
- `MQGT_paper_supplement_v2.pdf`

### Publish

Click **"Publish release"** - this creates a permanent, easily accessible release.

## ✅ Verification

After publishing, verify:
1. Go to: https://github.com/Cbaird26/MQGT-SCF/releases
2. Should see "v1.0" release listed
3. Should see attached PDFs
4. Should see release description

## Why This Matters

- **Releases are easier to fetch** than browsing repo trees
- **Attached files are directly downloadable**
- **Stable URLs** that don't change
- **Works for automated readers** that struggle with GitHub's dynamic UI

---

**After creating the release, update README to link to it:**
`[Latest Release](https://github.com/Cbaird26/MQGT-SCF/releases/latest)`

