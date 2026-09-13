def test_root_returns_application_details(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "School Management API V2"
    assert response.json()["docs"] == "/docs"


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_database_health_check_uses_test_database(client):
    response = client.get("/health/database")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"}
