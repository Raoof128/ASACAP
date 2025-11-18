"""Unit tests for the repository audit helper."""

from scripts import audit_repo


def test_run_audit_without_tests_passes_for_repo_assets(monkeypatch):
    """Skipping pytest ensures we only validate documentation presence here."""

    results = audit_repo.run_audit(skip_tests=True)
    assert results, "audit should produce check results"
    assert all(result.passed for result in results), "baseline repo should pass"


def test_audit_detects_missing_assets(monkeypatch, tmp_path):
    """Inject a fake expected file to confirm failures are surfaced."""

    missing_file = "docs/DOES_NOT_EXIST.md"
    monkeypatch.setattr(audit_repo, "EXPECTED_FILES", audit_repo.EXPECTED_FILES + [missing_file])

    results = audit_repo.run_audit(skip_tests=True)
    failures = [r for r in results if not r.passed and missing_file in r.name]
    assert failures, "audit should flag missing documentation"
