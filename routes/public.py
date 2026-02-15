from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.config import SERVICES
from backend.database import get_session
from backend.availability import get_available_slots
from backend.models import Appointment

router = APIRouter(prefix="/api")


class BookingRequest(BaseModel):
    customer_name: str
    customer_phone: str
    service_name: str
    date: date
    time: str  # "HH:MM"


@router.get("/services")
def list_services():
    return SERVICES


@router.get("/availability/{target_date}")
def availability(target_date: date, service: str, session: Session = Depends(get_session)):
    svc = next((s for s in SERVICES if s["name"] == service), None)
    if not svc:
        raise HTTPException(status_code=400, detail="Unknown service")
    slots = get_available_slots(target_date, svc["slots_needed"], session)
    return {"date": str(target_date), "service": service, "available_slots": slots}


@router.post("/book")
def book_appointment(req: BookingRequest, session: Session = Depends(get_session)):
    svc = next((s for s in SERVICES if s["name"] == req.service_name), None)
    if not svc:
        raise HTTPException(status_code=400, detail="Unknown service")

    available = get_available_slots(req.date, svc["slots_needed"], session)
    if req.time not in available:
        raise HTTPException(status_code=409, detail="Slot no longer available")

    parts = req.time.split(":")
    start_time = time(int(parts[0]), int(parts[1]))

    appt = Appointment(
        customer_name=req.customer_name,
        customer_phone=req.customer_phone,
        service_name=req.service_name,
        date=req.date,
        start_time=start_time,
        slots_needed=svc["slots_needed"],
    )
    session.add(appt)
    session.commit()
    session.refresh(appt)
    return {
        "status": "booked",
        "appointment_id": appt.id,
        "service": appt.service_name,
        "date": str(appt.date),
        "time": req.time,
        "customer_name": appt.customer_name,
    }
