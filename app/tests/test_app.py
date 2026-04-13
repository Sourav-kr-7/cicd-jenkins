from app.main import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_root_endpoint_has_message():
    app = create_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload["message"] == "CI/CD Automation Project"
