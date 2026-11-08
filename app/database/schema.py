
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    ForeignKey,
    ForeignKeyConstraint,
    UniqueConstraint,
    Enum as SAEnum,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


# ==========================================
# USER TABLE
# ==========================================

class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)

    # Never store plain-text passwords.
    password_hash = Column(String(255), nullable=False)

    is_active = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    categories = relationship("CategoryTable", back_populates="user")
    suppliers = relationship("SupplierTable", back_populates="user")
    products = relationship("ProductTable", back_populates="user")
    transactions = relationship("TransactionTable", back_populates="user")


# ==========================================
# CATEGORY TABLE
# ==========================================

class CategoryTable(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "name",
            name="uq_category_user_name",
        ),
        UniqueConstraint(
            "id",
            "user_id",
            name="uq_category_id_user",
        ),
    )

    user = relationship("UserTable", back_populates="categories")

    products = relationship(
        "ProductTable",
        back_populates="category",
        primaryjoin="and_(CategoryTable.id == ProductTable.category_id, "
                    "CategoryTable.user_id == ProductTable.user_id)",
        foreign_keys="ProductTable.category_id",
    )


# ==========================================
# SUPPLIER TABLE
# ==========================================

class SupplierTable(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(150), nullable=False)
    contact_name = Column(String(150), nullable=True)
    email = Column(String(150), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        UniqueConstraint(
            "id",
            "user_id",
            name="uq_supplier_id_user",
        ),
    )

    user = relationship("UserTable", back_populates="suppliers")

    products = relationship(
        "ProductTable",
        back_populates="supplier",
        primaryjoin="and_(SupplierTable.id == ProductTable.supplier_id, "
                    "SupplierTable.user_id == ProductTable.user_id)",
        foreign_keys="ProductTable.supplier_id",
    )


# ==========================================
# PRODUCT TABLE
# ==========================================

class ProductTable(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(200), nullable=False)
    sku = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, nullable=False, default=10)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    category_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "sku",
            name="uq_product_user_sku",
        ),
        UniqueConstraint(
            "id",
            "user_id",
            name="uq_product_id_user",
        ),
        ForeignKeyConstraint(
            ["category_id", "user_id"],
            ["categories.id", "categories.user_id"],
            ondelete="RESTRICT",
            name="fk_product_category_owner",
        ),
        ForeignKeyConstraint(
            ["supplier_id", "user_id"],
            ["suppliers.id", "suppliers.user_id"],
            ondelete="RESTRICT",
            name="fk_product_supplier_owner",
        ),
    )

    user = relationship("UserTable", back_populates="products")

    category = relationship(
        "CategoryTable",
        back_populates="products",
        primaryjoin="and_(ProductTable.category_id == CategoryTable.id, "
                    "ProductTable.user_id == CategoryTable.user_id)",
        foreign_keys=[category_id],
    )

    supplier = relationship(
        "SupplierTable",
        back_populates="products",
        primaryjoin="and_(ProductTable.supplier_id == SupplierTable.id, "
                    "ProductTable.user_id == SupplierTable.user_id)",
        foreign_keys=[supplier_id],
    )

    transactions = relationship(
        "TransactionTable",
        back_populates="product",
        primaryjoin="and_(ProductTable.id == TransactionTable.product_id, "
                    "ProductTable.user_id == TransactionTable.user_id)",
        foreign_keys="TransactionTable.product_id",
        passive_deletes=True,
    )


# ==========================================
# TRANSACTION TABLE
# ==========================================

class TransactionTable(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    transaction_type = Column(
        SAEnum("STOCK_IN", "STOCK_OUT", name="transaction_type"),
        nullable=False,
    )

    quantity = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)

    transaction_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    product_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["product_id", "user_id"],
            ["products.id", "products.user_id"],
            ondelete="CASCADE",
            name="fk_transaction_product_owner",
        ),
    )

    user = relationship("UserTable", back_populates="transactions")

    product = relationship(
        "ProductTable",
        back_populates="transactions",
        primaryjoin="and_(TransactionTable.product_id == ProductTable.id, "
                    "TransactionTable.user_id == ProductTable.user_id)",
        foreign_keys=[product_id],
    )
