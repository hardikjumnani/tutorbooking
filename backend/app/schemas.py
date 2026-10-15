from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Status = Literal["BOOKED", "CONFIRMED", "CANCELLED", "DONE"]


class AppointmentCreate(BaseModel):
    student_name: str = Field(min_length=1, max_length=120)
    tutor: str = Field(min_length=1, max_length=120)
    subject: str = Field(min_length=1, max_length=120)
    class_time: datetime
    status: Status = "BOOKED"
    notes: str = ""


class AppointmentUpdate(BaseModel):
    student_name: str | None = Field(default=None, min_length=1, max_length=120)
    tutor: str | None = Field(default=None, min_length=1, max_length=120)
    subject: str | None = Field(default=None, min_length=1, max_length=120)
    class_time: datetime | None = None
    status: Status | None = None
    notes: str | None = None


class AppointmentOut(AppointmentCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class StatsOut(BaseModel):
    total: int
    booked: int
    confirmed: int
    cancelled: int
    done: int
