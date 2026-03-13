from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.position import PositionCreate, PositionResponse
from app.services.position_service import (
    create_position,
    get_position_by_id,
    list_positions,
    get_position_by_asset_id,
)

router = APIRouter(prefix="/positions", tags=["positions"])


@router.post("/", response_model=PositionResponse, status_code=201)
def create_position_endpoint(
    position: PositionCreate,
    db: Session = Depends(get_db),
):
    return create_position(db, position)


@router.get("/", response_model=list[PositionResponse])
def list_positions_endpoint(db: Session = Depends(get_db)):
    return list_positions(db)


@router.get("/by-asset/{asset_id}", response_model=PositionResponse)
def get_position_by_asset_id_endpoint(asset_id: int, db: Session = Depends(get_db)):
    return get_position_by_asset_id(db, asset_id)


@router.get("/{position_id}", response_model=PositionResponse)
def get_position_endpoint(position_id: int, db: Session = Depends(get_db)):
    return get_position_by_id(db, position_id)
