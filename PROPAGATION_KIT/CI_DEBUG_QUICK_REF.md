# CI Debug Quick Reference

## When CI Fails

**Grab these two things:**
1. **Failing step name** (e.g., "Install dependencies", "Run tests", "Check Python syntax")
2. **First real error line** (first actual exception, not cascade)

**Then say:** "CI is failing on [repo] at step [X] with error [Y]"

## Common CI Failure Patterns

### "Install dependencies" fails
- Missing `requirements.txt`
- Wrong path in workflow
- Dependency version conflicts

### "Check Python syntax" fails
- Syntax errors in Python files
- Indentation issues
- Import errors at parse time

### "Verify code imports" fails
- Missing dependencies
- Wrong import paths
- Relative vs absolute imports

### "Run tests" fails
- Missing `tests/` directory (if workflow is strict)
- Test failures
- Missing test dependencies

### "Check code style" fails
- Flake8/ruff errors
- Usually just warnings, can be adjusted

## Quick Fixes I Can Do

✅ Update workflow paths
✅ Fix import statements
✅ Add missing dependencies
✅ Adjust test requirements
✅ Fix syntax errors
✅ Update CI configuration

**Just paste the failing step + error line, and I'll fix it fast.** 🛠️

