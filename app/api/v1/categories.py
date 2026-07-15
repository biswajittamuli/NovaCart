from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import category_service

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/",response_model=list[CategoryResponse])
def get_all_categories(
    db: Session = Depends(get_db),
):
    return category_service.get_all_categories(db)

@router.post("/", response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate,db : Session= Depends(get_db)):
    return category_service.create_category(db,category_data)
    