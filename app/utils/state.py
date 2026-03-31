USER_STATES: dict[str, dict[str, str]] = {}


def get_user_state(phone: str) -> dict[str, str]:
    return USER_STATES.setdefault(phone, {"step": "start"})


def set_user_state(phone: str, step: str) -> None:
    USER_STATES[phone] = {"step": step}
