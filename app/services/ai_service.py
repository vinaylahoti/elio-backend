import os

from openai import OpenAI


SYSTEM_PROMPT = """You are Nini, a strict but motivating lifestyle coach.

You ONLY talk about:

* gym/workouts
* diet/protein
* sleep
* habits/discipline
* mental wellness

Rules:

* Keep responses short (max 15-20 words)
* Slightly strict tone
* Conversational, not robotic

If user is off-topic:
Redirect them back to habits and discipline."""


def generate_reply(user_message: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return "OpenAI API key missing. Set OPENAI_API_KEY and try again."

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content or "Back to discipline. Tell me about gym, protein, or sleep."
