# Contributing to ASACAP

Thank you for investing time in the Australian SOCI Act Compliance Automation Platform. We welcome code, documentation, and operational expertise from the Australian critical infrastructure community. This guide describes the expectations that keep the repository production-ready.

## Code of Conduct

By participating you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Contact **oss@asacap.example** if you observe behaviour that violates the policy.

## Ways to contribute

- Improve FastAPI or React features (automation endpoints, demo UX, reporting views).
- Extend Terraform/Ansible assets for new reference architectures.
- Enhance documentation (architecture, runbooks, demo collateral, QA checks).
- Report bugs by opening a GitHub issue that includes reproduction steps and expected behaviour.

## Development workflow

1. Fork the repository and create a branch named `feature/<summary>` or `fix/<summary>`.
2. Install backend dependencies:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r services/backend/requirements-dev.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd services/frontend/webapp
   npm install
   ```
4. Implement your change with tests and documentation.
5. Run the quality gates from the repository root:
   ```bash
   make test
   make audit
   ```
6. Submit a pull request that links to any related issues and summarises the risk/benefit of the change.

## Coding standards

### Python (FastAPI services and scripts)

- Use type hints and docstrings for new modules or functions.
- Prefer small, pure functions that are easily testable.
- Keep runtime dependencies pinned in `services/backend/requirements.txt` and run `pip-compile` (or equivalent) when bumping versions.
- Tests live in `tests/` and should run via `pytest -q`.

### JavaScript/TypeScript (React frontend)

- Use functional components with hooks.
- Keep API calls in dedicated helpers and respect the `REACT_APP_API_BASE_URL` setting.
- Run `npm run lint && npm test` before submitting changes to the web application.

### Infrastructure as Code

- Terraform modules must pass `terraform fmt` and `terraform validate`.
- Ansible playbooks should remain idempotent and include comments referencing IEC 62443 controls where relevant.

## Documentation expectations

- Update the README if you add new workflows, CLI commands, or developer tooling.
- Operational changes should be reflected in `docs/OPERATIONS_RUNBOOK.md`.
- Security-affecting changes must mention the mitigation in `docs/security_hardening_checklist.md` or `docs/QUALITY_ASSURANCE.md`.

## Testing and audit automation

- `make test` runs the FastAPI unit tests and CLI coverage.
- `make audit` executes `scripts/audit_repo.py`, which confirms mandatory artefacts exist and that README sections remain intact. Pull requests must keep the audit green.

## Security disclosures

Never file public issues for vulnerabilities. Follow the steps in [SECURITY.md](SECURITY.md) so the maintainers can coordinate a responsible disclosure.

We appreciate every contribution that helps Australia's critical infrastructure operators accelerate SOCI Act compliance.
