# Democratiza AI - Contrato Seguro Platform

## Overview

Democratiza AI is a platform aimed at democratizing legal understanding in Brazil. It transforms uncertainty and vulnerability into confidence and empowerment, allowing individuals to truly understand what they are signing.

## Mission

To empower users with legal clarity and understanding, ensuring that everyone can navigate contracts with confidence.

## Vision

To build the leading end-to-end platform for the lifecycle of B2C and SME contracts in Brazil, combining AI analysis, electronic signatures, and intelligent management.

## Architecture

The platform is built on a service-oriented architecture, utilizing a modern tech stack:

- **Frontend**: Next.js 14+, React 18+, TypeScript, Tailwind CSS
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Database**: PostgreSQL with pg_vector extension
- **AI Orchestration**: Specialized contract agents

## Key Features

- **Contract Analysis**: AI-driven analysis of contracts to identify risks and abusive clauses.
- **E-signature Integration**: Seamless electronic signing of contracts.
- **Document Processing**: Efficient handling of document uploads and OCR processing.
- **Real-time Chat**: Interactive chat with AI agents for immediate assistance.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js (for frontend)
- PostgreSQL (for database)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd democratiza-ai
   ```

2. Set up the backend:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

### Running the Application

- **Backend**:
  ```
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

- **Frontend**:
  ```
  npm run dev
  ```

### Accessing the Application

- The backend will be available at `http://localhost:8000`
- The frontend will be available at `http://localhost:3000`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.