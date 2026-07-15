from pydantic import  BaseModel
from decimal import Decimal

class ProductCreate(BaseModel):
    name:str
    description:str
    price:Decimal
    brand:str
    category_id:int


class ProductResponse(ProductCreate):
    id: int
    sku: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }
    


