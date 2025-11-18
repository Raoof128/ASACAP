# Security hardening checklist

- [ ] Enforce Azure AD conditional access with MFA and device compliance checks.
- [ ] Store all application secrets inside Azure Key Vault with RBAC enforced.
- [ ] Enable Azure Defender for Cloud across the subscription and Log Analytics.
- [ ] Configure Azure Monitor alerts for API anomaly detection and audit log gaps.
- [ ] Apply CIS hardened images to AKS node pools and container base images.
- [ ] Enable TLS 1.2+ end-to-end (Azure Application Gateway + backend services).
- [ ] Turn on Azure Storage immutability policies for evidence artefacts.
- [ ] Run Ansible hardening playbooks across OT/edge nodes weekly.
- [ ] Review Terraform state access controls; back Terraform state in AU regions.
- [ ] Execute quarterly penetration tests and capture remediation in CIRMP.
