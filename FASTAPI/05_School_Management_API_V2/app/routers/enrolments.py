from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.services.enrolment_service import (
    enrol_student as enrol_student_service,
    get_class_students as get_class_students_service,
    get_student_classes as get_student_classes_service,
    remove_student_from_class as remove_student_from_class_service,
)


router = APIRouter(
    prefix="/api/v1/enrolments",
    tags=["Enrolments"]
)


@router.post(
    "/classes/{class_id}/students/{student_id}",
    status_code=status.HTTP_201_CREATED
)
def enrol_student(
    class_id: int,
    student_id: int,
    db: Session = Depends(get_db)
):

    return enrol_student_service(db=db, class_id=class_id, student_id=student_id)


@router.delete(
    "/classes/{class_id}/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_student_from_class(
    class_id: int,
    student_id: int,
    db: Session = Depends(get_db)
):

    remove_student_from_class_service(db=db, class_id=class_id, student_id=student_id)
    return


@router.get(
    "/classes/{class_id}/students"
)
def get_class_students(
    class_id: int,
    db: Session = Depends(get_db)
):

    return get_class_students_service(db=db, class_id=class_id)


@router.get(
    "/students/{student_id}/classes"
)
def get_student_classes(
    student_id: int,
    db: Session = Depends(get_db)
):

    return get_student_classes_service(db=db, student_id=student_id)