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
    AttendanceStatus,
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
    student_id: int | None = Query(default=None, gt=0),
    class_id: int | None = Query(default=None, gt=0),
    attendance_date: date | None = None,
    attendance_status: AttendanceStatus | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):

    statement = select(
        AttendanceModel
    )

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
            AttendanceModel.status == attendance_status.value
        )

    statement = statement.order_by(
        AttendanceModel.attendance_date.desc(),
        AttendanceModel.id.desc()
    ).offset(offset).limit(limit)

    return db.scalars(statement).all()


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


@router.put(
    "/{attendance_id}",
    response_model=Attendance
)
def update_attendance_record(
    attendance_id: int,
    updated_attendance: AttendanceCreate,
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

    student = db.get(
        StudentModel,
        updated_attendance.student_id
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    school_class = db.get(
        SchoolClassModel,
        updated_attendance.class_id
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


@router.patch(
    "/{attendance_id}",
    response_model=Attendance
)
def patch_attendance_record(
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
    "/students/{student_id}",
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
        AttendanceModel.attendance_date.desc(),
        AttendanceModel.id.desc()
    )

    return db.scalars(statement).all()


@router.get(
    "/classes/{class_id}",
    response_model=list[Attendance]
)
def get_class_attendance_records(
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

    statement = select(
        AttendanceModel
    ).where(
        AttendanceModel.class_id == class_id
    ).order_by(
        AttendanceModel.attendance_date.desc(),
        AttendanceModel.id.desc()
    )

    return db.scalars(statement).all()


@router.get(
    "/classes/{class_id}/dates/{attendance_date}",
    response_model=list[Attendance]
)
def get_attendance_for_class_and_date(
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
    ).order_by(
        AttendanceModel.id
    )

    return db.scalars(statement).all()