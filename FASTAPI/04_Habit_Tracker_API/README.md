# Personal Productivity & Habit Tracker API

This project is the next step after Pokemon API V2. It will grow from a small FastAPI app into a production-style backend for habits, tasks, goals, and daily progress.

The project is built one feature and one Git commit at a time so each new idea stays easy to understand.

## Current step: Project foundation

The first version includes:

- a structured `app` package
- FastAPI application metadata
- a root information route
- a health-check route
- automatic Swagger documentation

## Run the app

From this project folder:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

On Windows PowerShell, activate the environment with:

```powershell
venv\Scripts\Activate.ps1
```

Then open:

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Learning roadmap

1. ✅ Create the runnable project foundation
2. Add Pydantic habit schemas and validation
3. Build in-memory habit CRUD routes
4. Store habits in SQLite with SQLAlchemy
5. Add users, password hashing, and JWT authentication
6. Record habit completions and calculate streaks
7. Add related tasks, goals, priorities, and deadlines
8. Add filtering, sorting, pagination, and analytics
9. Test the API with pytest and FastAPI TestClient
10. Prepare configuration, CORS, and deployment

## Planned resources

- Users
- Habits
- Habit completions
- Tasks
- Goals

Each step will introduce only the files and concepts needed for that feature.
