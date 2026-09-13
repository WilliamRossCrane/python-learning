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
    TeacherPatch,
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

    statement = select(
        TeacherModel
    ).where(
        TeacherModel.email == teacher.email
    )
    existing_email = db.scalar(statement)

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A teacher with this email already exists"
        )

    statement = select(
        TeacherModel
    ).where(
        TeacherModel.staff_code == teacher.staff_code
    )
    existing_code = db.scalar(statement)

    if existing_code is not None:
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

    statement = select(
        TeacherModel
    ).where(
        TeacherModel.email == updated_teacher.email,
        TeacherModel.id != teacher_id
    )
    existing_email = db.scalar(statement)

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A teacher with this email already exists"
        )

    statement = select(
        TeacherModel
    ).where(
        TeacherModel.staff_code == updated_teacher.staff_code,
        TeacherModel.id != teacher_id
    )
    existing_code = db.scalar(statement)

    if existing_code is not None:
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


@router.patch(
    "/{teacher_id}",
    response_model=Teacher
)
def patch_teacher(
    teacher_id: int,
    updated_teacher: TeacherPatch,
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

    if updated_teacher.email is not None:
        statement = select(
            TeacherModel
        ).where(
            TeacherModel.email == updated_teacher.email,
            TeacherModel.id != teacher_id
        )
        existing_email = db.scalar(statement)

        if existing_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A teacher with this email already exists"
            )
        teacher.email = updated_teacher.email

    if updated_teacher.staff_code is not None:
        statement = select(
            TeacherModel
        ).where(
            TeacherModel.staff_code == updated_teacher.staff_code,
            TeacherModel.id != teacher_id
        )
        existing_code = db.scalar(statement)

        if existing_code is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A teacher with this staff code already exists"
            )
        teacher.staff_code = updated_teacher.staff_code

    if updated_teacher.first_name is not None:
        teacher.first_name = updated_teacher.first_name

    if updated_teacher.last_name is not None:
        teacher.last_name = updated_teacher.last_name

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