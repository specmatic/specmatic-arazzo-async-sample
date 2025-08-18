from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import select

from order_api import SessionDep
from order_api.models import Product, ProductPublic

products = APIRouter()


@products.get("/products", response_model=list[ProductPublic])
async def get_products(session: SessionDep, shipping_zone: Annotated[str, Query(alias="shippingZone")]):
    query = select(Product).where(Product.shipping_zone == shipping_zone)
    return session.exec(query)
