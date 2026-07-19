from sqlalchemy.orm import Session

from app.models.order import OrderItem


class OrderItemRepository:

    def create_order_item(
        self,
        db: Session,
        order_item: OrderItem,
    ):
        db.add(order_item)
        db.flush()
        return order_item


order_item_repository = OrderItemRepository()