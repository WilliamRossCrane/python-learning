from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import (
    Student,
    StudentCreate,
    StudentUpdate
)
from app.services.student_service import (
    create_student as create_student_service,
    delete_student as delete_student_service,
    get_student as get_student_service,
    get_students as get_students_service,
    update_student as update_student_service,
)


router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"]
)


@router.get(
    "/",
    response_model=list[Student]
)
def get_students(
    year_level: int | None = Query(default=None, ge=7, le=12),
    search: str | None = Query(default=None),
    sort_by: str = Query(default="id", pattern="^(id|first_name|last_name|year_level|email)$"),
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):

    return get_students_service(
        db=db,
        year_level=year_level,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{student_id}",
    response_model=Student
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    return get_student_service(db=db, student_id=student_id)


@router.post(
    "/",
    response_model=Student,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    return create_student_service(db=db, student=student)


@router.put(
    "/{student_id}",
    response_model=Student
)
def update_student(
    student_id: int,
    updated_student: StudentUpdate,
    db: Session = Depends(get_db)
):

    return update_student_service(db=db, student_id=student_id, updated_student=updated_student)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    delete_student_service(db=db, student_id=student_id)
    return