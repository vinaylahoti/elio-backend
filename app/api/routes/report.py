from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.log import WeeklyReport
from app.services.report_service import generate_weekly_report


router = APIRouter()


@router.get("/report/{user_id}", response_model=WeeklyReport)
def get_weekly_report(user_id: int, db: Session = Depends(get_db)) -> WeeklyReport:
    return generate_weekly_report(db=db, user_id=user_id)
