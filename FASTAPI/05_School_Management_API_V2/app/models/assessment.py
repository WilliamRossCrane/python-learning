from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    Float,
    ForeignKey,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database import Base


if TYPE_CHECKING:
    from app.models.assessment_result import AssessmentResultModel
    from app.models.school_class import SchoolClassModel


class AssessmentModel(Base):

    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    class_id: Mapped[int] = mapped_column(
        ForeignKey(
            "classes.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    assessment_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    max_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    school_class: Mapped["SchoolClassModel"] = relationship(
        back_populates="assessments"
    )

    results: Mapped[list["AssessmentResultModel"]] = relationship(
        back_populates="assessment",
        cascade="all, delete-orphan"
    )