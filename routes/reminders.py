import os
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session, select
from twilio.rest import Client

from backend.database import get_session
from backend.models import Appointment

router = APIRouter(prefix="/api")


@router.post("/reminders/send")
def send_reminders(
    x_cron_secret: str = Header(...),
    session: Session = Depends(get_session),
):
    if x_cron_secret != os.environ["CRON_SECRET"]:
        raise HTTPException(status_code=401, detail="Unauthorized")

    tomorrow = date.today() + timedelta(days=1)

    appointments = session.exec(
        select(Appointment).where(
            Appointment.date == tomorrow,
            Appointment.reminder_sent == False,
        )
    ).all()

    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

    sent = 0
    for appt in appointments:
        try:
            client.messages.create(
                body=(
                    f"Hi {appt.customer_name}, just a reminder that you have a "
                    f"{appt.service_name} booked for tomorrow at "
                    f"{appt.start_time.strftime('%H:%M')} with CutsByAK. See you then!"
                ),
                from_=os.environ["TWILIO_FROM_NUMBER"],
                to=appt.customer_phone,
            )
            appt.reminder_sent = True
            session.add(appt)
            sent += 1
        except Exception:
            pass

    session.commit()
    return {"sent": sent, "date": str(tomorrow)}
