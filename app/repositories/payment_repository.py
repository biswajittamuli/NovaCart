from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    def create_payment(
        self,
        db: Session,
        payment: Payment,
    ):
        db.add(payment)
        db.flush()
        return payment

    def get_payment_by_order(
        self,
        db: Session,
        order_id: int,
    ):
        return (
            db.query(Payment)
            .filter(Payment.order_id == order_id)
            .first()
        )


payment_repository = PaymentRepository()