from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.school_class import SchoolClassModel
from app.models.subject import SubjectModel
from app.models.teacher import TeacherModel
from app.schemas.school_class import (
    SchoolClass,
    SchoolClassCreate,
    SchoolClassUpdate
)


router = APIRouter(
    prefix="/api/v1/classes",
    tags=["Classes"]
)


@router.get(
    "/",
    response_model=list[SchoolClass]
)
def get_classes(
    db: Session = Depends(get_db)
):

    statement = select(
        SchoolClassModel
    )

    classes = db.scalars(
        statement
    ).all()

    return classes


@router.get(
    "/{class_id}",
    response_model=SchoolClass
)
def get_class(
    class_id: int,
    db: Session = Depends(get_db)
):

    school_class = db.get(
        SchoolClassModel,
        class_id
    )

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    return school_class


@router.post(
    "/",
    response_model=SchoolClass,
    status_code=status.HTTP_201_CREATED
)
def create_class(
    school_class: SchoolClassCreate,
    db: Session = Depends(get_db)
):

    teacher = db.get(
        TeacherModel,
        school_class.teacher_id
    )

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    subject = db.get(
        SubjectModel,
        school_class.subject_id
    )

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


@router.put(
    "/{class_id}",
    response_model=SchoolClass
)
def update_class(
    class_id: int,
    updated_class: SchoolClassUpdate,
    db: Session = Depends(get_db)
):

    school_class = db.get(
        SchoolClassModel,
        class_id
    )

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    teacher = db.get(
        TeacherModel,
        updated_class.teacher_id
    )

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    subject = db.get(
        SubjectModel,
        updated_class.subject_id
    )

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


@router.delete(
    "/{class_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_class(
    class_id: int,
    db: Session = Depends(get_db)
):

    school_class = db.get(
        SchoolClassModel,
        class_id
    )

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    db.delete(school_class)
    db.commit()

    return