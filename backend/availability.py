from datetime import date, time
from sqlmodel import Session, select

from backend.config import DAY_HOURS, SLOT_MINUTES
from backend.models import Appointment, BlockedSlot


def get_all_slots(start_h: int, start_m: int, end_h: int, end_m: int) -> list[time]:
    slots = []
    hour = start_h
    minute = start_m
    end_total = end_h * 60 + end_m
    while hour * 60 + minute < end_total:
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
    weekday = target_date.weekday()  # Monday=0, Sunday=6
    if weekday not in DAY_HOURS:
        return []

    start_h, start_m, end_h, end_m = DAY_HOURS[weekday]
    all_slots = get_all_slots(start_h, start_m, end_h, end_m)

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
