
# Changelog

All notable changes to StockPilot are documented in this file.

This project follows the Keep a Changelog format.

## [Unreleased]

### Planned

- Additional automated tests for inventory operations.
- Improved error handling and logging.
- Application screenshots and demonstration media.
- Further documentation improvements.

## [0.1.0] - 2026-11-08

### Added

- Streamlit-based web application.
- User registration and login functionality.
- Argon2 password hashing.
- User-specific inventory data isolation.
- Product management.
- Category management.
- Supplier management.
- Stock-in and stock-out operations.
- Dashboard and inventory statistics.
- Reports and AI-powered inventory insights.
- SQLite database integration using SQLAlchemy.
- Custom dark-themed application interface.
- Initial project documentation.
- Architecture and database design documentation.
- Five Architecture Decision Records (ADRs).
- Authentication and password-related tests.

### Security

- Passwords stored as hashes instead of plain-text values.
- User-specific ownership relationships.
- Composite foreign-key constraints for related inventory records.
- Environment-based configuration for the Groq API key.

---

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
[Semantic Versioning](https://semver.org/spec/v2.0.0.html)
