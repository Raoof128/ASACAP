# Security policy

We take the protection of Australian critical infrastructure seriously. This document explains how to report vulnerabilities, what to expect from the triage process, and which versions of ASACAP receive fixes.

## Supported versions

| Version | Supported | Notes |
| --- | --- | --- |
| `main` (default branch) | ✅ | Receives security and dependency fixes immediately.
| Tagged demo releases | ⚠️ | Fixes are backported when the issue affects reference deployments.
| Archived snapshots | ❌ | Not maintained; please upgrade to a supported tag.

## Reporting a vulnerability

1. Email **security@asacap.example** with the words "ASACAP security" in the subject line.
2. Provide enough detail for us to reproduce the issue. Screenshots and proof-of-concept payloads are welcome.
3. Do **not** create a public issue until the fix has shipped. If you need to encrypt the report, request our PGP key in the initial email.
4. If the vulnerability involves a third-party dependency, include the affected package and version so we can coordinate upstream disclosure where appropriate.

## Our commitment

- We will acknowledge your report within two business days.
- Maintainers will provide a triage update within five business days that outlines severity, impact, and remediation path.
- Coordinated disclosure timelines are agreed with you. We target a fix within 30 days for high severity issues.
- You will be credited in the release notes (optional) once the fix is public.

## Temporary mitigations

If an immediate patch is not possible, we will document mitigations (configuration changes, firewall rules, feature flags) in the README and `docs/QUALITY_ASSURANCE.md` to help operators stay protected.

## Incident contacts

- **security@asacap.example** – Primary contact for vulnerability reports
- **oss@asacap.example** – Escalation path if you have not received a response within the timelines above

Thank you for helping us keep the SOCI Act Compliance Automation Platform safe and trustworthy.
