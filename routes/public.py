from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from sqlmodel import Session, select

from database import get_session
from models import Service, Booking
from availability import get_available_slots

router = APIRouter()


@router.get("/services")
def list_services(session: Session = Depends(get_session)):
    return session.exec(select(Service)).all()


@router.get("/availability/{target_date}")
def availability(target_date: date, session: Session = Depends(get_session)):
    return get_available_slots(session, target_date)


@router.post("/book")
def book_appointment(booking: Booking, session: Session = Depends(get_session)):
    available = get_available_slots(session, booking.date)

    if booking.time not in available:
        raise HTTPException(status_code=400, detail="Slot unavailable")

    session.add(booking)
    session.commit()
    return {"status": "booked"}
