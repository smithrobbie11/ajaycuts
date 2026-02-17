from datetime import date, time, datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    duration_minutes: int
    price: float


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    customer_contact: str
    service_id: int
    date: date
    time: time
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BlockedSlot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    time: Optional[time] = None