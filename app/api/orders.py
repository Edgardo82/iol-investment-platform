from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import create_order, list_orders, get_order_by_id

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)


@router.get("/", response_model=list[OrderResponse])
def list_orders_endpoint(db: Session = Depends(get_db)):
    return list_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    return get_order_by_id(db, order_id)
