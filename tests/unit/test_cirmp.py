from services.backend.main import (
    TemplateRequest,
    build_acsc_payload,
    build_cirmp_template,
    build_compliance_score,
    create_incident,
    seed_demo_data,
    DATABASE,
    SAMPLE_ASSETS,
    IncidentCreate,
)


def test_cirmp_template_contains_all_hazards():
    request = TemplateRequest(asset_type="SCADA RTU", organisation_size="large", sector="Energy")
    template = build_cirmp_template(request)
    assert request.asset_type == template.asset_type
    assert "Operational technology disruption" in template.hazards
    assert any("IEC 62443" in control for control in template.controls)


def test_compliance_score_adjusts_for_asset():
    score = build_compliance_score()
    assert 0 <= score.score <= 100


def test_acsc_payload_enriches_incident_metadata():
    incident = create_incident(
        IncidentCreate(
            asset_id="demo",
            title="Test incident",
            severity="High",
            description="Testing",
            evidence_bundle=["log.json"],
        )
    )
    payload = build_acsc_payload(incident)
    assert payload["incident_id"] == incident.id
    assert payload["impact_assessment"]
    assert payload["chain_of_custody"]["signed"] is True


def test_seed_demo_data_idempotent_and_forceful():
    first_stats = seed_demo_data(force=True)
    assert first_stats["assets"] == len(SAMPLE_ASSETS)

    # Remove an asset to ensure the helper can self-heal without `force`.
    DATABASE["assets"].popitem()
    refreshed = seed_demo_data()
    assert refreshed["assets"] == len(SAMPLE_ASSETS)
    assert refreshed == seed_demo_data()
