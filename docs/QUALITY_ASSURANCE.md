# Quality assurance + readiness validation

The ASACAP repository now bundles an automated audit helper to document the
state of core artefacts. The intent is to make it trivial for delivery teams,
program managers, and assessors to prove that the platform is presentation
ready before handing it to stakeholders or regulators.

## What the audit checks

1. **Critical artefacts** – verifies that the README, architecture docs, CIRMP
   templates, infrastructure-as-code, and OT automation files all exist.
2. **Readme completeness** – ensures the README exposes core sections that
   executives, engineers, and operators expect (features, getting started,
   testing, documentation, tooling, and deployment instructions).
3. **Automated tests** – executes the pytest suite to confirm that core flows
   continue to work.

## Running the audit

```bash
python scripts/audit_repo.py           # human-readable summary
python scripts/audit_repo.py --json    # summary + JSON output
python scripts/audit_repo.py --skip-tests  # only structural checks
```

The script exits with a non-zero status code if any check fails. Wire it into CI
or run it locally via `make audit` to validate deliverables ahead of executive
presentations.
