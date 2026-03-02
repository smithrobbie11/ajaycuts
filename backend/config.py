import os

ADMIN_PIN = os.getenv("ADMIN_PIN", "1234")

START_HOUR = 9
END_HOUR = 17
SLOT_MINUTES = 15

SERVICES = [
    {"name": "Skin Fade", "duration": 60, "slots_needed": 4, "price": 20},
    {"name": "Haircut", "duration": 45, "slots_needed": 3, "price": 18},
    {"name": "Skin Fade + Beard", "duration": 75, "slots_needed": 5, "price": 25},
    {"name": "Beard Trim", "duration": 30, "slots_needed": 2, "price": 10},
    {"name": "Under 16s", "duration": 45, "slots_needed": 3, "price": 16},
]
