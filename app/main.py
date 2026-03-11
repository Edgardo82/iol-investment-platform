from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.dependencies import get_db
from app.api.assets import router as asset_router
from app.api.strategies import router as strategy_router
from app.api.signals import router as signal_router
from app.api.orders import router as order_router
from app.models.asset import Asset  # noqa: F401

# from app.db.session import Base, engine


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for investment automation and portfolio analysis.",
)
# se reemplaza por alembic
# Base.metadata.create_all(bind=engine)

app.include_router(asset_router)
app.include_router(strategy_router)
app.include_router(signal_router)
app.include_router(order_router)


@app.get("/")
def root():
    return {"message": "IOL Investment Platform API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
