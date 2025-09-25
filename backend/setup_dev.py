"""
Bootstrap simplificado para ambiente de desenvolvimento
Inicializa sistema sem dependências externas
"""
import os
import sys
import asyncio
from pathlib import Path

# Adiciona o path do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.mock_rag_service import mock_rag_service
from app.services.mock_llm_service import mock_llm_service

async def setup_development_environment():
    """Configura ambiente de desenvolvimento"""
    print("🚀 Inicializando Democratiza AI - Ambiente de Desenvolvimento")
    print("=" * 60)
    
    # 1. Criar diretórios necessários
    print("📁 Criando diretórios...")
    directories = [
        "uploads",
        "data",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    # 2. Verificar serviços mock
    print("\n🧪 Verificando serviços mock...")
    
    # Testar RAG Service mock
    try:
        test_query = "cláusulas abusivas em contratos"
        results = await mock_rag_service.search_similar_content(test_query)
        print(f"   ✅ RAG Service Mock: {len(results)} documentos encontrados")
    except Exception as e:
        print(f"   ❌ Erro no RAG Service Mock: {e}")
        return False
    
    # Testar LLM Service mock
    try:
        test_contract = """
        CONTRATO DE LOCAÇÃO
        
        O LOCADOR se exime de qualquer responsabilidade por danos ao imóvel.
        Em caso de atraso no pagamento, será aplicada multa de 50% sobre o valor do aluguel.
        O contrato não pode ser cancelado pelo locatário sob nenhuma hipótese.
        """
        
        analysis = await mock_llm_service.analyze_contract(test_contract)
        print(f"   ✅ LLM Service Mock: Análise gerada (Risco: {analysis['risk_level']})")
    except Exception as e:
        print(f"   ❌ Erro no LLM Service Mock: {e}")
        return False
    
    # 3. Verificar base de conhecimento
    print("\n📚 Verificando base de conhecimento jurídico...")
    knowledge_stats = {
        "Total de documentos": len(mock_rag_service.knowledge_base),
        "Categorias": len(set(doc["category"] for doc in mock_rag_service.knowledge_base)),
        "Leis incluídas": [doc["id"] for doc in mock_rag_service.knowledge_base]
    }
    
    for key, value in knowledge_stats.items():
        print(f"   📋 {key}: {value}")
    
    # 4. Demonstrar funcionalidades
    print("\n🎯 Demonstrando funcionalidades...")
    
    # Busca por diferentes tipos de contratos
    test_cases = [
        ("Contratos de locação", "aluguel garantias fiança"),
        ("Contratos de telecom", "internet velocidade cancelamento"),
        ("Proteção do consumidor", "cláusulas abusivas CDC")
    ]
    
    for description, query in test_cases:
        results = await mock_rag_service.search_similar_content(query, limit=2)
        print(f"   🔍 {description}: {len(results)} resultados relevantes")
        if results:
            print(f"      📖 Exemplo: {results[0]['title']}")
    
    # 5. Testar análise completa
    print("\n🔍 Testando análise completa de contrato...")
    
    sample_contracts = {
        "Locação problemática": """
        CONTRATO DE LOCAÇÃO RESIDENCIAL
        
        Cláusula 5: O LOCADOR não se responsabiliza por qualquer dano causado ao imóvel.
        Cláusula 8: Em caso de atraso no pagamento, será aplicada multa de 20% sobre o valor do aluguel.
        Cláusula 12: O presente contrato é irrevogável e irretratável.
        
        Valor do aluguel: R$ 2.500,00
        Prazo: 30 meses
        """,
        
        "Telecom com problemas": """
        CONTRATO DE INTERNET BANDA LARGA
        
        Velocidade: Até 100 Mbps (não garantida)
        Permanência mínima: 24 meses
        Multa por cancelamento: R$ 1.500,00
        
        A empresa não se responsabiliza por oscilações na velocidade.
        Renovação automática por igual período.
        """
    }
    
    for contract_name, contract_text in sample_contracts.items():
        print(f"\n   📄 Analisando: {contract_name}")
        analysis = await mock_llm_service.analyze_contract(contract_text)
        
        print(f"      🎯 Tipo: {analysis['contract_type']}")
        print(f"      ⚠️  Risco: {analysis['risk_level']}")
        print(f"      🔴 Riscos altos: {len(analysis['risk_analysis']['high'])}")
        print(f"      🟡 Riscos médios: {len(analysis['risk_analysis']['medium'])}")
        
        if analysis['recommendations']:
            print(f"      💡 Recomendação: {analysis['recommendations'][0][:80]}...")
    
    print("\n" + "=" * 60)
    print("✅ Ambiente de desenvolvimento configurado com sucesso!")
    print("\n🎯 Próximos passos:")
    print("   1. Inicie o backend: uvicorn app.main:app --reload")
    print("   2. Inicie o frontend: cd frontend && npm run dev")
    print("   3. Acesse: http://localhost:3000")
    
    print("\n🧪 Funcionalidades disponíveis:")
    print("   • Análise automática de contratos")
    print("   • Base jurídica com leis brasileiras")
    print("   • Chat interativo sobre contratos")
    print("   • Upload e processamento de documentos")
    print("   • Tudo funcionando offline!")
    
    return True

def create_env_file():
    """Cria arquivo .env básico para desenvolvimento"""
    env_content = """# Arquivo de configuração para desenvolvimento
# Não são necessárias chaves de APIs externas

DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///./contracts_dev.db

# Flags para usar serviços mock
USE_MOCK_RAG=True
USE_MOCK_OCR=True
USE_MOCK_LLM=True
USE_MOCK_SIGNATURES=True

# Configurações locais
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=52428800
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("📝 Arquivo .env criado com configurações de desenvolvimento")

async def main():
    """Função principal do bootstrap"""
    print("🔧 Configurando ambiente de desenvolvimento...")
    
    # Criar arquivo .env se não existir
    if not os.path.exists(".env"):
        create_env_file()
    
    # Executar setup
    success = await setup_development_environment()
    
    if success:
        print(f"\n🎉 Sistema pronto para desenvolvimento!")
        print("   Todos os serviços estão funcionando em modo simulado.")
        print("   Não há custos de APIs externas.")
        
        # Perguntar se deve iniciar os serviços
        response = input("\n🚀 Deseja iniciar o servidor de desenvolvimento agora? (s/n): ")
        if response.lower() in ['s', 'sim', 'y', 'yes']:
            print("\n🔄 Iniciando servidor...")
            print("💡 Use Ctrl+C para parar o servidor")
            os.system("uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ Erro na configuração. Verifique os logs acima.")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Setup interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)