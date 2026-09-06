# School Management API V2

A database-backed FastAPI learning project using SQLAlchemy.

## Focus

This project builds on a previous in-memory FastAPI project by introducing persistent database storage and relational database concepts.

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Current Progress

- FastAPI project structure
- SQLite database configuration
- SQLAlchemy engine
- SQLAlchemy session factory
- Database health check

## Run

Create and activate the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```
