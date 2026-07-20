from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import OrderStatus
from app.models.payment import Payment, PaymentStatus
from app.repositories.order_repository import order_repository
from app.repositories.payment_repository import payment_repository


class PaymentService:

    def pay_order(
        self,
        db: Session,
        order_id: int,
    ):

        order = order_repository.get_order_by_id(
            db,
            order_id,
        )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found",
            )

        if order.status != OrderStatus.PENDING:
            raise HTTPException(
                status_code=400,
                detail="Order cannot be paid",
            )

        existing = payment_repository.get_payment_by_order(
            db,
            order_id,
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Payment already exists",
            )

        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            status=PaymentStatus.SUCCESS,
        )

        payment_repository.create_payment(
            db,
            payment,
        )

        order.status = OrderStatus.PAID

        db.commit()
        db.refresh(payment)

        return payment

    def get_payment(
        self,
        db: Session,
        order_id: int,
    ):

        payment = payment_repository.get_payment_by_order(
            db,
            order_id,
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found",
            )

        return payment


payment_service = PaymentService()