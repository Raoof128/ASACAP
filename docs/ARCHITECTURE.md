# ASACAP reference architecture

## Overview

The Australian SOCI Act Compliance Automation Platform (ASACAP) is a reference
implementation that demonstrates how to automate CIRMP workflows end-to-end.
The repository ships infrastructure-as-code, application services, demo data and
documentation so operators can stand up a production-ready environment inside
Australian Azure regions.

```
┌──────────────────────┐        ┌───────────────────────┐
│ React Control Room   │        │ Automation CLI / API  │
│ (services/frontend)  │◄──────►│ Operators & Integr..  │
└────────┬─────────────┘        └─────────┬─────────────┘
         │ REST / WebSocket                    │ CI/CD
┌────────▼──────────┐         ┌───────────────▼──────────────┐
│ FastAPI backend   │         │ GitHub Actions / Terraform   │
│ (services/backend)│         │ (infra/terraform, Makefile)  │
└────────┬──────────┘         └───────────────┬──────────────┘
         │  DB + queues                        │ Provisioning
┌────────▼──────────────────────────────────────▼────────────┐
│ Azure PaaS: PostgreSQL, ACR, Key Vault, App Gateway, LA    │
└────────────────────────────────────────────────────────────┘
```

## Component responsibilities

| Component | Description |
| --- | --- |
| `services/backend` | FastAPI service with REST endpoints for assets, CIRMP templates, compliance scores, incidents, ACSC payloads, supply-chain ingest and board reports. Uses in-memory storage in the kata but the data models align with PostgreSQL tables. |
| `services/frontend` | React SPA that surfaces dashboards, alerts, incident workflows and exports. Responsive layout targets SOCI operations centres and board viewers. |
| `infra/terraform` | Azure-native infrastructure including RG, PostgreSQL Flexible Server, Container Registry, Container Instances for backend/frontend, Key Vault, Storage Account, Log Analytics and Application Insights dashboard. All regions default to Australia East but can be overridden. |
| `ansible/playbooks` | OT/edge hardening example that enforces IEC 62443-aligned firewall policies for remote substations or plants. |
| `demo/seed_data` & `scripts/cli.py` | Data seeding tools for repeatable demos. CLI now supports custom API base URLs and integrates with the `/demo/seed` endpoint. |
| `docs/*` | Compliance collateral including CIRMP samples, ACSC guidance, security hardening checklist, audit report and demo playbooks. |

## Data model summary

Entities map to the OpenAPI schema defined in `docs/openapi.yaml`:

- **Asset** – contains SOCI sector, category, type, criticality and owner
  metadata. CRUD available along with CSV bulk import and CLI helpers.
- **Template** – CIRMP template objects include hazards, controls, evidence, and
  review cadence. Sector-specific controls are enriched with IEC 62443 context.
- **Incident** – workflow-friendly record with severity, triage status,
  evidence bundles and ACSC-ready payload generation.
- **Supplier** – supply-chain risk scores derived from tier, dependencies and
  geography. Aggregated view drives dashboards and board reports.
- **BoardReport** – summarises KPIs, top risks, attachments and next-quarter
  priorities for executive consumption.

## Security architecture

- **Identity** – integrate Azure AD via OIDC/SAML for operators. Demo mode ships
  sample users documented in `README.md`.
- **Secrets** – Terraform provisions Azure Key Vault. Application workloads
  retrieve database credentials and ACSC tokens via managed identity.
- **Data protection** – PostgreSQL and Storage accounts enforce AES-256
  encryption at rest, TLS 1.2 in transit and regional residency inside AU East /
  AU Southeast.
- **Observability** – Application diagnostics and audit logs stream into Azure
  Log Analytics, with dashboards exposed through `azurerm_dashboard`.

## Deployment workflow

1. Fork repo, configure GitHub Actions with OIDC trust to Azure subscription.
2. `make terraform-init terraform-apply` inside `infra/terraform`.
3. Build and push containers to ACR via CI pipeline.
4. GitHub Actions deploy manifests to Azure Container Instances/AKS, wiring
   Key Vault references and App Gateway routing.
5. Run Ansible playbook (`make ansible`) against OT nodes for IEC 62443
   hardening.
6. Execute `scripts/cli.py demo-data --force --api-base https://api.example.au`
   to seed demo fixtures in staging.

## Extensibility

- Add RabbitMQ/Azure Service Bus for asynchronous evidence ingestion.
- Replace the in-memory store with PostgreSQL models via SQLAlchemy.
- Enable Prometheus/Grafana via Azure Monitor managed prometheus.
- Add policy-as-code (OPA/Conftest) to continuously test CIRMP controls.
