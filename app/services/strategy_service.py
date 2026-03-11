from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.strategy import Strategy
from app.schemas.strategy import StrategyCreate


def create_strategy(db: Session, strategy: StrategyCreate):
    existing_strategy = (
        db.query(Strategy).filter(Strategy.name == strategy.name).first()
    )

    if existing_strategy:
        raise HTTPException(
            status_code=400,
            detail=f"Strategy with name '{strategy.name}' already exists.",
        )

    db_strategy = Strategy(
        name=strategy.name,
        description=strategy.description,
        is_active=strategy.is_active,
    )

    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)

    return db_strategy


def get_strategies(db: Session):
    return db.query(Strategy).order_by(Strategy.id).all()
