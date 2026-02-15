from datetime import date, time, datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    customer_phone: str
    service_name: str
    date: date
    start_time: time
    slots_needed: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BlockedSlot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    time: Optional[str] = None  # "HH:MM" or None for whole day blocked
