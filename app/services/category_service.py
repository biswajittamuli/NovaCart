from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import category_repository
from app.schemas.category import CategoryCreate


class CategoryService:

    def get_all_categories(self, db: Session):
        return category_repository.get_all_categories(db)

    def create_category(
        self,
        db: Session,
        category_data: CategoryCreate,
    ):
        category = Category(
            name=category_data.name
        )

        return category_repository.create_category(
            db,
            category
        )


category_service = CategoryService()