from decimal import Decimal
from pydantic import BaseModel


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = {
        "from_attributes": True,
    }


class CartResponse(BaseModel):
    id: int
    total: Decimal
    items: list[CartItemResponse]

    model_config = {
        "from_attributes": True,
    }