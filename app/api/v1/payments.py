from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.payment import PaymentResponse
from app.services.payment_service import payment_service

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post("/pay/{order_id}", response_model=PaymentResponse)
def pay_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return payment_service.pay_order(
        db,
        order_id,
    )


@router.get("/{order_id}", response_model=PaymentResponse)
def get_payment(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return payment_service.get_payment(
        db,
        order_id,
    )