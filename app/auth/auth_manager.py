
import re

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from database.schema import UserTable
from app.auth.password_manager import PasswordManager


class AuthManager:
    """
    Handles user registration, authentication,
    and account retrieval.

    All database operations are performed through
    the DatabaseManager session factory.
    """

    def __init__(self, db_manager):
        self.db = db_manager

    # ==========================================
    # VALIDATION
    # ==========================================

    @staticmethod
    def _validate_name(name):
        if not isinstance(name, str):
            raise ValueError("Name must be text.")

        name = name.strip()

        if not name:
            raise ValueError("Name is required.")

        if len(name) > 150:
            raise ValueError("Name cannot exceed 150 characters.")

        return name

    @staticmethod
    def _validate_email(email):
        if not isinstance(email, str):
            raise ValueError("Email must be text.")

        email = email.strip().lower()

        if not email:
            raise ValueError("Email is required.")

        if len(email) > 255:
            raise ValueError("Email cannot exceed 255 characters.")

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(email_pattern, email):
            raise ValueError("Please enter a valid email address.")

        return email

    @staticmethod
    def _serialize_user(user):
        """
        Return safe user information.

        Never expose the password hash to the UI.
        """

        if user is None:
            return None

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_active": bool(user.is_active),
            "created_at": user.created_at,
        }

    # ==========================================
    # REGISTER
    # ==========================================

    def register_user(self, name, email, password):
        """
        Register a new user.

        Returns:
            dict: Safe user information.

        Raises:
            ValueError: If validation fails or email exists.
        """

        name = self._validate_name(name)
        email = self._validate_email(email)

        # Hash password before storing it.
        password_hash = PasswordManager.hash_password(password)

        session = self.db.get_session()

        try:
            # Check whether the email is already registered.
            existing_user = (
                session.query(UserTable)
                .filter(func.lower(UserTable.email) == email)
                .first()
            )

            if existing_user:
                raise ValueError(
                    "An account with this email already exists."
                )

            new_user = UserTable(
                name=name,
                email=email,
                password_hash=password_hash,
                is_active=1,
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            # Build the response while the session is open.
            user_data = self._serialize_user(new_user)

            return user_data

        except IntegrityError:
            session.rollback()

            raise ValueError(
                "An account with this email already exists."
            )

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    # ==========================================
    # LOGIN
    # ==========================================

    def login_user(self, email, password):
        """
        Authenticate an existing user.

        Returns:
            dict: Safe user information on success.
            None: If credentials are invalid or account inactive.
        """

        if not isinstance(email, str) or not isinstance(password, str):
            return None

        email = email.strip().lower()

        if not email or not password:
            return None

        session = self.db.get_session()

        try:
            user = (
                session.query(UserTable)
                .filter(func.lower(UserTable.email) == email)
                .first()
            )

            # Use a generic failure response.
            if user is None:
                return None

            if not user.is_active:
                return None

            if not PasswordManager.verify_password(
                password,
                user.password_hash,
            ):
                return None

            # Upgrade the stored hash if Argon2 settings change.
            if PasswordManager.needs_rehash(user.password_hash):
                user.password_hash = PasswordManager.hash_password(password)
                session.commit()
                session.refresh(user)

            return self._serialize_user(user)

        finally:
            session.close()

    # ==========================================
    # GET USER BY ID
    # ==========================================

    def get_user_by_id(self, user_id):
        """
        Retrieve an active user using their database ID.

        Returns:
            dict: Safe user information.
            None: If the user does not exist or is inactive.
        """

        if isinstance(user_id, bool) or not isinstance(user_id, int):
            return None

        if user_id <= 0:
            return None

        session = self.db.get_session()

        try:
            user = (
                session.query(UserTable)
                .filter(
                    UserTable.id == user_id,
                    UserTable.is_active == 1,
                )
                .first()
            )

            return self._serialize_user(user)

        finally:
            session.close()

    # ==========================================
    # CHECK EMAIL AVAILABILITY
    # ==========================================

    def email_exists(self, email):
        """
        Check whether an email is already registered.
        """

        try:
            email = self._validate_email(email)
        except ValueError:
            return False

        session = self.db.get_session()

        try:
            return (
                session.query(UserTable.id)
                .filter(func.lower(UserTable.email) == email)
                .first()
                is not None
            )

        finally:
            session.close()
