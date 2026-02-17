from datetime import datetime, timedelta, time


def generate_slots(start: time, end: time, duration_minutes: int):
    slots = []
    current = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)

    while current + timedelta(minutes=duration_minutes) <= end_dt:
        slots.append(current.time())
        current += timedelta(minutes=duration_minutes)

    return slots
