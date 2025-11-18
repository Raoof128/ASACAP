# Repository audit report

Date: 2025-05-05
Auditor: Jules AI

## Scope

- Application services (FastAPI backend, React frontend)
- Infrastructure-as-code (Terraform, Ansible)
- Tooling (CLI, Make targets, demo seeds, audit automation)
- Documentation (README, operations, security, demo collateral)
- Community governance (Code of Conduct, contributing guide, security policy)

## Findings summary

| Area | Status | Notes |
| --- | --- | --- |
| Source control hygiene | ✅ | Single branch, clean status, CI-ready Make targets |
| API coverage | ✅ | Endpoints for assets, CIRMP, compliance, incidents, supply chain, board reports, demo seeding |
| Testing | ✅ | `pytest` suite covers CIRMP generator, ACSC payloads, seeding helper, and API endpoints |
| Documentation | ✅ | README links to architecture, operations runbook, demo playbook, audit pack, QA guide, and new contributor docs |
| Security + disclosure | ✅ | `SECURITY.md` documents reporting channels, timelines, and supported versions |
| Community governance | ✅ | `CODE_OF_CONDUCT.md` and a detailed `CONTRIBUTING.md` now set expectations |
| Licensing | ✅ | MIT license published with explicit redistribution terms |
| Missing assets | ⚠️ | Demo video placeholder remains; production recording still outstanding |

## Gap remediation this iteration

1. **Demo collateral documentation** – Added `demo/README.md` so demo curators can
   review the provenance and schema of CSV/JSON fixtures before workshops.
2. **Automation CLI reference** – Published `docs/CLI_REFERENCE.md` and surfaced
   the helper in the README to formalise the supported commands.
3. **Audit automation coverage** – Extended `scripts/audit_repo.py` so it now
   checks for the CLI reference, demo playbook, and LICENSE file, keeping the
   documentation pack enforceable in CI.
4. **API quality hardening** – Normalised mutable defaults in the FastAPI models
   to keep incident payloads and supplier dependency lists isolated between
   requests.
5. **License stewardship** – Added an MIT license and surfaced it inside the
   README to clarify redistribution rights for downstream adopters.
6. **Release governance** – Published `docs/RELEASE_CHECKLIST.md` and linked it
   from the README so every release follows the same verification steps (tests,
   audit script, demo refresh, and documentation review).

## Evidence map

| Requirement | Artefact |
| --- | --- |
| CIRMP templates for 3 asset classes | `docs/CIRMP_templates/*.json` |
| OpenAPI spec | `docs/openapi.yaml` + FastAPI `/docs` |
| Compliance checklist generator/CLI | `scripts/cli.py` with `seed`, `demo-data`, `board-report` commands |
| Board-level report (PDF & Markdown) | `docs/reports/board_report_sample.md` + `docs/reports/board_report_sample.pdf` |
| Security hardening guidance | `docs/security_hardening_checklist.md` + `docs/QUALITY_ASSURANCE.md` |
| ACSC automation guidance | `docs/ACSC_integration.md` |
| Infra-as-code | `infra/terraform/*.tf` |
| OT automation | `ansible/playbooks/ot_site.yml` + template |
| Demo instructions | `docs/DEMO_PLAYBOOK.md` + README section |
| Operations guidance | `docs/OPERATIONS_RUNBOOK.md` |
| Governance + responsible disclosure | `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md` |
| Release readiness | `docs/RELEASE_CHECKLIST.md` + README section |

## Outstanding actions

1. Record the requested 3–5 minute demo video and store it under `docs/`.
2. Integrate Azure AD SSO in the frontend once tenant details are available.
3. Replace the in-memory FastAPI store with PostgreSQL persistence during the next iteration.
4. Review `scripts/audit_repo.py` output on each release to keep the readiness score green in CI.

## Sign-off

The repository now contains the governance, documentation, and automation artefacts required for stakeholder review and is considered presentation-ready. Remaining actions are tracked above for the next release.
