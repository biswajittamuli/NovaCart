from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cart import Cart, CartItem
from app.models.user import User
from app.repositories.cart_repository import cart_repository
from app.repositories.product_repository import product_repository
from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.schemas.order import OrderCreate, OrderItemCreate
from app.services.order_service import order_service


class CartService:

    def add_to_cart(
        self,
        db: Session,
        current_user: User,
        item: CartItemCreate,
    ):

        cart = cart_repository.get_cart_by_user(
            db,
            current_user.id,
        )

        if not cart:
            cart = Cart(user_id=current_user.id)
            cart = cart_repository.create_cart(
                db,
                cart,
            )

        product = product_repository.get_product_by_id(
            db,
            item.product_id,
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        cart_item = cart_repository.get_cart_item(
            db,
            cart.id,
            product.id,
        )

        if cart_item:
            cart_item.quantity += item.quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=item.quantity,
            )
            cart_repository.add_item(
                db,
                cart_item,
            )

        db.commit()
        db.refresh(cart)

        return self.get_cart(
            db,
            current_user,
        )

    def get_cart(
        self,
        db: Session,
        current_user: User,
    ):

        cart = cart_repository.get_cart_by_user(
            db,
            current_user.id,
        )

        if not cart:
            return {
                "id": 0,
                "total": Decimal("0.00"),
                "items": [],
            }

        total = Decimal("0.00")

        for item in cart.items:
            total += item.product.price * item.quantity

        return {
            "id": cart.id,
            "total": total,
            "items": cart.items,
        }

    def update_cart_item(
        self,
        db: Session,
        item_id: int,
        quantity: CartItemUpdate,
    ):

        item = cart_repository.get_item_by_id(
            db,
            item_id,
        )

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found",
            )

        item.quantity = quantity.quantity

        db.commit()

        return item

    def remove_cart_item(
        self,
        db: Session,
        item_id: int,
    ):

        item = cart_repository.get_item_by_id(
            db,
            item_id,
        )

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found",
            )

        cart_repository.delete_item(
            db,
            item,
        )

        db.commit()

        return {
            "message": "Item removed",
        }

    def clear_cart(
        self,
        db: Session,
        current_user: User,
    ):

        cart = cart_repository.get_cart_by_user(
            db,
            current_user.id,
        )

        if not cart:
            return {
                "message": "Cart already empty",
            }

        cart_repository.clear_cart(
            db,
            cart,
        )

        db.commit()

        return {
            "message": "Cart cleared",
        }

    def checkout(
        self,
        db: Session,
        current_user: User,
    ):

        cart = cart_repository.get_cart_by_user(
            db,
            current_user.id,
        )

        if not cart or not cart.items:
            raise HTTPException(
                status_code=400,
                detail="Cart is empty",
            )

        order_items = []

        for item in cart.items:

            order_items.append(
                OrderItemCreate(
                    product_id=item.product_id,
                    quantity=item.quantity,
                )
            )

        order = order_service.create_order(
            db,
            current_user,
            OrderCreate(
                items=order_items,
            ),
        )

        cart_repository.clear_cart(
            db,
            cart,
        )

        db.commit()

        return order


cart_service = CartService()