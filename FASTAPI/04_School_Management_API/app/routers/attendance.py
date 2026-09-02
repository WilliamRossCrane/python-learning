from fastapi import APIRouter, HTTPException, status

from app.schemas.attendance import (
    Attendance,
    AttendanceCreate,
    AttendanceUpdate
)

from app.routers.classes import classes


router = APIRouter(
    prefix="/api/v1/attendance",
    tags=["Attendance"]
)


attendance_records = [
    {
        "id": 1,
        "class_id": 1,
        "student_id": 1,
        "status": "present"
    },
    {
        "id": 2,
        "class_id": 1,
        "student_id": 2,
        "status": "late"
    }
]


def get_class_by_id(class_id: int):

    for school_class in classes:
        if school_class["id"] == class_id:
            return school_class

    return None


@router.get("/", response_model=list[Attendance])
def get_attendance():
    return attendance_records


@router.get("/{attendance_id}", response_model=Attendance)
def get_attendance_record(attendance_id: int):

    for record in attendance_records:
        if record["id"] == attendance_id:
            return record

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Attendance record not found"
    )


@router.get(
    "/class/{class_id}",
    response_model=list[Attendance]
)
def get_class_attendance(class_id: int):

    school_class = get_class_by_id(class_id)

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    return [
        record
        for record in attendance_records
        if record["class_id"] == class_id
    ]


@router.post(
    "/",
    response_model=Attendance,
    status_code=status.HTTP_201_CREATED
)
def create_attendance(attendance: AttendanceCreate):

    school_class = get_class_by_id(attendance.class_id)

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    if attendance.student_id not in school_class["student_ids"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not enrolled in this class"
        )

    for existing_record in attendance_records:
        if (
            existing_record["class_id"] == attendance.class_id
            and existing_record["student_id"] == attendance.student_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Attendance has already been recorded for this student"
            )

    new_id = max(
        record["id"]
        for record in attendance_records
    ) + 1 if attendance_records else 1

    new_record = {
        "id": new_id,
        **attendance.model_dump()
    }

    attendance_records.append(new_record)

    return new_record


@router.put(
    "/{attendance_id}",
    response_model=Attendance
)
def update_attendance(
    attendance_id: int,
    updated_attendance: AttendanceUpdate
):

    for index, record in enumerate(attendance_records):

        if record["id"] == attendance_id:

            attendance_records[index] = {
                **record,
                "status": updated_attendance.status
            }

            return attendance_records[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Attendance record not found"
    )


@router.delete(
    "/{attendance_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_attendance(attendance_id: int):

    for index, record in enumerate(attendance_records):

        if record["id"] == attendance_id:
            attendance_records.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Attendance record not found"
    )