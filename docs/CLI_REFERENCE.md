# Automation CLI reference

The `scripts/cli.py` helper provides a thin automation layer over the FastAPI
backend so operators can seed data, register assets, and generate reports
without leaving their terminal. The commands are intentionally dependency-free
(`urllib.request` under the hood) which makes them easy to execute from jump
hosts or CI/CD steps.

## Usage

```bash
python scripts/cli.py --api-base http://localhost:8000 <command> [options]
```

Pass a custom API endpoint via the `--api-base` flag or the
`ASACAP_API_BASE` environment variable. Every command prints prettified JSON so
it can be chained to `jq` or redirected to artefact storage.

## Commands

| Command | Description | Key options |
| --- | --- | --- |
| `seed` | Loads assets from a CSV file (defaults to `demo/seed_data/assets.csv`). | `--csv /path/to/assets.csv` |
| `demo-data` | Calls `POST /demo/seed` to (re)seed assets, templates, and suppliers in the API. | `--force` clears all demo stores before loading fixtures. |
| `register` | Registers a single asset from a JSON payload that matches the `AssetCreate` schema. | Positional `payload` argument (path to JSON file). |
| `board-report` | Generates the executive report via `POST /reports/board`. | None. |

## Examples

```bash
# Load bespoke CSV data when testing an import workflow
python scripts/cli.py seed --csv ~/Downloads/new_assets.csv

# Reset the entire environment before a demo
python scripts/cli.py demo-data --force --api-base https://demo.asacap.example

# Register an asset directly from the repository's sample payload
python scripts/cli.py register demo/seed_data/sample_asset.json

# Capture a board report to review KPI language
python scripts/cli.py board-report > /tmp/board_report.json
```

## Extending the CLI

1. Add a new sub-command in `scripts/cli.py` with `subparsers.add_parser`.
2. Keep dependencies in the standard library so the CLI remains lightweight.
3. Document new commands here and link to relevant runbooks or API endpoints.
4. Add smoke tests (for example via `pytest` + `subprocess`) when commands grow
   more complex than simple HTTP wrappers.

Following the steps above keeps the CLI aligned with the rest of the
documentation portfolio and ensures reviewers can validate new automation flows
quickly.
