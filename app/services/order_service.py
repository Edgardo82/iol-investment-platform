from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.order import Order
from app.models.signal import Signal
from app.schemas.enums import OrderType, OrderStatus, OrderSide
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.services.position_service import apply_executed_order_to_position


def create_order(db: Session, order_data: OrderCreate) -> Order:
    asset = db.query(Asset).filter(Asset.id == order_data.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if order_data.signal_id is not None:
        signal = db.query(Signal).filter(Signal.id == order_data.signal_id).first()
        if not signal:
            raise HTTPException(status_code=404, detail="Signal not found")

        if signal.asset_id != order_data.asset_id:
            raise HTTPException(
                status_code=400,
                detail="Signal asset_id does not match order asset_id",
            )

        if signal.signal_type == "HOLD":
            raise HTTPException(
                status_code=400,
                detail="Cannot create an order from a HOLD signal",
            )

        if signal.signal_type != order_data.side.value:
            raise HTTPException(
                status_code=400,
                detail="Signal type does not match order side",
            )

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


def list_orders(
    db: Session,
    asset_id: int | None = None,
    status: OrderStatus | None = None,
    side: OrderSide | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Order]:
    query = db.query(Order)

    if asset_id is not None:
        query = query.filter(Order.asset_id == asset_id)

    if status is not None:
        query = query.filter(Order.status == status.value)

    if side is not None:
        query = query.filter(Order.side == side.value)

    return query.order_by(Order.id).offset(offset).limit(limit).all()


def get_order_by_id(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def update_order_status(
    db: Session, order_id: int, order_data: OrderStatusUpdate
) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    allowed_transitions = {
        "PENDING": {"SUBMITTED", "CANCELLED", "REJECTED"},
        "SUBMITTED": {"EXECUTED", "CANCELLED", "REJECTED"},
        "EXECUTED": set(),
        "CANCELLED": set(),
        "REJECTED": set(),
    }

    current_status = order.status
    new_status = order_data.status.value

    if new_status == current_status:
        raise HTTPException(
            status_code=400,
            detail=f"Order is already in status: {current_status}",
        )

    if new_status not in allowed_transitions.get(current_status, set()):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {current_status} to {new_status}",
        )

    if order_data.status == OrderStatus.EXECUTED and order_data.executed_price is None:
        raise HTTPException(
            status_code=400,
            detail="executed_price is required when status is EXECUTED",
        )

    if (
        order_data.status != OrderStatus.EXECUTED
        and order_data.executed_price is not None
    ):
        raise HTTPException(
            status_code=400,
            detail="executed_price must be empty unless status is EXECUTED",
        )

    try:
        order.status = new_status

        if order_data.executed_price is not None:
            order.executed_price = order_data.executed_price

        if order_data.broker_order_id is not None:
            order.broker_order_id = order_data.broker_order_id

        if order_data.notes is not None:
            order.notes = order_data.notes

        if new_status == OrderStatus.EXECUTED.value:
            apply_executed_order_to_position(db, order)

        db.commit()
        db.refresh(order)
        return order

    except Exception:
        db.rollback()
        raise
