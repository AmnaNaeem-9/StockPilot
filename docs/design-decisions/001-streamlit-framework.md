
# ADR 001: Use Streamlit as the Web Application Framework

- **Status:** Accepted
- 

## Context

StockPilot was originally developed as a Python-based inventory management application.

A browser-based interface was needed to make the system easier to access and demonstrate as a portfolio project.

The project also needed to reuse its existing Python business logic without introducing an entirely separate frontend application.

## Decision

Streamlit was selected as the web application framework.

The application uses Streamlit to provide:

- Browser-based user interfaces.
- Login and registration screens.
- Inventory management pages.
- Dashboard visualizations and reporting.
- Interactive forms and navigation.

The main entry point is `web_app.py`, while individual pages are organized inside `web_ui/views/`.

## Alternatives Considered

- **Flask:** A Python web framework offering greater control over routing and application structure, but requiring more frontend development.
- **Django:** A full-stack Python framework with built-in authentication and administration features, but offering more framework functionality than this project currently needs.
- **React with a Python API:** A separate frontend and backend architecture requiring additional development and integration.

## Consequences

### Positive

- Enables rapid development of interactive interfaces.
- Allows the project to remain primarily Python-based.
- Integrates with existing Python libraries.
- Simplifies local development and demonstration.

### Trade-offs

- Provides less frontend customization than a dedicated frontend framework.
- Uses Streamlit's application execution and session model.
- Deployment requires consideration of Streamlit's hosting and filesystem behavior.

## Conclusion

Streamlit provides a practical balance between development speed, Python integration, and usability for StockPilot's current requirements.
