from fastapi import FastAPI

from app.api.routes import goals, log, report, user
from app.core.database import Base, engine
from app.models import DailyLog, Goals, User  # noqa: F401


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Elio API", version="1.0.0")

app.include_router(user.router, tags=["user"])
app.include_router(goals.router, tags=["goals"])
app.include_router(log.router, tags=["log"])
app.include_router(report.router, tags=["report"])


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
