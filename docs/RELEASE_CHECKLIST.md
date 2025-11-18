# Release readiness checklist

Use this checklist before tagging a release or presenting the platform to stakeholders. It keeps the demo environment, governance artefacts, and automation workflows aligned with the SOCI obligations the repository showcases.

## 1. Code health

- [ ] `make test` executes cleanly with 100% passing pytest suites.
- [ ] `python -m compileall services/backend` succeeds (or run `make lint`).
- [ ] Dependencies in `services/backend/requirements-dev.txt` and the frontend `package.json` reflect the versions used during testing.

## 2. Documentation and governance

- [ ] README reflects the current deployment workflow, demo credentials, and feature set.
- [ ] `docs/ARCHITECTURE.md`, `docs/DATA_MODEL.md`, and `docs/OPERATIONS_RUNBOOK.md` mirror the state of the codebase.
- [ ] Governance artefacts (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE`) are unchanged since the last review or have been re-approved.
- [ ] Demo fixtures have been regenerated using `python scripts/cli.py demo-data --force` and verified against `demo/README.md`.

## 3. Automation checks

- [ ] `python scripts/audit_repo.py` reports all PASS results.
- [ ] GitHub Actions workflow status badges (or the most recent run) are green.
- [ ] Terraform plan reviewed for the target environment; apply only after approval.

## 4. Operational sign-off

- [ ] Incident automation tested end-to-end using `/incidents` APIs and the CLI board report exporter.
- [ ] Runbooks reviewed for accuracy (contacts, escalation, mitigation steps).
- [ ] Demo video placeholder replaced with the latest recording placed under `docs/`.

## 5. Release packaging

- [ ] Update `docs/AUDIT_REPORT.md` with the current date, findings summary, and outstanding actions.
- [ ] Tag the release (`git tag -s vX.Y.Z`) and push to origin.
- [ ] Attach the board report sample PDF and architecture diagram to the release notes if publishing externally.

Document the completion of each checklist item inside the release issue or pull request for traceability.
