# StockPilot — Inventory Management System

A web-based inventory management application built with Python, Streamlit, and Object-Oriented Programming principles. StockPilot helps users organize products, manage stock movements, monitor inventory levels, and gain insights into inventory operations.

## Project Overview

StockPilot is a personal software development project that transforms a traditional inventory management system into an interactive web application.

It combines a modular Python backend with a Streamlit interface, SQLite database storage, user authentication, and AI-powered inventory insights.

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

## Technology Stack

| Area            | Technologies  |
| --------------- | ------------- |
| Language        | Python        |
| Frontend        | Streamlit     |
| Backend         | Python, OOP   |
| Database        | SQLite        |
| ORM             | SQLAlchemy    |
| Authentication  | Argon2        |
| AI Integration  | Groq API      |
| Data Processing | Pandas        |
| Configuration   | python-dotenv |
| Styling         | CSS           |

## Project Architecture

StockPilot follows a layered structure that separates the user interface, business logic, authentication, database operations, and AI integration.

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
│   └── views/               # Streamlit pages
│
├── tests/                   # Automated tests
├── docs/                    # Technical documentation
├── .streamlit/              # Streamlit configuration
│
├── web_app.py               # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── CHANGELOG.md             # Project change history
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/StockPilot.git
cd StockPilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do not commit `.env` or expose your API key.

### 5. Run the application

```bash
python -m streamlit run web_app.py
```

Streamlit will provide a local URL in the terminal, usually:

`http://localhost:8501`

## Database

StockPilot uses SQLite with SQLAlchemy ORM.

The database is initialized by the application, and its default location is:

`app/inventory.db`

Database files are excluded from version control. A fresh database is initialized when required.

See [Database Design](docs/database-design.md).

## Security

- Passwords are hashed using Argon2.
- Authenticated users access their own inventory records.
- Database relationships enforce user ownership constraints.
- Sensitive environment variables are excluded from version control.

See [Security Documentation](docs/security.md).

## Testing

Run the authentication tests:

```bash
python -m unittest discover -s tests -v
```

See [Setup Guide](docs/setup.md) for additional development and testing information.

## Documentation

- [Architecture](docs/architecture.md)
- [Setup Guide](docs/setup.md)
- [Database Design](docs/database-design.md)
- [Security](docs/security.md)
- [Architecture Decision Records](docs/design-decisions/)

## Future Improvements

- Improve automated test coverage.
- Add more detailed reporting and analytics.
- Enhance inventory forecasting and AI recommendations.
- Improve deployment and database persistence.
- Add application screenshots and a demonstration video.

## Author

**Amna Naeem**

GitHub: [AmnaNaeem-9](https://github.com/AmnaNaeem-9)

---

*StockPilot is a personal portfolio project developed to demonstrate Python, OOP, database management, authentication, and web application development.*
