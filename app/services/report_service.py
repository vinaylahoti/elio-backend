from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.daily_log import DailyLog
from app.models.goals import Goals
from app.models.user import User
from app.schemas.log import WeeklyReport
from app.utils.scoring import calculate_daily_score


def generate_weekly_report(db: Session, user_id: int) -> WeeklyReport:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    goals = db.query(Goals).filter(Goals.user_id == user_id).first()
    if not goals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goals not found")

    end_date = date.today()
    start_date = end_date - timedelta(days=6)

    logs = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == user_id, DailyLog.date >= start_date, DailyLog.date <= end_date)
        .order_by(DailyLog.date.asc())
        .all()
    )

    gym_days = sum(1 for log in logs if log.gym)
    avg_protein = round(sum(log.protein for log in logs) / len(logs), 2) if logs else 0.0
    alcohol_days = sum(1 for log in logs if log.alcohol)
    smoking_days = sum(1 for log in logs if log.smoking)
    sleep_consistency = sum(1 for log in logs if log.sleep >= 7)

    average_score = (
        round(sum(calculate_daily_score(log=log, protein_target=goals.protein_target) for log in logs) / len(logs), 2)
        if logs
        else 0.0
    )

    return WeeklyReport(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        gym_days=gym_days,
        avg_protein=avg_protein,
        alcohol_days=alcohol_days,
        smoking_days=smoking_days,
        sleep_consistency=sleep_consistency,
        average_score=average_score,
    )
