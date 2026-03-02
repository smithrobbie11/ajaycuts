import os
import requests
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session, select

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

    account_sid = os.environ["SMS_ACCOUNT_SID"]
    auth_token = os.environ["SMS_AUTH_TOKEN"]
    from_number = os.environ["SMS_FROM_NUMBER"]
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    sent = 0
    for appt in appointments:
        try:
            requests.post(
                url,
                auth=(account_sid, auth_token),
                data={
                    "From": from_number,
                    "To": appt.customer_phone,
                    "Body": (
                        f"Hi {appt.customer_name}, just a reminder that you have a "
                        f"{appt.service_name} booked for tomorrow at "
                        f"{appt.start_time.strftime('%H:%M')} with CutsByAK. See you then!"
                    ),
                },
            )
            appt.reminder_sent = True
            session.add(appt)
            sent += 1
        except Exception:
            pass

    session.commit()
    return {"sent": sent, "date": str(tomorrow)}
