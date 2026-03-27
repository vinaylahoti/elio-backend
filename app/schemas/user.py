from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    phone: str = Field(min_length=8, max_length=20)


class UserRead(BaseModel):
    id: int
    phone: str

    model_config = {"from_attributes": True}
