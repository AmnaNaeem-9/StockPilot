
from datetime import datetime

from database.db_manager import DatabaseManager
from database.schema import (
    ProductTable,
    CategoryTable,
    SupplierTable,
    TransactionTable,
)


class InventoryManager:
    """
    Business logic layer for StockPilot.

    Each instance belongs to exactly one authenticated user.

    All inventory queries are scoped to self.user_id.
    The UI must never access the database directly.
    """

    # Fields that users are allowed to update on a product.
    ALLOWED_PRODUCT_FIELDS = {
        "name",
        "sku",
        "description",
        "price",
        "quantity",
        "reorder_level",
        "category_id",
        "supplier_id",
    }

    def __init__(self, db_manager: DatabaseManager, user_id: int):

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("A valid authenticated user ID is required.")

        self.db = db_manager
        self.user_id = user_id

    # ==========================================
    # OWNERSHIP VALIDATION
    # ==========================================

    def _get_owned_product(self, session, product_id):
        """Return a product only if it belongs to this user."""

        product = (
            session.query(ProductTable)
            .filter(
                ProductTable.id == product_id,
                ProductTable.user_id == self.user_id,
            )
            .first()
        )

        if product is None:
            raise ValueError(
                f"Product with id={product_id} not found."
            )

        return product

    def _validate_category(self, session, category_id):
        """Ensure the category belongs to this user."""

        category = (
            session.query(CategoryTable)
            .filter(
                CategoryTable.id == category_id,
                CategoryTable.user_id == self.user_id,
            )
            .first()
        )

        if category is None:
            raise ValueError(
                "The selected category does not exist in your inventory."
            )

    def _validate_supplier(self, session, supplier_id):
        """Ensure the supplier belongs to this user."""

        if supplier_id is None:
            return

        supplier = (
            session.query(SupplierTable)
            .filter(
                SupplierTable.id == supplier_id,
                SupplierTable.user_id == self.user_id,
            )
            .first()
        )

        if supplier is None:
            raise ValueError(
                "The selected supplier does not exist in your inventory."
            )

    # ==========================================
    # CATEGORY OPERATIONS
    # ==========================================

    def add_category(self, name, description=None):

        name = name.strip() if name else ""

        if not name:
            raise ValueError("Category name is required.")

        session = self.db.get_session()

        try:
            category = CategoryTable(
                user_id=self.user_id,
                name=name,
                description=description,
            )

            session.add(category)
            session.commit()
            session.refresh(category)

            return category

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def get_all_categories(self):

        session = self.db.get_session()

        try:
            return (
                session.query(CategoryTable)
                .filter(CategoryTable.user_id == self.user_id)
                .order_by(CategoryTable.name)
                .all()
            )

        finally:
            session.close()

    # ==========================================
    # SUPPLIER OPERATIONS
    # ==========================================

    def add_supplier(
        self,
        name,
        contact_name=None,
        email=None,
        phone=None,
        address=None,
    ):

        name = name.strip() if name else ""

        if not name:
            raise ValueError("Supplier name is required.")

        session = self.db.get_session()

        try:
            supplier = SupplierTable(
                user_id=self.user_id,
                name=name,
                contact_name=contact_name,
                email=email,
                phone=phone,
                address=address,
            )

            session.add(supplier)
            session.commit()
            session.refresh(supplier)

            return supplier

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def get_all_suppliers(self):

        session = self.db.get_session()

        try:
            return (
                session.query(SupplierTable)
                .filter(SupplierTable.user_id == self.user_id)
                .order_by(SupplierTable.name)
                .all()
            )

        finally:
            session.close()

    # ==========================================
    # PRODUCT OPERATIONS
    # ==========================================

    def add_product(
        self,
        name,
        sku,
        price,
        quantity,
        reorder_level,
        category_id,
        supplier_id=None,
        description=None,
    ):

        name = name.strip() if name else ""
        sku = sku.strip() if sku else ""

        if not name:
            raise ValueError("Product name is required.")

        if not sku:
            raise ValueError("Product SKU is required.")

        if price < 0:
            raise ValueError("Price cannot be negative.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        if reorder_level < 0:
            raise ValueError("Reorder level cannot be negative.")

        session = self.db.get_session()

        try:
            self._validate_category(session, category_id)
            self._validate_supplier(session, supplier_id)

            product = ProductTable(
                user_id=self.user_id,
                name=name,
                sku=sku,
                price=price,
                quantity=quantity,
                reorder_level=reorder_level,
                category_id=category_id,
                supplier_id=supplier_id,
                description=description,
            )

            session.add(product)
            session.commit()
            session.refresh(product)

            return product

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def get_all_products(self):

        session = self.db.get_session()

        try:
            return (
                session.query(ProductTable)
                .filter(ProductTable.user_id == self.user_id)
                .order_by(ProductTable.name)
                .all()
            )

        finally:
            session.close()

    def get_product_by_id(self, product_id):

        session = self.db.get_session()

        try:
            return (
                session.query(ProductTable)
                .filter(
                    ProductTable.id == product_id,
                    ProductTable.user_id == self.user_id,
                )
                .first()
            )

        finally:
            session.close()

    def update_product(self, product_id, **kwargs):

        invalid_fields = set(kwargs) - self.ALLOWED_PRODUCT_FIELDS

        if invalid_fields:
            raise ValueError(
                f"Fields cannot be updated: {', '.join(sorted(invalid_fields))}"
            )

        session = self.db.get_session()

        try:
            product = self._get_owned_product(session, product_id)

            if "category_id" in kwargs:
                self._validate_category(session, kwargs["category_id"])

            if "supplier_id" in kwargs:
                self._validate_supplier(session, kwargs["supplier_id"])

            if "name" in kwargs:
                kwargs["name"] = kwargs["name"].strip()

                if not kwargs["name"]:
                    raise ValueError("Product name cannot be empty.")

            if "sku" in kwargs:
                kwargs["sku"] = kwargs["sku"].strip()

                if not kwargs["sku"]:
                    raise ValueError("Product SKU cannot be empty.")

            if "price" in kwargs and kwargs["price"] < 0:
                raise ValueError("Price cannot be negative.")

            if "quantity" in kwargs and kwargs["quantity"] < 0:
                raise ValueError("Quantity cannot be negative.")

            if "reorder_level" in kwargs and kwargs["reorder_level"] < 0:
                raise ValueError("Reorder level cannot be negative.")

            for key, value in kwargs.items():
                setattr(product, key, value)

            product.updated_at = datetime.utcnow()

            session.commit()
            session.refresh(product)

            return product

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def delete_product(self, product_id):

        session = self.db.get_session()

        try:
            product = self._get_owned_product(session, product_id)

            session.delete(product)
            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    # ==========================================
    # STOCK TRANSACTION OPERATIONS
    # ==========================================

    def stock_in(self, product_id, quantity, notes=None):

        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive whole number.")

        session = self.db.get_session()

        try:
            product = self._get_owned_product(session, product_id)

            product.quantity += quantity
            product.updated_at = datetime.utcnow()

            transaction = TransactionTable(
                user_id=self.user_id,
                product_id=product.id,
                transaction_type="STOCK_IN",
                quantity=quantity,
                notes=notes,
            )

            session.add(transaction)
            session.commit()
            session.refresh(transaction)

            return transaction

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def stock_out(self, product_id, quantity, notes=None):

        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive whole number.")

        session = self.db.get_session()

        try:
            product = self._get_owned_product(session, product_id)

            if product.quantity < quantity:
                raise ValueError(
                    f"Insufficient stock. Available: {product.quantity}, "
                    f"Requested: {quantity}"
                )

            product.quantity -= quantity
            product.updated_at = datetime.utcnow()

            transaction = TransactionTable(
                user_id=self.user_id,
                product_id=product.id,
                transaction_type="STOCK_OUT",
                quantity=quantity,
                notes=notes,
            )

            session.add(transaction)
            session.commit()
            session.refresh(transaction)

            return transaction

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def get_transaction_history(self, product_id=None):

        session = self.db.get_session()

        try:
            query = (
                session.query(TransactionTable)
                .filter(TransactionTable.user_id == self.user_id)
            )

            if product_id is not None:
                query = query.filter(
                    TransactionTable.product_id == product_id
                )

            return query.order_by(
                TransactionTable.transaction_date.desc()
            ).all()

        finally:
            session.close()

    # ==========================================
    # SMART QUERIES
    # ==========================================

    def get_low_stock_products(self):

        session = self.db.get_session()

        try:
            return (
                session.query(ProductTable)
                .filter(
                    ProductTable.user_id == self.user_id,
                    ProductTable.quantity <= ProductTable.reorder_level,
                )
                .order_by(ProductTable.quantity)
                .all()
            )

        finally:
            session.close()

    def get_dashboard_stats(self):

        session = self.db.get_session()

        try:
            products = (
                session.query(ProductTable)
                .filter(ProductTable.user_id == self.user_id)
                .all()
            )

            low_stock_count = (
                session.query(ProductTable)
                .filter(
                    ProductTable.user_id == self.user_id,
                    ProductTable.quantity <= ProductTable.reorder_level,
                )
                .count()
            )

            return {
                "total_products": len(products),

                "total_categories": (
                    session.query(CategoryTable)
                    .filter(CategoryTable.user_id == self.user_id)
                    .count()
                ),

                "total_suppliers": (
                    session.query(SupplierTable)
                    .filter(SupplierTable.user_id == self.user_id)
                    .count()
                ),

                "low_stock_count": low_stock_count,

                "inventory_value": sum(
                    product.price * product.quantity
                    for product in products
                ),
            }

        finally:
            session.close()
