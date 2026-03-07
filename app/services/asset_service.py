from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate


def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(symbol=asset.symbol, name=asset.name, market=asset.market)

    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)

    return db_asset


def get_assets(db: Session):
    return db.query(Asset).all()
