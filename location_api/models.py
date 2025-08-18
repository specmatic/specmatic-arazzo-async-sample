from pydantic import BaseModel, EmailStr, StrictInt
from pydantic.alias_generators import to_camel
from sqlmodel import Field, SQLModel


class LocationRequest(BaseModel):
    email: EmailStr
    password: str


class LocationResponse(BaseModel):
    client_token: str = Field(alias="clientToken")
    shipping_zone: str = Field(alias="shippingZone")
    country: str
    region: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class User(SQLModel, table=True):
    id: StrictInt | None = Field(primary_key=True, default=None)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    shipping_zone: str
    country: str
    region: str

    class Config: # pyright: ignore[reportIncompatibleVariableOverride]
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
