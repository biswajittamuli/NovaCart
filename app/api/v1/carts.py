from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
)
from app.services.cart_service import cart_service

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post("/add", response_model=CartResponse)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cart_service.add_to_cart(
        db,
        current_user,
        item,
    )


@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cart_service.get_cart(
        db,
        current_user,
    )


@router.patch("/item/{item_id}")
def update_item(
    item_id: int,
    quantity: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cart_service.update_cart_item(
        db,
        item_id,
        quantity,
    )


@router.delete("/item/{item_id}")
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cart_service.remove_cart_item(
        db,
        item_id,
    )


@router.delete("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cart_service.clear_cart(
        db,
        current_user,
    )


@router.post("/checkout")
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return cart_service.checkout(
        db,
        current_user,
    )