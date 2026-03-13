from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PositionCreate(BaseModel):
    asset_id: int
    quantity: Decimal
    average_price: Decimal


class PositionResponse(BaseModel):
    id: int
    asset_id: int
    quantity: Decimal
    average_price: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
