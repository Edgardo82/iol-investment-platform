from pydantic import BaseModel


class AssetCreate(BaseModel):
    symbol: str
    name: str
    market: str


class AssetResponse(BaseModel):
    id: int
    symbol: str
    name: str
    market: str

    class Config:
        from_attributes = True
