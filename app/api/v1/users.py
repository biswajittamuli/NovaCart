from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.auth import create_access_token
from app.schemas.user import UserLogin, Token
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import user_service
from app.core.auth import get_current_user
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.create_user(
        db,
        user_create,
    )


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_all_users(
    db: Session = Depends(get_db),
):
    return user_service.get_all_users(db)

@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    return user_service.get_user_by_id(
        db,
        user_id,
    )


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
)
def soft_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return user_service.soft_delete_user(
        db,
        user_id,
    )
    
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_service.authenticate_user(
        db,
        form_data.username,   # email goes here
        form_data.password,
    )

    access_token = create_access_token(
        {
            "sub": str(user.id),
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
    
