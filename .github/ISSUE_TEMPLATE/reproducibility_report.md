---
name: Reproducibility Report
about: Report results from attempting to reproduce results or run code
title: '[REPRO] '
labels: reproducibility
assignees: ''
---

## Reproduction Attempt

**Goal:**
- [ ] Reproduce paper results
- [ ] Run code/simulations
- [ ] Verify installation
- [ ] Test specific experiment
- [ ] Other: ___________

## Environment

**Operating System:**
- OS: 
- Version: 
- Architecture: 

**Python Environment:**
- Python version: 
- Python full version: `python -c "import sys; print(sys.version)"`
- Python executable: `which python` or `where python`
- Installation method: [ ] pip [ ] conda [ ] venv [ ] system [ ] other: ___________
- Virtual environment: [ ] Yes [ ] No
- pip version: `pip -V`

**Dependencies:**
- Install command used: 
- Lockfile used: [ ] Yes (`requirements-lock.txt`) [ ] No (`requirements.txt`)
- Any dependency conflicts? [ ] Yes [ ] No
  - If yes, describe:

## Command Executed

**Exact command(s) run:**
```bash
# Paste exact commands here
```

**Expected result:**
- 

**Actual result:**
- 

## Output/Results

**Console output:**
```
Paste relevant output here
```

**Result files generated:**
- Location: 
- Files: 

**Result hash/checksum (if applicable):**
- File: 
- Hash: 

## Verification

**Did it match expected results?**
- [ ] Yes (matches exactly)
- [ ] Yes (matches within tolerance)
- [ ] No (different results)
- [ ] No (error/failure)
- [ ] Partial (some parts work, others don't)

**If different/error, describe:**
- 

## Logs/Error Messages

```
Paste any error messages, stack traces, or relevant logs
```

## Configuration

**Any configuration changes made?**
- [ ] No (used defaults)
- [ ] Yes (describe below)

**Configuration used:**
```yaml
# or JSON, or describe
```

## Comparison

**If comparing to paper/results:**
- Paper version: 
- Section/Figure: 
- Expected values: 
- Actual values: 

**If comparing to other runs:**
- Previous run hash/commit: 
- Differences observed: 

## System Information

**Hardware (if relevant):**
- CPU: 
- RAM: 
- GPU (if used): 

**Other relevant system info:**
- 

## Additional Context

Any other information that might help diagnose or understand the reproduction attempt:
- 

## Verification Checklist

- [ ] Environment details provided
- [ ] Exact commands documented
- [ ] Output/results included
- [ ] Error messages included (if any)
- [ ] Configuration documented
- [ ] Comparison made (if applicable)

---

**Note:** For reproducibility, please include as much detail as possible. This helps identify environment-specific issues and improves the project's reproducibility.

