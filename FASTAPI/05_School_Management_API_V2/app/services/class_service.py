from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.school_class import SchoolClassModel
from app.models.subject import SubjectModel
from app.models.teacher import TeacherModel
from app.schemas.school_class import SchoolClassCreate, SchoolClassUpdate


def get_classes(
    db: Session,
    teacher_id: int | None = None,
    subject_id: int | None = None,
    search: str | None = None,
    limit: int = 20,
    offset: int = 0,
):

    statement = select(SchoolClassModel)

    if teacher_id is not None:
        statement = statement.where(
            SchoolClassModel.teacher_id == teacher_id
        )

    if subject_id is not None:
        statement = statement.where(
            SchoolClassModel.subject_id == subject_id
        )

    if search is not None and search.strip():
        search_term = f"%{search.strip()}%"
        statement = statement.where(
            SchoolClassModel.name.ilike(search_term)
        )

    statement = statement.order_by(
        SchoolClassModel.name.asc()
    ).offset(offset).limit(limit)

    return db.scalars(statement).all()


def get_class(db: Session, class_id: int):

    school_class = db.get(SchoolClassModel, class_id)

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    return school_class


def create_class(db: Session, school_class: SchoolClassCreate):

    teacher = db.get(TeacherModel, school_class.teacher_id)
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    subject = db.get(SubjectModel, school_class.subject_id)
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    new_class = SchoolClassModel(
        name=school_class.name,
        teacher_id=school_class.teacher_id,
        subject_id=school_class.subject_id
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class


def update_class(db: Session, class_id: int, updated_class: SchoolClassUpdate):

    school_class = get_class(db, class_id)

    teacher = db.get(TeacherModel, updated_class.teacher_id)
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    subject = db.get(SubjectModel, updated_class.subject_id)
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    school_class.name = updated_class.name
    school_class.teacher_id = updated_class.teacher_id
    school_class.subject_id = updated_class.subject_id

    db.commit()
    db.refresh(school_class)

    return school_class


def delete_class(db: Session, class_id: int):

    school_class = get_class(db, class_id)

    db.delete(school_class)
    db.commit()

    return
