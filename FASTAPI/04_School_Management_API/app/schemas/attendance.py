from enum import Enum

from pydantic import BaseModel


class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"


class AttendanceBase(BaseModel):
    class_id: int
    student_id: int
    status: AttendanceStatus


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    status: AttendanceStatus


class Attendance(AttendanceBase):
    id: int