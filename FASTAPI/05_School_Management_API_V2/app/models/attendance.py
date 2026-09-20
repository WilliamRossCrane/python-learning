from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database import Base


if TYPE_CHECKING:
    from app.models.school_class import SchoolClassModel
    from app.models.student import StudentModel


class AttendanceModel(Base):

    __tablename__ = "attendance"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "class_id",
            "attendance_date",
            name="uq_student_class_attendance_date"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey(
            "classes.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    student: Mapped["StudentModel"] = relationship(
        back_populates="attendance_records"
    )

    school_class: Mapped["SchoolClassModel"] = relationship(
        back_populates="attendance_records"
    )