"""
Democratiza AI - Demonstração do Sistema RAG
Simula consultas inteligentes na base de conhecimento jurídico
"""

import json
import asyncio
from typing import List, Dict, Any
from dataclasses import dataclass
import random

@dataclass
class DocumentResult:
    """Representa um resultado de busca na base de conhecimento"""
    content: str
    metadata: Dict[str, Any]
    similarity: float
    source: str
    category: str

class MockRAGDemo:
    """Demonstração do sistema RAG com a base de conhecimento populada"""
    
    def __init__(self):
        # Carregar estatísticas da base
        try:
            with open('base_knowledge_stats.json', 'r', encoding='utf-8') as f:
                self.stats = json.load(f)
        except:
            self.stats = {"total_documents": 20, "status": "populated"}
    
    def simulate_search(self, query: str, category: str = None) -> List[DocumentResult]:
        """Simula busca semântica na base de conhecimento"""
        
        # Documentos simulados baseados na base real
        mock_results = {
            "cláusulas abusivas": [
                DocumentResult(
                    content="Art. 51. São nulas de pleno direito as cláusulas contratuais que estabeleçam obrigações consideradas iníquas, abusivas, que coloquem o consumidor em desvantagem exagerada...",
                    metadata={"source": "CDC", "article": "51", "risk_level": "alto"},
                    similarity=0.95,
                    source="CDC Art. 51",
                    category="consumer_protection"
                ),
                DocumentResult(
                    content="São consideradas leoninas ou abusivas as cláusulas que estabelecem vantagem exagerada para uma das partes ou violam o princípio da boa-fé objetiva...",
                    metadata={"source": "Doutrina", "concept": "clausulas_abusivas", "risk_level": "alto"},
                    similarity=0.88,
                    source="Doutrina Jurídica",
                    category="general_principles"
                )
            ],
            
            "locação aluguel": [
                DocumentResult(
                    content="Art. 22. O locador é obrigado a: I - entregar ao locatário o imóvel alugado em estado de servir ao uso a que se destina; II - garantir o uso pacífico do imóvel...",
                    metadata={"source": "Lei_8245", "article": "22", "risk_level": "medio"},
                    similarity=0.92,
                    source="Lei 8.245/91 Art. 22",
                    category="rental_law"
                ),
                DocumentResult(
                    content="É vedada, sob pena de nulidade, mais de uma das modalidades de garantia num mesmo contrato de locação...",
                    metadata={"source": "Lei_8245", "article": "9", "risk_level": "alto"},
                    similarity=0.85,
                    source="Lei 8.245/91 Art. 9º",
                    category="rental_law"
                )
            ],
            
            "previdência privada": [
                DocumentResult(
                    content="TAXA DE ADMINISTRAÇÃO: Limite máximo de 3% ao ano sobre o patrimônio. TAXA DE CARREGAMENTO: Máximo de 10% sobre aportes regulares...",
                    metadata={"source": "SUSEP", "regulation": "CNSP", "risk_level": "alto"},
                    similarity=0.90,
                    source="SUSEP - Regulamentação",
                    category="retirement_pension"
                ),
                DocumentResult(
                    content="O regime de previdência complementar é operado por entidades que têm por objetivo instituir planos de benefícios. MODALIDADES: PGBL e VGBL...",
                    metadata={"source": "Lei_Complementar", "law": "109/01", "risk_level": "medio"},
                    similarity=0.87,
                    source="Lei Complementar 109/01",
                    category="retirement_pension"
                )
            ],
            
            "telecomunicações internet": [
                DocumentResult(
                    content="O acesso à internet é essencial ao exercício da cidadania. São direitos: inviolabilidade da intimidade, não suspensão da conexão, manutenção da qualidade...",
                    metadata={"source": "Marco_Civil", "article": "7", "risk_level": "alto"},
                    similarity=0.93,
                    source="Marco Civil Art. 7º",
                    category="telecommunications"
                ),
                DocumentResult(
                    content="Os usuários têm direito a informações claras sobre planos, qualidade dos serviços, facilidades para cancelamento e ressarcimento por falhas...",
                    metadata={"source": "Anatel", "regulation": "RGC", "risk_level": "alto"},
                    similarity=0.86,
                    source="Anatel - RGC",
                    category="telecommunications"
                )
            ]
        }
        
        # Buscar documentos relevantes baseados na query
        query_lower = query.lower()
        results = []
        
        for key_terms, docs in mock_results.items():
            if any(term in query_lower for term in key_terms.split()):
                results.extend(docs)
        
        # Filtrar por categoria se especificado
        if category:
            results = [r for r in results if r.category == category]
        
        # Ordenar por similaridade
        results.sort(key=lambda x: x.similarity, reverse=True)
        
        return results[:3]  # Top 3 resultados

class ContractAnalysisDemo:
    """Demonstração de análise de contratos usando o conhecimento jurídico"""
    
    def __init__(self):
        self.rag_demo = MockRAGDemo()
    
    def analyze_contract_sample(self, contract_type: str, contract_excerpt: str) -> Dict[str, Any]:
        """Simula análise completa de um contrato"""
        
        # Buscar conhecimento relevante
        relevant_knowledge = self.rag_demo.simulate_search(contract_type)
        
        # Simulação da análise (normalmente seria feita pela API do Claude)
        analysis_results = {
            "rental": {
                "overall_risk": "MÉDIO",
                "risk_score": 65,
                "key_issues": [
                    "Múltiplas garantias no mesmo contrato (vedado por lei)",
                    "Falta de descrição detalhada do estado do imóvel",
                    "Prazo de pagamento em desacordo com lei"
                ],
                "positive_aspects": [
                    "Obrigações do locador claramente definidas",
                    "Respeita prazo legal para entrega"
                ],
                "legal_references": [
                    "Lei 8.245/91 Art. 9º - Garantias locatícias",
                    "Lei 8.245/91 Art. 22 - Obrigações do locador"
                ],
                "recommendations": [
                    "Escolher apenas uma modalidade de garantia",
                    "Exigir vistoria detalhada antes da assinatura",
                    "Verificar prazo de pagamento conforme lei"
                ]
            },
            
            "previdencia": {
                "overall_risk": "ALTO", 
                "risk_score": 80,
                "key_issues": [
                    "Taxa de administração acima do limite (3.5% vs 3% máximo)",
                    "Taxa de carregamento excessiva (12% vs 10% máximo)",
                    "Cláusula de alteração unilateral de condições"
                ],
                "positive_aspects": [
                    "Transparência nas informações básicas",
                    "Portabilidade permitida"
                ],
                "legal_references": [
                    "SUSEP - Limite de taxas de administração",
                    "Lei Complementar 109/01 - Previdência complementar"
                ],
                "recommendations": [
                    "Negociar redução da taxa de administração",
                    "Buscar planos com menores custos",
                    "Verificar alternativas no mercado"
                ]
            },
            
            "telecom": {
                "overall_risk": "ALTO",
                "risk_score": 85,
                "key_issues": [
                    "Cobrança por serviços não solicitados",
                    "Falta de transparência nos custos adicionais", 
                    "Dificuldades impostas para cancelamento"
                ],
                "positive_aspects": [
                    "Qualidade do serviço dentro dos padrões",
                    "Canais de atendimento disponíveis"
                ],
                "legal_references": [
                    "Marco Civil Art. 7º - Direitos dos usuários",
                    "Anatel - Regulamento Geral de Direitos do Consumidor"
                ],
                "recommendations": [
                    "Questionar serviços não solicitados",
                    "Exigir transparência total nos custos",
                    "Conhecer direitos de cancelamento"
                ]
            }
        }
        
        return analysis_results.get(contract_type, {
            "overall_risk": "MÉDIO",
            "risk_score": 50,
            "message": f"Análise para {contract_type} ainda em desenvolvimento"
        })

async def run_demo():
    """Executa demonstração completa do sistema"""
    
    print("🤖 DEMOCRATIZA AI - DEMONSTRAÇÃO DO SISTEMA RAG")
    print("=" * 60)
    
    # Inicializar demonstração
    rag_demo = MockRAGDemo()
    analyzer = ContractAnalysisDemo()
    
    print(f"📊 Base de Conhecimento: {rag_demo.stats['total_documents']} documentos")
    print(f"📅 Status: {rag_demo.stats['status']}")
    
    # Demonstrar consultas RAG
    print(f"\n🔍 DEMONSTRAÇÃO DE CONSULTAS INTELIGENTES")
    print("-" * 50)
    
    test_queries = [
        "cláusulas abusivas em contratos",
        "obrigações em contratos de locação", 
        "taxas em previdência privada",
        "direitos em telecomunicações"
    ]
    
    for query in test_queries:
        print(f"\n📝 Consulta: '{query}'")
        results = rag_demo.simulate_search(query)
        
        if results:
            print(f"   ✅ {len(results)} documentos encontrados:")
            for i, result in enumerate(results, 1):
                print(f"      {i}. {result.source} (Relevância: {result.similarity:.0%})")
                print(f"         Categoria: {result.category}")
                print(f"         Preview: {result.content[:100]}...")
        else:
            print("   ❌ Nenhum documento encontrado")
    
    # Demonstrar análises de contratos
    print(f"\n🔍 DEMONSTRAÇÃO DE ANÁLISE DE CONTRATOS")
    print("-" * 50)
    
    contract_samples = [
        ("rental", "Contrato de locação com fiança + caução + seguro"),
        ("previdencia", "Contrato PGBL com taxa de administração 3.5%"),
        ("telecom", "Contrato de internet com serviços adicionais")
    ]
    
    for contract_type, description in contract_samples:
        print(f"\n📄 Analisando: {description}")
        analysis = analyzer.analyze_contract_sample(contract_type, description)
        
        print(f"   🎯 Risco Geral: {analysis.get('overall_risk', 'N/A')}")
        print(f"   📊 Score: {analysis.get('risk_score', 0)}/100")
        
        if 'key_issues' in analysis:
            print(f"   ⚠️  Principais Riscos:")
            for issue in analysis['key_issues'][:2]:
                print(f"      - {issue}")
        
        if 'recommendations' in analysis:
            print(f"   💡 Recomendações:")
            for rec in analysis['recommendations'][:2]:
                print(f"      - {rec}")
    
    print(f"\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print(f"💬 O sistema está pronto para:")
    print(f"   - Análise inteligente de contratos brasileiros")
    print(f"   - Identificação automática de cláusulas abusivas")
    print(f"   - Orientações jurídicas baseadas em legislação real")
    print(f"   - Suporte especializado por tipo de contrato")
    
    print(f"\n🔑 Próximo passo: Configurar API do Anthropic Claude para ativação completa!")

if __name__ == "__main__":
    asyncio.run(run_demo())