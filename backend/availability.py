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


def get_available_slots(target_date: date, slots_needed: int, session: Session) -> list[str]:
    all_slots = get_all_slots()

    # Check if whole day is blocked
    day_blocks = session.exec(
        select(BlockedSlot).where(
            BlockedSlot.date == target_date,
            BlockedSlot.time == None,  # noqa: E711
        )
    ).first()
    if day_blocks:
        return []

    # Get blocked time slots for this date
    blocked = session.exec(
        select(BlockedSlot).where(
            BlockedSlot.date == target_date,
            BlockedSlot.time != None,  # noqa: E711
        )
    ).all()
    blocked_times = {b.time for b in blocked}

    # Get existing appointments for this date
    appointments = session.exec(
        select(Appointment).where(Appointment.date == target_date)
    ).all()

    # Build set of occupied slot indices
    occupied = set()
    for appt in appointments:
        idx = _slot_index(appt.start_time, all_slots)
        if idx >= 0:
            for i in range(appt.slots_needed):
                occupied.add(idx + i)

    # Find available start times
    available = []
    max_start_index = len(all_slots) - slots_needed

    for i, slot in enumerate(all_slots):
        if i > max_start_index:
            break

        # Check all required consecutive slots
        can_book = True
        for j in range(slots_needed):
            check_idx = i + j
            if check_idx >= len(all_slots):
                can_book = False
                break
            if check_idx in occupied:
                can_book = False
                break
            if all_slots[check_idx].strftime("%H:%M") in blocked_times:
                can_book = False
                break

        if can_book:
            available.append(slot.strftime("%H:%M"))

    return available
