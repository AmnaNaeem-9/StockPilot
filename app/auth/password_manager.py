
from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError,
)


# ==========================================
# PASSWORD CONFIGURATION
# ==========================================

# PasswordHasher uses Argon2id by default.
# Its default parameters provide a secure starting point.
password_hasher = PasswordHasher()


# ==========================================
# PASSWORD MANAGER
# ==========================================

class PasswordManager:
    """
    Handles secure password hashing and verification.

    Plain-text passwords are never stored in the database.
    Only their Argon2 hashes are stored.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using Argon2id.

        Returns:
            str: Secure password hash.
        """

        if not isinstance(password, str):
            raise ValueError("Password must be a string.")

        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters.")

        if len(password) > 128:
            raise ValueError("Password cannot exceed 128 characters.")

        if not password.strip():
            raise ValueError("Password cannot be empty.")

        return password_hasher.hash(password)

    @staticmethod
    def verify_password(
        password: str,
        password_hash: str,
    ) -> bool:
        """
        Verify a plain-text password against its stored hash.

        Returns:
            bool: True if the password matches, otherwise False.
        """

        if not isinstance(password, str):
            return False

        if not isinstance(password_hash, str) or not password_hash:
            return False

        try:
            return password_hasher.verify(password_hash, password)

        except (
            VerifyMismatchError,
            VerificationError,
            InvalidHashError,
            ValueError,
        ):
            return False

    @staticmethod
    def needs_rehash(password_hash: str) -> bool:
        """
        Check whether a password hash should be upgraded
        to the current Argon2 configuration.
        """

        if not isinstance(password_hash, str) or not password_hash:
            return False

        try:
            return password_hasher.check_needs_rehash(password_hash)

        except (VerificationError, InvalidHashError, ValueError):
            return False
