from sqlalchemy import Column, ForeignKey, Table

from app.database import Base


class_enrolments = Table(
    "class_enrolments",
    Base.metadata,

    Column(
        "student_id",
        ForeignKey(
            "students.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),

    Column(
        "class_id",
        ForeignKey(
            "classes.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)