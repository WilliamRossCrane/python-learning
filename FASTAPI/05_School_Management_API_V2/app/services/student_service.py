from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.student import StudentModel
from app.schemas.student import StudentCreate, StudentPatch, StudentUpdate


def get_students(
    db: Session,
    year_level: int | None = None,
    search: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    limit: int = 20,
    offset: int = 0,
):

    statement = select(StudentModel)

    if year_level is not None:
        statement = statement.where(
            StudentModel.year_level == year_level
        )

    if search is not None and search.strip():
        search_term = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                StudentModel.first_name.ilike(search_term),
                StudentModel.last_name.ilike(search_term),
                StudentModel.email.ilike(search_term)
            )
        )

    sort_columns = {
        "id": StudentModel.id,
        "first_name": StudentModel.first_name,
        "last_name": StudentModel.last_name,
        "year_level": StudentModel.year_level,
        "email": StudentModel.email
    }

    sort_column = sort_columns[sort_by]
    if sort_order == "desc":
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    statement = statement.offset(offset).limit(limit)

    return db.scalars(statement).all()


def get_student(db: Session, student_id: int):

    student = db.get(StudentModel, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


def create_student(db: Session, student: StudentCreate):

    existing_student = db.scalar(
        select(StudentModel).where(
            StudentModel.email == student.email
        )
    )

    if existing_student is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists"
        )

    new_student = StudentModel(
        first_name=student.first_name,
        last_name=student.last_name,
        year_level=student.year_level,
        email=student.email
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def update_student(db: Session, student_id: int, updated_student: StudentUpdate):

    student = get_student(db, student_id)

    existing_student = db.scalar(
        select(StudentModel).where(
            StudentModel.email == updated_student.email,
            StudentModel.id != student_id
        )
    )

    if existing_student is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists"
        )

    student.first_name = updated_student.first_name
    student.last_name = updated_student.last_name
    student.year_level = updated_student.year_level
    student.email = updated_student.email

    db.commit()
    db.refresh(student)

    return student


def patch_student(db: Session, student_id: int, updated_student: StudentPatch):

    student = get_student(db, student_id)

    if updated_student.first_name is not None:
        student.first_name = updated_student.first_name

    if updated_student.last_name is not None:
        student.last_name = updated_student.last_name

    if updated_student.year_level is not None:
        student.year_level = updated_student.year_level

    if updated_student.email is not None:
        existing_student = db.scalar(
            select(StudentModel).where(
                StudentModel.email == updated_student.email,
                StudentModel.id != student_id
            )
        )

        if existing_student is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A student with this email already exists"
            )

        student.email = updated_student.email

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):

    student = get_student(db, student_id)

    db.delete(student)
    db.commit()

    return
