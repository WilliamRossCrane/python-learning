from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.school_class import SchoolClassModel
from app.models.student import StudentModel


def enrol_student(db: Session, class_id: int, student_id: int):

    school_class = db.get(SchoolClassModel, class_id)
    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    student = db.get(StudentModel, student_id)
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

    school_class.students.append(student)
    db.commit()

    return {
        "message": "Student enrolled successfully",
        "class_id": class_id,
        "student_id": student_id
    }


def remove_student_from_class(db: Session, class_id: int, student_id: int):

    school_class = db.get(SchoolClassModel, class_id)
    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    student = db.get(StudentModel, student_id)
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

    school_class.students.remove(student)
    db.commit()

    return


def get_class_students(db: Session, class_id: int):

    school_class = db.get(SchoolClassModel, class_id)
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


def get_student_classes(db: Session, student_id: int):

    student = db.get(StudentModel, student_id)
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
