from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DailyLog(Base):
    __tablename__ = "daily_logs"
    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_user_log_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    gym: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    protein: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    alcohol: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    smoking: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sleep: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mood: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    user = relationship("User", back_populates="daily_logs")
