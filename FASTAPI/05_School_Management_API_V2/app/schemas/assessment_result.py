from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class AssessmentResultCreate(BaseModel):

    assessment_id: int = Field(
        gt=0
    )

    student_id: int = Field(
        gt=0
    )

    score: float = Field(
        ge=0
    )


class AssessmentResultUpdate(BaseModel):

    score: float = Field(
        ge=0
    )


class AssessmentResult(BaseModel):

    id: int
    assessment_id: int
    student_id: int
    score: float

    model_config = ConfigDict(
        from_attributes=True
    )