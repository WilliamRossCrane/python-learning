def test_assessment_crud_and_filters(client, create_class):
    assessments = [
        {"class_id": create_class["id"], "title": "Algebra Exam", "assessment_type": "exam", "max_score": 50, "due_date": "2026-09-13"},
        {"class_id": create_class["id"], "title": "Algebra Quiz", "assessment_type": "quiz", "max_score": 20, "due_date": "2026-09-10"},
        {"class_id": create_class["id"], "title": "Algebra Project", "assessment_type": "project", "max_score": 100, "due_date": "2026-09-20"},
    ]
    created = [client.post("/api/v1/assessments/", json=payload) for payload in assessments]
    assert all(response.status_code == 201 for response in created)
    assessment_id = created[0].json()["id"]

    assert client.post("/api/v1/assessments/", json={**assessments[0], "class_id": 999}).status_code == 404
    assert len(client.get("/api/v1/assessments/").json()) == 3
    assert client.get(f"/api/v1/assessments/{assessment_id}").status_code == 200
    assert client.get("/api/v1/assessments/999").status_code == 404
    assert len(client.get(f"/api/v1/assessments/?class_id={create_class['id']}").json()) == 3
    assert client.get("/api/v1/assessments/?assessment_type=quiz").json()[0]["title"] == "Algebra Quiz"
    assert client.get("/api/v1/assessments/?search=project").json()[0]["assessment_type"] == "project"
    assert client.get("/api/v1/assessments/?sort_order=desc").json()[0]["title"] == "Algebra Project"
    assert len(client.get("/api/v1/assessments/?limit=2&offset=1").json()) == 2
    assert client.get("/api/v1/assessments/?assessment_type=invalid").status_code == 422

    updated = {**assessments[0], "title": "Updated Exam", "max_score": 60}
    assert client.put(f"/api/v1/assessments/{assessment_id}", json=updated).status_code == 200
    assert client.delete(f"/api/v1/assessments/{assessment_id}").status_code == 204


def test_class_assessments_endpoint(client, create_class, create_assessment):
    response = client.get(f"/api/v1/assessments/classes/{create_class['id']}/assessments")

    assert response.status_code == 200
    assert response.json()[0]["id"] == create_assessment["id"]
