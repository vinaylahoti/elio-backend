from datetime import date

from pydantic import BaseModel, Field


class DailyLogCreate(BaseModel):
    user_id: int
    date: date
    gym: bool = False
    protein: int = Field(ge=0, le=500)
    alcohol: bool = False
    smoking: bool = False
    sleep: bool = False
    mood: int = Field(ge=1, le=4)


class DailyLogRead(DailyLogCreate):
    id: int

    model_config = {"from_attributes": True}


class WeeklyReport(BaseModel):
    user_id: int
    start_date: date
    end_date: date
    gym_days: int
    avg_protein: float
    alcohol_days: int
    smoking_days: int
    sleep_consistency: int
    average_score: float
