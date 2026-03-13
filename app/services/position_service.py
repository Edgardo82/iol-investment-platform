from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.position import Position
from app.schemas.position import PositionCreate
from app.models.order import Order

from decimal import Decimal


def create_position(db: Session, position_data: PositionCreate) -> Position:
    asset = db.query(Asset).filter(Asset.id == position_data.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    existing_position = (
        db.query(Position).filter(Position.asset_id == position_data.asset_id).first()
    )
    if existing_position:
        raise HTTPException(
            status_code=400,
            detail="Position already exists for this asset",
        )

    if position_data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero",
        )

    if position_data.average_price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Average price must be greater than zero",
        )

    position = Position(
        asset_id=position_data.asset_id,
        quantity=position_data.quantity,
        average_price=position_data.average_price,
    )

    db.add(position)
    db.commit()
    db.refresh(position)
    return position


def list_positions(db: Session) -> list[Position]:
    return db.query(Position).order_by(Position.id).all()


def get_position_by_id(db: Session, position_id: int) -> Position:
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


def get_position_by_asset_id(db: Session, asset_id: int) -> Position:
    position = db.query(Position).filter(Position.asset_id == asset_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found for this asset")
    return position


def apply_executed_order_to_position(db: Session, order: Order) -> Position | None:
    if order.status != "EXECUTED":
        raise HTTPException(
            status_code=400,
            detail="Only EXECUTED orders can be applied to positions",
        )

    existing_position = (
        db.query(Position).filter(Position.asset_id == order.asset_id).first()
    )

    order_quantity = Decimal(order.quantity)
    executed_price = order.executed_price

    if executed_price is None:
        raise HTTPException(
            status_code=400,
            detail="EXECUTED order must have executed_price",
        )

    executed_price = Decimal(executed_price)

    if order.side == "BUY":
        if not existing_position:
            position = Position(
                asset_id=order.asset_id,
                quantity=order_quantity,
                average_price=executed_price,
            )
            db.add(position)
            db.flush()
            return position

        current_quantity = Decimal(existing_position.quantity)
        current_average_price = Decimal(existing_position.average_price)

        new_quantity = current_quantity + order_quantity
        new_average_price = (
            (current_quantity * current_average_price)
            + (order_quantity * executed_price)
        ) / new_quantity

        existing_position.quantity = new_quantity
        existing_position.average_price = new_average_price
        db.flush()
        return existing_position

    if order.side == "SELL":
        if not existing_position:
            raise HTTPException(
                status_code=400,
                detail="Cannot execute SELL order without an existing position",
            )

        current_quantity = Decimal(existing_position.quantity)

        if order_quantity > current_quantity:
            raise HTTPException(
                status_code=400,
                detail="Cannot sell more than the current position quantity",
            )

        new_quantity = current_quantity - order_quantity

        if new_quantity == 0:
            db.delete(existing_position)
            db.flush()
            return None

        existing_position.quantity = new_quantity
        db.flush()
        return existing_position

    raise HTTPException(status_code=400, detail=f"Unsupported order side: {order.side}")
