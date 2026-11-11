
import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"

# Load local environment variables from .env
load_dotenv(BASE_DIR / ".env")

# Add the app directory to Python's import path
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


# ==========================================
# STREAMLIT CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="StockPilot | Inventory Management",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# IMPORTS
# ==========================================

from database.db_manager import DatabaseManager
from managers.inventory_manager import InventoryManager

from app.auth.auth_manager import AuthManager

from web_ui.views import (
    dashboard,
    products,
    categories,
    suppliers,
    reports,
    ai_insights,
    stock,
)


# ==========================================
# LOAD CSS
# ==========================================

css_path = BASE_DIR / "web_ui" / "styles" / "main.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

@st.cache_resource
def initialize_database():
    """
    Initialize the database connection.

    Database priority:
    1. Streamlit Cloud Secrets (DB_URL)
    2. Local environment variable (.env)
    3. DatabaseManager default SQLite configuration

    SQLite is used for local development.
    PostgreSQL is used for cloud deployment.
    """

    db_url = None

    # Check Streamlit Secrets first.
    try:
        db_url = st.secrets["DB_URL"]

    except (KeyError, FileNotFoundError):
        pass

    # Check local environment variables if no secret exists.
    if not db_url:
        db_url = os.getenv("DB_URL")

    # DatabaseManager uses its default SQLite URL
    # when db_url is None.
    db_manager = DatabaseManager(db_url=db_url)

    # Create tables that do not already exist.
    db_manager.init_db()

    return db_manager


db_manager = initialize_database()

auth_manager = AuthManager(db_manager)


# ==========================================
# SESSION INITIALIZATION
# ==========================================

if "authenticated_user_id" not in st.session_state:
    st.session_state.authenticated_user_id = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"


# ==========================================
# AUTHENTICATION HELPERS
# ==========================================

def logout():
    """
    Log out the current user and reset session state.
    """

    st.session_state.authenticated_user_id = None
    st.session_state.selected_page = "Dashboard"
    st.session_state.auth_mode = "login"

    st.rerun()


# ==========================================
# LANDING PAGE
# ==========================================

def render_landing_page():

    st.title("StockPilot")

    st.subheader("Smart Inventory Management")

    st.write(
        """
        Manage your inventory, monitor stock levels,
        organize suppliers, and make better business decisions
        from one centralized platform.
        """
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Existing User")

        st.write(
            "Access your personal inventory dashboard."
        )

        if st.button(
            "Login",
            key="landing_login",
            use_container_width=True,
            type="primary",
        ):

            st.session_state.auth_mode = "login"
            st.rerun()

    with col2:

        st.subheader("New User")

        st.write(
            "Create your account and start managing inventory."
        )

        if st.button(
            "Create Account",
            key="landing_signup",
            use_container_width=True,
        ):

            st.session_state.auth_mode = "signup"
            st.rerun()


# ==========================================
# LOGIN PAGE
# ==========================================

def render_login_page():

    st.title("Welcome Back")

    st.write(
        "Log in to access your StockPilot account."
    )

    with st.form("login_form"):

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
            type="primary",
        )

        if submitted:

            if not email.strip() or not password:

                st.error(
                    "Please enter your email and password."
                )

            else:

                try:

                    user = auth_manager.login_user(
                        email,
                        password,
                    )

                    if user:

                        st.session_state.authenticated_user_id = user["id"]
                        st.session_state.selected_page = "Dashboard"

                        st.success("Login successful!")

                        st.rerun()

                    else:

                        st.error(
                            "Invalid email or password."
                        )

                except Exception:

                    st.error(
                        "Unable to log in right now. Please try again."
                    )

    st.divider()

    st.write("Don't have an account?")

    if st.button(
        "Create a new account",
        key="login_to_signup",
    ):

        st.session_state.auth_mode = "signup"
        st.rerun()

    if st.button(
        "Back to Home",
        key="login_to_home",
    ):

        st.session_state.auth_mode = "home"
        st.rerun()


# ==========================================
# SIGNUP PAGE
# ==========================================

def render_signup_page():

    st.title("Create Your Account")

    st.write(
        "Register to start using StockPilot."
    )

    with st.form("signup_form"):

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Enter your password again",
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True,
            type="primary",
        )

        if submitted:

            if not name.strip() or not email.strip():

                st.error(
                    "Name and email are required."
                )

            elif not password or not confirm_password:

                st.error(
                    "Please enter and confirm your password."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                try:

                    user = auth_manager.register_user(
                        name=name,
                        email=email,
                        password=password,
                    )

                    st.session_state.authenticated_user_id = user["id"]
                    st.session_state.selected_page = "Dashboard"

                    st.success(
                        "Account created successfully!"
                    )

                    st.rerun()

                except ValueError as error:

                    st.error(str(error))

                except Exception:

                    st.error(
                        "Unable to create your account. Please try again."
                    )

    st.divider()

    st.write("Already have an account?")

    if st.button(
        "Go to Login",
        key="signup_to_login",
    ):

        st.session_state.auth_mode = "login"
        st.rerun()

    if st.button(
        "Back to Home",
        key="signup_to_home",
    ):

        st.session_state.auth_mode = "home"
        st.rerun()


# ==========================================
# AUTHENTICATION ROUTER
# ==========================================

def render_authentication():

    st.sidebar.empty()

    st.markdown(
        """
        <div style="text-align:center; padding: 35px 0 15px 0;">
            <h1>StockPilot</h1>
            <p style="color: #9CA3AF;">
                Inventory Management System
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    auth_mode = st.session_state.auth_mode

    if auth_mode == "login":

        render_login_page()

    elif auth_mode == "signup":

        render_signup_page()

    else:

        render_landing_page()


# ==========================================
# VERIFY AUTHENTICATED USER
# ==========================================

authenticated_user = None

user_id = st.session_state.authenticated_user_id

if user_id is not None:

    try:

        authenticated_user = auth_manager.get_user_by_id(
            user_id
        )

    except Exception:

        authenticated_user = None

    if authenticated_user is None:

        st.session_state.authenticated_user_id = None
        st.session_state.selected_page = "Dashboard"
        st.session_state.auth_mode = "login"

        st.rerun()


# ==========================================
# SHOW AUTHENTICATION OR INVENTORY APP
# ==========================================

if authenticated_user is None:

    render_authentication()

else:

    # ======================================
    # CREATE USER-SCOPED INVENTORY MANAGER
    # ======================================

    inventory = InventoryManager(
        db_manager,
        user_id=authenticated_user["id"],
    )

    # ======================================
    # PAGE REGISTRY
    # ======================================

    PAGES = {
        "Dashboard": dashboard.render,
        "Products": products.render,
        "Categories": categories.render,
        "Suppliers": suppliers.render,
        "Stock Management": stock.render,
        "Reports": reports.render,
        "AI Insights": ai_insights.render,
    }

    # ======================================
    # PAGE ICONS
    # ======================================

    PAGE_ICONS = {
        "Dashboard": ":material/dashboard:",
        "Products": ":material/inventory_2:",
        "Categories": ":material/category:",
        "Suppliers": ":material/local_shipping:",
        "Stock Management": ":material/warehouse:",
        "Reports": ":material/bar_chart:",
        "AI Insights": ":material/psychology:",
    }

    # ======================================
    # VALIDATE SELECTED PAGE
    # ======================================

    if st.session_state.selected_page not in PAGES:

        st.session_state.selected_page = "Dashboard"

    # ======================================
    # SIDEBAR
    # ======================================

    st.sidebar.title("StockPilot")

    st.sidebar.caption(
        "Inventory Management System"
    )

    st.sidebar.divider()

    st.sidebar.write(
        f"**Welcome, {authenticated_user['name']}**"
    )

    st.sidebar.caption(
        authenticated_user["email"]
    )

    st.sidebar.divider()

    # ======================================
    # NAVIGATION
    # ======================================

    for page_name in PAGES:

        if st.sidebar.button(
            page_name,
            key=f"nav_{page_name}",
            icon=PAGE_ICONS.get(
                page_name,
                ":material/description:",
            ),
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.selected_page == page_name
                else "secondary"
            ),
        ):

            st.session_state.selected_page = page_name
            st.rerun()

    st.sidebar.divider()

    # ======================================
    # LOGOUT
    # ======================================

    if st.sidebar.button(
        "Logout",
        key="logout_button",
        icon=":material/logout:",
        use_container_width=True,
    ):

        logout()

    # ======================================
    # RENDER SELECTED PAGE
    # ======================================

    selected_page = st.session_state.selected_page

    try:

        PAGES[selected_page](inventory)

    except Exception:

        st.error(
            f"Unable to display {selected_page}. "
            "Please try again or contact the administrator."
        )
