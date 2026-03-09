from pydantic import BaseModel, ConfigDict


class StrategyCreate(BaseModel):
    name: str
    description: str
    is_active: bool = True


class StrategyResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool

    class Config:
        from_attributes = True
