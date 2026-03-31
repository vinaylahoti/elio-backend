from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.services.ai_service import generate_reply


router = APIRouter()


def is_simple_log(msg: str) -> bool:
    msg = msg.lower()
    return "gym" in msg or "protein" in msg or "sleep" in msg


@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    body = str(form_data.get("Body", "")).strip()

    print("Incoming message:", body)

    if is_simple_log(body):
        reply = "Logged 💪"
    else:
        reply = generate_reply(body)

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>
"""

    return Response(content=twiml, media_type="application/xml")
