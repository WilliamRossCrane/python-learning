from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.subject import SubjectModel
from app.schemas.subject import SubjectCreate, SubjectPatch, SubjectUpdate


def get_subjects(db: Session):

    return db.scalars(select(SubjectModel)).all()


def get_subject(db: Session, subject_id: int):

    subject = db.get(SubjectModel, subject_id)

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    return subject


def create_subject(db: Session, subject: SubjectCreate):

    existing_subject = db.scalar(
        select(SubjectModel).where(
            SubjectModel.code == subject.code
        )
    )

    if existing_subject is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A subject with this code already exists"
        )

    new_subject = SubjectModel(
        name=subject.name,
        code=subject.code,
        description=subject.description
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject


def update_subject(db: Session, subject_id: int, updated_subject: SubjectUpdate):

    subject = get_subject(db, subject_id)

    existing_subject = db.scalar(
        select(SubjectModel).where(
            SubjectModel.code == updated_subject.code,
            SubjectModel.id != subject_id
        )
    )

    if existing_subject is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A subject with this code already exists"
        )

    subject.name = updated_subject.name
    subject.code = updated_subject.code
    subject.description = updated_subject.description

    db.commit()
    db.refresh(subject)

    return subject


def patch_subject(db: Session, subject_id: int, updated_subject: SubjectPatch):

    subject = get_subject(db, subject_id)

    if updated_subject.name is not None:
        subject.name = updated_subject.name

    if updated_subject.code is not None:
        existing_subject = db.scalar(
            select(SubjectModel).where(
                SubjectModel.code == updated_subject.code,
                SubjectModel.id != subject_id
            )
        )

        if existing_subject is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A subject with this code already exists"
            )

        subject.code = updated_subject.code

    if updated_subject.description is not None:
        subject.description = updated_subject.description

    db.commit()
    db.refresh(subject)

    return subject


def delete_subject(db: Session, subject_id: int):

    subject = get_subject(db, subject_id)

    db.delete(subject)
    db.commit()

    return
