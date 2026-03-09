from sqlalchemy.orm import Session

from app.models.strategy import Strategy
from app.schemas.strategy import StrategyCreate


def create_strategy(db: Session, strategy: StrategyCreate):
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
    return db.query(Strategy).all()
