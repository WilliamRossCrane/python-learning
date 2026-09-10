from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.school_class import SchoolClassModel
from app.models.student import StudentModel


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

    school_class = db.get(
        SchoolClassModel,
        class_id
    )

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    student = db.get(
        StudentModel,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if student in school_class.students:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student is already enrolled in this class"
        )

    school_class.students.append(
        student
    )

    db.commit()

    return {
        "message": "Student enrolled successfully",
        "class_id": class_id,
        "student_id": student_id
    }


@router.delete(
    "/classes/{class_id}/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_student_from_class(
    class_id: int,
    student_id: int,
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

    student = db.get(
        StudentModel,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if student not in school_class.students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student is not enrolled in this class"
        )

    school_class.students.remove(
        student
    )

    db.commit()

    return


@router.get(
    "/classes/{class_id}/students"
)
def get_class_students(
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

    return [
        {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "year_level": student.year_level,
            "email": student.email
        }
        for student in school_class.students
    ]


@router.get(
    "/students/{student_id}/classes"
)
def get_student_classes(
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

    return [
        {
            "id": school_class.id,
            "name": school_class.name,
            "teacher_id": school_class.teacher_id,
            "subject_id": school_class.subject_id
        }
        for school_class in student.classes
    ]