from fastapi.testclient import TestClient

from lending_club_credit_risk.api.app import create_app

def test_health_endpoint_returns_ok():
    """
    Test that the /health endpoint returns a 200 status code and the expected response.
    """
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}