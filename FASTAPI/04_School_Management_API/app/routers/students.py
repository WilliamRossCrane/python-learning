from fastapi import APIRouter, HTTPException, status

from app.schemas.student import Student, StudentCreate, StudentUpdate


router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"]
)


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


@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@router.post(
    "/",
    response_model=Student,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: StudentCreate):

    for existing_student in students:
        if existing_student["email"].lower() == student.email.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A student with this email already exists"
            )

    new_id = max(
        existing_student["id"]
        for existing_student in students
    ) + 1 if students else 1

    new_student = {
        "id": new_id,
        **student.model_dump()
    }

    students.append(new_student)

    return new_student


@router.put("/{student_id}", response_model=Student)
def update_student(
    student_id: int,
    updated_student: StudentUpdate
):

    for index, student in enumerate(students):

        if student["id"] == student_id:

            for existing_student in students:
                if (
                    existing_student["id"] != student_id
                    and existing_student["email"].lower()
                    == updated_student.email.lower()
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="A student with this email already exists"
                    )

            students[index] = {
                "id": student_id,
                **updated_student.model_dump()
            }

            return students[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student["id"] == student_id:
            students.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )