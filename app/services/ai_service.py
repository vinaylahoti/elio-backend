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
* Ask only one question at a time

If user is off-topic:
Redirect them back to habits and discipline."""

STEP_FALLBACKS = {
    "gym": "Gym done today?",
    "workout_type": "What did you train?",
    "protein": "Protein intake today?",
    "sleep": "Sleep hours last night?",
    "done": "Logged 👍",
}


def generate_step_reply(current_step: str, user_message: str, next_step: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return STEP_FALLBACKS.get(next_step, "Logged 👍")

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Current step: {current_step}\n"
                    f"User message: {user_message}\n"
                    f"Next step to ask: {next_step}\n"
                    "Reply with a short coaching response that naturally asks the next-step question."
                ),
            },
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content or STEP_FALLBACKS.get(next_step, "Logged 👍")
