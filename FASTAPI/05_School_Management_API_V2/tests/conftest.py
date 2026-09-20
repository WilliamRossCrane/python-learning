import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'test_school.db'}"
    test_engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}
    )
    testing_session_local = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False
    )

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)

    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


@pytest.fixture()
def student_payload():
    return {
        "first_name": "Asha",
        "last_name": "Patel",
        "year_level": 10,
        "email": "asha@example.com"
    }


@pytest.fixture()
def teacher_payload():
    return {
        "first_name": "Jordan",
        "last_name": "Lee",
        "email": "jordan@example.com",
        "staff_code": "T001"
    }


@pytest.fixture()
def subject_payload():
    return {
        "name": "Mathematics",
        "code": "MATH",
        "description": "Mathematics fundamentals"
    }


@pytest.fixture()
def create_teacher(client, teacher_payload):
    return client.post("/api/v1/teachers/", json=teacher_payload).json()


@pytest.fixture()
def create_subject(client, subject_payload):
    return client.post("/api/v1/subjects/", json=subject_payload).json()


@pytest.fixture()
def create_student(client, student_payload):
    return client.post("/api/v1/students/", json=student_payload).json()


@pytest.fixture()
def create_class(client, create_teacher, create_subject):
    response = client.post(
        "/api/v1/classes/",
        json={
            "name": "Year 10 Mathematics",
            "teacher_id": create_teacher["id"],
            "subject_id": create_subject["id"]
        }
    )
    return response.json()


@pytest.fixture()
def create_enrolled_student(client, create_class, create_student):
    response = client.post(
        f"/api/v1/enrolments/classes/{create_class['id']}/students/{create_student['id']}"
    )
    assert response.status_code == 201
    return create_student


@pytest.fixture()
def create_assessment(client, create_class):
    response = client.post(
        "/api/v1/assessments/",
        json={
            "class_id": create_class["id"],
            "title": "Algebra Exam",
            "assessment_type": "exam",
            "max_score": 50,
            "due_date": "2026-09-13"
        }
    )
    return response.json()
