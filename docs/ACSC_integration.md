# ACSC integration approach

The platform never connects directly to ACSC production systems from the demo
environment. Instead, the FastAPI backend produces a standards-aligned payload
via `/incidents/{id}/report` and publishes the JSON body that would be sent to
ACSC's secure endpoint. For production roll-outs:

1. Use Azure Key Vault managed identities to store ACSC API credentials.
2. Submit the payload over TLS 1.2+ to the ACSC gateway and log the immutable
   transaction metadata into Azure Log Analytics.
3. Store the evidence manifest alongside SHA-256 hashes in Azure Storage with
   immutability policies enabled.
4. Update the `build_acsc_payload` helper to include accreditation IDs, impact
   severity per ACSC taxonomy, and optional attachments.

## Mock endpoint workflow

- Security officers create an incident via `/incidents`.
- The workflow guides them through impact assessment and evidence bundling.
- The `report_incident` route serialises the payload and mimics a successful
  submission to the mock endpoint, enabling the frontend demo to show real-time
  status updates without risking sensitive information.

## Accreditation considerations

- Maintain an IRAP-aligned assurance package stored in `docs/security_hardening_checklist.md`.
- Align incident reporting with ACSC guidance version 2023+.
- Every submission must capture reporter identity, time stamps, and chain of
  custody proof derived from Azure AD tokens.
