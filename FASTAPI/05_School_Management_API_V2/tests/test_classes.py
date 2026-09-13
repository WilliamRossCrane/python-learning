def test_create_get_update_and_delete_class(client, create_teacher, create_subject):
    payload = {
        "name": "Year 10 Mathematics",
        "teacher_id": create_teacher["id"],
        "subject_id": create_subject["id"]
    }
    created = client.post("/api/v1/classes/", json=payload)
    assert created.status_code == 201
    class_id = created.json()["id"]

    assert client.get(f"/api/v1/classes/{class_id}").status_code == 200
    assert client.get("/api/v1/classes/999").status_code == 404
    assert client.post("/api/v1/classes/", json={**payload, "teacher_id": 999}).status_code == 404
    assert client.post("/api/v1/classes/", json={**payload, "subject_id": 999}).status_code == 404

    updated = {**payload, "name": "Year 11 Mathematics"}
    response = client.put(f"/api/v1/classes/{class_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["name"] == "Year 11 Mathematics"
    assert client.delete(f"/api/v1/classes/{class_id}").status_code == 204


def test_class_queries(client, create_teacher, create_subject):
    other_teacher = client.post("/api/v1/teachers/", json={
        "first_name": "Sam", "last_name": "Hill", "email": "sam@example.com", "staff_code": "T002"
    }).json()
    other_subject = client.post("/api/v1/subjects/", json={
        "name": "Science", "code": "SCI", "description": "Science fundamentals"
    }).json()
    classes = [
        {"name": "Algebra", "teacher_id": create_teacher["id"], "subject_id": create_subject["id"]},
        {"name": "Biology", "teacher_id": other_teacher["id"], "subject_id": other_subject["id"]},
        {"name": "Geometry", "teacher_id": create_teacher["id"], "subject_id": create_subject["id"]},
    ]
    for payload in classes:
        assert client.post("/api/v1/classes/", json=payload).status_code == 201

    assert len(client.get(f"/api/v1/classes/?teacher_id={create_teacher['id']}").json()) == 2
    assert len(client.get(f"/api/v1/classes/?subject_id={create_subject['id']}").json()) == 2
    assert client.get("/api/v1/classes/?search=geo").json()[0]["name"] == "Geometry"
    assert len(client.get("/api/v1/classes/?limit=2").json()) == 2
    assert client.get("/api/v1/classes/?offset=2&limit=1").json()[0]["name"] == "Geometry"
