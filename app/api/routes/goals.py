from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.goals import Goals
from app.models.user import User
from app.schemas.goals import GoalsCreate, GoalsRead


router = APIRouter()


@router.post("/goals", response_model=GoalsRead, status_code=status.HTTP_201_CREATED)
def set_goals(payload: GoalsCreate, db: Session = Depends(get_db)) -> Goals:
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    goals = db.query(Goals).filter(Goals.user_id == payload.user_id).first()
    if goals:
        goals.gym_target = payload.gym_target
        goals.protein_target = payload.protein_target
        goals.alcohol_limit = payload.alcohol_limit
        goals.smoking_limit = payload.smoking_limit
    else:
        goals = Goals(**payload.model_dump())
        db.add(goals)

    db.commit()
    db.refresh(goals)
    return goals


@router.get("/goals/{user_id}", response_model=GoalsRead)
def get_goals(user_id: int, db: Session = Depends(get_db)) -> Goals:
    goals = db.query(Goals).filter(Goals.user_id == user_id).first()
    if not goals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goals not found")
    return goals
