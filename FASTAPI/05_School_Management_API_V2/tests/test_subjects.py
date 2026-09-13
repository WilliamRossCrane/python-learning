def test_subject_crud_and_duplicate_code(client, subject_payload):
    created = client.post("/api/v1/subjects/", json=subject_payload)
    assert created.status_code == 201
    subject_id = created.json()["id"]

    assert client.get("/api/v1/subjects/").status_code == 200
    assert client.get(f"/api/v1/subjects/{subject_id}").status_code == 200
    assert client.get("/api/v1/subjects/999").status_code == 404
    assert client.post("/api/v1/subjects/", json={**subject_payload, "name": "Other"}).status_code == 409

    updated = {**subject_payload, "name": "Advanced Mathematics", "code": "AMTH"}
    assert client.put(f"/api/v1/subjects/{subject_id}", json=updated).status_code == 200
    assert client.delete(f"/api/v1/subjects/{subject_id}").status_code == 204
