from pydantic import StrictInt, StrictStr
from pydantic.alias_generators import to_camel
from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: StrictStr = Field(min_length=1)
    price: StrictInt = Field(gt=0)
    quantity: StrictInt = Field(gt=0)

    class Config:  # pyright: ignore[reportIncompatibleVariableOverride]
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class ProductPublic(ProductBase):
    product_id: StrictInt = Field(alias="productId")


class Product(ProductBase, table=True):
    product_id: StrictInt | None = Field(default=None, primary_key=True, alias="productId")
    shipping_zone: StrictStr


class OrderBase(SQLModel):
    product_id: StrictInt = Field(gt=0, alias="productId")
    quantity: StrictInt = Field(gt=0)

    class Config:  # pyright: ignore[reportIncompatibleVariableOverride]
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class OrderPublic(SQLModel):
    order_id: StrictInt = Field(alias="orderId")

    class Config:  # pyright: ignore[reportIncompatibleVariableOverride]
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class Order(OrderBase, table=True):
    order_id: StrictInt | None = Field(default=None, primary_key=True, alias="orderId")
