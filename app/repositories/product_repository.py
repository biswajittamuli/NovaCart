from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, or_

from app.models.product import Product
from app.core.enums import SortOrder


class ProductRepository:

    def create_product(self, db: Session, product: Product):
        db.add(product)
        db.flush()
        return product

    def get_product_by_id(self, db: Session, product_id: int):
        return (
            db.query(Product)
            .filter_by(id=product_id, is_active=True)
            .first()
        )

    def get_all_products(
        self,
        db: Session,
        offset: int,
        limit: int,
        brand: str | None = None,
        category_id: int | None = None,
        sort_by: str | None = None,
        order: SortOrder = SortOrder.asc,
        search: str | None = None,
    ):
        query = db.query(Product).filter_by(is_active=True)

        # Filter by brand
        if brand:
            query = query.filter(Product.brand == brand)

        # Filter by category
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)

        # Search in name or brand
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.brand.ilike(f"%{search}%"),
                )
            )

        # Allowed sortable columns
        sort_columns = {
            "name": Product.name,
            "price": Product.price,
            "brand": Product.brand,
        }

        # Sorting
        if sort_by and sort_by in sort_columns:
            column = sort_columns[sort_by]
            if order == SortOrder.asc:
                query = query.order_by(asc(column))
            else:
                query = query.order_by(desc(column))

        return query.offset(offset).limit(limit).all()

    def update_product(self, db: Session, product: Product):
        db.add(product)
        db.flush()
        return product

    def soft_delete_product(self, db: Session, product: Product):
        """Soft delete by setting is_active = False"""
        # You can use direct assignment or setattr
        product.is_active = False
        # setattr(product, "is_active", False)  # Alternative using setattr

        db.flush()
        return product


# Repository instance
product_repository = ProductRepository()