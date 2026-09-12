from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enrolment import class_enrolments


if TYPE_CHECKING:
    from app.models.attendance import AttendanceModel
    from app.models.student import StudentModel
    from app.models.subject import SubjectModel
    from app.models.teacher import TeacherModel


class SchoolClassModel(Base):

    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id"),
        nullable=False
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable=False
    )

    teacher: Mapped["TeacherModel"] = relationship(
        back_populates="classes"
    )

    subject: Mapped["SubjectModel"] = relationship(
        back_populates="classes"
    )

    students: Mapped[list["StudentModel"]] = relationship(
        secondary=class_enrolments,
        back_populates="classes"
    )

    attendance_records: Mapped[list["AttendanceModel"]] = relationship(
        back_populates="school_class",
        cascade="all, delete-orphan"
    )