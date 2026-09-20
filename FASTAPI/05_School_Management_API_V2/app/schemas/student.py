from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


class StudentBase(BaseModel):

    first_name: str = Field(
        min_length=1,
        max_length=50
    )

    last_name: str = Field(
        min_length=1,
        max_length=50
    )

    year_level: int = Field(
        ge=7,
        le=12
    )

    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentPatch(BaseModel):

    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    year_level: int | None = Field(
        default=None,
        ge=7,
        le=12
    )

    email: EmailStr | None = None


class Student(StudentBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )