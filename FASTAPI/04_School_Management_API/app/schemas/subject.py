from pydantic import BaseModel, Field


class SubjectBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=10)
    description: str = Field(min_length=2, max_length=200)


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int