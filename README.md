# StockPilot — Inventory Management System

A web-based inventory management application built with Python, Streamlit, and Object-Oriented Programming principles.

StockPilot helps users organize products, manage stock movements, monitor inventory levels, and gain insights into inventory operations.

## Project Overview

StockPilot is a personal software development project that transforms a traditional inventory management system into an interactive web application.

It combines a modular Python backend with a Streamlit interface, Supabase PostgreSQL database storage, user authentication, and AI-powered inventory insights.

The application is designed around a layered architecture that separates the user interface, business logic, authentication, and database operations.

## Features

- **User Authentication:** Account registration, login, and logout with Argon2 password hashing.
- **Dashboard:** Overview of inventory statistics and stock information.
- **Product Management:** Add, view, update, and delete products.
- **Category Management:** Organize products into categories.
- **Supplier Management:** Maintain supplier information.
- **Stock Management:** Record stock-in and stock-out operations.
- **Reports:** Review inventory information and stock reports.
- **AI Insights:** Generate inventory insights and restocking suggestions using the Groq API.
- **User Data Isolation:** Keep inventory records scoped to their respective authenticated users.
- **Persistent Database:** Store application data using Supabase PostgreSQL.

## Technology Stack

| Area              | Technologies                     |
| ----------------- | -------------------------------- |
| Language          | Python                           |
| Frontend          | Streamlit                        |
| Backend           | Python, OOP                      |
| Database          | Supabase PostgreSQL              |
| ORM               | SQLAlchemy                       |
| Database Driver   | Psycopg 3                        |
| Authentication    | Argon2                           |
| AI Integration    | Groq API                         |
| Data Processing   | Pandas                           |
| Configuration     | python-dotenv, Streamlit Secrets |
| Styling           | CSS                              |
| Version Control   | Git, GitHub                      |
| Deployment Target | Streamlit Community Cloud        |

## Project Architecture

StockPilot follows a layered structure that separates the user interface, business logic, authentication, database operations, and AI integration.

The application uses SQLAlchemy to communicate with Supabase PostgreSQL through Psycopg 3.

See [Architecture Documentation](docs/architecture.md) for details.

## Project Structure

```text
StockPilot/
├── app/
│   ├── ai/                 # AI integration
│   ├── auth/               # Authentication and password management
│   ├── database/           # Database configuration and schema
│   └── managers/           # Inventory business logic
│
├── web_ui/
│   ├── components/         # Reusable UI components
│   ├── styles/             # Application styles
│   └── views/              # Streamlit pages
│
├── tests/                  # Automated tests
├── docs/                   # Technical documentation
├── .streamlit/             # Streamlit configuration
│
├── web_app.py              # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── CHANGELOG.md            # Project change history
├── LICENSE                 # MIT License
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later.
- Git.
- A Supabase account with a configured PostgreSQL project.
- A Groq API key for AI Insights (optional).

### 1. Clone the repository

```bash
git clone https://github.com/AmnaNaeem-9/StockPilot.git
cd StockPilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows CMD:

```cmd
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure database credentials

Create the following file:

```text
.streamlit/secrets.toml
```

Add your Supabase PostgreSQL connection URL:

```toml
DB_URL = "YOUR_SUPABASE_POSTGRESQL_CONNECTION_URL"
```

Use your Supabase Session Pooler connection details.

The connection URL should follow this format:

```text
postgresql+psycopg://USERNAME:PASSWORD@HOST:5432/postgres?sslmode=require
```

### 5. Configure the Groq API key

Create a `.env` file in the project root using `.env.example` as a template.

Add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

AI Insights requires a valid Groq API key. Other inventory features do not require AI configuration.

**Security:** Never commit `.env` or `.streamlit/secrets.toml` to GitHub. Keep database credentials and API keys private.

### 6. Run the application

```bash
python -m streamlit run web_app.py
```

Streamlit will provide a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open the URL in your browser.

For detailed instructions, see the [Installation and Setup Guide](docs/setup.md).

## Database

StockPilot uses **Supabase PostgreSQL** with SQLAlchemy ORM and Psycopg 3.

The database is managed through:

```text
app/database/db_manager.py
```

Database models are defined in:

```text
app/database/schema.py
```

The application initializes missing database tables through SQLAlchemy.

Database credentials are supplied through the `DB_URL` configuration variable. Local development uses Streamlit secrets or environment configuration, while Streamlit Community Cloud uses its Secrets settings.

See [Database Design](docs/database-design.md) for table definitions, relationships, constraints, and user data isolation.

## Deployment

StockPilot's deployment architecture uses:

| Component              | Platform                  |
| ---------------------- | ------------------------- |
| Application Hosting    | Streamlit Community Cloud |
| Source Code Repository | GitHub                    |
| Database Hosting       | Supabase PostgreSQL       |
| AI Integration         | Groq API                  |

The application is designed to be deployed from the GitHub repository to Streamlit Community Cloud.

The hosted application uses Streamlit Secrets to configure the Supabase database connection and Groq API key.

See the [Setup Guide](docs/setup.md) for deployment instructions.

## Security

- Passwords are hashed using Argon2.
- Authenticated users access their own inventory records.
- Database relationships enforce user ownership constraints.
- Sensitive environment variables are excluded from version control.
- Database credentials and API keys are stored outside the source code.

See [Security Documentation](docs/security.md).

## Testing

Run the automated tests from the project root:

```bash
python -m unittest discover -s tests -v
```

The tests cover authentication and password handling.

See [Setup Guide](docs/setup.md) for additional development and testing information.

## Documentation

- [Architecture](docs/architecture.md)
- [Setup Guide](docs/setup.md)
- [Database Design](docs/database-design.md)
- [Security](docs/security.md)
- [Architecture Decision Records](docs/design-decisions/)

## Future Improvements

- Expand automated test coverage across application modules.
- Add more detailed reporting and analytics.
- Enhance inventory forecasting and AI recommendations.
- Improve the application with additional user-focused features.

## Author

**Amna Naeem**

GitHub: [AmnaNaeem-9](https://github.com/AmnaNaeem-9)

---

*StockPilot is a personal portfolio project developed to demonstrate Python, OOP, database management, authentication, and web application development.*
