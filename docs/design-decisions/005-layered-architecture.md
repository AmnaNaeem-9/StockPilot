# ADR 005: Adopt a Layered Application Architecture

- **Status:** Accepted

## Context

As StockPilot evolved from a basic inventory management application into a browser-based application, the codebase needed a clear structure.

Keeping user interface code, authentication, business logic, and database operations together would make the application harder to maintain and extend.

A structured architecture was needed to separate responsibilities and improve code organization.

## Decision

StockPilot follows a layered application architecture.

The application is organized into the following main layers:

### 1. Presentation Layer

**Location:** `web_app.py` and `web_ui/`

Responsible for:

- Rendering Streamlit pages.
- Handling user interactions.
- Managing application navigation.
- Displaying inventory information.

### 2. Authentication Layer

**Location:** `app/auth/`

Responsible for:

- User registration.
- Login validation.
- Password hashing and verification.
- Retrieving and validating user accounts.

### 3. Business Logic Layer

**Location:** `app/managers/`

Responsible for:

- Product management.
- Category management.
- Supplier management.
- Stock operations.
- Inventory-related business rules.

### 4. Data Access Layer

**Location:** `app/database/`

Responsible for:

- Database configuration.
- SQLAlchemy engine and session management.
- Database models.
- Database relationships and constraints.

### 5. AI Integration Layer

**Location:** `app/ai/`

Responsible for:

- Communication with the Groq API.
- AI-powered inventory insights.
- Restocking recommendations.

## Alternatives Considered

- **Monolithic structure:** Keep all functionality in a small number of modules. This is simpler initially but becomes harder to maintain as features grow.
- **Microservices architecture:** Separate application functionality into independently deployed services. This introduces unnecessary operational complexity for the current project.
- **Model-View-Controller (MVC):** Organize application responsibilities around models, views, and controllers. This was not selected as the primary structure because the existing Streamlit application follows a more direct layered approach.

## Consequences

### Positive

- Clear separation of responsibilities.
- Better code organization.
- Easier debugging and testing.
- Reusable business logic.
- Easier future feature development.
- UI components remain separate from database implementation.

### Trade-offs

- Requires more modules and organized imports.
- Developers must understand the responsibilities of each layer.
- Communication between layers needs consistent interfaces.

## Architectural Principle

The presentation layer should not directly implement database operations.

Instead, inventory views communicate with `InventoryManager`, while database operations are handled through the database access layer.

Authentication is handled through `AuthManager`, with password-related operations delegated to `PasswordManager`.

This keeps responsibilities separated and makes the application easier to maintain.

## Conclusion

A layered architecture provides a practical structure for StockPilot, balancing maintainability, simplicity, and future extensibility without introducing unnecessary microservice complexity.
