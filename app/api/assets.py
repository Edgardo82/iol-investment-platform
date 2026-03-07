from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.asset import AssetCreate, AssetResponse
from app.services.asset_service import create_asset, get_assets

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.post("/", response_model=AssetResponse)
def create(asset: AssetCreate, db: Session = Depends(get_db)):
    return create_asset(db, asset)


@router.get("/", response_model=list[AssetResponse])
def list_assets(db: Session = Depends(get_db)):
    return get_assets(db)
