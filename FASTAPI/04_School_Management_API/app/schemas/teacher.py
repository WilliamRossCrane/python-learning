from pydantic import BaseModel, EmailStr, Field


class TeacherBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    staff_code: str = Field(min_length=2, max_length=10)


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(TeacherBase):
    pass


class Teacher(TeacherBase):
    id: int