from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.signal import Signal
from app.models.strategy import Strategy
from app.schemas.signal import SignalCreate


def create_signal(db: Session, signal: SignalCreate):
    strategy = db.query(Strategy).filter(Strategy.id == signal.strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=404, detail=f"Strategy with id {signal.strategy_id} not found."
        )

    asset = db.query(Asset).filter(Asset.id == signal.asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=404, detail=f"Asset with id {signal.asset_id} not found."
        )

    db_signal = Signal(
        strategy_id=signal.strategy_id,
        asset_id=signal.asset_id,
        signal_type=signal.signal_type,
    )

    db.add(db_signal)
    db.commit()
    db.refresh(db_signal)

    return db_signal


def get_signals(db: Session):
    return db.query(Signal).order_by(Signal.id).all()
