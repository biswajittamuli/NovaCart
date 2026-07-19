from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.security import verify_password


class UserService:

    def create_user(
        self,
        db: Session,
        user_create: UserCreate,
    ):
        # Check if email already exists
        existing_user = user_repository.get_user_by_email(
            db,
            user_create.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            )

        user = User(
            full_name=user_create.full_name,
            email=user_create.email,
            password_hash=hash_password(user_create.password),
        )

        try:
            user = user_repository.create_user(
                db,
                user,
            )

            db.commit()
            db.refresh(user)

            return user

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Internal server error",
            )

    def get_user_by_id(
        self,
        db: Session,
        user_id: int,
    ):
        user = user_repository.get_user_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        return user

    def get_all_users(
        self,
        db: Session,
    ):
        return user_repository.get_all_users(db)

    def soft_delete_user(
        self,
        db: Session,
        user_id: int,
    ):
        user = user_repository.get_user_by_id(
            db,
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=409,
                detail="User already inactive",
            )

        try:
            user = user_repository.soft_delete_user(
                db,
                user,
            )

            db.commit()
            db.refresh(user)

            return user

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Internal server error",
            )

    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str,
    ):
        print("Email received:", repr(email))

        user = user_repository.get_user_by_email(db, email)

        print("User found:", user)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        print("Stored hash:", user.password_hash)

        is_valid = verify_password(password, user.password_hash)
        print("Password valid:", is_valid)

        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        return user


# Singleton instance
user_service = UserService()