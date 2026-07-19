from sqlalchemy.orm import Session
from app.models.category import Category

class CategoryRepository:
    def get_all_categories(self,db: Session):
        return db.query(Category).all()
    
    def create_category(self,db: Session,category: Category):
        db.add(category)
        db.flush()
        return category
    
    def get_category_by_id(self,db: Session,category_id: int):
        return(
            db.query(Category).filter_by(id=category_id).first())
        
    



category_repository = CategoryRepository()