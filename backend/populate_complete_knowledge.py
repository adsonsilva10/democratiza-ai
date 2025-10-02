"""
Democratiza AI - Populador da Base de Conhecimento Jurídico
Sistema completo de população da base de conhecimento jurídico brasileiro
"""

import asyncio
import json
from typing import List, Dict, Any
from pathlib import Path
import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Simulação dos serviços (já que ainda não temos a API do Claude configurada)
class MockRAGService:
    """Mock do RAG Service para popular a base de dados"""
    
    def __init__(self):
        self.documents = []
        
    async def add_document(self, content: str, metadata: Dict):
        """Adiciona documento à base (simulado)"""
        doc_id = len(self.documents) + 1
        document = {
            "id": doc_id,
            "content": content,
            "metadata": metadata,
            "created_at": "2025-10-02"
        }
        self.documents.append(document)
        print(f"  📄 Documento adicionado: {metadata.get('source', 'N/A')} - {metadata.get('article', '')}")
        return doc_id

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalKnowledgePopulator:
    """
    Populador da base de conhecimento jurídico brasileiro
    Foca no 'hiato pré-judicial' - conhecimento preventivo
    """
    
    def __init__(self):
        self.rag_service = MockRAGService()
    
    async def populate_all_knowledge(self):
        """População completa da base de conhecimento"""
        
        logger.info("🏛️ Iniciando população da base de conhecimento jurídico...")
        
        knowledge_sets = [
            self.get_cdc_knowledge(),           # Código de Defesa do Consumidor
            self.get_rental_law_knowledge(),    # Lei do Inquilinato
            self.get_civil_code_knowledge(),    # Código Civil - Contratos
            self.get_telecom_knowledge(),       # Marco Civil Internet + Anatel
            self.get_financial_knowledge(),     # Regulamentação financeira
            self.get_labor_knowledge(),         # CLT - Trabalho
            self.get_general_contract_law(),    # Direito contratual geral
            self.get_retirement_knowledge(),    # Aposentadoria e Previdência
        ]
        
        total_docs = 0
        for knowledge_set in knowledge_sets:
            count = await self.add_knowledge_set(knowledge_set)
            total_docs += count
        
        logger.info(f"✅ Base de conhecimento populada com {total_docs} documentos!")
        return total_docs
    
    async def add_knowledge_set(self, knowledge_set: Dict[str, List[Dict]]) -> int:
        """Adiciona um conjunto de conhecimento à base"""
        
        category = knowledge_set.get("category", "unknown")
        documents = knowledge_set.get("documents", [])
        
        logger.info(f"📚 Adicionando {len(documents)} documentos de {category}...")
        
        for doc in documents:
            try:
                await self.rag_service.add_document(
                    content=doc["content"],
                    metadata={
                        **doc.get("metadata", {}),
                        "category": category,
                        "added_by": "system_init"
                    }
                )
            except Exception as e:
                logger.error(f"❌ Erro ao adicionar documento {doc.get('title', 'sem título')}: {e}")
        
        return len(documents)
    
    def get_cdc_knowledge(self) -> Dict[str, Any]:
        """Código de Defesa do Consumidor - Foco em contratos B2C"""
        return {
            "category": "consumer_protection",
            "description": "Código de Defesa do Consumidor - Lei 8.078/90",
            "documents": [
                {
                    "title": "CDC Art. 6º - Direitos Básicos do Consumidor",
                    "content": """
                    Art. 6º São direitos básicos do consumidor:
                    I - a proteção da vida, saúde e segurança contra riscos provocados por práticas no fornecimento de produtos e serviços considerados perigosos ou nocivos;
                    II - a educação e divulgação sobre o consumo adequado dos produtos e serviços, assegurando informações corretas, claras, precisas, ostensivas e em língua portuguesa;
                    III - a informação adequada e clara sobre os diferentes produtos e serviços, com especificação correta de quantidade, características, composição, qualidade e preço, bem como sobre os riscos que apresentem;
                    IV - a proteção contra a publicidade enganosa e abusiva, métodos comerciais coercitivos ou desleais, bem como contra práticas e cláusulas abusivas ou impostas no fornecimento de produtos e serviços;
                    V - a modificação das cláusulas contratuais que estabeleçam prestações desproporcionais ou sua revisão em razão de fatos supervenientes que as tornem excessivamente onerosas;
                    VI - a efetiva prevenção e reparação de danos patrimoniais e morais, individuais, coletivos e difusos;
                    """,
                    "metadata": {
                        "source": "CDC",
                        "article": "6",
                        "law": "8078/90",
                        "risk_level": "alto",
                        "contract_types": ["consumer", "services", "products"],
                        "key_points": ["direitos_basicos", "informacao", "protecao"]
                    }
                },
                {
                    "title": "CDC Art. 51 - Cláusulas Abusivas",
                    "content": """
                    Art. 51. São nulas de pleno direito, entre outras, as cláusulas contratuais relativas ao fornecimento de produtos e serviços que:
                    I - impossibilitem, exonerem ou atenuem a responsabilidade do fornecedor por vícios de qualquer natureza dos produtos e serviços ou impliquem renúncia ou disposição de direitos;
                    II - subtraiam ao consumidor a opção de reembolso da quantia já paga, nos casos previstos neste código;
                    III - transfiram responsabilidades a terceiros;
                    IV - estabeleçam obrigações consideradas iníquas, abusivas, que coloquem o consumidor em desvantagem exagerada, ou sejam incompatíveis com a boa-fé ou a equidade;
                    V - (Vetado);
                    VI - estabeleçam inversão do ônus da prova em prejuízo do consumidor;
                    VII - determinem a utilização compulsória de arbitragem;
                    VIII - imponham representante para concluir ou realizar outro negócio jurídico pelo consumidor;
                    IX - deixem ao fornecedor a opção de concluir ou não o contrato, embora obrigando o consumidor;
                    X - permitam ao fornecedor, direta ou indiretamente, variação do preço de maneira unilateral;
                    """,
                    "metadata": {
                        "source": "CDC", 
                        "article": "51",
                        "law": "8078/90",
                        "risk_level": "alto",
                        "contract_types": ["consumer", "services"],
                        "key_points": ["clausulas_abusivas", "nulidade", "desvantagem_exagerada"]
                    }
                },
                {
                    "title": "CDC Art. 54 - Contratos de Adesão",
                    "content": """
                    Art. 54. Contrato de adesão é aquele cujas cláusulas tenham sido aprovadas pela autoridade competente ou estabelecidas unilateralmente pelo fornecedor de produtos ou serviços, sem que o consumidor possa discutir ou modificar substancialmente seu conteúdo.
                    § 3º Os contratos de adesão escritos serão redigidos em termos claros e com caracteres ostensivos e legíveis, cujo tamanho da fonte não será inferior ao corpo doze, de modo a facilitar sua compreensão pelo consumidor.
                    § 4º As cláusulas que implicarem limitação de direito do consumidor deverão ser redigidas com destaque, permitindo sua imediata e fácil compreensão.
                    """,
                    "metadata": {
                        "source": "CDC",
                        "article": "54", 
                        "law": "8078/90",
                        "risk_level": "medio",
                        "contract_types": ["adhesion", "consumer"],
                        "key_points": ["contrato_adesao", "clareza", "destaque_clausulas"]
                    }
                }
            ]
        }
    
    def get_rental_law_knowledge(self) -> Dict[str, Any]:
        """Lei do Inquilinato - Contratos de Locação"""
        return {
            "category": "rental_law",
            "description": "Lei do Inquilinato - Lei 8.245/91",
            "documents": [
                {
                    "title": "Lei 8.245/91 Art. 22 - Obrigações do Locador",
                    "content": """
                    Art. 22. O locador é obrigado a:
                    I - entregar ao locatário o imóvel alugado em estado de servir ao uso a que se destina;
                    II - garantir, durante todo o tempo da locação, o uso pacífico do imóvel locado;
                    III - manter o imóvel em estado de servir ao uso a que se destina;
                    IV - responder pelos vícios ou defeitos anteriores à locação;
                    V - fornecer ao locatário, caso este solicite, descrição minuciosa do estado do imóvel quando da elaboração do contrato, com expressa referência aos eventuais defeitos existentes.
                    """,
                    "metadata": {
                        "source": "Lei_8245",
                        "article": "22",
                        "law": "8245/91",
                        "risk_level": "medio",
                        "contract_types": ["rental", "real_estate"],
                        "key_points": ["obrigacoes_locador", "estado_imovel", "uso_pacifico"]
                    }
                },
                {
                    "title": "Lei 8.245/91 Art. 23 - Obrigações do Locatário", 
                    "content": """
                    Art. 23. O locatário é obrigado a:
                    I - servir-se do imóvel para o uso convencionado ou presumido, compatível com a natureza deste e com o fim a que se destina;
                    II - conservar o imóvel e utilizá-lo com o mesmo cuidado como se fosse seu;
                    III - pagar pontualmente o aluguel e os encargos da locação, legal ou contratualmente exigíveis, no prazo estipulado ou, em sua falta, até o sexto dia útil do mês seguinte ao vencido;
                    IV - levar imediatamente ao conhecimento do locador o surgimento de qualquer dano ou defeito cuja reparação a este incumba;
                    V - realizar a entrega do imóvel, finda a locação, no estado em que o recebeu, salvo as deteriorações decorrentes do uso normal;
                    """,
                    "metadata": {
                        "source": "Lei_8245",
                        "article": "23",
                        "law": "8245/91", 
                        "risk_level": "medio",
                        "contract_types": ["rental", "real_estate"],
                        "key_points": ["obrigacoes_locatario", "conservacao", "pagamento"]
                    }
                },
                {
                    "title": "Lei 8.245/91 Art. 9º - Garantias Locatícias",
                    "content": """
                    Art. 9º A locação também poderá ser garantida mediante:
                    I - caução; II - fiança; III - seguro de fiança locatícia.
                    § 2º É vedada, sob pena de nulidade, mais de uma das modalidades de garantia num mesmo contrato de locação.
                    § 3º Não se aplica o disposto no inciso III aos contratos de locação de imóveis destinados à residência familiar.
                    """,
                    "metadata": {
                        "source": "Lei_8245",
                        "article": "9",
                        "law": "8245/91",
                        "risk_level": "alto",
                        "contract_types": ["rental"],
                        "key_points": ["garantias", "nulidade", "multiplas_garantias"]
                    }
                }
            ]
        }
    
    def get_civil_code_knowledge(self) -> Dict[str, Any]:
        """Código Civil - Direito dos Contratos"""
        return {
            "category": "civil_contracts",
            "description": "Código Civil - Lei 10.406/02 - Direito dos Contratos",
            "documents": [
                {
                    "title": "CC Art. 421 - Função Social do Contrato",
                    "content": """
                    Art. 421. A liberdade contratual será exercida nos limites da função social do contrato.
                    Parágrafo único. Nas relações contratuais privadas, prevalecerá o princípio da intervenção mínima e a excepcionalidade da revisão contratual.
                    """,
                    "metadata": {
                        "source": "CC",
                        "article": "421",
                        "law": "10406/02",
                        "risk_level": "medio",
                        "contract_types": ["general"],
                        "key_points": ["funcao_social", "liberdade_contratual", "revisao_contratual"]
                    }
                },
                {
                    "title": "CC Art. 422 - Boa-fé Objetiva",
                    "content": """
                    Art. 422. Os contratantes são obrigados a guardar, assim na conclusão do contrato, como em sua execução, os princípios de probidade e boa-fé.
                    """,
                    "metadata": {
                        "source": "CC",
                        "article": "422", 
                        "law": "10406/02",
                        "risk_level": "alto",
                        "contract_types": ["general"],
                        "key_points": ["boa_fe", "probidade", "execucao_contrato"]
                    }
                },
                {
                    "title": "CC Art. 478 - Teoria da Imprevisão",
                    "content": """
                    Art. 478. Nos contratos de execução continuada ou diferida, se a prestação de uma das partes se tornar excessivamente onerosa, com extrema vantagem para a outra, em virtude de acontecimentos extraordinários e imprevisíveis, poderá o devedor pedir a resolução do contrato.
                    """,
                    "metadata": {
                        "source": "CC",
                        "article": "478",
                        "law": "10406/02",
                        "risk_level": "alto",
                        "contract_types": ["general", "continuous"],
                        "key_points": ["onerosidade_excessiva", "imprevisibilidade", "resolucao"]
                    }
                }
            ]
        }
    
    def get_telecom_knowledge(self) -> Dict[str, Any]:
        """Telecomunicações - Marco Civil e Anatel"""
        return {
            "category": "telecommunications",
            "description": "Regulamentação de Telecomunicações - Anatel e Marco Civil",
            "documents": [
                {
                    "title": "Anatel - Direitos dos Usuários de Telecomunicações",
                    "content": """
                    Os usuários de serviços de telecomunicações têm direito a:
                    - Informações claras sobre planos, preços e condições;
                    - Qualidade dos serviços conforme padrões regulamentados;
                    - Não cobrança por serviços não solicitados;
                    - Facilidades para cancelamento de serviços;
                    - Ressarcimento por falhas na prestação do serviço;
                    - Privacidade e proteção de dados pessoais;
                    - Atendimento adequado e canais de reclamação eficazes.
                    """,
                    "metadata": {
                        "source": "Anatel",
                        "regulation": "RGC",
                        "risk_level": "alto",
                        "contract_types": ["telecom", "internet", "mobile"],
                        "key_points": ["direitos_usuario", "qualidade", "cancelamento"]
                    }
                },
                {
                    "title": "Marco Civil da Internet - Art. 7º",
                    "content": """
                    Art. 7º O acesso à internet é essencial ao exercício da cidadania, e ao usuário são assegurados os seguintes direitos:
                    I - inviolabilidade da intimidade e da vida privada;
                    II - inviolabilidade e sigilo do fluxo de suas comunicações pela internet;
                    IV - não suspensão da conexão à internet, salvo por débito diretamente decorrente de sua utilização;
                    V - manutenção da qualidade contratada da conexão à internet;
                    VI - informações claras e completas sobre os termos de uso, privacidade e gerenciamento da rede nos contratos.
                    """,
                    "metadata": {
                        "source": "Marco_Civil",
                        "article": "7",
                        "law": "12965/14",
                        "risk_level": "alto", 
                        "contract_types": ["internet", "telecom"],
                        "key_points": ["privacidade", "qualidade", "transparencia"]
                    }
                }
            ]
        }
    
    def get_financial_knowledge(self) -> Dict[str, Any]:
        """Regulamentação Financeira - Bacen e CMN"""
        return {
            "category": "financial_regulation",
            "description": "Regulamentação Financeira - Banco Central e CMN",
            "documents": [
                {
                    "title": "Resolução CMN 4.693/18 - Transparência em Operações de Crédito",
                    "content": """
                    As instituições financeiras devem fornecer informações claras sobre:
                    - Custo Efetivo Total (CET) da operação;
                    - Taxa de juros efetiva anual;
                    - Valor e periodicidade das prestações;
                    - Encargos e tarifas aplicáveis;
                    - Condições para quitação antecipada;
                    - Consequências do inadimplemento;
                    - Direito de arrependimento quando aplicável.
                    """,
                    "metadata": {
                        "source": "CMN",
                        "resolution": "4693/18",
                        "risk_level": "alto",
                        "contract_types": ["financial", "credit", "loan"],
                        "key_points": ["transparencia", "CET", "informacoes_claras"]
                    }
                },
                {
                    "title": "Lei da Usura - Decreto 22.626/33",
                    "content": """
                    É vedado, e será punido nos termos desta Lei, estipular em quaisquer contratos taxas de juros superiores ao dobro da taxa legal.
                    A taxa legal é de 6% ao ano, salvo quando autorizada por lei especial.
                    Considera-se usurária toda taxa que exceder o limite legal permitido.
                    """,
                    "metadata": {
                        "source": "Lei_Usura",
                        "decree": "22626/33",
                        "risk_level": "alto",
                        "contract_types": ["financial", "loan"],
                        "key_points": ["usura", "limite_juros", "taxa_legal"]
                    }
                }
            ]
        }
    
    def get_labor_knowledge(self) -> Dict[str, Any]:
        """CLT - Consolidação das Leis do Trabalho"""
        return {
            "category": "labor_law",
            "description": "Consolidação das Leis do Trabalho - CLT",
            "documents": [
                {
                    "title": "CLT Art. 444 - Relação de Emprego",
                    "content": """
                    Art. 444. As relações contratuais de trabalho podem ser objeto de livre estipulação das partes interessadas em tudo quanto não contravenha às disposições de proteção ao trabalho, aos contratos coletivos que lhes sejam aplicáveis e às decisões das autoridades competentes.
                    """,
                    "metadata": {
                        "source": "CLT",
                        "article": "444",
                        "risk_level": "medio",
                        "contract_types": ["employment", "labor"],
                        "key_points": ["livre_estipulacao", "protecao_trabalho"]
                    }
                },
                {
                    "title": "CLT Art. 9º - Nulidade de Disposições Contrárias",
                    "content": """
                    Art. 9º Serão nulos de pleno direito os atos praticados com o objetivo de desvirtuar, impedir ou fraudar a aplicação dos preceitos contidos na presente Consolidação.
                    """,
                    "metadata": {
                        "source": "CLT",
                        "article": "9",
                        "risk_level": "alto",
                        "contract_types": ["employment", "labor"],
                        "key_points": ["nulidade", "fraude", "preceitos_clt"]
                    }
                }
            ]
        }
    
    def get_general_contract_law(self) -> Dict[str, Any]:
        """Princípios Gerais do Direito Contratual"""
        return {
            "category": "general_principles", 
            "description": "Princípios Gerais do Direito Contratual Brasileiro",
            "documents": [
                {
                    "title": "Princípio da Força Obrigatória dos Contratos",
                    "content": """
                    O contrato faz lei entre as partes (pacta sunt servanda). 
                    As obrigações contratuais devem ser cumpridas tal como foram estabelecidas.
                    Exceções: impossibilidade superveniente, caso fortuito, força maior, onerosidade excessiva.
                    """,
                    "metadata": {
                        "source": "Doutrina",
                        "principle": "pacta_sunt_servanda",
                        "risk_level": "medio",
                        "contract_types": ["general"],
                        "key_points": ["forca_obrigatoria", "cumprimento", "excecoes"]
                    }
                },
                {
                    "title": "Cláusulas Leoninas e Abusivas",
                    "content": """
                    São consideradas leoninas ou abusivas as cláusulas que:
                    - Estabelecem vantagem exagerada para uma das partes;
                    - Restringem direitos fundamentais;
                    - Impõem obrigações desproporcionais;
                    - Violam o princípio da boa-fé objetiva;
                    - Comprometem o equilíbrio contratual.
                    Tais cláusulas podem ser declaradas nulas pelo Poder Judiciário.
                    """,
                    "metadata": {
                        "source": "Doutrina",
                        "concept": "clausulas_abusivas",
                        "risk_level": "alto",
                        "contract_types": ["general"],
                        "key_points": ["vantagem_exagerada", "nulidade", "equilibrio"]
                    }
                }
            ]
        }
    
    def get_retirement_knowledge(self) -> Dict[str, Any]:
        """Aposentadoria e Previdência"""
        return {
            "category": "retirement_pension",
            "description": "Legislação Previdenciária - INSS e Previdência Privada",
            "documents": [
                {
                    "title": "Lei 8.213/91 - Benefícios da Previdência Social",
                    "content": """
                    Art. 42. A aposentadoria por idade será devida ao segurado que, cumprida a carência exigida, completar 65 (sessenta e cinco) anos de idade, se homem, e 62 (sessenta e dois) anos, se mulher.
                    Art. 48. A aposentadoria por tempo de contribuição será devida ao segurado que completar 35 (trinta e cinco) anos de contribuição, se homem, e 30 (trinta) anos, se mulher.
                    """,
                    "metadata": {
                        "source": "INSS",
                        "law": "8213/91",
                        "articles": ["42", "48"],
                        "risk_level": "baixo",
                        "contract_types": ["pension", "social_security"],
                        "key_points": ["idade_minima", "tempo_contribuicao", "carencia"]
                    }
                },
                {
                    "title": "Lei Complementar 109/01 - Previdência Privada",
                    "content": """
                    Art. 1º O regime de previdência complementar é operado por entidades de previdência complementar que têm por objetivo instituir e executar planos de benefícios de caráter previdenciário.
                    MODALIDADES: PGBL (Plano Gerador de Benefício Livre) e VGBL (Vida Gerador de Benefício Livre).
                    """,
                    "metadata": {
                        "source": "Lei_Complementar",
                        "law": "109/01",
                        "risk_level": "medio",
                        "contract_types": ["private_pension", "pgbl", "vgbl"],
                        "key_points": ["previdencia_complementar", "entidades_abertas", "beneficios"]
                    }
                },
                {
                    "title": "Principais Riscos em Contratos de Previdência Privada",
                    "content": """
                    CLÁUSULAS DE ATENÇÃO EM PREVIDÊNCIA PRIVADA:
                    1. TAXA DE ADMINISTRAÇÃO: Limite máximo de 3% ao ano sobre o patrimônio
                    2. TAXA DE CARREGAMENTO: Máximo de 10% sobre aportes regulares, 5% sobre extraordinários
                    3. CLÁUSULAS ABUSIVAS COMUNS: Alteração unilateral de taxas, restrições excessivas ao resgate
                    4. FALTA DE TRANSPARÊNCIA: Sobre rentabilidade e cobrança de taxas não previstas
                    """,
                    "metadata": {
                        "source": "SUSEP",
                        "regulation": "CNSP",
                        "risk_level": "alto",
                        "contract_types": ["private_pension", "pgbl", "vgbl"],
                        "key_points": ["taxas", "carregamento", "clausulas_abusivas", "resgate"]
                    }
                }
            ]
        }

async def main():
    """Função principal para executar a população da base de dados"""
    
    print("🏛️ DEMOCRATIZA AI - POPULANDO BASE DE CONHECIMENTO JURÍDICO COMPLETA")
    print("=" * 70)
    
    populator = LegalKnowledgePopulator()
    
    try:
        print("✅ Conexão estabelecida (modo simulação)")
        
        # Popular base de conhecimento
        total_docs = await populator.populate_all_knowledge()
        
        print("\n" + "=" * 70)
        print(f"🎉 SUCESSO! Base populada com {total_docs} documentos jurídicos")
        print("📚 Categorias incluídas:")
        print("   ✅ Código de Defesa do Consumidor (CDC)")
        print("   ✅ Lei do Inquilinato (8.245/91)") 
        print("   ✅ Código Civil - Contratos (10.406/02)")
        print("   ✅ Telecomunicações (Anatel/Marco Civil)")
        print("   ✅ Regulamentação Financeira (Bacen/CMN)")
        print("   ✅ CLT - Direito do Trabalho")
        print("   ✅ Princípios Gerais Contratuais")
        print("   ✅ Aposentadoria e Previdência (Novo!)")
        
        print(f"\n🚀 Sistema RAG pronto para análise de contratos:")
        print("   - Contratos de consumo")
        print("   - Contratos de locação")
        print("   - Contratos de telecomunicações")
        print("   - Contratos financeiros")
        print("   - Contratos de trabalho")
        print("   - Contratos de previdência (PGBL/VGBL)")
        print("   - Análise geral de cláusulas abusivas")
        
        # Salvar estatísticas
        with open('base_knowledge_stats.json', 'w', encoding='utf-8') as f:
            json.dump({
                "total_documents": total_docs,
                "categories": [
                    "consumer_protection",
                    "rental_law",
                    "civil_contracts", 
                    "telecommunications",
                    "financial_regulation",
                    "labor_law",
                    "general_principles",
                    "retirement_pension"
                ],
                "status": "populated",
                "populated_at": "2025-10-02"
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Estatísticas salvas em: base_knowledge_stats.json")
        print("🎯 PRONTO PARA ANÁLISE INTELIGENTE DE CONTRATOS!")
        
    except Exception as e:
        logger.error(f"❌ Erro durante população da base: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())