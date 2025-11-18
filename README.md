# Australian SOCI Act Compliance Automation Platform (ASACAP)

Enterprise-ready reference implementation that demonstrates how to automate
CIRMP obligations for Australia's SOCI Act (2018). The repository bundles API
services, Terraform + Ansible automation, demo data, documentation, and a React
UX aimed at both operational teams and boards.

## Features

- **Asset management** – register assets across the 11 SOCI sectors via API,
  CLI, or CSV. Every asset includes sector tags, categories, and owners.
- **CIRMP generator** – `POST /cirmp/templates/generate` produces an all-hazards
  template that covers physical, personnel, supply chain, cyber, and OT risks.
- **Continuous compliance** – calculated scores highlight drift indicators and
  open incidents across IT and OT estates.
- **Incident automation** – guided workflow to create and report incidents to a
  mock ACSC endpoint while preserving chain-of-custody metadata.
- **Supply chain + IEC 62443 mapping** – ingest vendor inventories and align
  OT controls to IEC 62443 families.
- **Board-level reporting** – generate printable Markdown/PDF friendly reports
  that summarise KPIs, risks, and remediation plans.
- **Demo mode** – sample templates, assets, suppliers, and users for quick
  walkthroughs. Demo credentials are documented in this README.

## Getting started

```bash
# 0. Install backend deps (dev requirements pin FastAPI + pytest versions)
python -m venv .venv && source .venv/bin/activate
pip install -r services/backend/requirements-dev.txt

# 1. Start the FastAPI backend
uvicorn services.backend.main:app --reload

# 2. Start the React frontend
cd services/frontend/webapp
npm install
npm start

# 3. (Optional) Refresh demo fixtures via CLI pointing at your API base URL
python scripts/cli.py demo-data --force --api-base http://localhost:8000
```

The backend seeds demo data automatically on startup via FastAPI lifespan
handlers, so `/docs` immediately exposes the OpenAPI spec. Use the new `demo-data`
CLI command (or call `POST /demo/seed?force=true`) whenever you want to reset to
the curated fixtures of assets, templates, and suppliers. The frontend expects
the API at `http://localhost:8000`; override via `REACT_APP_API_BASE_URL`.

## Automation CLI

The repository ships with an automation-first CLI (`scripts/cli.py`) to keep
common operator tasks scripted and reproducible. The helper exposes:

- `seed` – bulk loads a CSV file that mirrors `AssetCreate`.
- `demo-data` – calls `/demo/seed` (optionally with `--force`) to reload the
  curated fixtures documented under `demo/README.md`.
- `register` – registers an individual asset from a JSON payload, ideal for
  smoke-testing new schemas.
- `board-report` – generates the executive summary used in the board pack.

Each command accepts `--api-base` or the `ASACAP_API_BASE` environment variable.
See [`docs/CLI_REFERENCE.md`](docs/CLI_REFERENCE.md) for advanced usage,
examples, and extension guidance.

### Demo users

| Role              | Username                            | Password |
| ----------------- | ----------------------------------- | -------- |
| Admin             | admin@demo.asacap                   | Demo123! |
| Security Officer  | sec.officer@demo.asacap             | Demo123! |
| Auditor           | auditor@demo.asacap                 | Demo123! |

Credentials are used solely for walkthroughs; integrate Azure AD for production.

## Testing

```bash
make test
```

Tests use FastAPI's helpers to validate the CIRMP generator, compliance scores,
ACSC payload creation, and HTTP endpoints via `fastapi.testclient`.

## Documentation portfolio

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) – system components, security
  controls, deployment workflow, and extension options.
- [`docs/OPERATIONS_RUNBOOK.md`](docs/OPERATIONS_RUNBOOK.md) – day-2 operations
  for demo refreshes, incidents, supply-chain alerts, DR and contacts.
- [`docs/DEMO_PLAYBOOK.md`](docs/DEMO_PLAYBOOK.md) – ready-to-deliver script for
  the mandated 3–5 minute walkthrough.
- [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) – schema mapping to PostgreSQL.
- [`docs/AUDIT_REPORT.md`](docs/AUDIT_REPORT.md) – traceability matrix and
  outstanding actions (demo video + PostgreSQL persistence hardening).
- [`docs/QUALITY_ASSURANCE.md`](docs/QUALITY_ASSURANCE.md) – how to execute the
  automated readiness audit for executive sign-off.
- [`docs/CLI_REFERENCE.md`](docs/CLI_REFERENCE.md) – automation CLI usage and
  extension notes.
- [`demo/README.md`](demo/README.md) – explains the curated demo fixtures and
  how to update them safely.
- [`docs/reports/board_report_sample.md`](docs/reports/board_report_sample.md)
  and the accompanying [`PDF`](docs/reports/board_report_sample.pdf) – printable
  artefacts for executive stakeholders.

Run `python scripts/audit_repo.py` (or `make audit`) whenever you want to
collect a structured summary of repository completeness. The helper validates
that the documentation tree exists, README sections remain intact, and the test
suite passes.

## Tooling

- **Terraform** (`infra/terraform`) builds the Azure resource group, PostgreSQL,
  Key Vault, Storage, Application Gateway, and Log Analytics workspace.
- **Ansible** (`ansible/playbooks/ot_site.yml`) hardens simulated OT devices.
- **GitHub Actions** (`.github/workflows/ci.yml`) executes linting + pytest.
- **Docker** – container definitions for backend and frontend services.

## Repository layout

```
.
├── docs/                 # OpenAPI spec, CIRMP samples, Postman collection
├── services/backend      # FastAPI service
├── services/frontend     # React single-page application
├── infra/terraform       # Azure infrastructure as code
├── ansible/playbooks     # Sample OT/edge automation
├── demo/seed_data        # CSV + JSON fixtures for demo mode
├── scripts/cli.py        # CLI for automation-first operators
└── tests/                # Pytest coverage
```

## Deployment overview

1. Run `terraform init && terraform apply` in `infra/terraform` to provision AU
   region resources (Application Gateway, AKS/Container Apps, PostgreSQL,
   Key Vault, Storage, Log Analytics).
2. Build and push container images to Azure Container Registry.
3. Deploy workloads via GitHub Actions using OIDC federation for secrets.
4. Configure Azure AD enterprise app for RBAC, ensuring Security Officer,
   Asset Owner, Auditor, and Admin roles map to application scopes.
5. Execute Ansible playbooks against OT edge nodes (or simulations) to enforce
   IEC 62443 controls.

## Demo video

Record a 3–5 minute walkthrough covering asset import, compliance dashboard,
incident reporting, and board report export. Store it under `docs/` when ready –
a placeholder is left intentionally so future contributors can drop in the MP4.

## Release readiness

Before tagging a release or presenting to stakeholders, run through the
checklist in [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md). It
captures the code-quality gates (tests, linting), governance artefacts, demo
fixture refresh process, automation checks, and operational dry-runs so every
shipment meets the same standard.

## Contributing

We welcome improvements from operators, engineers, and researchers who rely on
the reference implementation. Review [CONTRIBUTING.md](CONTRIBUTING.md) for the
full workflow, including how to install dependencies, naming branches, and the
coding standards for FastAPI, React, Terraform, and Ansible assets. Every pull
request must:

1. Include tests and documentation updates for new workflows.
2. Pass `make test` and `make audit` locally before requesting a review.
3. Follow the [Code of Conduct](CODE_OF_CONDUCT.md) to keep discussions
   respectful and inclusive.

## Security and responsible disclosure

Never raise public GitHub issues for vulnerabilities. Instead, follow the steps
in [SECURITY.md](SECURITY.md) so the maintainers can triage the report with you
confidentially. We acknowledge reports within two business days and aim to ship
high-severity fixes within 30 days. Temporary mitigations are documented in the
runbooks when required.

## License

The project is distributed under the [MIT License](LICENSE), which permits
commercial and non-commercial use, modification, distribution, and private
usage provided that copyright notices remain intact. Review the license before
integrating ASACAP artefacts into production offerings.
