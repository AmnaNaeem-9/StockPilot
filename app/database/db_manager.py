
import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from database.schema import Base


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DEFAULT_DB_URL = (
    f"sqlite:///{os.path.join(BASE_DIR, 'inventory.db')}"
)


class DatabaseManager:

    def __init__(self, db_url=None):

        self.db_url = db_url or os.getenv(
            "DB_URL",
            DEFAULT_DB_URL
        )

        connect_args = {}

        if self.db_url.startswith("sqlite"):
            connect_args = {
                "check_same_thread": False,
                "timeout": 30
            }

        self.engine = create_engine(
            self.db_url,
            connect_args=connect_args,
            pool_pre_ping=True
        )

        # Enable SQLite foreign-key enforcement
        if self.db_url.startswith("sqlite"):

            @event.listens_for(self.engine, "connect")
            def enable_foreign_keys(
                dbapi_connection,
                connection_record
            ):

                cursor = dbapi_connection.cursor()

                cursor.execute("PRAGMA foreign_keys=ON")

                cursor.close()

        # SQLAlchemy session factory
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=True,
            expire_on_commit=True
        )

    # ======================================
    # DATABASE INITIALIZATION
    # ======================================

    def init_db(self):
        """
        Create database tables that do not exist.

        Important:
        create_all() does not modify existing tables.
        Use a fresh database for the new authentication schema.
        """

        Base.metadata.create_all(self.engine)

    # ======================================
    # SESSION MANAGEMENT
    # ======================================

    def get_session(self):
        """Return a new database session."""

        return self.SessionLocal()

    # ======================================
    # ENGINE DISPOSAL
    # ======================================

    def close(self):
        """Dispose of the database engine."""

        self.engine.dispose()
