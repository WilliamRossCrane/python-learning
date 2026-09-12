from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enrolment import class_enrolments


if TYPE_CHECKING:
    from app.models.attendance import AttendanceModel
    from app.models.school_class import SchoolClassModel


class StudentModel(Base):

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    year_level: Mapped[int] = mapped_column(
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    classes: Mapped[list["SchoolClassModel"]] = relationship(
        secondary=class_enrolments,
        back_populates="students"
    )

    attendance_records: Mapped[list["AttendanceModel"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan"
    )