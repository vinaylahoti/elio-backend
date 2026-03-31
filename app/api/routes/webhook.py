from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.utils.state import get_user_state, set_user_state


router = APIRouter()


@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    body = str(form_data.get("Body", "")).strip()
    phone = str(form_data.get("From", "")).strip()
    message = body.lower()

    state = get_user_state(phone)
    step = state["step"]

    if step == "start":
        reply = "Gym done today?"
        set_user_state(phone, "gym")
    elif step == "gym":
        if message in {"yes", "y"}:
            reply = "What did you train?"
            set_user_state(phone, "workout_type")
        else:
            reply = "Protein intake today?"
            set_user_state(phone, "protein")
    elif step == "workout_type":
        reply = "Protein intake today?"
        set_user_state(phone, "protein")
    elif step == "protein":
        reply = "Sleep hours last night?"
        set_user_state(phone, "sleep")
    else:
        reply = "Logged 👍"
        set_user_state(phone, "start")

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>
"""

    return Response(content=twiml, media_type="application/xml")
