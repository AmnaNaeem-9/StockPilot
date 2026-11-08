
# StockPilot — Security Documentation

## 1. Overview

StockPilot includes authentication and user-specific data isolation to protect inventory information.

The application uses an internal authentication system rather than relying on third-party authentication providers.

Security-related functionality is implemented primarily in:

```text
app/
├── auth/
│   ├── auth_manager.py
│   └── password_manager.py
│
└── database/
    ├── db_manager.py
    └── schema.py
```

## 2. Authentication

StockPilot provides user registration and login functionality.

The `AuthManager` class, implemented in `app/auth/auth_manager.py`, handles authentication operations.

Its responsibilities include:

- Registering new users.
- Checking whether an email address already exists.
- Validating login credentials.
- Retrieving user account information.
- Supporting authenticated user validation.

Each registered account has its own user ID, which is used to associate inventory records with the correct account.

## 3. Password Security

StockPilot uses **Argon2** for password hashing.

The implementation is located in:

```text
app/auth/password_manager.py
```

Passwords are never intended to be stored as plain-text values.

### Password handling process

**During registration:**

1. The user submits a password.
2. The password manager generates a secure password hash.
3. The hash is stored in the `password_hash` column of the users table.

**During login:**

1. The user submits their email and password.
2. The authentication manager retrieves the corresponding account.
3. The password manager verifies the submitted password against the stored hash.
4. Access is granted only when authentication succeeds and the account is active.

### Why Argon2?

Argon2 is a password-hashing algorithm designed to make password guessing more computationally expensive.

It supports:

- Salted password hashing.
- Configurable computational cost.
- Memory-intensive hashing.
- Password verification without storing the original password.

## 4. User Data Isolation

StockPilot associates inventory records with their respective users.

The following tables contain a `user_id` field:

- Categories
- Suppliers
- Products
- Transactions

This association ensures that inventory operations are scoped to the authenticated user.

### Database-level protection

The database schema uses composite foreign keys to ensure that related records belong to the same user.

For example, a product's category relationship includes both:

```text
category_id
user_id
```

This prevents a product belonging to one user from referencing another user's category.

Similar ownership checks apply to supplier and transaction relationships.

### Application-level protection

The `InventoryManager` receives the authenticated user's ID and uses it when performing inventory operations.

This provides an additional layer of protection beyond database constraints.

## 5. Database Security

StockPilot currently uses SQLite.

The local database file is:

```text
app/inventory.db
```

Database-related security considerations include:

- Database files should not be committed to public repositories.
- Database backups should be kept private.
- Access to the project directory should be controlled.
- Database operations should use the application's database and business logic layers.

The project's `.gitignore` excludes database files from Git tracking.

## 6. Environment Variables and API Credentials

StockPilot uses environment variables to manage sensitive configuration.

The Groq API key is accessed through:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The actual `.env` file must remain private.

The repository includes `.env.example` as a template for required configuration.

Security rules:

- Never commit `.env`.
- Never hardcode API keys in source files.
- Never share API credentials in screenshots or documentation.
- Configure secrets securely when deploying the application.

## 7. Session and Account Security

StockPilot uses Streamlit session state to maintain authentication information during application interactions.

The application should validate the authenticated user's account before allowing access to protected inventory pages.

An inactive account should not be allowed to use protected application functionality.

## 8. Security Limitations and Future Improvements

Security is an ongoing process. The current implementation can be improved further.

Potential improvements include:

- Password reset functionality.
- Email verification.
- Login rate limiting.
- Stronger session-expiration controls.
- Security event logging.
- Automated security testing.
- Regular dependency updates.
- Production deployment security review.

These are potential improvements and should not be considered implemented features unless added and tested.

## 9. Security Checklist

| Security measure                   | Implementation         |
| ---------------------------------- | ---------------------- |
| Password hashing                   | Argon2                 |
| Plain-text password storage        | Avoided                |
| Unique user email                  | Database constraint    |
| User-specific inventory            | `user_id` scoping    |
| Cross-user relationship protection | Composite foreign keys |
| API key configuration              | Environment variable   |
| Database exclusion from Git        | `.gitignore`         |
| Authentication management          | `AuthManager`        |

---

**Document:** Security Documentation
**Project:** StockPilot — Inventory Management System
**Status:** Current security implementation and improvement considerations
