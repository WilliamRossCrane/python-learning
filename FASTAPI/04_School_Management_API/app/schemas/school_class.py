from pydantic import BaseModel, Field


class SchoolClassBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    teacher_id: int = Field(gt=0)
    subject_id: int = Field(gt=0)
    student_ids: list[int] = []


class SchoolClassCreate(SchoolClassBase):
    pass


class SchoolClassUpdate(SchoolClassBase):
    pass


class SchoolClass(SchoolClassBase):
    id: int