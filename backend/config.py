import os

ADMIN_PIN = os.getenv("ADMIN_PIN", "1234")

START_HOUR = 9
END_HOUR = 17
SLOT_MINUTES = 30

SERVICES = [
    {"name": "Haircut / Skinfade", "duration": 60, "slots_needed": 2},
    {"name": "Skin Fade + Beard", "duration": 75, "slots_needed": 3},
    {"name": "Beard Trim", "duration": 30, "slots_needed": 1},
    {"name": "Under 16s", "duration": 45, "slots_needed": 2},
]
