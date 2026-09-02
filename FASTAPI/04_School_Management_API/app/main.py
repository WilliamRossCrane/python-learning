from fastapi import FastAPI

from app.routers import (
    students,
    teachers,
    subjects,
    classes,
    attendance,
    assessments,
    examples,
    weather,
    dashboard,
    reports
)


app = FastAPI(
    title="School Management API",
    description="An intermediate FastAPI learning project for managing school data.",
    version="1.0.0"
)


app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(subjects.router)
app.include_router(classes.router)
app.include_router(attendance.router)
app.include_router(assessments.router)
app.include_router(examples.router)
app.include_router(weather.router)
app.include_router(dashboard.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "name": "School Management API",
        "version": "1.0.0",
        "message": "Welcome to the School Management API",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/api/v1")
def api_info():
    return {
        "version": "v1",
        "description": "Version 1 of the School Management API",
        "status": "in development",
        "resources": [
            "students",
            "teachers",
            "subjects",
            "classes",
            "attendance",
            "assessments",
            "examples",
            "weather",
            "dashboard",
            "reports"
        ]
    }