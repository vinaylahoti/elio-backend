from app.models.daily_log import DailyLog


def calculate_daily_score(log: DailyLog, protein_target: int = 100) -> int:
    score = 0

    if log.gym:
        score += 20
    if log.protein >= protein_target:
        score += 20
    if not log.alcohol:
        score += 20
    if log.sleep >= 7:
        score += 20

    return score
