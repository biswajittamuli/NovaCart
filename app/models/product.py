from decimal import Decimal
from sqlalchemy import String, Numeric, Text,ForeignKey
from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship

class Product(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100),nullable=False)
    description :Mapped[str] = mapped_column(Text,nullable=False)
    price:Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    brand:Mapped[str] = mapped_column(String(100),nullable=False)
    order_items: Mapped[list["OrderItem"]] = relationship(
    back_populates="product",)
    stock: Mapped[int] = mapped_column(
    default=0,
    nullable=False,)
    sku:Mapped[str] = mapped_column(String(30),unique=True,index=True,nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True,nullable=False)

    # ORM Relationship
    category: Mapped["Category"] = relationship(back_populates="products")
    
