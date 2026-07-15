from sqlalchemy import String
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100),
        unique=True,
        nullable=False,
        index=True,
)

    #orm relationship
    products: Mapped[list["Product"]] = relationship(
    back_populates="category"
)