from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.daily_log import DailyLog
from app.models.goals import Goals
from app.models.user import User
from app.schemas.log import DailyLogCreate


def create_daily_log(db: Session, payload: DailyLogCreate) -> DailyLog:
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    goals = db.query(Goals).filter(Goals.user_id == payload.user_id).first()
    if not goals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goals not found")

    existing_log = (
        db.query(DailyLog)
        .filter(DailyLog.user_id == payload.user_id, DailyLog.date == payload.date)
        .first()
    )
    if existing_log:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Daily log already exists for this date",
        )

    if payload.protein > goals.protein_target * 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Protein value unrealistic",
        )

    daily_log = DailyLog(**payload.model_dump())
    db.add(daily_log)
    db.commit()
    db.refresh(daily_log)
    return daily_log


def get_user_logs(db: Session, user_id: int) -> list[DailyLog]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db.query(DailyLog).filter(DailyLog.user_id == user_id).order_by(DailyLog.date.desc()).all()
