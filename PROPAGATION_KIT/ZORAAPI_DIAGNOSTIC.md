# ZoraAPI CI Diagnostic Guide

## Common Issues & Quick Fixes

### Issue 1: Stuck "In Progress" (Most Likely)

**Symptom:** CI run shows "In progress" for 35+ minutes

**Causes:**
- Queued (waiting for runner)
- Hung (pip install stuck, network hiccup)
- Blocked (waiting for approval)

**Fix:**
1. Click the in-progress run → click the job
2. Look at the last line printed
3. If idle for minutes: **Cancel workflow** → **Re-run jobs**

### Issue 2: Wrong Badge URL / Workflow Name Mismatch

**Symptom:** Badge shows red even when CI is green

**Check:**
- Workflow name in `.github/workflows/ci.yml` should be `name: CI`
- Badge URL should match: `.../workflows/CI/badge.svg`

**Fix:**
- Ensure workflow name is exactly `CI` to match badge

### Issue 3: Old Red Entry (Not Your CI)

**Symptom:** Red "Create secret-scan.yml" from May visible

**Fix:**
- Ignore it - it's not your CI
- Only the newest run for your CI workflow matters

## Diagnostic Steps

**On GitHub:**
1. ZoraAPI → **Actions**
2. Click the run that's "In progress"
3. Look at the job list:
   - If **Queued** → runner delay (Cancel + re-run)
   - If running, click it and check last step:
     - Stuck on "Install dependencies" → pip hang
     - Stuck on "Run tests" → test command waiting

**Report back with:**
```
Repo: ZoraAPI
Status: (Queued / In progress / Failed)
Last step shown: (e.g., Install dependencies)
Last line printed: [last line]
```

## Quick Fixes Ready

**If stuck on pip install:**
- Add timeout to install step
- Split dependencies if needed

**If workflow name mismatch:**
- Update workflow name to `CI`
- Or update badge URL to match workflow name

---

**Status:** Ready to diagnose and fix once you provide the status details. 🛡️✨

