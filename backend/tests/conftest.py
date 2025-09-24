import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db, Base
from app.core.config import settings

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    test_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with TestingSessionLocal() as session:
        yield session
        
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(db_session):
    """Create a test client with overridden dependencies."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_contract_text():
    """Sample contract text for testing."""
    return """
    CONTRATO DE LOCAÇÃO RESIDENCIAL
    
    LOCADOR: João Silva, brasileiro, casado, engenheiro
    LOCATÁRIO: Maria Santos, brasileira, solteira, professora
    
    CLÁUSULA 1ª - DO OBJETO
    O presente contrato tem por objeto a locação do imóvel situado na Rua das Flores, 123.
    
    CLÁUSULA 2ª - DO PRAZO
    O prazo de locação é de 12 (doze) meses, iniciando em 01/01/2024.
    
    CLÁUSULA 3ª - DO VALOR
    O valor mensal da locação é de R$ 1.500,00 (mil e quinhentos reais).
    
    CLÁUSULA 4ª - DO REAJUSTE
    O valor será reajustado anualmente pelo IGPM.
    
    CLÁUSULA 5ª - DAS OBRIGAÇÕES
    O locatário se obriga a pagar pontualmente o aluguel.
    
    CLÁUSULA 6ª - DO FORO
    Fica eleito o foro da Comarca de São Paulo para dirimir questões.
    """

@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "name": "Teste User",
        "email": "teste@exemplo.com",
        "password": "senha123"
    }

@pytest.fixture
def mock_claude_response():
    """Mock response from Claude API."""
    return {
        "content": [
            {
                "text": """
                {
                    "contract_type": "locacao",
                    "risk_level": "medium",
                    "summary": "Contrato de locação residencial com algumas cláusulas que requerem atenção.",
                    "key_findings": [
                        "Prazo definido de 12 meses",
                        "Valor de aluguel dentro da média de mercado",
                        "Reajuste pelo IGPM"
                    ],
                    "risk_factors": [
                        {
                            "type": "reajuste",
                            "severity": "medium",
                            "description": "Reajuste pelo IGPM pode ser volátil"
                        }
                    ],
                    "recommendations": [
                        "Considere negociar teto para reajuste",
                        "Verifique condições de rescisão antecipada"
                    ],
                    "confidence_score": 0.85
                }
                """
            }
        ]
    }

class MockClaudeClient:
    """Mock Claude client for testing."""
    
    def __init__(self, response_data=None):
        self.response_data = response_data or {}
    
    async def messages_create(self, **kwargs):
        """Mock message creation."""
        from unittest.mock import MagicMock
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(text=self.response_data.get("text", "Mock response"))
        ]
        return mock_response

@pytest.fixture
def mock_claude_client(mock_claude_response):
    """Provide mock Claude client."""
    return MockClaudeClient({"text": mock_claude_response["content"][0]["text"]})

@pytest.fixture
def mock_rag_service():
    """Mock RAG service for testing."""
    class MockRAGService:
        async def get_relevant_context(self, query: str) -> str:
            return "Contexto jurídico relevante para teste"
        
        async def add_document(self, content: str, metadata: dict):
            return {"status": "success", "id": "test-doc-123"}
    
    return MockRAGService()