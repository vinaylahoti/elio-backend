from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.log import DailyLogCreate, DailyLogRead
from app.services.log_service import create_daily_log, get_user_logs


router = APIRouter()


@router.post("/log", response_model=DailyLogRead, status_code=201)
def create_log(payload: DailyLogCreate, db: Session = Depends(get_db)) -> DailyLogRead:
    return create_daily_log(db=db, payload=payload)


@router.get("/log/{user_id}", response_model=list[DailyLogRead])
def fetch_logs(user_id: int, db: Session = Depends(get_db)) -> list[DailyLogRead]:
    return get_user_logs(db=db, user_id=user_id)
