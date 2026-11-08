
import sys
from pathlib import Path

# Add the app directory to Python's import path.
BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"

sys.path.insert(0, str(APP_DIR))

# Import application modules.
from database.db_manager import DatabaseManager
from app.auth.auth_manager import AuthManager


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

db_manager = DatabaseManager()
db_manager.init_db()

auth = AuthManager(db_manager)


# ==========================================
# TEST ACCOUNT
# ==========================================

name = "Test User"
email = "testuser@example.com"
password = "TestPassword@123"


try:
    print("\n--- SIGNUP TEST ---")

    try:
        user = auth.register_user(name, email, password)

        print("Registration successful!")
        print("User:", user)

    except ValueError as error:
        print("Registration message:", error)

    print("\n--- LOGIN TEST ---")

    logged_in_user = auth.login_user(email, password)

    if logged_in_user:
        print("Login successful!")
        print("Logged-in user:", logged_in_user)
    else:
        print("Login failed!")

    print("\n--- WRONG PASSWORD TEST ---")

    wrong_login = auth.login_user(
        email,
        "IncorrectPassword123"
    )

    print("Wrong password rejected:", wrong_login is None)

    print("\n--- EMAIL CHECK TEST ---")

    print("Email exists:", auth.email_exists(email))

    print("\n--- USER RETRIEVAL TEST ---")

    if logged_in_user:
        retrieved_user = auth.get_user_by_id(
            logged_in_user["id"]
        )

        print("User retrieved:", retrieved_user is not None)

finally:
    db_manager.close()
