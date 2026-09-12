from datetime import date
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class AttendanceStatus(str, Enum):

    present = "present"
    absent = "absent"
    late = "late"


class AttendanceBase(BaseModel):

    student_id: int = Field(
        gt=0
    )

    class_id: int = Field(
        gt=0
    )

    attendance_date: date

    status: AttendanceStatus


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):

    status: AttendanceStatus


class Attendance(AttendanceBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )