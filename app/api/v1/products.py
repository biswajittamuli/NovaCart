from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.product_service import product_service
router = APIRouter(
    prefix= "/products",
    tags=["Products"],
)

@router.get("/")
def  get_products(db:Session= Depends(get_db)):
    return product_service.get_all_products(db)

