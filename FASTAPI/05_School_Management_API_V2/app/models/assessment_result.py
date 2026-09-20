from typing import TYPE_CHECKING

from sqlalchemy import (
    Float,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database import Base


if TYPE_CHECKING:
    from app.models.assessment import AssessmentModel
    from app.models.student import StudentModel


class AssessmentResultModel(Base):

    __tablename__ = "assessment_results"

    __table_args__ = (
        UniqueConstraint(
            "assessment_id",
            "student_id",
            name="uq_assessment_student_result"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    assessment_id: Mapped[int] = mapped_column(
        ForeignKey(
            "assessments.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    assessment: Mapped["AssessmentModel"] = relationship(
        back_populates="results"
    )

    student: Mapped["StudentModel"] = relationship(
        back_populates="assessment_results"
    )