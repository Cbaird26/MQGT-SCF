# Check CI Status

## Quick Links

**Open these in your browser:**

1. [ZoraAPI Actions](https://github.com/Cbaird26/ZoraAPI/actions)
2. [ComprehensivePhysicsSolver Actions](https://github.com/Cbaird26/ComprehensivePhysicsSolver/actions)
3. [toe-studio Actions](https://github.com/Cbaird26/toe-studio/actions)

## What to Look For

**For each repo:**
1. Click the Actions tab
2. Find the most recent workflow run on `main` branch
3. Check if it's ✅ green or ❌ red

## If Any Are Red

**Click on the failed run, then:**
1. Find the failing step (e.g., "Install dependencies", "Run tests")
2. Click on that step
3. Scroll to find the first actual error (not just warnings)
4. Copy the first real error line

**Then paste here in this format:**

```
Repo: [repo name]
Failing step: [step name]
First real error line: [error line]
```

## Expected Timeline

- **First run:** May take 2-5 minutes to complete
- **If no run triggered:** Make a tiny commit and push to trigger it
- **If red:** I'll help fix it quickly

---

**Once all 3 are green → proceed to branch protection setup.** 🛡️✨

