"""
Servidor simplificado para demonstração sem dependências complexas
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

def get_agent_response(question: str, agent_type: str = "general") -> dict:
    """Gerar resposta baseada no tipo de agente e pergunta"""
    
    # Agente de Locação (Rental)
    if agent_type == "rental":
        if "rescisão" in question.lower() or "cancelar" in question.lower():
            return {
                "response": "🏠 **LOCAÇÃO - Rescisão**: Em contratos de locação, há diferentes modalidades: **Rescisão imotivada** (com aviso prévio de 30 dias para inquilino, 90 para locador), **Rescisão por descumprimento** (sem aviso), **Cláusula de arrependimento** (primeiros 3 anos). 📋 **Multa**: Geralmente 3 aluguéis se rescindido pelo locador antes do prazo.",
                "agent": "Agente de Locação",
                "specialization": "Contratos Imobiliários"
            }
        elif "reforma" in question.lower() or "benfeitoria" in question.lower():
            return {
                "response": "🔨 **LOCAÇÃO - Reformas**: **Benfeitorias necessárias** (locador paga), **Úteis** (acordo entre partes), **Voluptuárias** (inquilino não tem direito a indenização). ⚠️ **Importante**: Sempre comunicar por escrito e obter autorização prévia do locador.",
                "agent": "Agente de Locação",
                "specialization": "Contratos Imobiliários"
            }
        else:
            return {
                "response": f"🏠 **AGENTE DE LOCAÇÃO**: Analisando sua pergunta sobre '{question}'. Sou especializado em **contratos de aluguel**, **direitos do inquilino/locador**, **IPTU**, **reformas**, **rescisão** e **reajustes**. Como posso ajudá-lo especificamente?",
                "agent": "Agente de Locação",
                "specialization": "Contratos Imobiliários"
            }
    
    # Agente Financeiro
    elif agent_type == "financial":
        if "juros" in question.lower() or "taxa" in question.lower():
            return {
                "response": "💰 **FINANCEIRO - Juros**: **CDC**: Juros máx. 2% ao mês + multa 2%. **Cartão de Crédito**: Rotativo máx. 15% ao mês (Bacen). **Financiamentos**: CET deve incluir todas as taxas. 🚨 **Abusivo**: Juros superiores aos limites legais ou taxas não discriminadas.",
                "agent": "Agente Financeiro", 
                "specialization": "Contratos Bancários e Financeiros"
            }
        elif "cdc" in question.lower() or "consumidor" in question.lower():
            return {
                "response": "⚖️ **CDC - Direitos**: **Direito de arrependimento** (7 dias), **Informação clara** sobre taxas, **Revisão de cláusulas abusivas**, **Renegociação de dívidas**. 📞 **Canais**: Procon, Bacen, Justiça Gratuita para revisão contratual.",
                "agent": "Agente Financeiro",
                "specialization": "Contratos Bancários e Financeiros"
            }
        else:
            return {
                "response": f"💰 **AGENTE FINANCEIRO**: Analisando '{question}'. Especializo-me em **empréstimos**, **financiamentos**, **cartões de crédito**, **seguros**, **CDC** e **revisão de contratos bancários**. Qual aspecto específico posso esclarecer?",
                "agent": "Agente Financeiro",
                "specialization": "Contratos Bancários e Financeiros"
            }
    
    # Agente de Telecomunicações
    elif agent_type == "telecom":
        if "cancelar" in question.lower() or "cancelamento" in question.lower():
            return {
                "response": "� **TELECOM - Cancelamento**: **Direito livre** após 12 meses de fidelidade. **Antes da fidelidade**: Multa proporcional ao período restante. **Serviços adicionais**: Cancelamento imediato sem multa. 📞 **Como**: Call center, chat, presencial ou anatel.gov.br.",
                "agent": "Agente de Telecomunicações",
                "specialization": "Contratos de Telefonia e Internet"
            }
        elif "velocidade" in question.lower() or "internet" in question.lower():
            return {
                "response": "🌐 **INTERNET - Velocidade**: **Mínimo garantido**: 40% da velocidade contratada via cabo, 20% via rádio. **Teste oficial**: anatel.gov.br/brasilbandalarga. **Não cumpre**: Desconto na fatura ou rescisão sem multa. � **Medição**: Faça testes em horários diversos.",
                "agent": "Agente de Telecomunicações", 
                "specialization": "Contratos de Telefonia e Internet"
            }
        else:
            return {
                "response": f"📱 **AGENTE TELECOM**: Analisando '{question}'. Sou expert em **planos de celular**, **internet banda larga**, **TV por assinatura**, **fidelidade**, **velocidade** e **Anatel**. Que aspecto posso esclarecer?",
                "agent": "Agente de Telecomunicações",
                "specialization": "Contratos de Telefonia e Internet"
            }
    
    # Agente Geral (default)
    else:
        if "rescisão" in question.lower():
            return {
                "response": "🏛️ **Cláusula de Rescisão**: Define condições para encerramento antecipado. **Elementos**: Prazo de aviso, multas, devolução de valores, estado de entrega. ⚖️ **Tipos**: Rescisão imotivada, por descumprimento, ou consensual. Varia por tipo de contrato.",
                "agent": "Assistente Jurídico Geral",
                "specialization": "Análise Geral de Contratos"
            }
        elif "pagamento" in question.lower():
            return {
                "response": "💰 **Condições de Pagamento**: **Vencimento**, **forma** (débito, boleto, PIX), **multa por atraso** (máx. 2%), **juros de mora** (máx. 1% ao mês), **desconto por antecipação**. � **Verificar**: Taxas abusivas ou não discriminadas.",
                "agent": "Assistente Jurídico Geral", 
                "specialization": "Análise Geral de Contratos"
            }
        elif "olá" in question.lower() or "oi" in question.lower():
            return {
                "response": "👋 Olá! Sou seu assistente jurídico. Posso **analisar contratos**, **explicar cláusulas**, **identificar riscos** e **sugerir melhorias**. Para atendimento especializado, especifique: **Locação** 🏠, **Financeiro** 💰, ou **Telecom** 📱. Como posso ajudar?",
                "agent": "Assistente Jurídico Geral",
                "specialization": "Análise Geral de Contratos"
            }
        else:
            return {
                "response": f"🤖 **Pergunta**: '{question}'. Como assistente jurídico, analiso **contratos**, **cláusulas**, **riscos** e **direitos**. Para resposta especializada, especifique o tipo: 🏠**Locação**, 💰**Financeiro**, 📱**Telecom**. Quer que eu classifique automaticamente?",
                "agent": "Assistente Jurídico Geral",
                "specialization": "Análise Geral de Contratos"  
            }

@app.get("/api/v1/demo/chat")
async def demo_chat_get(question: str = "", agent_type: str = "general", contract_id: str = ""):
    """Chat com agentes especializados via GET"""
    
    if not question:
        return {"error": "Pergunta é obrigatória"}
    
    # Gerar resposta baseada no agente
    agent_response = get_agent_response(question, agent_type)
    
    return {
        "message": agent_response["response"],
        "response": agent_response["response"],
        "question": question,
        "agent": agent_response["agent"],
        "specialization": agent_response["specialization"],
        "agent_type": agent_type,
        "contract_id": contract_id,
        "context": "Resposta gerada por agente especializado"
    }

@app.get("/api/v1/demo/classify-contract")
async def classify_contract(text: str = "", contract_type: str = ""):
    """Classificar tipo de contrato baseado no texto"""
    
    if not text and not contract_type:
        return {"error": "Texto ou tipo de contrato é obrigatório"}
    
    # Se tipo foi fornecido diretamente
    if contract_type:
        agent_type = contract_type
    else:
        # Classificação automática baseada em palavras-chave
        text_lower = text.lower()
        if any(word in text_lower for word in ["aluguel", "locação", "inquilino", "locador", "imóvel"]):
            agent_type = "rental"
        elif any(word in text_lower for word in ["empréstimo", "financiamento", "juros", "banco", "crédito", "cdc"]):
            agent_type = "financial"
        elif any(word in text_lower for word in ["telefone", "internet", "celular", "banda larga", "telecom", "anatel"]):
            agent_type = "telecom"
        else:
            agent_type = "general"
    
    # Mapear tipos para informações do agente
    agent_info = {
        "rental": {
            "name": "Agente de Locação",
            "icon": "🏠",
            "description": "Especialista em contratos imobiliários, locação e direitos do inquilino/locador",
            "areas": ["Aluguel", "IPTU", "Reformas", "Rescisão", "Reajustes"]
        },
        "financial": {
            "name": "Agente Financeiro", 
            "icon": "💰",
            "description": "Expert em contratos bancários, empréstimos e direito do consumidor",
            "areas": ["Empréstimos", "Cartão de Crédito", "CDC", "Juros", "Seguros"]
        },
        "telecom": {
            "name": "Agente de Telecomunicações",
            "icon": "📱", 
            "description": "Especialista em contratos de telefonia, internet e TV por assinatura",
            "areas": ["Celular", "Internet", "TV", "Fidelidade", "Anatel"]
        },
        "general": {
            "name": "Assistente Jurídico Geral",
            "icon": "🤖",
            "description": "Análise geral de contratos e orientação jurídica básica", 
            "areas": ["Contratos", "Cláusulas", "Riscos", "Direitos"]
        }
    }
    
    return {
        "agent_type": agent_type,
        "agent_info": agent_info[agent_type],
        "classification_method": "automatic" if not contract_type else "manual",
        "text_analyzed": bool(text)
    }

@app.get("/api/v1/demo/agents")
async def get_available_agents():
    """Listar agentes especializados disponíveis"""
    
    agents = {
        "general": {
            "name": "Assistente Jurídico Geral",
            "icon": "🤖",
            "description": "Análise geral de contratos e orientação jurídica básica",
            "areas": ["Contratos", "Cláusulas", "Riscos", "Direitos"],
            "color": "blue"
        },
        "rental": {
            "name": "Agente de Locação", 
            "icon": "🏠",
            "description": "Especialista em contratos imobiliários e direitos locatários",
            "areas": ["Aluguel", "IPTU", "Reformas", "Rescisão", "Reajustes"],
            "color": "green"
        },
        "financial": {
            "name": "Agente Financeiro",
            "icon": "💰", 
            "description": "Expert em contratos bancários e direito do consumidor",
            "areas": ["Empréstimos", "Cartão", "CDC", "Juros", "Seguros"],
            "color": "yellow"
        },
        "telecom": {
            "name": "Agente de Telecomunicações",
            "icon": "📱",
            "description": "Especialista em telefonia, internet e regulamentação Anatel",
            "areas": ["Celular", "Internet", "TV", "Fidelidade", "Cancelamento"],
            "color": "purple"
        }
    }
    
    return {"agents": agents}

@app.post("/api/v1/demo/chat")  
async def demo_chat_post():
    """Chat POST - simplificado por enquanto"""
    from fastapi import Request
    
    return {
        "message": "🤖 Olá! Sou seu assistente jurídico. Como posso ajudá-lo hoje?",
        "response": "🤖 Olá! Sou seu assistente jurídico. Como posso ajudá-lo hoje?",
        "question": "teste",
        "context": "Chat POST funcionando"
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