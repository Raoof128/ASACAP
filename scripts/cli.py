"""Simple automation-first CLI for SOCI Act asset operations."""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys
import urllib.request

API_DEFAULT = "http://localhost:8000"
ROOT = pathlib.Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "demo" / "seed_data"


def _request(method: str, endpoint: str, data: bytes | None = None) -> dict:
    request = urllib.request.Request(
        f"{API_DEFAULT}{endpoint}", data=data, method=method.upper()
    )
    request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request) as response:  # noqa: S310 (demo tool)
        return json.loads(response.read())


def seed_assets_from_csv(csv_path: pathlib.Path) -> dict:
    with csv_path.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        _request("POST", "/assets", data=json.dumps(row).encode())
    return {"imported": len(rows)}


def register_asset(payload_path: pathlib.Path) -> dict:
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    return _request("POST", "/assets", data=json.dumps(payload).encode())


def generate_board_report() -> dict:
    payload = json.dumps({"audience": "Board", "include_supply_chain": True}).encode()
    return _request("POST", "/reports/board", payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="SOCI automation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    seed_parser = subparsers.add_parser("seed", help="Bulk load assets from CSV")
    seed_parser.add_argument(
        "--csv",
        type=pathlib.Path,
        default=SEED_DIR / "assets.csv",
        help="CSV file with assets",
    )

    demo_seed_parser = subparsers.add_parser(
        "demo-data", help="Trigger API-side seeding (assets, templates, suppliers)"
    )
    demo_seed_parser.add_argument(
        "--force",
        action="store_true",
        help="Clear existing demo data before reloading fixtures",
    )

    register_parser = subparsers.add_parser("register", help="Register a single asset")
    register_parser.add_argument("payload", type=pathlib.Path)

    subparsers.add_parser("board-report", help="Generate board report summary")

    args = parser.parse_args()

    if args.command == "seed":
        result = seed_assets_from_csv(args.csv)
    elif args.command == "demo-data":
        suffix = "?force=true" if args.force else ""
        result = _request("POST", f"/demo/seed{suffix}")
    elif args.command == "register":
        result = register_asset(args.payload)
    else:
        result = generate_board_report()

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - user feedback
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
