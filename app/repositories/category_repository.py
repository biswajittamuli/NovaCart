from sqlalchemy.orm import Session
from app.models.category import Category

class CategoryRepository:
    def get_all_categories(self,db: Session):
        return db.query(Category).all()
    
    def create_category(self,db: Session,category: Category):
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    



category_repository = CategoryRepository()