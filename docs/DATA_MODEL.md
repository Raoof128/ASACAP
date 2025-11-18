# Data model quick reference

The backend currently uses in-memory dictionaries but mirrors the relational
schema below so it can be mapped directly to PostgreSQL.

## Entity relationship overview

```
Assets 1 ─── * Incidents
Assets 1 ─── * CIRMP Templates
Suppliers 1 ──── 1..* Board Report attachments
```

## Tables

### assets

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID | Primary key |
| name | text | Unique per tenant |
| sector | text | Enum referencing 11 SOCI sectors |
| category | text | OT/IT classification |
| asset_type | text | e.g. IT server, SCADA RTU |
| criticality | text | Critical/High/Medium/Low |
| owner | text | Owner email or group |
| created_at | timestamptz | Default now() |

### cirmp_templates

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID |
| asset_type | text |
| organisation_size | text | Enum {small, medium, large} |
| sector | text |
| hazards | jsonb |
| controls | jsonb |
| evidence | jsonb |
| review_cadence_days | integer |

### incidents

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID |
| asset_id | UUID nullable | FK `assets.id` |
| title | text |
| severity | text |
| description | text |
| impact_assessment | text |
| evidence_bundle | jsonb |
| status | text | triage/reported |
| created_at | timestamptz |

### suppliers

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID |
| name | text |
| geo | text |
| tier | integer |
| risk_score | numeric |

### board_reports

| Column | Type | Notes |
| --- | --- | --- |
| id | UUID |
| generated_at | timestamptz |
| audience | text |
| kpis | jsonb |
| executive_summary | text |
| next_quarter_priorities | jsonb |
| top_risks | jsonb |
| attachments | jsonb |

## Migrations guidance

- Use Alembic or Atlas to manage schema versions.
- Default timezone aware timestamps and enforce row-level security in PostgreSQL
  for tenant isolation.
- Store audit logs in a separate append-only table with immutable retention.
