
# StockPilot — Installation and Setup Guide

## 1. Overview

This guide explains how to install, configure, and run StockPilot locally.

StockPilot is built with Python and Streamlit. It uses SQLite for database storage and SQLAlchemy for database operations.

## 2. Prerequisites

Before installing StockPilot, make sure you have:

- Python 3.10 or later.
- Git.
- A code editor such as Visual Studio Code.
- An internet connection for installing dependencies.
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
git clone https://github.com/YOUR_USERNAME/StockPilot.git
```

Navigate into the project directory:

```bash
cd StockPilot
```

Replace `YOUR_USERNAME` with the actual GitHub username after the repository is published.

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

## 6. Configure Environment Variables

Create a `.env` file in the project root.

Copy the contents of `.env.example` into `.env` and configure the required values.

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own Groq API key.

**Important:** Never commit your actual `.env` file or expose API credentials publicly.

AI functionality requires a valid Groq API key. Other application features should be used independently of AI configuration where supported by the application.

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

## 8. Database Initialization

StockPilot currently uses SQLite.

The local database file is:

```text
app/inventory.db
```

Database configuration is managed through:

```text
app/database/db_manager.py
```

Database models are defined in:

```text
app/database/schema.py
```

The application initializes its database tables through SQLAlchemy.

Do not delete the database file if you want to preserve existing local inventory records.

## 9. Running Tests

StockPilot includes automated tests for authentication and password handling.

Run the test suite using:

```bash
python -m unittest discover -s tests -v
```

The command should be run from the project root with the virtual environment activated.

## 10. Project Structure

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
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── web_app.py
```

## 11. Troubleshooting

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

### AI Insights not working

Check that:

- The `.env` file exists in the project root.
- `GROQ_API_KEY` is configured correctly.
- The API key is valid.
- Your internet connection is working.

Never paste your API key into an issue, screenshot, or public discussion.

### Database issues

Check that:

- The application has permission to access the project directory.
- The SQLite database file is available.
- The database configuration points to the intended database.

Back up your database before attempting manual database changes.

## 12. Additional Documentation

For more information, see:

- [System Architecture](architecture.md)
- [Database Design](database-design.md)
- [Security Documentation](security.md)
- [Design Decisions](design-decisions/)

---

**Document:** Installation and Setup Guide
**Project:** StockPilot — Inventory Management System
