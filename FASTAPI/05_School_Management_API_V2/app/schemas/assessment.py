class AssessmentPatch(BaseModel):

    class_id: int | None = Field(
        default=None,
        gt=0
    )

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    assessment_type: AssessmentType | None = None

    max_score: float | None = Field(
        default=None,
        gt=0
    )

    due_date: date | None = None