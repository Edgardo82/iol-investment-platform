from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.strategy import StrategyCreate, StrategyResponse
from app.services.strategy_service import create_strategy, get_strategies

router = APIRouter(prefix="/strategies", tags=["Strategies"])


@router.post("/", response_model=StrategyResponse)
def create(strategy: StrategyCreate, db: Session = Depends(get_db)):
    return create_strategy(db, strategy)


@router.get("/", response_model=list[StrategyResponse])
def list_strategies(db: Session = Depends(get_db)):
    return get_strategies(db)
