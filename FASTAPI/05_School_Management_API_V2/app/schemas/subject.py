class SubjectPatch(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    code: str | None = Field(
        default=None,
        min_length=2,
        max_length=10
    )

    description: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )