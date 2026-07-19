from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def create_user(
        self,
        db: Session,
        user: User,
    ) -> User:
        db.add(user)
        db.flush()
        return user

    def get_user_by_id(
        self,
        db: Session,
        user_id: int,
    ) -> User | None:
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_user_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_all_users(
        self,
        db: Session,
    ):
        return (
            db.query(User)
            .filter(User.is_active == True)
            .all()
        )

    def update_user(
        self,
        db: Session,
        user: User,
    ) -> User:
        db.add(user)
        db.flush()
        return user

    def soft_delete_user(
        self,
        db: Session,
        user: User,
    ) -> User:
        user.is_active = False
        db.flush()
        return user


user_repository = UserRepository()