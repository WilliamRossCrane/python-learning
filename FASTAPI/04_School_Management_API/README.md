# School Management API

An intermediate FastAPI learning project demonstrating REST API design, validation, relationships, business rules, asynchronous programming, external API integration, reporting and background tasks.

## Project Overview

The School Management API provides endpoints for managing common school data including:

- Students
- Teachers
- Subjects
- Classes
- Attendance
- Assessments
- Weather
- Dashboard data
- CSV reports
- PDF reports
- Background audit tasks

The project uses in-memory Python data rather than a database so the focus remains on learning FastAPI architecture and backend concepts.

---

## Technologies

- Python
- FastAPI
- Pydantic
- Uvicorn
- HTTPX
- ReportLab

---

## Project Structure

```text
app/
├── main.py
│
├── routers/
│   ├── students.py
│   ├── teachers.py
│   ├── subjects.py
│   ├── classes.py
│   ├── attendance.py
│   ├── assessments.py
│   ├── examples.py
│   ├── weather.py
│   ├── dashboard.py
│   ├── reports.py
│   └── tasks.py
│
└── schemas/
    ├── student.py
    ├── teacher.py
    ├── subject.py
    ├── school_class.py
    ├── attendance.py
    └── assessment.py
```

---

## Setup

Clone the repository and move into the project directory.

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## API Resources

### Students

```text
GET    /api/v1/students/
GET    /api/v1/students/{student_id}
POST   /api/v1/students/
PUT    /api/v1/students/{student_id}
DELETE /api/v1/students/{student_id}
```

Includes validation and duplicate email protection.

### Teachers

```text
GET    /api/v1/teachers/
GET    /api/v1/teachers/{teacher_id}
POST   /api/v1/teachers/
PUT    /api/v1/teachers/{teacher_id}
DELETE /api/v1/teachers/{teacher_id}
```

Teacher email addresses and staff codes must be unique.

### Subjects

```text
GET    /api/v1/subjects/
GET    /api/v1/subjects/{subject_id}
POST   /api/v1/subjects/
PUT    /api/v1/subjects/{subject_id}
DELETE /api/v1/subjects/{subject_id}
```

Subject codes must be unique.

### Classes

```text
GET    /api/v1/classes/
GET    /api/v1/classes/{class_id}
POST   /api/v1/classes/
PUT    /api/v1/classes/{class_id}
DELETE /api/v1/classes/{class_id}
```

Classes connect:

- one teacher
- one subject
- multiple students

Referenced teachers, subjects and students must exist.

### Attendance

```text
GET    /api/v1/attendance/
GET    /api/v1/attendance/{attendance_id}
GET    /api/v1/attendance/class/{class_id}
POST   /api/v1/attendance/
PUT    /api/v1/attendance/{attendance_id}
DELETE /api/v1/attendance/{attendance_id}
```

Attendance rules include:

- the class must exist
- the student must belong to the class
- attendance status must be valid
- duplicate attendance records are prevented

### Assessments

```text
GET    /api/v1/assessments/
GET    /api/v1/assessments/{assessment_id}
GET    /api/v1/assessments/class/{class_id}
POST   /api/v1/assessments/
PUT    /api/v1/assessments/{assessment_id}
DELETE /api/v1/assessments/{assessment_id}
```

Assessment types include:

- exam
- assignment
- quiz
- project

Assessments are linked to classes and include a maximum score and due date.

---

## Async Examples

The project includes examples demonstrating synchronous and asynchronous code.

```text
GET /api/v1/examples/sync
GET /api/v1/examples/async
GET /api/v1/examples/async-dashboard
```

These demonstrate:

- `def`
- `async def`
- blocking operations
- non-blocking operations
- `await`
- `asyncio`
- `asyncio.gather()`

---

## External Weather API

```text
GET /api/v1/weather/current
```

The API uses HTTPX asynchronously to retrieve current weather information from Open-Meteo.

This demonstrates real asynchronous I/O:

```python
async with httpx.AsyncClient() as client:
    response = await client.get(...)
```

---

## Concurrent Dashboard

```text
GET /api/v1/dashboard/
```

The dashboard combines multiple sources of information including:

- weather
- attendance
- assessments

Independent operations are run concurrently using:

```python
await asyncio.gather(...)
```

---

## Reports

Attendance data can be exported in multiple formats.

CSV:

```text
GET /api/v1/reports/attendance/{class_id}
```

PDF:

```text
GET /api/v1/reports/attendance/{class_id}/pdf
```

The project demonstrates:

- CSV generation
- in-memory files
- `StringIO`
- `BytesIO`
- `StreamingResponse`
- ReportLab PDF generation

---

## Background Tasks

```text
POST /api/v1/tasks/audit
```

FastAPI `BackgroundTasks` is used to write audit information after the HTTP response has been returned.

Assessment creation also demonstrates automatic background audit logging.

---

## Key Concepts Learned

This project demonstrates:

- REST API design
- FastAPI routers
- Pydantic schemas
- request validation
- response models
- CRUD operations
- HTTP status codes
- error handling
- business rules
- resource relationships
- enums
- query parameters
- synchronous programming
- asynchronous programming
- `async` and `await`
- HTTPX
- external APIs
- concurrent I/O
- `asyncio.gather()`
- dynamically generated files
- CSV exports
- PDF exports
- background tasks

---

## HTTP Status Codes Used

```text
200 OK
201 Created
204 No Content
400 Bad Request
404 Not Found
409 Conflict
422 Unprocessable Entity
502 Bad Gateway
```

FastAPI and Pydantic automatically handle validation errors where appropriate.

---

## Current Limitations

This project intentionally uses in-memory Python lists.

Data is reset whenever the server restarts.

A future version could introduce:

- SQLAlchemy
- PostgreSQL
- database relationships
- authentication and authorization
- PATCH endpoints
- automated testing
- service and repository layers
- Docker
- deployment

These features have been intentionally left for later projects so this project can focus on core FastAPI concepts.

---

## Learning Purpose

This project was created as part of a progression from beginner Python APIs toward more advanced backend development.

The main focus was moving beyond basic CRUD and understanding how a structured FastAPI application handles validation, relationships, business logic, asynchronous I/O and generated responses.
