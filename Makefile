.PHONY: backend frontend test lint terraform-init terraform-apply ansible audit

backend:
	uvicorn services.backend.main:app --reload

frontend:
	cd services/frontend/webapp && npm install && npm start

lint:
	python -m compileall services/backend

test:
	pytest -q

audit:
	python scripts/audit_repo.py

terraform-init:
	cd infra/terraform && terraform init

terraform-apply:
	cd infra/terraform && terraform apply

ansible:
	ansible-playbook ansible/playbooks/ot_site.yml
