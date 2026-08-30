from fastapi import APIRouter, HTTPException, status

from app.schemas.student import Student, StudentCreate, StudentUpdate

students = [
    {
        "id": 1,
        "first_name": "Ash",
        "last_name": "Ketchum",
        "year_level": 10,
        "email": "ash@example.com"
    },
    {
        "id": 2,
        "first_name": "Misty",
        "last_name": "Waterflower",
        "year_level": 9,
        "email": "misty@example.com"
    }
]

@router.get("/", response_model=list[Student])
def get_students():
    return students 

router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"]
)

@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )