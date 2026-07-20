from pydantic import BaseModel, Field


class StockUpdate(BaseModel):
    quantity: int = Field(gt=0)


class StockResponse(BaseModel):
    product_id: int
    stock: int