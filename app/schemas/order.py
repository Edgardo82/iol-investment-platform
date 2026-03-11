from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.enums import OrderSide, OrderStatus, OrderType


class OrderCreate(BaseModel):
    signal_id: int | None = None
    asset_id: int
    side: OrderSide
    quantity: Decimal
    order_type: OrderType
    status: OrderStatus = OrderStatus.PENDING
    requested_price: Decimal | None = None
    executed_price: Decimal | None = None
    broker_order_id: str | None = None
    notes: str | None = None


class OrderResponse(BaseModel):
    id: int
    signal_id: int | None
    asset_id: int
    side: OrderSide
    quantity: Decimal
    order_type: OrderType
    status: OrderStatus
    requested_price: Decimal | None
    executed_price: Decimal | None
    broker_order_id: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
