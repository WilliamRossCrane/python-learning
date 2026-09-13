def test_create_student(client, student_payload):
    response = client.post("/api/v1/students/", json=student_payload)

    assert response.status_code == 201
    assert response.json()["id"] > 0
    assert response.json()["first_name"] == "Asha"
    assert response.json()["last_name"] == "Patel"
    assert response.json()["year_level"] == 10
    assert response.json()["email"] == "asha@example.com"


def test_student_validation_rejects_invalid_values(client, student_payload):
    for field, value in (("year_level", 6), ("year_level", 13), ("email", "invalid"), ("first_name", "")):
        payload = student_payload.copy()
        payload[field] = value
        response = client.post("/api/v1/students/", json=payload)
        assert response.status_code == 422


def test_duplicate_student_email_returns_409(client, student_payload):
    assert client.post("/api/v1/students/", json=student_payload).status_code == 201

    response = client.post("/api/v1/students/", json={**student_payload, "first_name": "Other"})

    assert response.status_code == 409


def test_get_student_and_nonexistent_student(client, create_student):
    response = client.get(f"/api/v1/students/{create_student['id']}")

    assert response.status_code == 200
    assert response.json()["email"] == create_student["email"]
    assert client.get("/api/v1/students/999").status_code == 404


def test_get_students_filters_searches_sorts_and_paginates(client):
    students = [
        {"first_name": "Asha", "last_name": "Patel", "year_level": 10, "email": "asha@example.com"},
        {"first_name": "Ben", "last_name": "Ashford", "year_level": 10, "email": "ben@example.com"},
        {"first_name": "Casey", "last_name": "Brown", "year_level": 11, "email": "casey@example.com"},
        {"first_name": "Drew", "last_name": "Stone", "year_level": 10, "email": "drew@example.com"},
    ]
    for student in students:
        assert client.post("/api/v1/students/", json=student).status_code == 201

    assert len(client.get("/api/v1/students/?year_level=10").json()) == 3
    assert client.get("/api/v1/students/?search=ASHFORD").json()[0]["last_name"] == "Ashford"
    assert client.get("/api/v1/students/?search=casey@example.com").json()[0]["first_name"] == "Casey"
    assert [item["last_name"] for item in client.get("/api/v1/students/?sort_by=last_name&sort_order=asc").json()] == ["Ashford", "Brown", "Patel", "Stone"]
    assert client.get("/api/v1/students/?sort_by=last_name&sort_order=desc").json()[0]["last_name"] == "Stone"
    assert len(client.get("/api/v1/students/?limit=2").json()) == 2
    assert client.get("/api/v1/students/?offset=2&limit=1").json()[0]["first_name"] == "Casey"
    assert len(client.get("/api/v1/students/?year_level=10&search=example&limit=2").json()) == 2


def test_student_query_validation(client):
    assert client.get("/api/v1/students/?year_level=20").status_code == 422
    assert client.get("/api/v1/students/?sort_by=unknown").status_code == 422


def test_update_student_put_and_delete(client, create_student):
    student_id = create_student["id"]
    updated = {"first_name": "Mia", "last_name": "Turner", "year_level": 12, "email": "mia@example.com"}

    response = client.put(f"/api/v1/students/{student_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Mia"
    assert response.json()["email"] == "mia@example.com"

    assert client.delete(f"/api/v1/students/{student_id}").status_code == 204
    assert client.get(f"/api/v1/students/{student_id}").status_code == 404


def test_student_email_uniqueness_is_checked_during_put(client, student_payload):
    client.post("/api/v1/students/", json=student_payload)
    second = client.post("/api/v1/students/", json={**student_payload, "email": "second@example.com"}).json()

    response = client.put(
        f"/api/v1/students/{second['id']}",
        json={**student_payload, "first_name": "Second"}
    )

    assert response.status_code == 409
