"""
Servidor principal com suporte a modo de desenvolvimento
Detecta automaticamente se deve usar mocks ou APIs reais
"""
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Detectar modo de desenvolvimento
USE_DEV_MODE = os.getenv("USE_MOCK_RAG", "False").lower() == "true" or not os.getenv("OPENAI_API_KEY")

if USE_DEV_MODE:
    print("🧪 Iniciando em MODO DE DESENVOLVIMENTO (Mocks ativados)")
    # Usar configuração de desenvolvimento
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from app.core.dev_config import dev_settings as settings
else:
    print("🚀 Iniciando em MODO DE PRODUÇÃO (APIs reais)")
    from app.core.config import settings

# Importar routers (criar versões simplificadas se necessário)
from app.api.v1 import auth

app = FastAPI(
    title="Contrato Seguro API" + (" - DEV" if USE_DEV_MODE else ""),
    description="API para análise inteligente de contratos brasileiros",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers básicos sempre disponíveis
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])

# Adicionar routers específicos conforme disponibilidade
try:
    from app.api.v1 import contracts
    app.include_router(contracts.router, prefix="/api/v1/contracts", tags=["contracts"])
except ImportError as e:
    print(f"⚠️  Router contracts não disponível: {e}")

try:
    from app.api.v1 import chat
    app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
except ImportError as e:
    print(f"⚠️  Router chat não disponível: {e}")

# Endpoints básicos
@app.get("/")
async def root():
    return {
        "message": "Contrato Seguro API",
        "version": "1.0.0",
        "status": "active",
        "mode": "development" if USE_DEV_MODE else "production",
        "features": {
            "mock_rag": USE_DEV_MODE,
            "mock_llm": USE_DEV_MODE,
            "mock_ocr": USE_DEV_MODE
        }
    }

@app.get("/health")
async def health_check():
    checks = {
        "status": "healthy",
        "mode": "development" if USE_DEV_MODE else "production"
    }
    
    if USE_DEV_MODE:
        # Verificar serviços mock
        try:
            from app.services.mock_rag_service import mock_rag_service
            from app.services.mock_llm_service import mock_llm_service
            
            # Teste rápido dos serviços
            test_result = await mock_rag_service.search_similar_content("teste", limit=1)
            checks["rag_service"] = "ok" if test_result else "warning"
            checks["llm_service"] = "ok"
            
        except Exception as e:
            checks["error"] = str(e)
            checks["status"] = "degraded"
    
    return checks

@app.get("/api/v1/demo/analyze")
async def demo_analyze():
    """Endpoint de demonstração para análise de contratos"""
    if not USE_DEV_MODE:
        raise HTTPException(
            status_code=404, 
            detail="Demo endpoint only available in development mode"
        )
    
    from app.services.mock_llm_service import mock_llm_service
    
    sample_contract = """
    CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE INTERNET
    
    Cláusula 1: A velocidade de internet é de até 100 Mbps, não sendo garantida.
    Cláusula 2: O contrato tem permanência mínima de 24 meses.
    Cláusula 3: Em caso de cancelamento antecipado, será cobrada multa de R$ 2.000,00.
    Cláusula 4: A empresa não se responsabiliza por instabilidades na conexão.
    Cláusula 5: O reajuste será feito anualmente conforme IGP-M.
    """
    
    analysis = await mock_llm_service.analyze_contract(sample_contract)
    
    return {
        "message": "Demonstração de análise de contrato",
        "contract_sample": sample_contract,
        "analysis": analysis
    }

@app.get("/api/v1/demo/search")
async def demo_search(query: str = "cláusulas abusivas"):
    """Endpoint de demonstração para busca na base jurídica"""
    if not USE_DEV_MODE:
        raise HTTPException(
            status_code=404, 
            detail="Demo endpoint only available in development mode"
        )
    
    from app.services.mock_rag_service import mock_rag_service
    
    results = await mock_rag_service.search_similar_content(query, limit=3)
    
    return {
        "message": "Demonstração de busca na base jurídica",
        "query": query,
        "results": results,
        "total_found": len(results)
    }

if __name__ == "__main__":
    import uvicorn
    
    print(f"\n{'='*60}")
    print(f"🚀 Democratiza AI - Contrato Seguro")
    print(f"{'='*60}")
    print(f"Modo: {'Desenvolvimento (Mock)' if USE_DEV_MODE else 'Produção (APIs Reais)'}")
    print(f"Documentação: http://localhost:8000/docs")
    if USE_DEV_MODE:
        print(f"Demo Análise: http://localhost:8000/api/v1/demo/analyze")
        print(f"Demo Busca: http://localhost:8000/api/v1/demo/search?query=locacao")
    print(f"{'='*60}\n")
    
    uvicorn.run(
        "dev_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )