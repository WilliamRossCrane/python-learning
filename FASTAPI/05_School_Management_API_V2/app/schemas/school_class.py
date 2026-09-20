from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class SchoolClassBase(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    teacher_id: int = Field(
        gt=0
    )

    subject_id: int = Field(
        gt=0
    )


class SchoolClassCreate(SchoolClassBase):
    pass


class SchoolClassUpdate(SchoolClassBase):
    pass


class SchoolClass(SchoolClassBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )