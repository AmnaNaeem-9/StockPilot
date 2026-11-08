
# ADR 004: Use Argon2 for Password Hashing

- **Status:** Accepted
- **Date:** 2026-11-08

## Context

StockPilot supports user registration and login.

User passwords must be stored securely. Saving plain-text passwords would expose user credentials if the database were accessed by an unauthorized person.

The application therefore requires a password-hashing solution designed specifically for password storage.

## Decision

Argon2 was selected for password hashing.

The implementation uses the `argon2-cffi` Python package.

Password-related functionality is implemented in:

```text
app/auth/password_manager.py
```

The password manager is responsible for:

- Generating password hashes.
- Verifying submitted passwords.
- Checking whether an existing hash requires updating.

The database stores the resulting password hash in the `password_hash` column of the `users` table.

Plain-text passwords are not stored.

## Alternatives Considered

- **bcrypt:** A widely used password-hashing algorithm with configurable computational cost.
- **PBKDF2:** A password-based key derivation function that can be configured for password hashing.
- **Plain SHA-256:** A general-purpose cryptographic hash function, but not an appropriate standalone password-storage solution.

## Consequences

### Positive

- Provides purpose-built password hashing.
- Uses salted hashes.
- Supports configurable computational and memory costs.
- Password verification does not require storing the original password.
- Separates password handling from the authentication manager.

### Trade-offs

- Password hashing requires computational and memory resources.
- Hashing parameters should be selected carefully for the deployment environment.
- The application must maintain the password-hashing dependency.

## Security Considerations

- Passwords must never be logged or displayed.
- Password hashes must not be exposed through application interfaces.
- Authentication failures should not reveal whether an email address exists.
- Password reset and account recovery features may be considered in future development.

## Conclusion

Argon2 provides a suitable password-hashing solution for StockPilot and supports the application's goal of protecting user credentials.
