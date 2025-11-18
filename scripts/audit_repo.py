"""Repository readiness audit helper.

The script verifies documentation, infrastructure artefacts, and automated
checks so stakeholders can prove the SOCI platform is presentation ready.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "demo/README.md",
    "docs/ARCHITECTURE.md",
    "docs/ACSC_integration.md",
    "docs/OPERATIONS_RUNBOOK.md",
    "docs/DEMO_PLAYBOOK.md",
    "docs/DATA_MODEL.md",
    "docs/AUDIT_REPORT.md",
    "docs/QUALITY_ASSURANCE.md",
    "docs/CLI_REFERENCE.md",
    "docs/CIRMP_templates/README.md",
    "docs/security_hardening_checklist.md",
    "docs/openapi.yaml",
    "docs/postman_collection.json",
    "docs/reports/board_report_sample.pdf",
    "docs/RELEASE_CHECKLIST.md",
    "infra/terraform/main.tf",
    "ansible/playbooks/ot_site.yml",
    "services/backend/main.py",
    "services/frontend/webapp/src/App.js",
    "tests/unit/test_api_endpoints.py",
]

README_SECTIONS = [
    "Features",
    "Getting started",
    "Automation CLI",
    "Testing",
    "Documentation portfolio",
    "Tooling",
    "Deployment overview",
    "Demo video",
    "Release readiness",
]


@dataclass
class CheckResult:
    """Represents a single audit check output."""

    name: str
    passed: bool
    detail: str

    def as_dict(self) -> dict:
        return {"name": self.name, "passed": self.passed, "detail": self.detail}


def _check_paths(paths: Iterable[str]) -> List[CheckResult]:
    results: List[CheckResult] = []
    for rel in paths:
        resolved = ROOT / rel
        if resolved.exists():
            results.append(CheckResult(f"asset:{rel}", True, "present"))
        else:
            results.append(
                CheckResult(
                    f"asset:{rel}", False, f"missing required asset at {resolved}"  # noqa: E501
                )
            )
    return results


def _check_readme_sections(readme_path: Path) -> List[CheckResult]:
    text = readme_path.read_text(encoding="utf-8")
    results: List[CheckResult] = []
    for section in README_SECTIONS:
        marker = f"## {section}"
        results.append(
            CheckResult(
                f"readme:{section}",
                marker in text,
                "section documented" if marker in text else f"missing '{marker}'",
            )
        )
    return results


def _run_tests(test_args: Sequence[str]) -> CheckResult:
    try:
        completed = subprocess.run(
            test_args,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:  # pragma: no cover - defensive guard
        return CheckResult("tests", False, f"failed to execute: {exc}")

    detail = completed.stdout.strip()
    if completed.stderr:
        detail = f"{detail}\n{completed.stderr.strip()}" if detail else completed.stderr.strip()

    return CheckResult("tests", completed.returncode == 0, detail or "pytest output captured")


def run_audit(skip_tests: bool = False) -> List[CheckResult]:
    """Run all configured checks and return their results."""

    results: List[CheckResult] = []
    results.extend(_check_paths(EXPECTED_FILES))
    results.extend(_check_readme_sections(ROOT / "README.md"))
    if not skip_tests:
        results.append(_run_tests([sys.executable, "-m", "pytest", "-q"]))
    return results


def _summarise(results: Iterable[CheckResult]) -> str:
    lines = ["ASACAP Readiness Audit"]
    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]
    lines.append(f"Pass: {len(passed)} | Fail: {len(failed)}")
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        lines.append(f"- [{status}] {result.name}: {result.detail}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="ASACAP repository audit helper")
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Print JSON results in addition to the human readable summary",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip pytest execution (useful for offline reviews)",
    )
    args = parser.parse_args()

    results = run_audit(skip_tests=args.skip_tests)
    summary = _summarise(results)
    print(summary)

    if args.json_output:
        print(json.dumps([r.as_dict() for r in results], indent=2))

    if any(not r.passed for r in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
