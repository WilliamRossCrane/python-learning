from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.teacher import TeacherModel
from app.schemas.teacher import TeacherCreate, TeacherPatch, TeacherUpdate


def get_teachers(db: Session):

    return db.scalars(select(TeacherModel)).all()


def get_teacher(db: Session, teacher_id: int):

    teacher = db.get(TeacherModel, teacher_id)

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    return teacher


def create_teacher(db: Session, teacher: TeacherCreate):

    existing_email = db.scalar(
        select(TeacherModel).where(
            TeacherModel.email == teacher.email
        )
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A teacher with this email already exists"
        )

    existing_code = db.scalar(
        select(TeacherModel).where(
            TeacherModel.staff_code == teacher.staff_code
        )
    )

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


def update_teacher(db: Session, teacher_id: int, updated_teacher: TeacherUpdate):

    teacher = get_teacher(db, teacher_id)

    existing_email = db.scalar(
        select(TeacherModel).where(
            TeacherModel.email == updated_teacher.email,
            TeacherModel.id != teacher_id
        )
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A teacher with this email already exists"
        )

    existing_code = db.scalar(
        select(TeacherModel).where(
            TeacherModel.staff_code == updated_teacher.staff_code,
            TeacherModel.id != teacher_id
        )
    )

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


def patch_teacher(db: Session, teacher_id: int, updated_teacher: TeacherPatch):

    teacher = get_teacher(db, teacher_id)

    if updated_teacher.email is not None:
        existing_email = db.scalar(
            select(TeacherModel).where(
                TeacherModel.email == updated_teacher.email,
                TeacherModel.id != teacher_id
            )
        )

        if existing_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A teacher with this email already exists"
            )

        teacher.email = updated_teacher.email

    if updated_teacher.staff_code is not None:
        existing_code = db.scalar(
            select(TeacherModel).where(
                TeacherModel.staff_code == updated_teacher.staff_code,
                TeacherModel.id != teacher_id
            )
        )

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


def delete_teacher(db: Session, teacher_id: int):

    teacher = get_teacher(db, teacher_id)

    db.delete(teacher)
    db.commit()

    return
