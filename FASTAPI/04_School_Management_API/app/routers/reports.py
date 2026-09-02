import csv
import io

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

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


def get_class_attendance(class_id: int):

    return [
        record
        for record in attendance_records
        if record["class_id"] == class_id
    ]


def create_filename(class_name: str):

    return (
        class_name
        .lower()
        .replace(" ", "_")
    )


@router.get("/attendance/{class_id}")
def download_attendance_csv(class_id: int):

    school_class = get_class_by_id(class_id)

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    class_attendance = get_class_attendance(class_id)

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

    filename = create_filename(
        school_class["name"]
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


@router.get("/attendance/{class_id}/pdf")
def download_attendance_pdf(class_id: int):

    school_class = get_class_by_id(class_id)

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    class_attendance = get_class_attendance(
        class_id
    )

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        f"{school_class['name']} Attendance Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1, 0.5 * cm)
    )

    summary = Paragraph(
        f"Total attendance records: {len(class_attendance)}",
        styles["Normal"]
    )

    elements.append(summary)

    elements.append(
        Spacer(1, 0.5 * cm)
    )

    table_data = [
        [
            "Student ID",
            "First Name",
            "Last Name",
            "Status"
        ]
    ]

    for record in class_attendance:

        student = get_student_by_id(
            record["student_id"]
        )

        if student is None:
            continue

        table_data.append([
            student["id"],
            student["first_name"],
            student["last_name"],
            record["status"].title()
        ])

    table = Table(
        table_data,
        colWidths=[
            2.5 * cm,
            4 * cm,
            4 * cm,
            3.5 * cm
        ]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.black
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, 0),
                10
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            )
        ])
    )

    elements.append(table)

    document.build(elements)

    buffer.seek(0)

    filename = create_filename(
        school_class["name"]
    )

    headers = {
        "Content-Disposition":
        f'attachment; filename="{filename}_attendance.pdf"'
    }

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers=headers
    )