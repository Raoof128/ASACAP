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
# 1. Start the FastAPI backend
uvicorn services.backend.main:app --reload

# 2. Start the React frontend
cd services/frontend/webapp
npm install
npm start

# 3. (Optional) Refresh demo fixtures via CLI
python scripts/cli.py demo-data --force
```

The backend seeds demo data automatically on startup via FastAPI lifespan
handlers, so `/docs` immediately exposes the OpenAPI spec. Use the new `demo-data`
CLI command (or call `POST /demo/seed?force=true`) whenever you want to reset to
the curated fixtures of assets, templates, and suppliers. The frontend expects
the API at `http://localhost:8000`; override via `REACT_APP_API_BASE_URL`.

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
and ACSC payload creation.

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions should maintain Australian
English, pass CI, and include documentation for new workflows.
