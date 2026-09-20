def test_attendance_create_filters_history_and_delete(client, create_class, create_student, create_enrolled_student):
    attendance = {
        "student_id": create_student["id"],
        "class_id": create_class["id"],
        "attendance_date": "2026-09-13",
        "status": "present"
    }
    created = client.post("/api/v1/attendance/", json=attendance)
    assert created.status_code == 201
    attendance_id = created.json()["id"]

    assert client.post("/api/v1/attendance/", json=attendance).status_code == 409
    assert len(client.get(f"/api/v1/attendance/?student_id={create_student['id']}").json()) == 1
    assert len(client.get(f"/api/v1/attendance/?class_id={create_class['id']}").json()) == 1
    assert len(client.get("/api/v1/attendance/?attendance_date=2026-09-13&attendance_status=present").json()) == 1
    assert len(client.get("/api/v1/attendance/?limit=1&offset=0").json()) == 1
    assert client.get(f"/api/v1/attendance/{attendance_id}").status_code == 200
    assert len(client.get(f"/api/v1/attendance/students/{create_student['id']}").json()) == 1
    assert len(client.get(f"/api/v1/attendance/classes/{create_class['id']}").json()) == 1
    assert len(client.get(f"/api/v1/attendance/classes/{create_class['id']}/dates/2026-09-13").json()) == 1

    assert client.patch(f"/api/v1/attendance/{attendance_id}", json={"status": "late"}).json()["status"] == "late"
    updated = {**attendance, "status": "absent"}
    assert client.put(f"/api/v1/attendance/{attendance_id}", json=updated).json()["status"] == "absent"
    assert client.delete(f"/api/v1/attendance/{attendance_id}").status_code == 204
    assert client.get(f"/api/v1/attendance/{attendance_id}").status_code == 404


def test_attendance_requires_enrolment_and_valid_status(client, create_class, create_student):
    attendance = {
        "student_id": create_student["id"],
        "class_id": create_class["id"],
        "attendance_date": "2026-09-13",
        "status": "present"
    }
    assert client.post("/api/v1/attendance/", json=attendance).status_code == 400
    assert client.post("/api/v1/attendance/", json={**attendance, "status": "sleeping"}).status_code == 422
