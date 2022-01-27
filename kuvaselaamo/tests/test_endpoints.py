def test_healthz_and_readiness_endpoints(client):
    response = client.get("/healthz")
    assert response.status_code == 200

    response = client.get("/readiness")
    assert response.status_code == 200
