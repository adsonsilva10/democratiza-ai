"""
Servidor simplificado para demonstração sem dependências complexas
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configurar variável de ambiente para usar mocks
os.environ["USE_MOCK_RAG"] = "True"

app = FastAPI(
    title="Contrato Seguro API - Demo",
    description="API demo para análise inteligente de contratos brasileiros",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Contrato Seguro API - Demonstração",
        "version": "1.0.0",
        "status": "active",
        "mode": "development",
        "features": {
            "mock_rag": True,
            "mock_llm": True,
            "mock_ocr": True,
            "demo_endpoints": True
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "development"}

@app.get("/api/v1/demo/analyze")
async def demo_analyze():
    """Endpoint de demonstração para análise de contratos"""
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
    from app.services.mock_rag_service import mock_rag_service
    
    results = await mock_rag_service.search_similar_content(query, limit=3)
    
    return {
        "message": "Demonstração de busca na base jurídica",
        "query": query,
        "results": results,
        "total_found": len(results)
    }

@app.post("/api/v1/demo/analyze-text")
async def demo_analyze_text(contract_data: dict):
    """Analisa texto de contrato enviado pelo usuário"""
    from app.services.mock_llm_service import mock_llm_service
    
    contract_text = contract_data.get("text", "")
    contract_type = contract_data.get("type", None)
    
    if not contract_text:
        return {"error": "Texto do contrato é obrigatório"}
    
    analysis = await mock_llm_service.analyze_contract(contract_text, contract_type)
    
    return {
        "message": "Análise concluída",
        "input_text": contract_text[:200] + "..." if len(contract_text) > 200 else contract_text,
        "analysis": analysis
    }

@app.post("/api/v1/demo/chat")
async def demo_chat(chat_data: dict):
    """Chat sobre análise de contrato"""
    from app.services.mock_llm_service import mock_llm_service
    
    contract_analysis = chat_data.get("contract_analysis", {})
    user_question = chat_data.get("question", "")
    
    if not user_question:
        return {"error": "Pergunta é obrigatória"}
    
    response = await mock_llm_service.chat_with_contract(contract_analysis, user_question)
    
    return {
        "question": user_question,
        "response": response,
        "context": "Esta é uma resposta automatizada baseada na análise do contrato"
    }

if __name__ == "__main__":
    import uvicorn
    
    print(f"\n{'='*60}")
    print(f"🚀 Democratiza AI - Contrato Seguro DEMO")
    print(f"{'='*60}")
    print(f"Modo: Desenvolvimento (Mock)")
    print(f"Documentação: http://localhost:8000/docs")
    print(f"Demo Análise: http://localhost:8000/api/v1/demo/analyze")
    print(f"Demo Busca: http://localhost:8000/api/v1/demo/search?query=locacao")
    print(f"{'='*60}\n")
    
    uvicorn.run(
        "simple_demo:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )