from datetime import date, time, timedelta
from sqlmodel import Session, select

from backend.config import START_HOUR, END_HOUR, SLOT_MINUTES
from backend.models import Appointment, BlockedSlot


def get_all_slots() -> list[time]:
    slots = []
    hour = START_HOUR
    minute = 0
    while hour < END_HOUR or (hour == END_HOUR and minute == 0):
        if hour == END_HOUR and minute == 0:
            break
        slots.append(time(hour, minute))
        minute += SLOT_MINUTES
        if minute >= 60:
            hour += minute // 60
            minute = minute % 60
    return slots


def _slot_index(t: time, all_slots: list[time]) -> int:
    for i, s in enumerate(all_slots):
        if s == t:
            return i
    return -1


def get_available_slots(session, target_date: date):
    # Generate all possible slots
    slots = generate_slots(WORK_START, WORK_END, SLOT_DURATION)

    # Block whole day?
    blocked_day = session.exec(
        select(BlockedSlot).where(
            BlockedSlot.date == target_date,
            BlockedSlot.time == None
        )
    ).first()

    if blocked_day:
        return []

    # Get blocked times
    blocked_times = {
        b.time for b in session.exec(
            select(BlockedSlot).where(
                BlockedSlot.date == target_date,
                BlockedSlot.time != None
            )
        )
    }

    # Get booked times
    booked_times = {
        b.time for b in session.exec(
            select(Booking).where(Booking.date == target_date)
        )
    }

    return [
        slot for slot in slots
        if slot not in blocked_times and slot not in booked_times
    ]
