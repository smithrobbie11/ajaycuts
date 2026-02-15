from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.config import ADMIN_PIN
from backend.database import get_session
from backend.models import Appointment, BlockedSlot
from backend.availability import get_all_slots

router = APIRouter(prefix="/api/admin")


def verify_pin(x_admin_pin: str = Header(...)):
    if x_admin_pin != ADMIN_PIN:
        raise HTTPException(status_code=403, detail="Invalid PIN")


class BlockSlotRequest(BaseModel):
    date: date
    time: str  # "HH:MM"


class BlockDayRequest(BaseModel):
    date: date


@router.get("/appointments")
def list_appointments(
    date: Optional[date] = None,
    session: Session = Depends(get_session),
    _pin: None = Depends(verify_pin),
):
    query = select(Appointment)
    if date:
        query = query.where(Appointment.date == date)
    query = query.order_by(Appointment.date, Appointment.start_time)
    appointments = session.exec(query).all()
    return [
        {
            "id": a.id,
            "customer_name": a.customer_name,
            "customer_phone": a.customer_phone,
            "service_name": a.service_name,
            "date": str(a.date),
            "time": a.start_time.strftime("%H:%M"),
            "slots_needed": a.slots_needed,
        }
        for a in appointments
    ]


@router.delete("/appointments/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    session: Session = Depends(get_session),
    _pin: None = Depends(verify_pin),
):
    appt = session.get(Appointment, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    session.delete(appt)
    session.commit()
    return {"status": "cancelled"}


@router.post("/block-slot")
def block_slot(
    req: BlockSlotRequest,
    session: Session = Depends(get_session),
    _pin: None = Depends(verify_pin),
):
    existing = session.exec(
        select(BlockedSlot).where(
            BlockedSlot.date == req.date,
            BlockedSlot.time == req.time,
        )
    ).first()
    if existing:
        return {"status": "already blocked"}
    session.add(BlockedSlot(date=req.date, time=req.time))
    session.commit()
    return {"status": "slot blocked"}


@router.delete("/unblock-slot")
def unblock_slot(
    req: BlockSlotRequest,
    session: Session = Depends(get_session),
    _pin: None = Depends(verify_pin),
):
    blocked = session.exec(
        select(BlockedSlot).where(
            BlockedSlot.date == req.date,
            BlockedSlot.time == req.time,
        )
    ).first()
    if not blocked:
        raise HTTPException(status_code=404, detail="Slot not blocked")
    session.delete(blocked)
    session.commit()
    return {"status": "slot unblocked"}


@router.post("/block-day")
def block_day(
    req: BlockDayRequest,
    session: Session = Depends(get_session),
    _pin: None = Depends(verify_pin),
):
    existing = session.exec(
        select(BlockedSlot).where(
            BlockedSlot.date == req.date,
            BlockedSlot.time == None,  # noqa: E711
        )
    ).first()
    if existing:
        return {"status": "already blocked"}
    session.add(BlockedSlot(date=req.date, time=None))
    session.commit()
    return {"status": "day blocked"}


@router.delete("/unblock-day")
def unblock_day(
    req: BlockDayRequest,
    session: Session = Depends(get_session),
    _pin: None = Depends(verify_pin),
):
    blocked = session.exec(
        select(BlockedSlot).where(
            BlockedSlot.date == req.date,
            BlockedSlot.time == None,  # noqa: E711
        )
    ).first()
    if not blocked:
        raise HTTPException(status_code=404, detail="Day not blocked")
    session.delete(blocked)
    session.commit()
    return {"status": "day unblocked"}


@router.get("/blocked/{target_date}")
def get_blocked(
    target_date: date,
    session: Session = Depends(get_session),
    _pin: None = Depends(verify_pin),
):
    blocks = session.exec(
        select(BlockedSlot).where(BlockedSlot.date == target_date)
    ).all()

    day_blocked = any(b.time is None for b in blocks)
    blocked_slots = [b.time for b in blocks if b.time is not None]

    return {
        "date": str(target_date),
        "day_blocked": day_blocked,
        "blocked_slots": blocked_slots,
        "all_slots": [s.strftime("%H:%M") for s in get_all_slots()],
    }
