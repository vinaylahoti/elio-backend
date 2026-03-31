from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models.daily_log import DailyLog
from app.models.user import User
from app.models.user_state import UserState
from app.utils.scoring import calculate_daily_score


STEP_GYM = "gym"
STEP_PROTEIN = "protein"
STEP_ALCOHOL = "alcohol"
STEP_SLEEP = "sleep"
STEP_DONE = "done"

PROMPT_GYM = "Did you go to the gym today? (yes/no)"
PROMPT_PROTEIN = "🍗 Protein intake today? (enter number in grams)"
PROMPT_ALCOHOL = "🍺 Alcohol today? (yes/no)"
PROMPT_SLEEP = "😴 Sleep hours?"


def get_or_create_user(db: Session, phone: str) -> User:
    user = db.query(User).filter(User.phone == phone).first()
    if user:
        return user

    user = User(phone=phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_state(db: Session, user_id: int) -> UserState:
    state = db.query(UserState).filter(UserState.user_id == user_id).first()
    if state:
        return state

    state = UserState(user_id=user_id, current_step=STEP_GYM)
    db.add(state)
    db.commit()
    db.refresh(state)
    return state


def get_or_create_daily_log(db: Session, user_id: int, log_date: date) -> DailyLog:
    daily_log = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == user_id, DailyLog.date == log_date)
        .first()
    )
    if daily_log:
        return daily_log

    daily_log = DailyLog(
        user_id=user_id,
        date=log_date,
        gym=False,
        protein=0,
        alcohol=False,
        smoking=False,
        sleep=0,
        mood=1,
    )
    db.add(daily_log)
    db.commit()
    db.refresh(daily_log)
    return daily_log


def normalize_phone(phone: str) -> str:
    return phone.replace("whatsapp:", "", 1).strip()


def normalize_message(message: str) -> str:
    return message.strip().lower()


def parse_yes_no(value: str) -> bool | None:
    if value == "yes":
        return True
    if value == "no":
        return False
    return None


def reset_state_if_new_day(state: UserState) -> None:
    if state.updated_at.date() < date.today():
        state.current_step = STEP_GYM


def touch_state(state: UserState) -> None:
    state.updated_at = datetime.utcnow()


def current_prompt(step: str) -> str:
    if step == STEP_GYM:
        return PROMPT_GYM
    if step == STEP_PROTEIN:
        return PROMPT_PROTEIN
    if step == STEP_ALCOHOL:
        return PROMPT_ALCOHOL
    if step == STEP_SLEEP:
        return PROMPT_SLEEP
    return "✅ Today's log is already complete. Come back tomorrow for the next check-in."


def handle_incoming_message(db: Session, phone: str, message: str) -> str:
    user = get_or_create_user(db=db, phone=normalize_phone(phone))
    state = get_or_create_state(db=db, user_id=user.id)
    reset_state_if_new_day(state)
    daily_log = get_or_create_daily_log(db=db, user_id=user.id, log_date=date.today())

    text = normalize_message(message)
    if not text:
        return current_prompt(state.current_step)

    if state.current_step == STEP_GYM:
        gym_value = parse_yes_no(text)
        if gym_value is None:
            return "Reply yes or no. Did you go to the gym today?"

        daily_log.gym = gym_value
        state.current_step = STEP_PROTEIN
        touch_state(state)
        db.commit()
        return PROMPT_PROTEIN

    if state.current_step == STEP_PROTEIN:
        if not text.isdigit():
            return "Enter valid number (e.g., 120)"

        protein = int(text)
        if protein < 0 or protein > 300:
            return "Enter valid number (e.g., 120)"

        daily_log.protein = protein
        state.current_step = STEP_ALCOHOL
        touch_state(state)
        db.commit()
        return PROMPT_ALCOHOL

    if state.current_step == STEP_ALCOHOL:
        alcohol_value = parse_yes_no(text)
        if alcohol_value is None:
            return "Reply yes or no. Alcohol today?"

        daily_log.alcohol = alcohol_value
        state.current_step = STEP_SLEEP
        touch_state(state)
        db.commit()
        return PROMPT_SLEEP

    if state.current_step == STEP_SLEEP:
        if not text.isdigit():
            return "Enter valid sleep hours (0-24)"

        sleep_hours = int(text)
        if sleep_hours < 0 or sleep_hours > 24:
            return "Enter valid sleep hours (0-24)"

        daily_log.sleep = sleep_hours
        state.current_step = STEP_DONE
        touch_state(state)
        db.commit()
        db.refresh(daily_log)

        score = calculate_daily_score(daily_log, protein_target=100)
        return (
            "✅ Log complete!\n\n"
            f"💪 Gym: {'Yes' if daily_log.gym else 'No'}\n"
            f"🍗 Protein: {daily_log.protein}g\n"
            f"🍺 Alcohol: {'Yes' if daily_log.alcohol else 'No'}\n"
            f"😴 Sleep: {daily_log.sleep} hrs\n\n"
            f"Score: {score}/100"
        )

    if state.current_step == STEP_DONE:
        touch_state(state)
        db.commit()
        return "✅ Today's log is already complete. Come back tomorrow for the next check-in."

    state.current_step = STEP_GYM
    touch_state(state)
    db.commit()
    return PROMPT_GYM
