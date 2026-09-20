def test_teacher_crud_and_unique_fields(client, teacher_payload):
    created = client.post("/api/v1/teachers/", json=teacher_payload)
    assert created.status_code == 201
    teacher_id = created.json()["id"]

    assert client.get("/api/v1/teachers/").json()[0]["staff_code"] == "T001"
    assert client.get(f"/api/v1/teachers/{teacher_id}").status_code == 200
    assert client.get("/api/v1/teachers/999").status_code == 404

    duplicate_email = {**teacher_payload, "staff_code": "T002"}
    assert client.post("/api/v1/teachers/", json=duplicate_email).status_code == 409
    duplicate_code = {**teacher_payload, "email": "second@example.com"}
    assert client.post("/api/v1/teachers/", json=duplicate_code).status_code == 409

    updated = {**teacher_payload, "first_name": "Taylor", "email": "taylor@example.com", "staff_code": "T003"}
    assert client.put(f"/api/v1/teachers/{teacher_id}", json=updated).status_code == 200
    patched = client.patch(f"/api/v1/teachers/{teacher_id}", json={"last_name": "Morgan"})
    assert patched.status_code == 200
    assert patched.json()["first_name"] == "Taylor"
    assert patched.json()["last_name"] == "Morgan"
    assert client.delete(f"/api/v1/teachers/{teacher_id}").status_code == 204
