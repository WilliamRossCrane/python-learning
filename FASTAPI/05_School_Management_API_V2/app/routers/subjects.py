from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.subject import SubjectModel
from app.schemas.subject import (
    Subject,
    SubjectCreate,
    SubjectUpdate
)


router = APIRouter(
    prefix="/api/v1/subjects",
    tags=["Subjects"]
)


@router.get(
    "/",
    response_model=list[Subject]
)
def get_subjects(
    db: Session = Depends(get_db)
):

    statement = select(
        SubjectModel
    )

    subjects = db.scalars(
        statement
    ).all()

    return subjects


@router.get(
    "/{subject_id}",
    response_model=Subject
)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):

    subject = db.get(
        SubjectModel,
        subject_id
    )

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    return subject


@router.post(
    "/",
    response_model=Subject,
    status_code=status.HTTP_201_CREATED
)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db)
):

    statement = select(
        SubjectModel
    ).where(
        SubjectModel.code == subject.code
    )

    existing_subject = db.scalar(
        statement
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


@router.put(
    "/{subject_id}",
    response_model=Subject
)
def update_subject(
    subject_id: int,
    updated_subject: SubjectUpdate,
    db: Session = Depends(get_db)
):

    subject = db.get(
        SubjectModel,
        subject_id
    )

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    statement = select(
        SubjectModel
    ).where(
        SubjectModel.code == updated_subject.code,
        SubjectModel.id != subject_id
    )

    existing_subject = db.scalar(
        statement
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


@router.delete(
    "/{subject_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):

    subject = db.get(
        SubjectModel,
        subject_id
    )

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    db.delete(subject)
    db.commit()

    return