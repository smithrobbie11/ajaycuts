import os

ADMIN_PIN = os.getenv("ADMIN_PIN", "1234")

START_HOUR = 9
END_HOUR = 17
SLOT_MINUTES = 15

SERVICES = [
    {"name": "Haircut / Skinfade", "duration": 60, "slots_needed": 4},
    {"name": "Skin Fade + Beard", "duration": 75, "slots_needed": 5},
    {"name": "Beard Trim", "duration": 30, "slots_needed": 2},
    {"name": "Under 16s", "duration": 45, "slots_needed": 3},
]
