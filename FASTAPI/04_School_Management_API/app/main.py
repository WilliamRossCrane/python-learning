from fastapi import FastAPI


app = FastAPI(
    title="School Management API",
    description="An intermediate FastAPI learning project for managing school data.",
    version="1.0.0"
)


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
        "resources": []
    }