def test_enrolment_roster_remove_and_relationship_preservation(client, create_class, create_student):
    class_id = create_class["id"]
    student_id = create_student["id"]

    response = client.post(f"/api/v1/enrolments/classes/{class_id}/students/{student_id}")
    assert response.status_code == 201
    assert client.post(f"/api/v1/enrolments/classes/{class_id}/students/{student_id}").status_code == 409

    roster = client.get(f"/api/v1/enrolments/classes/{class_id}/students")
    assert roster.status_code == 200
    assert roster.json()[0]["id"] == student_id

    student_classes = client.get(f"/api/v1/enrolments/students/{student_id}/classes")
    assert student_classes.status_code == 200
    assert student_classes.json()[0]["id"] == class_id

    assert client.delete(f"/api/v1/enrolments/classes/{class_id}/students/{student_id}").status_code == 204
    assert client.get(f"/api/v1/students/{student_id}").status_code == 200
    assert client.get(f"/api/v1/classes/{class_id}").status_code == 200
    assert client.get(f"/api/v1/enrolments/classes/{class_id}/students").json() == []


def test_enrolment_missing_class_and_student_return_404(client, create_class, create_student):
    assert client.post(f"/api/v1/enrolments/classes/999/students/{create_student['id']}").status_code == 404
    assert client.post(f"/api/v1/enrolments/classes/{create_class['id']}/students/999").status_code == 404
    assert client.delete(f"/api/v1/enrolments/classes/{create_class['id']}/students/999").status_code == 404
