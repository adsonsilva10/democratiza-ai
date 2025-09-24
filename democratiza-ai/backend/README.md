# Democratiza AI - Backend Documentation

## Overview

The backend of the Democratiza AI platform is built using FastAPI, a modern web framework for building APIs with Python 3.11+. This backend serves as the core of the application, handling authentication, contract management, chat functionality, and payment processing.

## Project Structure

The backend project is organized as follows:

```
/backend
├── app/                  # Main application package
│   ├── api/              # API endpoints
│   ├── agents/           # AI agents for contract analysis
│   ├── services/         # Business logic layer
│   ├── workers/          # Background processing tasks
│   ├── models/           # Database models
│   └── config.py         # Configuration settings
├── requirements.txt      # Python dependencies
├── alembic.ini           # Database migration configuration
└── README.md             # This documentation
```

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd democratiza-ai/backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

To run the FastAPI application locally, use the following command:

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

To manage database migrations, use Alembic. Make sure to configure your database connection in `alembic.ini` and run:

```
alembic upgrade head
```

## API Endpoints

The backend exposes several API endpoints for various functionalities:

- **Authentication**: Located in `app/api/v1/auth.py`
- **Contracts**: Located in `app/api/v1/contracts.py`
- **Chat**: Located in `app/api/v1/chat.py`
- **Payments**: Located in `app/api/v1/payments.py`

## Background Workers

The backend includes asynchronous workers for processing documents. You can run the document processor with:

```
python -m app.workers.document_processor
```

## Contributing

Contributions are welcome! Please follow the standard Git workflow for submitting changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.