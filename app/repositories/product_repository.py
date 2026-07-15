from sqlalchemy.orm  import Session
from app.models.product import Product

class ProductRepository:
    def get_all_products(self,db: Session):
        return db.query(Product).all()
    
product_repository = ProductRepository()