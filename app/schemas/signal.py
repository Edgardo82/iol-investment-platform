from datetime import datetime

from pydantic import BaseModel

from app.schemas.enums import SignalType


class SignalCreate(BaseModel):
    strategy_id: int
    asset_id: int
    signal_type: SignalType


class SignalResponse(BaseModel):
    id: int
    strategy_id: int
    asset_id: int
    signal_type: SignalType
    created_at: datetime

    class Config:
        from_attributes = True
