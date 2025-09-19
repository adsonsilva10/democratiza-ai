# Democratiza AI - Contrato Seguro Platform

## Project Overview

**Missão**: Democratizar a compreensão jurídica no Brasil. Transformar a incerteza e a vulnerabilidade em confiança e empoderamento, permitindo que qualquer pessoa entenda de verdade o que está assinando.

**Visão**: Construir a plataforma líder de ponta a ponta para o ciclo de vida de contratos B2C e PME no Brasil, combinando análise por IA, assinatura eletrônica e gestão inteligente.

## Architecture & Tech Stack

### Core Architecture
- **Service-oriented architecture** with message queue decoupling
- **Frontend**: Next.js 14+ (App Router), React 18+, TypeScript, Tailwind CSS, Shadcn/UI
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic, Uvicorn
- **Database**: PostgreSQL (via Supabase) with pg_vector extension
- **AI Orchestration**: contains-studio/agents framework with specialized contract agents

### Key Infrastructure Services
- **LLM**: Anthropic Claude 3 (Opus/Sonnet) via API
- **OCR**: Google Cloud Vision API  
- **E-signature**: D4Sign API
- **Payments**: Mercado Pago
- **File Storage**: Cloudflare R2
- **Message Queue**: AWS SQS
- **Emails**: SendGrid

## Project Structure

```
/backend
├── app/api/v1/          # API endpoints (auth, contracts, chat, payments)
├── app/agents/          # Specialized AI agents per contract type
│   ├── factory.py       # Agent factory pattern
│   ├── classifier_agent.py  # Contract type classification
│   └── *_agent.py       # Domain specialists (rental, telecom, financial)
├── app/services/        # Business logic layer
│   └── rag_service.py   # RAG indexing and retrieval
└── app/workers/         # Async background processing

/frontend
├── app/(auth)/          # Authentication routes group
├── app/(dashboard)/     # Protected dashboard routes
├── components/features/ # Core features (scanner, upload, chat)
└── lib/api.ts          # API client layer
```

## AI Agent System

### Agent Architecture Pattern
- **Factory Pattern**: `agents/factory.py` creates appropriate specialist agent
- **Classification First**: `classifier_agent.py` identifies contract type before routing
- **Domain Specialists**: Each contract type has dedicated agent with specialized knowledge
- **RAG Foundation**: All agents use `rag_service.py` for knowledge base queries

### Agent Specializations
- `rental_agent.py` - Locação contracts (rental agreements)
- `telecom_agent.py` - Telecommunications contracts  
- `financial_agent.py` - Financial/banking contracts

### Implementation Guidelines
- Agents should extend base agent class from contains-studio/agents
- Each agent maintains domain-specific prompt templates
- RAG context must be incorporated into agent reasoning
- Agent responses should be structured for frontend consumption

## Development Workflows

### Backend Development
```bash
# Local development with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run async workers separately
python -m app.workers.document_processor
```

### Frontend Development  
```bash
# Next.js development with App Router
npm run dev
# Runs on localhost:3000 with API proxy to backend
```

### Database Migrations
- Use SQLAlchemy Alembic for schema changes
- Always include pg_vector extension requirements
- Test migrations against Supabase staging environment

## Critical Integration Points

### Document Processing Flow
1. **Upload** → Cloudflare R2 storage
2. **OCR** → Google Cloud Vision API extraction  
3. **Classification** → `classifier_agent.py` determines contract type
4. **Analysis** → Appropriate specialist agent via factory
5. **RAG Enhancement** → Knowledge base consultation via `rag_service.py`
6. **Response** → Structured analysis returned to frontend

### Authentication & Authorization
- JWT-based authentication through FastAPI
- User sessions managed via Next.js middleware
- Protected routes use `(dashboard)` group pattern
- API endpoints require bearer token validation

### Real-time Features
- WebSocket connections for chat interface (`api/v1/chat.py`)
- Progress updates during document processing via SQS
- Live analysis feedback through `ChatWithAgent.tsx`

## Contract Analysis Conventions

### Risk Classification System
- **Alto Risco** (High Risk) - Red indicators
- **Médio Risco** (Medium Risk) - Yellow indicators  
- **Baixo Risco** (Low Risk) - Green indicators

### Key Analysis Areas
- **Cláusulas Abusivas** - Abusive clauses detection
- **Condições de Pagamento** - Payment terms analysis
- **Prazos e Rescisão** - Deadlines and termination conditions
- **Garantias e Penalidades** - Warranties and penalties

## Code Quality Standards

### Python Backend
- Type hints required for all functions
- Pydantic models for all API schemas
- FastAPI dependency injection for services
- Async/await for I/O operations
- Structured logging with correlation IDs

### TypeScript Frontend
- Strict TypeScript configuration
- Tailwind CSS for styling (no custom CSS)
- Shadcn/UI components only
- Error boundaries for all async operations
- React Query for API state management

## Testing Approach

### Backend Testing
- Pytest with async test support
- Mock external APIs (Claude, OCR, etc.)
- Integration tests for agent workflows
- Database tests use transaction rollbacks

### Frontend Testing  
- Jest + Testing Library for components
- MSW for API mocking
- E2E tests for critical user journeys
- Visual regression testing for contract displays

## Deployment Considerations

### Environment Variables
- Separate configs for staging/production
- Claude API keys rotation strategy
- Database connection pooling settings
- Message queue batch processing limits

### Monitoring Requirements
- Agent performance metrics (response time, accuracy)
- Document processing pipeline observability  
- User interaction analytics
- Error tracking with context preservation

## Security Guidelines

### Data Protection
- All contract documents encrypted at rest
- PII handling follows LGPD compliance
- Audit logs for all document access
- Rate limiting on API endpoints

### AI Safety
- Input sanitization before LLM processing
- Output filtering for sensitive information
- Prompt injection protection
- Content policy enforcement

This platform operates in the "hiato pré-judicial" (pre-legal gap), focusing on prevention rather than litigation. All development should prioritize user empowerment and legal clarity over technical complexity.
