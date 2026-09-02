from fastapi import APIRouter, HTTPException, status

from app.schemas.teacher import Teacher, TeacherCreate, TeacherUpdate


router = APIRouter(
    prefix="/api/v1/teachers",
    tags=["Teachers"]
)


teachers = [
    {
        "id": 1,
        "first_name": "Erwin",
        "last_name": "Munroe",
        "email": "erwin@example.com",
        "staff_code": "T001"
    },
    {
        "id": 2,
        "first_name": "Dan",
        "last_name": "Cousins",
        "email": "dan@example.com",
        "staff_code": "T002"
    }
]


@router.get("/", response_model=list[Teacher])
def get_teachers():
    return teachers


@router.get("/{teacher_id}", response_model=Teacher)
def get_teacher(teacher_id: int):

    for teacher in teachers:
        if teacher["id"] == teacher_id:
            return teacher

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Teacher not found"
    )


@router.post(
    "/",
    response_model=Teacher,
    status_code=status.HTTP_201_CREATED
)
def create_teacher(teacher: TeacherCreate):

    for existing_teacher in teachers:
        if existing_teacher["email"].lower() == teacher.email.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A teacher with this email already exists"
            )

        if existing_teacher["staff_code"].lower() == teacher.staff_code.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A teacher with this staff code already exists"
            )

    new_id = max(
        existing_teacher["id"]
        for existing_teacher in teachers
    ) + 1 if teachers else 1

    new_teacher = {
        "id": new_id,
        **teacher.model_dump()
    }

    teachers.append(new_teacher)

    return new_teacher


@router.put("/{teacher_id}", response_model=Teacher)
def update_teacher(
    teacher_id: int,
    updated_teacher: TeacherUpdate
):

    for index, teacher in enumerate(teachers):

        if teacher["id"] == teacher_id:

            for existing_teacher in teachers:

                if (
                    existing_teacher["id"] != teacher_id
                    and existing_teacher["email"].lower()
                    == updated_teacher.email.lower()
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="A teacher with this email already exists"
                    )

                if (
                    existing_teacher["id"] != teacher_id
                    and existing_teacher["staff_code"].lower()
                    == updated_teacher.staff_code.lower()
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="A teacher with this staff code already exists"
                    )

            teachers[index] = {
                "id": teacher_id,
                **updated_teacher.model_dump()
            }

            return teachers[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Teacher not found"
    )


@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_teacher(teacher_id: int):

    for index, teacher in enumerate(teachers):

        if teacher["id"] == teacher_id:
            teachers.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Teacher not found"
    )