from sqlalchemy.orm import Session

from app.models.order import Order


class OrderRepository:

    def create_order(
        self,
        db: Session,
        order: Order,
    ) -> Order:
        db.add(order)
        db.flush()          # Gets order.id without committing
        return order

    def update_order(
        self,
        db: Session,
        order: Order,
    ) -> Order:
        db.add(order)
        db.flush()
        return order

    def get_order_by_id(
        self,
        db: Session,
        order_id: int,
    ) -> Order | None:
        return (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    def get_orders_by_user(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .all()
        )

    def get_all_orders(
        self,
        db: Session,
    ):
        return (
            db.query(Order)
            .all()
        )


order_repository = OrderRepository()