from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_admin
from app.db.database import get_db
from app.models.user import User
from app.schemas.inventory import StockUpdate
from app.services.inventory_service import inventory_service

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.patch("/{product_id}/set-stock")
def set_stock(
    product_id: int,
    stock_data: StockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return inventory_service.set_stock(
        db,
        product_id,
        stock_data,
    )


@router.patch("/{product_id}/restock")
def restock(
    product_id: int,
    stock_data: StockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return inventory_service.restock(
        db,
        product_id,
        stock_data,
    )


@router.get("/low-stock")
def low_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return inventory_service.get_low_stock(db)


@router.get("/out-of-stock")
def out_of_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return inventory_service.get_out_of_stock(db)