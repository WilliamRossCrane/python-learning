from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    year_level: int = Field(ge=7, le=12)
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class Student(StudentBase):
    id: int