from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.product_repository import product_repository
from app.schemas.inventory import StockUpdate


class InventoryService:

    def set_stock(
        self,
        db: Session,
        product_id: int,
        stock_data: StockUpdate,
    ):

        product = product_repository.get_product_by_id(
            db,
            product_id,
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        product.stock = stock_data.quantity

        db.commit()
        db.refresh(product)

        return {
            "product_id": product.id,
            "stock": product.stock,
        }

    def restock(
        self,
        db: Session,
        product_id: int,
        stock_data: StockUpdate,
    ):

        product = product_repository.get_product_by_id(
            db,
            product_id,
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        product.stock += stock_data.quantity

        db.commit()
        db.refresh(product)

        return {
            "product_id": product.id,
            "stock": product.stock,
        }

    def get_low_stock(
        self,
        db: Session,
    ):
        return product_repository.get_low_stock_products(db)

    def get_out_of_stock(
        self,
        db: Session,
    ):
        return product_repository.get_out_of_stock_products(db)


inventory_service = InventoryService()