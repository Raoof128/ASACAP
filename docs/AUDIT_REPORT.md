# Repository audit report

Date: 2025-11-18
Auditor: Jules AI

## Scope

- Application services (FastAPI backend, React frontend)
- Infrastructure-as-code (Terraform, Ansible)
- Tooling (CLI, Make targets, demo seeds)
- Documentation (README, operations, security, demo collateral)

## Findings summary

| Area | Status | Notes |
| --- | --- | --- |
| Source control hygiene | ✅ | Single branch, clean status, CI ready |
| API coverage | ✅ | Endpoints for assets, CIRMP, compliance, incidents, supply chain, board reports, demo seeding |
| Testing | ✅ | `pytest` suite covers CIRMP generator, ACSC payloads, seeding helper and API endpoints |
| Documentation | ✅ | README links to architecture, operations runbook, demo playbook, audit pack, and automated QA guide |
| Infrastructure | ✅ | Terraform modules cover AU-only resources with encryption + monitoring |
| Missing assets | ⚠️ | Demo video needs to be recorded before production launch |

## Evidence map

| Requirement | Artefact |
| --- | --- |
| CIRMP templates for 3 asset classes | `docs/CIRMP_templates/*.json` |
| OpenAPI spec | `docs/openapi.yaml` + FastAPI `/docs` |
| Compliance checklist generator/CLI | `scripts/cli.py` with `seed`, `demo-data`, `board-report` commands |
| Board-level report (PDF & Markdown) | `docs/reports/board_report_sample.md` + `docs/reports/board_report_sample.pdf` |
| Security hardening guidance | `docs/security_hardening_checklist.md` |
| ACSC automation guidance | `docs/ACSC_integration.md` |
| Infra-as-code | `infra/terraform/*.tf` |
| OT automation | `ansible/playbooks/ot_site.yml` + template |
| Demo instructions | `docs/DEMO_PLAYBOOK.md` + README section |
| Operations guidance | `docs/OPERATIONS_RUNBOOK.md` |

## Outstanding actions

1. Record the requested 3–5 minute demo video and store it under `docs/`.
2. Integrate Azure AD SSO in the frontend once tenant details are available.
3. Replace the in-memory FastAPI store with PostgreSQL persistence during the
   next iteration.
4. Review `scripts/audit_repo.py` output on each release to keep the readiness
   score green in CI.

## Sign-off

The repository now contains all artefacts required for stakeholder review and is
considered presentation-ready. Remaining actions are tracked above for the next
release.
