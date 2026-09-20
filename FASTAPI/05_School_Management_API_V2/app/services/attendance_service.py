from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.attendance import AttendanceModel
from app.models.school_class import SchoolClassModel
from app.models.student import StudentModel
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


def get_attendance_records(
    db: Session,
    student_id: int | None = None,
    class_id: int | None = None,
    attendance_date: date | None = None,
    attendance_status: str | None = None,
    limit: int = 50,
    offset: int = 0,
):

    statement = select(AttendanceModel)

    if student_id is not None:
        statement = statement.where(
            AttendanceModel.student_id == student_id
        )

    if class_id is not None:
        statement = statement.where(
            AttendanceModel.class_id == class_id
        )

    if attendance_date is not None:
        statement = statement.where(
            AttendanceModel.attendance_date == attendance_date
        )

    if attendance_status is not None:
        statement = statement.where(
            AttendanceModel.status == attendance_status
        )

    statement = statement.order_by(
        AttendanceModel.attendance_date.desc(),
        AttendanceModel.id.desc()
    ).offset(offset).limit(limit)

    return db.scalars(statement).all()


def get_attendance_record(db: Session, attendance_id: int):

    attendance_record = db.get(AttendanceModel, attendance_id)

    if attendance_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )

    return attendance_record


def create_attendance_record(db: Session, attendance: AttendanceCreate):

    student = db.get(StudentModel, attendance.student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    school_class = db.get(SchoolClassModel, attendance.class_id)
    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    if student not in school_class.students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not enrolled in this class"
        )

    existing_record = db.scalar(
        select(AttendanceModel).where(
            AttendanceModel.student_id == attendance.student_id,
            AttendanceModel.class_id == attendance.class_id,
            AttendanceModel.attendance_date == attendance.attendance_date
        )
    )

    if existing_record is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendance record already exists for this student, class, and date"
        )

    new_record = AttendanceModel(
        student_id=attendance.student_id,
        class_id=attendance.class_id,
        attendance_date=attendance.attendance_date,
        status=attendance.status.value
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


def update_attendance_record(db: Session, attendance_id: int, updated_attendance: AttendanceCreate):

    attendance_record = get_attendance_record(db, attendance_id)

    student = db.get(StudentModel, updated_attendance.student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    school_class = db.get(SchoolClassModel, updated_attendance.class_id)
    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    if student not in school_class.students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not enrolled in this class"
        )

    duplicate = db.scalar(
        select(AttendanceModel).where(
            AttendanceModel.student_id == updated_attendance.student_id,
            AttendanceModel.class_id == updated_attendance.class_id,
            AttendanceModel.attendance_date == updated_attendance.attendance_date,
            AttendanceModel.id != attendance_id
        )
    )

    if duplicate is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendance record already exists for this student, class, and date"
        )

    attendance_record.student_id = updated_attendance.student_id
    attendance_record.class_id = updated_attendance.class_id
    attendance_record.attendance_date = updated_attendance.attendance_date
    attendance_record.status = updated_attendance.status.value

    db.commit()
    db.refresh(attendance_record)

    return attendance_record


def patch_attendance_record(db: Session, attendance_id: int, updated_attendance: AttendanceUpdate):

    attendance_record = get_attendance_record(db, attendance_id)
    attendance_record.status = updated_attendance.status.value

    db.commit()
    db.refresh(attendance_record)

    return attendance_record


def delete_attendance_record(db: Session, attendance_id: int):

    attendance_record = get_attendance_record(db, attendance_id)

    db.delete(attendance_record)
    db.commit()

    return


def get_student_attendance_history(db: Session, student_id: int):

    student = db.get(StudentModel, student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    statement = select(AttendanceModel).where(
        AttendanceModel.student_id == student_id
    ).order_by(
        AttendanceModel.attendance_date.desc(),
        AttendanceModel.id.desc()
    )

    return db.scalars(statement).all()


def get_class_attendance_records(db: Session, class_id: int):

    school_class = db.get(SchoolClassModel, class_id)
    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    statement = select(AttendanceModel).where(
        AttendanceModel.class_id == class_id
    ).order_by(
        AttendanceModel.attendance_date.desc(),
        AttendanceModel.id.desc()
    )

    return db.scalars(statement).all()


def get_attendance_for_class_and_date(db: Session, class_id: int, attendance_date: date):

    school_class = db.get(SchoolClassModel, class_id)
    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    statement = select(AttendanceModel).where(
        AttendanceModel.class_id == class_id,
        AttendanceModel.attendance_date == attendance_date
    ).order_by(AttendanceModel.id)

    return db.scalars(statement).all()
