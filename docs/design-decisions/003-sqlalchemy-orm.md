
# ADR 003: Use SQLAlchemy as the Object-Relational Mapper

- **Status:** Accepted

## Context

StockPilot needs a consistent way to interact with its relational database.

The application contains several related entities, including users, categories, suppliers, products, and transactions.

Managing database queries and relationships manually throughout the application would make the code harder to maintain.

## Decision

SQLAlchemy was selected as the Object-Relational Mapping (ORM) library.

The project uses SQLAlchemy to:

- Define database tables through Python classes.
- Represent database relationships using ORM relationships.
- Manage database connections and sessions.
- Execute database operations.
- Enforce database constraints through schema definitions.

The database implementation is organized into:

```text
app/database/
├── db_manager.py
├── schema.py
└── __init__.py
```

The `schema.py` module defines the database models, while `db_manager.py` manages the database engine and sessions.

## Alternatives Considered

- **Raw SQL:** Provides direct control over SQL queries but requires more manual query and relationship management.
- **Django ORM:** Offers ORM functionality integrated with Django, but would introduce a different application framework.
- **SQLModel:** Provides a SQLAlchemy-based ORM interface with Pydantic integration, but was not selected for the current implementation.

## Consequences

### Positive

- Python classes represent database tables.
- Relationships can be defined directly in the schema.
- Database operations are organized consistently.
- SQLAlchemy supports SQLite and other relational database engines.
- Centralized database management improves maintainability.

### Trade-offs

- Requires understanding ORM concepts.
- Complex queries may require additional SQLAlchemy knowledge.
- ORM-generated queries may need inspection when troubleshooting database performance.

## Conclusion

SQLAlchemy provides a structured and maintainable approach to database interaction and fits StockPilot's layered Python architecture.
