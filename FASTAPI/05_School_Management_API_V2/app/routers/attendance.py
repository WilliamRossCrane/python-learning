from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.attendance import (
    Attendance,
    AttendanceCreate,
    AttendanceStatus,
    AttendanceUpdate
)
from app.services.attendance_service import (
    create_attendance_record as create_attendance_record_service,
    delete_attendance_record as delete_attendance_record_service,
    get_attendance_for_class_and_date as get_attendance_for_class_and_date_service,
    get_attendance_record as get_attendance_record_service,
    get_attendance_records as get_attendance_records_service,
    get_class_attendance_records as get_class_attendance_records_service,
    get_student_attendance_history as get_student_attendance_history_service,
    patch_attendance_record as patch_attendance_record_service,
    update_attendance_record as update_attendance_record_service,
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

    return get_attendance_records_service(
        db=db,
        student_id=student_id,
        class_id=class_id,
        attendance_date=attendance_date,
        attendance_status=attendance_status,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{attendance_id}",
    response_model=Attendance
)
def get_attendance_record(
    attendance_id: int,
    db: Session = Depends(get_db)
):

    return get_attendance_record_service(db=db, attendance_id=attendance_id)


@router.post(
    "/",
    response_model=Attendance,
    status_code=status.HTTP_201_CREATED
)
def create_attendance_record(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):

    return create_attendance_record_service(db=db, attendance=attendance)


@router.put(
    "/{attendance_id}",
    response_model=Attendance
)
def update_attendance_record(
    attendance_id: int,
    updated_attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):

    return update_attendance_record_service(db=db, attendance_id=attendance_id, updated_attendance=updated_attendance)


@router.patch(
    "/{attendance_id}",
    response_model=Attendance
)
def patch_attendance_record(
    attendance_id: int,
    updated_attendance: AttendanceUpdate,
    db: Session = Depends(get_db)
):

    return patch_attendance_record_service(db=db, attendance_id=attendance_id, updated_attendance=updated_attendance)


@router.delete(
    "/{attendance_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_attendance_record(
    attendance_id: int,
    db: Session = Depends(get_db)
):

    delete_attendance_record_service(db=db, attendance_id=attendance_id)
    return


@router.get(
    "/students/{student_id}",
    response_model=list[Attendance]
)
def get_student_attendance_history(
    student_id: int,
    db: Session = Depends(get_db)
):

    return get_student_attendance_history_service(db=db, student_id=student_id)


@router.get(
    "/classes/{class_id}",
    response_model=list[Attendance]
)
def get_class_attendance_records(
    class_id: int,
    db: Session = Depends(get_db)
):

    return get_class_attendance_records_service(db=db, class_id=class_id)


@router.get(
    "/classes/{class_id}/dates/{attendance_date}",
    response_model=list[Attendance]
)
def get_attendance_for_class_and_date(
    class_id: int,
    attendance_date: date,
    db: Session = Depends(get_db)
):

    return get_attendance_for_class_and_date_service(db=db, class_id=class_id, attendance_date=attendance_date)