from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import StudentModel
from app.schemas.student import (
    Student,
    StudentCreate,
    StudentUpdate
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

    students = db.scalars(
        statement
    ).all()

    return students


@router.get(
    "/{student_id}",
    response_model=Student
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.get(
        StudentModel,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


@router.post(
    "/",
    response_model=Student,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    statement = select(
        StudentModel
    ).where(
        StudentModel.email == student.email
    )

    existing_student = db.scalar(
        statement
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


@router.put(
    "/{student_id}",
    response_model=Student
)
def update_student(
    student_id: int,
    updated_student: StudentUpdate,
    db: Session = Depends(get_db)
):

    student = db.get(
        StudentModel,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    statement = select(
        StudentModel
    ).where(
        StudentModel.email == updated_student.email,
        StudentModel.id != student_id
    )

    existing_student = db.scalar(
        statement
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


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.get(
        StudentModel,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    db.delete(student)

    db.commit()

    return