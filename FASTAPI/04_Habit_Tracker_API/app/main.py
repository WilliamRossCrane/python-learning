from fastapi import FastAPI


app = FastAPI(
    title="Personal Productivity & Habit Tracker API",
    description=(
        "A learning project for building habits, tasks, goals, "
        "and daily progress with FastAPI."
    ),
    version="0.1.0",
)


@app.get("/", tags=["General"], summary="Show API information")
def root() -> dict[str, str]:
    return {
        "name": "Personal Productivity & Habit Tracker API",
        "version": app.version,
        "message": "The Habit Tracker API is running.",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["General"], summary="Check API health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "The Habit Tracker API is healthy.",
    }
