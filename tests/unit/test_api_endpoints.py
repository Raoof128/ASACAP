from fastapi.testclient import TestClient

from services.backend.main import app, seed_demo_data, SAMPLE_ASSETS


client = TestClient(app)


def test_health_endpoint_returns_status():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_demo_seed_force_refreshes_assets():
    seed_demo_data(force=True)
    new_asset = {
        "name": "Temporary asset",
        "sector": "Energy",
        "category": "IT",
        "asset_type": "Server",
        "criticality": "Low",
        "owner": "Test",
    }
    client.post("/assets", json=new_asset)
    response = client.post("/demo/seed", params={"force": True})
    payload = response.json()
    assert payload["assets"] == len(SAMPLE_ASSETS)
    assert payload["templates"] >= 3


def test_board_report_endpoint_includes_supply_chain_signal():
    response = client.post("/reports/board", json={"audience": "Board"})
    assert response.status_code == 200
    body = response.json()
    assert "overall_compliance" in body["kpis"]
    assert any("CIRMP" in summary for summary in body["next_quarter_priorities"])
