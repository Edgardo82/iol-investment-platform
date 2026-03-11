from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.signal import SignalCreate, SignalResponse
from app.services.signal_service import create_signal, get_signals

router = APIRouter(prefix="/signals", tags=["Signals"])


@router.post("/", response_model=SignalResponse)
def create(signal: SignalCreate, db: Session = Depends(get_db)):
    return create_signal(db, signal)


@router.get("/", response_model=list[SignalResponse])
def list_signals(db: Session = Depends(get_db)):
    return get_signals(db)
