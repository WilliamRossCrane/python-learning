from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.teacher import TeacherModel
from app.schemas.teacher import (
    Teacher,
    TeacherCreate,
    TeacherUpdate
)


router = APIRouter(
    prefix="/api/v1/teachers",
    tags=["Teachers"]
)


@router.get(
    "/",
    response_model=list[Teacher]
)
def get_teachers(
    db: Session = Depends(get_db)
):

    statement = select(
        TeacherModel
    )

    teachers = db.scalars(
        statement
    ).all()

    return teachers


@router.get(
    "/{teacher_id}",
    response_model=Teacher
)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = db.get(
        TeacherModel,
        teacher_id
    )

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    return teacher


@router.post(
    "/",
    response_model=Teacher,
    status_code=status.HTTP_201_CREATED
)
def create_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db)
):

    email_statement = select(
        TeacherModel
    ).where(
        TeacherModel.email == teacher.email
    )

    existing_email = db.scalar(
        email_statement
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A teacher with this email already exists"
        )

    staff_code_statement = select(
        TeacherModel
    ).where(
        TeacherModel.staff_code == teacher.staff_code
    )

    existing_staff_code = db.scalar(
        staff_code_statement
    )

    if existing_staff_code is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A teacher with this staff code already exists"
        )

    new_teacher = TeacherModel(
        first_name=teacher.first_name,
        last_name=teacher.last_name,
        email=teacher.email,
        staff_code=teacher.staff_code
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher


@router.put(
    "/{teacher_id}",
    response_model=Teacher
)
def update_teacher(
    teacher_id: int,
    updated_teacher: TeacherUpdate,
    db: Session = Depends(get_db)
):

    teacher = db.get(
        TeacherModel,
        teacher_id
    )

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    email_statement = select(
        TeacherModel
    ).where(
        TeacherModel.email == updated_teacher.email,
        TeacherModel.id != teacher_id
    )

    existing_email = db.scalar(
        email_statement
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A teacher with this email already exists"
        )

    staff_code_statement = select(
        TeacherModel
    ).where(
        TeacherModel.staff_code == updated_teacher.staff_code,
        TeacherModel.id != teacher_id
    )

    existing_staff_code = db.scalar(
        staff_code_statement
    )

    if existing_staff_code is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A teacher with this staff code already exists"
        )

    teacher.first_name = updated_teacher.first_name
    teacher.last_name = updated_teacher.last_name
    teacher.email = updated_teacher.email
    teacher.staff_code = updated_teacher.staff_code

    db.commit()
    db.refresh(teacher)

    return teacher


@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = db.get(
        TeacherModel,
        teacher_id
    )

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    db.delete(teacher)
    db.commit()

    return