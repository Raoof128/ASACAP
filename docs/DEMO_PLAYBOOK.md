# Demo playbook

Use this script to deliver the 3–5 minute walkthrough requested by program
sponsors.

## Preparation

1. `make backend` in one terminal and `make frontend` in another.
2. `python scripts/cli.py demo-data --force` to ensure fixtures are loaded.
3. Log in to the frontend with `admin@demo.asacap / Demo123!`.
4. Keep `docs/postman_collection.json` open for quick API spot checks.

## Flow

1. **Asset onboarding (1 min)**
   - Show CLI `scripts/cli.py seed --csv demo/seed_data/assets.csv`.
   - Refresh frontend Assets view to highlight SOCI sector tagging.
2. **CIRMP template generator (1 min)**
   - Call `POST /cirmp/templates/generate` via Swagger UI or Postman.
   - Download the JSON template and point to `docs/CIRMP_templates/*.json`.
3. **Compliance dashboard & alerts (45 sec)**
   - Show compliance score widget, drift indicators and Slack alert preview.
4. **Incident reporting (1 min)**
   - Create incident via UI, then use CLI `board-report` to show ACSC payload.
   - Mention `docs/ACSC_integration.md` for production hand-off.
5. **Board-level reporting (45 sec)**
   - Use frontend export button or CLI board-report command.
   - Reference new PDF artefact at `docs/reports/board_report_sample.pdf`.

## Wrap-up talking points

- Infrastructure resides in Azure AU regions only (enforced via Terraform).
- RBAC roles available for Admin, Security Officer, Asset Owner and Auditor.
- Evidence bundling + chain-of-custody metadata ready for ACSC attestation.
- Policy-as-code and Sentinel playbook integrations are on the roadmap (see
  `docs/ARCHITECTURE.md`).
