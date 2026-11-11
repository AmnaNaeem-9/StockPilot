# StockPilot — Installation and Setup Guide

## 1. Overview

This guide explains how to install, configure, run, and test StockPilot locally.

StockPilot is built with Python and Streamlit. It uses **Supabase PostgreSQL** for persistent database storage, SQLAlchemy for database operations, and Psycopg 3 as its PostgreSQL driver.

The application also integrates Groq API for AI-powered inventory insights.

## 2. Prerequisites

Before installing StockPilot, make sure you have:

- Python 3.10 or later.
- Git.
- A code editor such as Visual Studio Code.
- An internet connection for installing dependencies and connecting to Supabase.
- A Supabase account and configured PostgreSQL project.
- A Groq API key if you want to use AI Insights.

Check your Python installation:

```bash
python --version
```

Check Git:

```bash
git --version
```

## 3. Clone the Repository

Clone the project:

```bash
git clone https://github.com/AmnaNaeem-9/StockPilot.git
```

Navigate into the project directory:

```bash
cd StockPilot
```

## 4. Create a Virtual Environment

Create an isolated Python environment:

```bash
python -m venv .venv
```

Activate it.

**Windows CMD:**

```cmd
.venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

## 5. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

The dependencies include:

- Streamlit for the web interface.
- SQLAlchemy for database operations.
- Psycopg 3 for PostgreSQL connectivity.
- Argon2 for password hashing.
- Pandas for data processing.
- Groq for AI-powered insights.
- Python-dotenv for environment variable management.

## 6. Configure Environment Variables and Secrets

StockPilot requires database connection credentials to connect to Supabase PostgreSQL.

AI Insights additionally requires a Groq API key.

### 6.1 Configure the Supabase Database Connection

Create the following file in the project root:

```text
.streamlit/secrets.toml
```

Add your Supabase PostgreSQL connection URL:

```toml
DB_URL = "YOUR_SUPABASE_POSTGRESQL_CONNECTION_URL"
```

Use the Supabase Session Pooler connection details.

The connection URL should follow this general format:

```text
postgresql+psycopg://USERNAME:PASSWORD@HOST:5432/postgres?sslmode=require
```

Replace the placeholders with your own Supabase connection details.

### 6.2 Configure the Groq API Key

Create a `.env` file in the project root if it does not already exist.

Add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own Groq API key.

### 6.3 Security Considerations

- Never commit `.env` or `.streamlit/secrets.toml` to GitHub.
- Never expose database passwords or API keys in screenshots, source code, or public discussions.
- Keep `.env.example` limited to placeholder values.
- Use Streamlit Community Cloud Secrets for credentials in the hosted application.

## 7. Run the Application

Start StockPilot using:

```bash
python -m streamlit run web_app.py
```

Streamlit will provide a local application URL, normally:

```text
http://localhost:8501
```

Open the URL in your browser.

Make sure your virtual environment is activated before running the application.

## 8. Database Configuration and Initialization

StockPilot uses **Supabase PostgreSQL** as its persistent database.

The database configuration is managed through:

```text
app/database/db_manager.py
```

Database models are defined in:

```text
app/database/schema.py
```

The application uses SQLAlchemy to initialize the database tables through:

```python
Base.metadata.create_all(engine)
```

This creates tables that do not already exist. It does not automatically migrate existing tables when the schema changes.

### Database Configuration Details

| Setting             | Configuration  |
| ------------------- | -------------- |
| Database provider   | Supabase       |
| Database engine     | PostgreSQL     |
| Connection mode     | Session Pooler |
| Port                | 5432           |
| Driver              | Psycopg 3      |
| ORM                 | SQLAlchemy     |
| Connection variable | `DB_URL`     |

The application connects to the configured database when it starts.

**Important:** StockPilot's intended shared and hosted database is Supabase PostgreSQL. Make sure `DB_URL` points to the correct Supabase project before running the application.

## 9. Running Tests

StockPilot includes automated tests for authentication and password handling.

Run the test suite using:

```bash
python -m unittest discover -s tests -v
```

The command should be run from the project root with the virtual environment activated.

## 10. Deployment on Streamlit Community Cloud

StockPilot is designed to use Streamlit Community Cloud for application hosting and Supabase for persistent database storage.

### 10.1 Deploy the GitHub Repository

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Sign in using your GitHub account.
3. Select the option to create a new app.
4. Choose the StockPilot GitHub repository.
5. Select the `main` branch.
6. Set the main file path to:

```text
web_app.py
```

7. Deploy the application.

### 10.2 Configure Cloud Secrets

After creating the application:

1. Open the application settings.
2. Navigate to the Secrets section.
3. Add the following configuration:

```toml
DB_URL = "YOUR_SUPABASE_POSTGRESQL_CONNECTION_URL"
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

4. Save the secrets.
5. Restart or redeploy the application if required.

The deployed application uses these secrets to connect to Supabase PostgreSQL and access the Groq API.

### 10.3 Deployment Architecture

The deployment uses the following arrangement:

| Component              | Platform                  |
| ---------------------- | ------------------------- |
| Application hosting    | Streamlit Community Cloud |
| Source code repository | GitHub                    |
| Relational database    | Supabase PostgreSQL       |
| Database driver        | Psycopg 3                 |
| AI integration         | Groq API                  |

The application and database are hosted separately. Streamlit Community Cloud runs the application, while Supabase stores persistent inventory and account data.

## 11. Project Structure

```text
StockPilot/
│
├── app/
│   ├── ai/
│   ├── auth/
│   ├── database/
│   └── managers/
│
├── docs/
│   ├── design-decisions/
│   ├── images/
│   ├── architecture.md
│   ├── database-design.md
│   ├── security.md
│   └── setup.md
│
├── tests/
│
├── web_ui/
│   ├── components/
│   ├── styles/
│   └── views/
│
├── .streamlit/
│   └── config.toml
│
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── requirements.txt
├── README.md
└── web_app.py
```

Local secret files such as `.env` and `.streamlit/secrets.toml` are intentionally excluded from version control.

## 12. Troubleshooting

### Streamlit command not found

Use:

```bash
python -m streamlit run web_app.py
```

Make sure your virtual environment is activated.

### ModuleNotFoundError

Check that dependencies are installed:

```bash
pip install -r requirements.txt
```

Also verify that you are running the command from the project root.

### AI Insights Not Working

Check that:

- The `.env` file exists in the project root during local development.
- `GROQ_API_KEY` is configured correctly.
- The API key is valid.
- Your internet connection is working.

For Streamlit Community Cloud, verify the `GROQ_API_KEY` value in the application's Secrets settings.

Never paste your API key into an issue, screenshot, or public discussion.

### PostgreSQL Connection Issues

Check that:

- The Supabase project is active.
- The `DB_URL` value is configured correctly.
- The username and password are correct.
- The connection URL uses the correct Supabase Session Pooler host and port.
- The connection URL uses the `postgresql+psycopg://` scheme.
- The connection includes `sslmode=require`.
- Your internet connection is working.

If the database password has been reset, update the connection configuration with the new password.

Never share your complete database connection URL publicly.

### Database Schema Issues

Check that:

- The application is connecting to the intended Supabase project.
- The database tables have been initialized.
- The current SQLAlchemy models match the database schema.

Remember that `Base.metadata.create_all()` creates missing tables but does not perform schema migrations.

Back up important database records before attempting manual schema changes.

## 13. Additional Documentation

For more information, see:

- [System Architecture](architecture.md)
- [Database Design](database-design.md)
- [Security Documentation](security.md)
- [Design Decisions](design-decisions/)

---

**Document:** Installation and Setup Guide
**Project:** StockPilot — Inventory Management System
**Application Framework:** Streamlit
**Database:** Supabase PostgreSQL
**Database Driver:** Psycopg 3
**ORM:** SQLAlchemy
**Deployment Platform:** Streamlit Community Cloud
