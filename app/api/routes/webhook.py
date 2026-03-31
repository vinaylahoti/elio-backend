from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.services.ai_service import generate_step_reply
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
        next_step = "gym"
        set_user_state(phone, next_step)
        reply = generate_step_reply(step, body, next_step)
    elif step == "gym":
        if message in {"yes", "y"}:
            next_step = "workout_type"
        else:
            next_step = "protein"
        set_user_state(phone, next_step)
        reply = generate_step_reply(step, body, next_step)
    elif step == "workout_type":
        next_step = "protein"
        set_user_state(phone, next_step)
        reply = generate_step_reply(step, body, next_step)
    elif step == "protein":
        next_step = "sleep"
        set_user_state(phone, next_step)
        reply = generate_step_reply(step, body, next_step)
    else:
        next_step = "done"
        set_user_state(phone, "start")
        reply = generate_step_reply(step, body, next_step)

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>
"""

    return Response(content=twiml, media_type="application/xml")
