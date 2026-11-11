
# ADR 006: Use Supabase PostgreSQL as the Primary Database

- **Status:** Accepted
- **Date:** 2026-11-11
- **Supersedes:** [ADR 002: Use SQLite as the Initial Database](002-sqlite-database.md)

## Context

StockPilot initially used SQLite as its relational database during local development.

As the project evolved toward hosted deployment, persistent database storage and support for concurrent users became important requirements.

A local SQLite database file is not an appropriate primary storage solution for the intended Streamlit Community Cloud deployment because hosted application files may not provide reliable persistent storage.

The project therefore required a managed relational database that could be accessed by the hosted application.

## Decision

Supabase PostgreSQL was selected as StockPilot's primary database.

Supabase provides a managed PostgreSQL database that supports persistent storage and relational database operations.

The application uses the following technologies:

- **Database:** Supabase PostgreSQL
- **ORM:** SQLAlchemy
- **Database driver:** Psycopg 3
- **Connection method:** Supabase Session Pooler
- **Pooler port:** 5432

The database connection is configured through the `DB_URL` environment variable or Streamlit secrets.

For local development, the connection is configured in:

```text
.streamlit/secrets.toml
```

For Streamlit Community Cloud, the database connection is configured through the application's Secrets settings.

Database credentials must never be committed to the GitHub repository.

## Alternatives Considered

- **SQLite:** Simple and suitable for local development, but file-based storage is not the preferred solution for the hosted deployment architecture.
- **Self-hosted PostgreSQL:** Provides PostgreSQL capabilities but requires additional server setup, maintenance, and administration.
- **MySQL:** A capable relational database, but PostgreSQL was selected for this implementation.
- **Supabase PostgreSQL:** Provides managed PostgreSQL hosting and reduces database infrastructure management.

## Consequences

### Positive

- Persistent database storage independent of the Streamlit application instance.
- Supports relational data and SQLAlchemy ORM operations.
- Better suited to concurrent database access than SQLite.
- Managed database infrastructure reduces server administration.
- Separates application hosting from database hosting.
- Provides a practical foundation for future application improvements.

### Trade-offs

- Requires an internet connection and valid database credentials.
- Application availability depends on the external database service.
- Connection pooling and database connection limits must be considered.
- Supabase service limits and pricing may affect future usage.
- Database schema changes require a migration strategy.

## Implementation Notes

The database connection is initialized through:

```text
app/database/db_manager.py
```

The database schema is defined in:

```text
app/database/schema.py
```

SQLAlchemy's `Base.metadata.create_all()` creates tables that do not already exist. It does not automatically migrate existing tables when the schema changes.

Future schema modifications should use a proper database migration approach.

The application uses Streamlit Community Cloud as its deployment target, while Supabase hosts the PostgreSQL database separately.

## Security Considerations

- Database credentials are stored in environment variables or Streamlit secrets.
- `.streamlit/secrets.toml` is excluded from version control.
- `.env` files are excluded from version control.
- User passwords are hashed using Argon2 before storage.
- Database access is handled through the application's database access layer.

## Conclusion

Supabase PostgreSQL provides StockPilot with persistent, managed relational database storage suitable for its intended hosted architecture.

SQLAlchemy and Psycopg 3 provide the integration between the Python application and PostgreSQL, while Streamlit secrets keep database credentials outside the source code.
