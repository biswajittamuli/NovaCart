import uuid
from app.core.enums import SortOrder
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product_repository import product_repository
from app.repositories.category_repository import category_repository
from app.models.product import Product


class ProductService:

    def create_product(self, db: Session, product_create: ProductCreate):
        # Check if category exists
        category = category_repository.get_category_by_id(
            db, product_create.category_id
        )
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Generate unique SKU
        sku = f"NOVA-{uuid.uuid4().hex[:6].upper()}"

        product = Product(
            name=product_create.name,
            description=product_create.description,
            price=product_create.price,
            brand=product_create.brand,
            category_id=product_create.category_id,
            sku=sku,
        )
        
        try:
            product = product_repository.create_product(
                db,
                product,
            )

            db.commit()
            db.refresh(product)

            return product

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Internal server error",
            )

    def get_all_products(self, db: Session, page: int, page_size: int, brand: str | None, category_id: int | None, sort_by: str | None, order: SortOrder, search: str | None):
        allowed_sort_fields = {
            "name",
            "price",
            "brand",
        }
        if sort_by and sort_by not in allowed_sort_fields:
            raise HTTPException(
                status_code=400,
                detail="Invalid sort field",
            )
        offset: int = (page - 1) * page_size
        limit: int = page_size
        return product_repository.get_all_products(db, offset, limit, brand, category_id, sort_by, order, search)

    def get_product_by_id(self, db: Session, product_id: int):
        product = product_repository.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        return product

    def update_product(
        self,
        db: Session,
        product_id: int,
        product_update: ProductUpdate,
    ) -> Product:
        # Check if product exists
        product = product_repository.get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        # Get only the fields that were actually sent by the client
        update_data = product_update.model_dump(exclude_unset=True)

        # If category_id is being updated, validate it
        if "category_id" in update_data:
            category = category_repository.get_category_by_id(
                db, update_data["category_id"]
            )
            if not category:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found",
                )

        # Update only the provided fields
        for key, value in update_data.items():
            setattr(product, key, value)

        # Save changes
        try:
            updated_product = product_repository.update_product(
                db,
                product,
            )

            db.commit()
            db.refresh(updated_product)

            return updated_product

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Internal server error",
            )

    def soft_delete_product(self, db: Session, product_id: int):
        product = product_repository.get_product_by_id(db, product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        if product.is_active is False:
            raise HTTPException(
                status_code=409,
                detail="Product is already deleted",
            )

        try:
            product = product_repository.soft_delete_product(
                db,
                product,
            )

            db.commit()
            db.refresh(product)

            return product

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Internal server error",
            )


# Singleton instance
product_service = ProductService()