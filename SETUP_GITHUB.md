# Setting Up GitHub Repository

Follow these steps to push your repository to GitHub.

## Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon → "New repository"
3. Repository name: `MQGT-SCF`
4. Description: "Merged Quantum Gauge and Scalar Consciousness Framework - Operational Constraints on Ethically-Weighted Quantum Measurement"
5. Set to **Public** (for visibility) or **Private** (if you prefer)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 2: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /Users/christophermichaelbaird/Downloads/MQGT-SCF

# Add all files
git add .

# Commit
git commit -m "Initial commit: MQGT-SCF publication package with full reproducibility"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/MQGT-SCF.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Add Repository Badges

After pushing, update your README.md with the actual repository URL:

1. Edit `README.md`
2. Replace `[your-username]` with your actual GitHub username
3. Update the repository URL in CITATION.cff
4. Commit and push:

```bash
git add README.md CITATION.cff
git commit -m "Update repository URLs"
git push
```

## Step 4: Add Topics/Tags

On GitHub, click "Add topics" and add:
- `quantum-measurement`
- `effective-field-theory`
- `bayesian-inference`
- `reproducibility`
- `physics`
- `consciousness`

## Step 5: Enable GitHub Pages (Optional)

If you want a website:
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `docs`
4. Save

## Step 6: Link to Zenodo (After Upload)

Once you have a Zenodo DOI:
1. Update `README.md` with actual DOI
2. Update `CITATION.cff` with actual DOI
3. On Zenodo, link to GitHub repository
4. Commit and push changes

## Troubleshooting

**If you get authentication errors:**
- Use GitHub Personal Access Token instead of password
- Or use SSH: `git remote set-url origin git@github.com:YOUR_USERNAME/MQGT-SCF.git`

**If files are too large:**
- Use Git LFS for large data files
- Or add to .gitignore and host separately

**If you want to keep some files private:**
- Use `.gitignore` to exclude sensitive files
- Or use a private repository

## Next Steps

After GitHub is set up:
1. ✅ Add Zenodo DOI when available
2. ✅ Add arXiv link when published
3. ✅ Update badges in README
4. ✅ Add more notebooks for reproducibility
5. ✅ Enable Issues for questions/discussions

