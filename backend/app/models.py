from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_name: Mapped[str] = mapped_column(String(120), nullable=False)
    tutor: Mapped[str] = mapped_column(String(120), nullable=False)
    subject: Mapped[str] = mapped_column(String(120), nullable=False)
    class_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="BOOKED")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
