from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine

from app.models.attendance import AttendanceModel
from app.models.enrolment import class_enrolments
from app.models.school_class import SchoolClassModel
from app.models.student import StudentModel
from app.models.subject import SubjectModel
from app.models.teacher import TeacherModel

from app.routers import (
    attendance,
    classes,
    enrolments,
    students,
    subjects,
    teachers
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(
        bind=engine
    )

    yield


app = FastAPI(
    title="School Management API V2",
    description="A database-backed FastAPI project using SQLAlchemy.",
    version="2.0.0",
    lifespan=lifespan
)


app.include_router(
    students.router
)

app.include_router(
    teachers.router
)

app.include_router(
    subjects.router
)

app.include_router(
    classes.router
)

app.include_router(
    enrolments.router
)

app.include_router(
    attendance.router
)


@app.get("/")
def root():

    return {
        "name": "School Management API V2",
        "version": "2.0.0",
        "message": "Database-backed school management API",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.get("/health/database")
def database_health_check():

    with engine.connect() as connection:

        connection.execute(
            text("SELECT 1")
        )

    return {
        "status": "healthy",
        "database": "connected"
    }