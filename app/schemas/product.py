from pydantic import  BaseModel
from typing import Optional
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
    
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    brand: Optional[str] = None
    category_id: Optional[int] = None   


