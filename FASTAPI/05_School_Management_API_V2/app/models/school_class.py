from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


if TYPE_CHECKING:
    from app.models.teacher import TeacherModel
    from app.models.subject import SubjectModel


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