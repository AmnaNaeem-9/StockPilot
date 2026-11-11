# ADR 002: Use SQLite as the Initial Database

- **Status:** Superseded
- **Date:** 2026-11-08
- **Superseded by:** [ADR 006: Use Supabase PostgreSQL](006-supabase-postgresql.md)

## Context

StockPilot requires a relational database to store user accounts and inventory information.

The database needs to support relationships between users, categories, suppliers, products, and stock transactions.

During the initial development phase, the project required a lightweight database with minimal configuration. As a personal portfolio application, SQLite was suitable for local development and early implementation.

## Decision

SQLite was initially selected as the relational database.

The local database file was stored at:

```text
app/inventory.db
```

SQLAlchemy managed database interactions through the application's database access layer.

The database configuration was implemented in:

```text
app/database/db_manager.py
```

The database schema was defined in:

```text
app/database/schema.py
```

## Alternatives Considered

- **PostgreSQL:** A powerful relational database suitable for concurrent access and production applications.
- **MySQL:** Another relational database option requiring a separate database service.
- **Supabase:** A hosted backend platform providing PostgreSQL database services and additional backend capabilities.

## Consequences

### Positive

- No separate database server was required.
- Simple local setup and development.
- Database storage was maintained in a single file.
- Compatible with SQLAlchemy.
- Suitable for the initial development and portfolio requirements.

### Trade-offs

- SQLite has limitations for applications with concurrent write operations.
- Database backup and file access require consideration.
- Hosted environments may not preserve local database files between restarts or redeployments.
- A separate database strategy may be required as application requirements evolve.

## Supersession

As StockPilot evolved toward hosted deployment, persistent database storage became an important requirement.

SQLite's local file-based storage was no longer the preferred solution for the intended hosting architecture.

Supabase PostgreSQL was selected to provide persistent hosted relational storage and better support for concurrent database access.

The updated implementation uses:

- **Database:** Supabase PostgreSQL
- **ORM:** SQLAlchemy
- **Database driver:** Psycopg 3
- **Connection:** Supabase Session Pooler

The new database decision is documented in [ADR 006: Use Supabase PostgreSQL](006-supabase-postgresql.md).

## Conclusion

SQLite was a practical choice during StockPilot's initial development. Its simplicity helped establish the database layer and implement the application's relational schema.

The decision was later superseded when the project moved toward a hosted architecture requiring persistent PostgreSQL storage.
