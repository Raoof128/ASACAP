# CIRMP Templates

Sample templates align with the CIRMP expectations for three representative
asset classes. They demonstrate the structure produced by the FastAPI
`/cirmp/templates/generate` endpoint and can be imported into the frontend for
board reporting demonstrations.

## Templates included

- `it_server.json` – suitable for large finance organisations with heavy ACSC
  reporting requirements.
- `scada_rtu.json` – targeted at OT/ICS deployments, mapping IEC 62443
  requirements.
- `comms_tower.json` – focused on communications assets where availability and
  supply chain dependencies dominate.

Each template contains hazards, control requirements, evidence artefacts, and a
review cadence aligned to the default demo mode (90-day for large, 180-day for
other tiers).
