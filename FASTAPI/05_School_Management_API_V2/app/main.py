from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine


app = FastAPI(
    title="School Management API V2",
    description="A database-backed FastAPI project using SQLAlchemy.",
    version="2.0.0"
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