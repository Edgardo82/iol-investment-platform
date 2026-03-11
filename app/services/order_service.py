from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.order import Order
from app.models.signal import Signal
from app.schemas.enums import OrderType
from app.schemas.order import OrderCreate


def create_order(db: Session, order_data: OrderCreate) -> Order:
    asset = db.query(Asset).filter(Asset.id == order_data.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if order_data.signal_id is not None:
        signal = db.query(Signal).filter(Signal.id == order_data.signal_id).first()
        if not signal:
            raise HTTPException(status_code=404, detail="Signal not found")

    if order_data.quantity <= 0:
        raise HTTPException(
            status_code=400, detail="Quantity must be greater than zero"
        )

    if order_data.order_type == OrderType.LIMIT and order_data.requested_price is None:
        raise HTTPException(
            status_code=400,
            detail="requested_price is required for LIMIT orders",
        )

    if (
        order_data.order_type == OrderType.MARKET
        and order_data.requested_price is not None
    ):
        raise HTTPException(
            status_code=400,
            detail="requested_price must be empty for MARKET orders",
        )

    order = Order(
        signal_id=order_data.signal_id,
        asset_id=order_data.asset_id,
        side=order_data.side.value,
        quantity=order_data.quantity,
        order_type=order_data.order_type.value,
        status=order_data.status.value,
        requested_price=order_data.requested_price,
        executed_price=order_data.executed_price,
        broker_order_id=order_data.broker_order_id,
        notes=order_data.notes,
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session) -> list[Order]:
    return db.query(Order).order_by(Order.id).all()


def get_order_by_id(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
