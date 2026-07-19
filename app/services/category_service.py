from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import category_repository
from app.schemas.category import CategoryCreate
from fastapi import HTTPException


class CategoryService:

    def get_all_categories(self, db: Session):
        return category_repository.get_all_categories(db)

    def create_category(
        self,
        db: Session,
        category_data: CategoryCreate,
    ):
        category = Category(name=category_data.name)

        try:
            category = category_repository.create_category(
                db,
                category,
            )

            db.commit()
            db.refresh(category)

            return category

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
category_service = CategoryService()