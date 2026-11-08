
# ADR 002: Use SQLite as the Database

- **Status:** Accepted
- **Date:** 2026-11-08

## Context

StockPilot requires a relational database to store user accounts and inventory information.

The database needs to support relationships between users, categories, suppliers, products, and stock transactions.

The project is a personal portfolio application, so a lightweight database with minimal configuration is suitable for its current requirements.

## Decision

SQLite was selected as the relational database.

The database is stored locally at:

```text
app/inventory.db
```

SQLAlchemy manages database interactions through the application's database access layer.

The database configuration is implemented in:

```text
app/database/db_manager.py
```

The database schema is defined in:

```text
app/database/schema.py
```

## Alternatives Considered

- **PostgreSQL:** A powerful relational database suitable for larger applications and multi-user production environments, but requiring a separate database service.
- **MySQL:** Another relational database option that requires additional database server configuration.
- **Supabase:** A hosted backend platform that provides PostgreSQL database services and additional backend capabilities.

## Consequences

### Positive

- No separate database server is required.
- Simple local setup and development.
- Database storage is maintained in a single file.
- Works with SQLAlchemy.
- Suitable for the project's current personal and portfolio development needs.

### Trade-offs

- SQLite has limitations for applications with many concurrent writers.
- Database backup and file access require consideration.
- Hosted environments may not preserve local database files between restarts or redeployments.
- Scaling to larger production workloads may require a different database strategy.

## Future Considerations

The current implementation will continue using SQLite.

Any future database migration should be based on actual requirements such as concurrent usage, hosting persistence, and application scale.

A migration is not currently planned.

## Conclusion

SQLite provides a simple and practical database solution for StockPilot's current scope while keeping the application's data layer straightforward.
