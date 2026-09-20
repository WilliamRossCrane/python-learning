from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.subject import (
    Subject,
    SubjectCreate,
    SubjectUpdate
)
from app.services.subject_service import (
    create_subject as create_subject_service,
    delete_subject as delete_subject_service,
    get_subject as get_subject_service,
    get_subjects as get_subjects_service,
    update_subject as update_subject_service,
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

    return get_subjects_service(db=db)


@router.get(
    "/{subject_id}",
    response_model=Subject
)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):

    return get_subject_service(db=db, subject_id=subject_id)


@router.post(
    "/",
    response_model=Subject,
    status_code=status.HTTP_201_CREATED
)
def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db)
):

    return create_subject_service(db=db, subject=subject)


@router.put(
    "/{subject_id}",
    response_model=Subject
)
def update_subject(
    subject_id: int,
    updated_subject: SubjectUpdate,
    db: Session = Depends(get_db)
):

    return update_subject_service(db=db, subject_id=subject_id, updated_subject=updated_subject)


@router.delete(
    "/{subject_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):

    delete_subject_service(db=db, subject_id=subject_id)
    return