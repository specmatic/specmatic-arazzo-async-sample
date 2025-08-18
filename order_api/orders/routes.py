from fastapi import APIRouter, HTTPException
from sqlmodel import select

from order_api import SessionDep
from order_api.models import Order, OrderPublic

orders = APIRouter()


@orders.get("/orders/{order_id}", response_model=OrderPublic)
async def get_orders(order_id: int, session: SessionDep):
    order = session.exec(select(Order).where(Order.order_id == order_id)).one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return order
