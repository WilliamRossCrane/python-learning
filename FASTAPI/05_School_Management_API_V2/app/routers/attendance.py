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