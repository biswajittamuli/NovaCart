from fastapi import APIRouter, Depends, status,Query
from sqlalchemy.orm import Session
from fastapi import Query
from app.core.enums import SortOrder
from app.db.database import get_db
from app.services.product_service import product_service
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_create: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product_create)


@router.get("/", response_model=list[ProductResponse])
def get_products(
    brand: str | None = Query(None),
    category_id: int | None = Query(None),
    sort_by: str | None = Query(None),
    order: SortOrder = Query(SortOrder.asc),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    db: Session = Depends(get_db)
    ):
    return product_service.get_all_products(db,page,page_size,brand,category_id,sort_by,order,search)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
):
    return product_service.get_product_by_id(
        db,
        product_id,
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
):
    return product_service.update_product(
        db,
        product_id,
        product_update,
    )

@router.delete("/{product_id}",response_model=ProductResponse)
def soft_delete_product(
    product_id : int,
    db : Session= Depends(get_db)
):
    return product_service.soft_delete_product(
        db,
        product_id,
    )
    
    