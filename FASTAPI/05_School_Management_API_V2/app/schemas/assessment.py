from datetime import date
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class AssessmentType(str, Enum):

    exam = "exam"
    assignment = "assignment"
    quiz = "quiz"
    project = "project"


class AssessmentBase(BaseModel):

    class_id: int = Field(
        gt=0
    )

    title: str = Field(
        min_length=2,
        max_length=100
    )

    assessment_type: AssessmentType

    max_score: float = Field(
        gt=0
    )

    due_date: date


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(AssessmentBase):
    pass


class Assessment(AssessmentBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )