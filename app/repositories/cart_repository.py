from sqlalchemy.orm import Session

from app.models.cart import Cart, CartItem


class CartRepository:

    def get_cart_by_user(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Cart)
            .filter(Cart.user_id == user_id)
            .first()
        )

    def create_cart(
        self,
        db: Session,
        cart: Cart,
    ):
        db.add(cart)
        db.flush()
        return cart

    def add_item(
        self,
        db: Session,
        item: CartItem,
    ):
        db.add(item)
        db.flush()
        return item

    def get_cart_item(
        self,
        db: Session,
        cart_id: int,
        product_id: int,
    ):
        return (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
            )
            .first()
        )

    def get_item_by_id(
        self,
        db: Session,
        item_id: int,
    ):
        return (
            db.query(CartItem)
            .filter(CartItem.id == item_id)
            .first()
        )

    def delete_item(
        self,
        db: Session,
        item: CartItem,
    ):
        db.delete(item)
        db.flush()
        
    def clear_cart(
    self,
    db: Session,
    cart: Cart,
    ):
        for item in cart.items:
            db.delete(item)

        db.flush()


cart_repository = CartRepository()