def test_result_create_validation_queries_summary_and_delete(client, create_class, create_student, create_enrolled_student, create_assessment):
    payload = {
        "assessment_id": create_assessment["id"],
        "student_id": create_student["id"],
        "score": 45
    }
    created = client.post("/api/v1/results/", json=payload)
    assert created.status_code == 201
    result_id = created.json()["id"]

    assert client.post("/api/v1/results/", json=payload).status_code == 409
    assert client.post("/api/v1/results/", json={**payload, "score": 60}).status_code == 400
    assert len(client.get(f"/api/v1/results/?student_id={create_student['id']}").json()) == 1
    assert len(client.get(f"/api/v1/results/?assessment_id={create_assessment['id']}").json()) == 1
    assert len(client.get("/api/v1/results/?limit=1&offset=0").json()) == 1
    assert client.get(f"/api/v1/results/{result_id}").status_code == 200

    summary = client.get("/api/v1/results/summary", params={"student_id": create_student["id"]})
    assert summary.status_code == 200
    assert summary.json() == {"total_results": 1, "average_score": 45.0, "highest_score": 45.0, "lowest_score": 45.0}

    assert client.patch(f"/api/v1/results/{result_id}", json={"score": 40}).json()["score"] == 40
    assert client.patch(f"/api/v1/results/{result_id}", json={"score": 60}).status_code == 400
    updated = {**payload, "score": 35}
    assert client.put(f"/api/v1/results/{result_id}", json=updated).json()["score"] == 35
    assert client.delete(f"/api/v1/results/{result_id}").status_code == 204
    assert client.get(f"/api/v1/results/{result_id}").status_code == 404


def test_result_requires_enrolled_student(client, create_class, create_student, create_assessment):
    response = client.post("/api/v1/results/", json={
        "assessment_id": create_assessment["id"],
        "student_id": create_student["id"],
        "score": 20
    })

    assert response.status_code == 400


def test_deleting_assessment_cascades_results(client, create_class, create_student, create_enrolled_student, create_assessment):
    result = client.post("/api/v1/results/", json={
        "assessment_id": create_assessment["id"],
        "student_id": create_student["id"],
        "score": 20
    }).json()

    assert client.delete(f"/api/v1/assessments/{create_assessment['id']}").status_code == 204
    assert client.get(f"/api/v1/results/{result['id']}").status_code == 404
