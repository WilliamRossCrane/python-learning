import csv
import io

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.routers.attendance import attendance_records
from app.routers.classes import classes
from app.routers.students import students


router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"]
)


def get_class_by_id(class_id: int):

    for school_class in classes:
        if school_class["id"] == class_id:
            return school_class

    return None


def get_student_by_id(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    return None


@router.get("/attendance/{class_id}")
def download_attendance_report(class_id: int):

    school_class = get_class_by_id(class_id)

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    class_attendance = [
        record
        for record in attendance_records
        if record["class_id"] == class_id
    ]

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Student ID",
        "First Name",
        "Last Name",
        "Attendance Status"
    ])

    for record in class_attendance:

        student = get_student_by_id(
            record["student_id"]
        )

        if student is None:
            continue

        writer.writerow([
            student["id"],
            student["first_name"],
            student["last_name"],
            record["status"]
        ])

    output.seek(0)

    filename = (
        school_class["name"]
        .lower()
        .replace(" ", "_")
    )

    headers = {
        "Content-Disposition":
        f'attachment; filename="{filename}_attendance.csv"'
    }

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers=headers
    )