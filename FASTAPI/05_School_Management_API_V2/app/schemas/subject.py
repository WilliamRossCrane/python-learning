from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class SubjectBase(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    code: str = Field(
        min_length=2,
        max_length=10
    )

    description: str = Field(
        min_length=2,
        max_length=200
    )


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    pass


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


class Subject(SubjectBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )