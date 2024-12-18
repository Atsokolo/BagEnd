from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from project.infrastructure.postgres.database import Base

from sqlalchemy import String, Integer, ForeignKey, Numeric, Text, Date, CheckConstraint, UniqueConstraint

class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column( nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)

class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column( nullable=False, unique=True)

class CoverType(Base):
    __tablename__ = "cover_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column( nullable=False, unique=True)

class Publisher(Base):
    __tablename__ = "publisher"

    id: Mapped[int] = mapped_column(primary_key=True)
    names: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column( nullable=True)

class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column( nullable=False)
    autor_id: Mapped[int] = mapped_column(ForeignKey("author.id", ondelete="SET NULL"), nullable=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id", ondelete="SET NULL"), nullable=True)
    cover_type: Mapped[int] = mapped_column(ForeignKey("cover_type.id"), nullable=True)
    language: Mapped[str] = mapped_column( nullable=True)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"), nullable=True)

class Discount(Base):
    __tablename__ = "discount"

    id: Mapped[int] = mapped_column(primary_key=True)
    percent: Mapped[float] = mapped_column(Numeric, CheckConstraint("percent >= 0"), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)

class DiscountList(Base):
    __tablename__ = "discount_list"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="SET NULL"), nullable=True)
    discount_id: Mapped[int] = mapped_column(ForeignKey("discount.id", ondelete="CASCADE"), nullable=False)

class Customers(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    address: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True)

class CustomerOrder(Base):
    __tablename__ = "customer_order"

    id: Mapped[int] = mapped_column(primary_key=True)
    discount_id: Mapped[int] = mapped_column(ForeignKey("discount_list.id", ondelete="CASCADE"), nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    order_date: Mapped[date] = mapped_column(Date, nullable=True)
    total: Mapped[float] = mapped_column(Numeric, nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=True)

class OrderDetails(Base):
    __tablename__ = "order_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("customer_order.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    count: Mapped[int] = mapped_column(Integer, CheckConstraint("count > 0"), nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Numeric, nullable=True)

class Reviews(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[float] = mapped_column(Numeric, CheckConstraint("rating BETWEEN 0 AND 5"), nullable=True)
    reviews_text: Mapped[str] = mapped_column(Text, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=True)

class Supplier(Base):
    __tablename__ = "supplier"

    id: Mapped[int] = mapped_column(primary_key=True)
    names: Mapped[str] = mapped_column( nullable=True)
    address: Mapped[str] = mapped_column( nullable=True)
    phone_number: Mapped[str] = mapped_column( nullable=True)
    email: Mapped[str] = mapped_column( nullable=True)

class SupplierOrder(Base):
    __tablename__ = "supplier_order"

    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.id", ondelete="CASCADE"), nullable=False)
    order_date: Mapped[date] = mapped_column(Date, nullable=True)
    total: Mapped[float] = mapped_column(Numeric, nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=True)

class OrderSupplierDetails(Base):
    __tablename__ = "order_supplier_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_publ_id: Mapped[int] = mapped_column(ForeignKey("supplier_order.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    count: Mapped[int] = mapped_column(Integer, CheckConstraint("count > 0"), nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Numeric, nullable=True)