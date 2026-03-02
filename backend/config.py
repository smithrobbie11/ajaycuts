import os

ADMIN_PIN = os.getenv("ADMIN_PIN", "1234")

SLOT_MINUTES = 15

# Per-day hours: (start_hour, start_minute, end_hour, end_minute)
# Monday=0 ... Saturday=5 ; Sunday=6 omitted = unavailable
DAY_HOURS = {
    0: (9, 30, 18, 0),   # Monday
    1: (9, 15, 18, 0),   # Tuesday
    2: (9, 15, 18, 0),   # Wednesday
    3: (9, 15, 18, 0),   # Thursday
    4: (9, 30, 17, 0),   # Friday
    5: (9,  0, 13, 0),   # Saturday
}

SERVICES = [
    {"name": "Skin Fade / Taper Fade", "duration": 60, "slots_needed": 4, "price": 20},
    {"name": "Haircut", "duration": 45, "slots_needed": 3, "price": 18},
    {"name": "Skin Fade + Beard Trim", "duration": 75, "slots_needed": 5, "price": 25},
    {"name": "Haircut + Beard Trim", "duration": 60, "slots_needed": 4, "price": 25},
    {"name": "Head Shave", "duration": 30, "slots_needed": 2, "price": 10},
    {"name": "Under 16s", "duration": 45, "slots_needed": 3, "price": 18},
]
