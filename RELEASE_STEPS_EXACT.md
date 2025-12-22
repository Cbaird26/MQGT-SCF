# Create GitHub Release v1.0 — Exact Steps

## ✅ OPTION A — Browser (Recommended, 2-3 minutes)

### Step 1: Open Release Page

👉 **https://github.com/Cbaird26/MQGT-SCF/releases/new**

### Step 2: Fill Fields EXACTLY

**Tag version:**
```
v1.0
```

**Target:**
```
main
```

**Release title:**
```
MQGT-SCF v1.0 — Initial Public Release
```

### Step 3: Paste Description

Copy **entire contents** of `RELEASE_DESCRIPTION_FINAL.md` and paste into the "Release description" field.

### Step 4: Upload PDFs

Drag and drop **both** files:
- `paper/MQGT_paper_main_v2.pdf`
- `paper/MQGT_paper_supplement_v2.pdf`

### Step 5: Click "Publish release"

**Important:** Make sure you click **"Publish release"** (green button at bottom), not "Save draft"

---

## ✅ OPTION B — GitHub CLI (If you prefer terminal)

```bash
# First, authenticate (if not already done)
gh auth login

# Create release
gh release create v1.0 \
  paper/MQGT_paper_main_v2.pdf \
  paper/MQGT_paper_supplement_v2.pdf \
  --title "MQGT-SCF v1.0 — Initial Public Release" \
  --notes-file RELEASE_DESCRIPTION_FINAL.md
```

---

## ✅ Verify Release is Live

After publishing, check:

👉 **https://github.com/Cbaird26/MQGT-SCF/releases**

**If you see:**
- ✅ Card titled "MQGT-SCF v1.0 — Initial Public Release"
- ✅ Attached PDFs visible
- ✅ Release description shown

**Then it's live!** The release URL will be:
`https://github.com/Cbaird26/MQGT-SCF/releases/tag/v1.0`

**If you see:**
- ❌ "There aren't any releases here"

Then the release wasn't published yet. Go back and click "Publish release".

---

## What Changes When Release is Live

✅ Releases page no longer says "There aren't any releases here"  
✅ Stable download URLs exist  
✅ Reviewers can cite "MQGT-SCF v1.0"  
✅ Automated systems can fetch files  
✅ Access problem permanently closed

---

**After publishing, tell me "release is live" and I'll verify it immediately.**

