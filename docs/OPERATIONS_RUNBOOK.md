# Operations runbook

This runbook documents day-2 operations for ASACAP. It is written for Security
Operations Centre (SOC) analysts, compliance teams and on-call engineers.

## Health checks

| Check | Command | Expected result |
| --- | --- | --- |
| API liveness | `curl https://api.example.au/health` | `{ "status": "healthy" }` |
| Database connectivity | `pg_isready -h <psql_host> -d asacap` | `accepting connections` |
| Frontend availability | Browser hit to `https://app.example.au` | Dashboard renders with compliance score widget |
| Terraform drift | `terraform plan` from `infra/terraform` | No changes outside controlled deploys |

If any liveness check fails, redeploy containers via CI or restart the Azure
Container Instances group.

## Demo data refresh

1. `python scripts/cli.py demo-data --force --api-base https://api.example.au`
2. Confirm `/assets` contains the 3 sample assets and `/cirmp/templates` lists
   IT server, SCADA RTU and Comms tower entries.
3. Notify demo presenters that the environment is reset.

## Incident workflow

1. Analyst creates incident via frontend wizard or `POST /incidents`.
2. Evidence artefacts uploaded to Azure Storage evidence container.
3. When ready, call `/incidents/{id}/report` or use CLI board-report command to
   capture an ACSC-ready payload.
4. Verify payload logged to Azure Log Analytics and share JSON with leadership.

## Supply-chain ingest

- Upload supplier CSVs via CLI `seed --csv demo/seed_data/suppliers.csv` or API.
- Monitor `/supplychain/risk-score` for spikes. Trigger mitigation playbooks
  stored in `docs/CIRMP_templates/README.md` if risk > 70.

## Alerting & monitoring

- Azure Monitor alerts route to Teams/Slack webhooks defined in GitHub Actions
  secrets.
- Responders reference `docs/security_hardening_checklist.md` for containment.
- Capture lessons learned and update CIRMP templates accordingly.

## Disaster recovery

1. Restore PostgreSQL Flexible Server from the latest PITR snapshot.
2. Redeploy containers via GitHub Actions referencing the recovered database.
3. Recreate Key Vault secrets if soft-delete is triggered.
4. Rerun `scripts/cli.py demo-data --force` to repopulate demo data for QA
   validation prior to reopening the environment.

## Support contacts

- **Product Owner** – security.officer@demo.asacap
- **Azure Admin** – platform.engineer@demo.asacap
- **OT Lead** – ot.ops@demo.asacap
