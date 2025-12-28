# Security Policy

## Supported Versions

We actively support security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | :white_check_mark: |
| 1.1.x   | :white_check_mark: |
| < 1.1   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in MQGT-SCF, please report it responsibly.

### How to Report

1. **Do not** open a public GitHub issue for security vulnerabilities.

2. Report via GitHub Security Advisories (recommended):
   - Go to: https://github.com/Cbaird26/MQGT-SCF/security/advisories/new
   - Click "Report a vulnerability"
   - Fill out the security advisory form
   
   Alternatively, create a private security issue:
   - Go to: https://github.com/Cbaird26/MQGT-SCF/issues/new
   - Use label: `security`
   - Mark as private/draft if possible
   - Include:
     - Description of the vulnerability
     - Steps to reproduce (if applicable)
     - Potential impact
     - Suggested fix (if you have one)

3. We will acknowledge receipt within 48 hours.

4. We will provide an initial assessment within 7 days.

5. We will keep you informed of progress and coordinate disclosure.

### What to Report

- Security vulnerabilities in code (e.g., injection, privilege escalation)
- Vulnerabilities in dependencies (if they affect MQGT-SCF usage)
- Issues with data handling or privacy
- Cryptographic weaknesses

### What NOT to Report

- General code quality issues (use regular issues)
- Feature requests (use discussions)
- Theoretical vulnerabilities without practical impact
- Issues in dependencies that don't affect MQGT-SCF

## Security Best Practices for Users

- Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- Review code before running in production environments
- Use virtual environments to isolate dependencies
- Do not commit API keys, tokens, or credentials to the repository

## Disclosure Policy

- We will credit you for responsible disclosure (unless you prefer anonymity)
- We will coordinate public disclosure after a fix is available
- We aim to fix critical vulnerabilities within 30 days

## Thank You

Thank you for helping keep MQGT-SCF and its users safe!

