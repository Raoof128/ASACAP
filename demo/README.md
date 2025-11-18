# Demo data playbook

The `demo/seed_data` directory centralises the curated fixtures that underpin
the default FastAPI demo mode. Seed files align with the CIRMP templates,
suppliers, and user journeys described in the README, demo playbook, and QA
guide.

## Files

| File | Purpose |
| --- | --- |
| `assets.csv` | Primary dataset for the `scripts/cli.py seed` command and the `/demo/seed` endpoint. It mirrors the `AssetCreate` schema. |
| `suppliers.csv` | Optional helper for bulk-injecting supply-chain partners when you want to customise demos beyond the seeded defaults. |
| `sample_asset.json` | Single payload used in documentation and smoke tests to illustrate the API contract. |

## Updating fixtures

1. Keep columns aligned with the backend models to avoid runtime validation
   errors. The schema is documented in `docs/DATA_MODEL.md`.
2. When adding new rows, ensure you cover multiple SOCI sectors so the demo
   illustrates cross-sector obligations.
3. Run `python scripts/cli.py demo-data --force` after editing any file to load
   the changes into the running API instance.
4. Update the demo playbook and README tables if credentials or notable assets
   change.

## Operational guidance

- Treat the CSV/JSON files as source-controlled artefacts—reviews should confirm
  the provenance of new data.
- When creating bespoke data for a workshop, store the temporary CSV in a
  different directory so the baseline fixtures remain clean.
- Reference this README from other documentation to make it obvious where demo
  collateral is maintained.
