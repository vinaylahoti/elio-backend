from app.models.daily_log import DailyLog


def calculate_daily_score(log: DailyLog, protein_target: int) -> int:
    score = 0

    if log.gym:
        score += 20
    if log.protein >= protein_target:
        score += 20
    if not log.alcohol:
        score += 20
    if not log.smoking:
        score += 20
    if log.sleep:
        score += 20

    return score
