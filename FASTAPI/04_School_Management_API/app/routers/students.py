from fastapi import APIRouter, HTTPException, status

from app.schemas.student import Student, StudentCreate, StudentUpdate


router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"]
)