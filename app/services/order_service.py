from decimal import Decimal
import traceback
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem, OrderStatus
from app.models.user import User, UserRole
from app.repositories.order_repository import order_repository
from app.repositories.order_item_repository import order_item_repository
from app.repositories.product_repository import product_repository
from app.schemas.order import OrderCreate


class OrderService:

    def create_order(
        self,
        db: Session,
        current_user: User,
        order_create: OrderCreate,
    ):

        total_amount = Decimal("0.00")

        try:

            order = Order(
                user_id=current_user.id,
                total_amount=Decimal("0.00"),
                status=OrderStatus.PENDING,
            )

            order_repository.create_order(
                db,
                order,
            )

            for item in order_create.items:

                product = product_repository.get_product_by_id(
                    db,
                    item.product_id,
                )

                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product {item.product_id} not found",
                    )

                if product.stock < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Insufficient stock for {product.name}",
                    )

                subtotal = product.price * item.quantity

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=product.price,
                    subtotal=subtotal,
                )

                order_item_repository.create_order_item(
                    db,
                    order_item,
                )

                product.stock -= item.quantity

                total_amount += subtotal

            order.total_amount = total_amount

            order_repository.update_order(
                db,
                order,
            )

            db.commit()
            db.refresh(order)

            return order

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            traceback.print_exc()
            raise

    def get_my_orders(
        self,
        db: Session,
        current_user: User,
    ):
        return order_repository.get_orders_by_user(
            db,
            current_user.id,
        )

    def get_order_by_id(
        self,
        db: Session,
        order_id: int,
        current_user: User,
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

        if (
            order.user_id != current_user.id
            and current_user.role != UserRole.ADMIN
        ):
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        return order

    def get_all_orders(
        self,
        db: Session,
    ):
        return order_repository.get_all_orders(db)

    def cancel_order(
        self,
        db: Session,
        order_id: int,
        current_user: User,
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

        if (
            order.user_id != current_user.id
            and current_user.role != UserRole.ADMIN
        ):
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        if order.status == OrderStatus.CANCELLED:
            raise HTTPException(
                status_code=400,
                detail="Already cancelled",
            )

        try:
            for item in order.items:

                product = product_repository.get_product_by_id(
                    db,
                    item.product_id,
                )

                if product:
                    product.stock += item.quantity

            order.status = OrderStatus.CANCELLED

            db.commit()
            db.refresh(order)

            return order

        except Exception:
            db.rollback()
            traceback.print_exc()
            raise


order_service = OrderService()