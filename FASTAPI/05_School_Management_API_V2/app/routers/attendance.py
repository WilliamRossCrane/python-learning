from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attendance import AttendanceModel
from app.models.school_class import SchoolClassModel
from app.models.student import StudentModel
from app.schemas.attendance import (
    Attendance,
    AttendanceCreate,
    AttendanceUpdate
)


router = APIRouter(
    prefix="/api/v1/attendance",
    tags=["Attendance"]
)


@router.get(
    "/",
    response_model=list[Attendance]
)
def get_attendance_records(
    db: Session = Depends(get_db)
):

    statement = select(
        AttendanceModel
    ).order_by(
        AttendanceModel.attendance_date.desc(),
        AttendanceModel.id.desc()
    )

    attendance_records = db.scalars(
        statement
    ).all()

    return attendance_records


@router.get(
    "/{attendance_id}",
    response_model=Attendance
)
def get_attendance_record(
    attendance_id: int,
    db: Session = Depends(get_db)
):

    attendance_record = db.get(
        AttendanceModel,
        attendance_id
    )

    if attendance_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )

    return attendance_record


@router.post(
    "/",
    response_model=Attendance,
    status_code=status.HTTP_201_CREATED
)
def create_attendance_record(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):

    student = db.get(
        StudentModel,
        attendance.student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    school_class = db.get(
        SchoolClassModel,
        attendance.class_id
    )

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

    duplicate_statement = select(
        AttendanceModel
    ).where(
        AttendanceModel.student_id == attendance.student_id,
        AttendanceModel.class_id == attendance.class_id,
        AttendanceModel.attendance_date == attendance.attendance_date
    )

    existing_attendance = db.scalar(
        duplicate_statement
    )

    if existing_attendance is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendance has already been recorded for this student, class and date"
        )

    new_attendance = AttendanceModel(
        student_id=attendance.student_id,
        class_id=attendance.class_id,
        attendance_date=attendance.attendance_date,
        status=attendance.status.value
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


@router.put(
    "/{attendance_id}",
    response_model=Attendance
)
def update_attendance_record(
    attendance_id: int,
    updated_attendance: AttendanceUpdate,
    db: Session = Depends(get_db)
):

    attendance_record = db.get(
        AttendanceModel,
        attendance_id
    )

    if attendance_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )

    attendance_record.status = updated_attendance.status.value

    db.commit()
    db.refresh(attendance_record)

    return attendance_record


@router.delete(
    "/{attendance_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_attendance_record(
    attendance_id: int,
    db: Session = Depends(get_db)
):

    attendance_record = db.get(
        AttendanceModel,
        attendance_id
    )

    if attendance_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )

    db.delete(attendance_record)
    db.commit()

    return


@router.get(
    "/classes/{class_id}/date/{attendance_date}",
    response_model=list[Attendance]
)
def get_class_attendance_by_date(
    class_id: int,
    attendance_date: date,
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

    statement = select(
        AttendanceModel
    ).where(
        AttendanceModel.class_id == class_id,
        AttendanceModel.attendance_date == attendance_date
    )

    attendance_records = db.scalars(
        statement
    ).all()

    return attendance_records


@router.get(
    "/students/{student_id}/history",
    response_model=list[Attendance]
)
def get_student_attendance_history(
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

    statement = select(
        AttendanceModel
    ).where(
        AttendanceModel.student_id == student_id
    ).order_by(
        AttendanceModel.attendance_date.desc()
    )

    attendance_records = db.scalars(
        statement
    ).all()

    return attendance_records