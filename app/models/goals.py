from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Goals(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False, index=True)
    gym_target: Mapped[int] = mapped_column(Integer, nullable=False)
    protein_target: Mapped[int] = mapped_column(Integer, nullable=False)
    alcohol_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    smoking_limit: Mapped[int] = mapped_column(Integer, nullable=False)

    user = relationship("User", back_populates="goals")
