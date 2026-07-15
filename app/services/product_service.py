from sqlalchemy.orm import Session
from app.repositories.product_repository import product_repository

class ProductService():
    def get_all_products(self, db: Session):
        return product_repository.get_all_products(db)
    
product_service = ProductService()