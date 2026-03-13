from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.enums import OrderSide, OrderStatus
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import (
    create_order,
    list_orders,
    get_order_by_id,
    update_order_status,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)


@router.get("/", response_model=list[OrderResponse])
def list_orders_endpoint(
    asset_id: int | None = None,
    status: OrderStatus | None = None,
    side: OrderSide | None = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    return list_orders(
        db, asset_id=asset_id, status=status, side=side, limit=limit, offset=offset
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    return get_order_by_id(db, order_id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status_endpoint(
    order_id: int,
    order_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
):
    return update_order_status(db, order_id, order_data)
