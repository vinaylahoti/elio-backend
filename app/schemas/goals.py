from pydantic import BaseModel, Field


class GoalsBase(BaseModel):
    user_id: int
    gym_target: int = Field(ge=0, le=7)
    protein_target: int = Field(ge=0, le=500)
    alcohol_limit: int = Field(ge=0, le=7)
    smoking_limit: int = Field(ge=0, le=7)


class GoalsCreate(GoalsBase):
    pass


class GoalsRead(GoalsBase):
    id: int

    model_config = {"from_attributes": True}
