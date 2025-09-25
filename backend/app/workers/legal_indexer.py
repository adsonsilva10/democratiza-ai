"""
Legal Knowledge Indexing Worker for RAG Service
Populates the legal documents database with Brazilian legal framework
"""
import asyncio
import json
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.services.rag_service import rag_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalKnowledgeIndexer:
    """Indexes Brazilian legal documents for the RAG service"""
    
    def __init__(self):
        self.rag_service = rag_service
    
    async def index_basic_legal_framework(self):
        """Index basic Brazilian legal framework for contract law"""
        
        basic_legal_docs = [
            {
                "title": "Lei do Inquilinato - Lei 8.245/91 - Artigo 1º",
                "content": """
                Art. 1º A locação de imóvel urbano regula-se pelo disposto nesta Lei.
                Parágrafo único. Continuam regulados pelo Código Civil e pelas leis especiais:
                a) as locações de imóveis de propriedade da União, dos Estados e dos Municípios, de suas autarquias e fundações públicas;
                b) as locações de vagas autônomas de garagem ou de espaços para estacionamento de veículos;
                c) as locações de espaços destinados à publicidade;
                d) as locações em apart-hotéis, hotéis-residência ou equiparados, assim considerados aqueles que prestam serviços regulares a seus usuários e como tais sejam autorizados a funcionar.
                """,
                "document_type": "lei",
                "category": "locacao",
                "source": "Lei 8.245/91",
                "reference_number": "Lei 8.245/91 - Art. 1º",
                "authority_level": "high",
                "legal_area": ["direito imobiliario", "contratos"],
                "keywords": ["locacao", "imovel urbano", "lei inquilinato"]
            },
            {
                "title": "Código de Defesa do Consumidor - Art. 51 - Cláusulas Abusivas",
                "content": """
                Art. 51. São nulas de pleno direito, entre outras, as cláusulas contratuais relativas ao fornecimento de produtos e serviços que:
                I - impossibilitem, exonerem ou atenuem a responsabilidade do fornecedor por vícios de qualquer natureza dos produtos e serviços ou impliquem renúncia ou disposição de direitos;
                IV - estabeleçam obrigações consideradas iníquas, abusivas, que coloquem o consumidor em desvantagem exagerada, ou sejam incompatíveis com a boa-fé ou a equidade;
                § 1º Presume-se exagerada, entre outros casos, a vantagem que:
                I - ofende os princípios fundamentais do sistema jurídico a que pertence;
                II - restringe direitos ou obrigações fundamentais inerentes à natureza do contrato, de tal modo a ameaçar seu objeto ou equilíbrio contratual;
                III - se mostra excessivamente onerosa para o consumidor, considerando-se a natureza e conteúdo do contrato, o interesse das partes e outras circunstâncias peculiares ao caso.
                """,
                "document_type": "lei",
                "category": "geral",
                "source": "CDC - Lei 8.078/90",
                "reference_number": "Lei 8.078/90 - Art. 51",
                "authority_level": "high",
                "legal_area": ["direito do consumidor", "contratos"],
                "keywords": ["clausulas abusivas", "consumidor", "fornecedor", "contrato"]
            },
            {
                "title": "ANATEL - Regulamento de Proteção e Defesa dos Direitos dos Usuários",
                "content": """
                Art. 47. É vedado às prestadoras inserir nos contratos de prestação de serviços de telecomunicações cláusulas que:
                I - impossibilitem, exonerem ou atenuem a responsabilidade da prestadora por danos causados aos usuários;
                II - estabeleçam a inversão do ônus da prova em prejuízo do usuário;
                III - adotem qualquer modalidade de cláusula de não indenizar;
                IV - imponham a utilização compulsória de arbitragem;
                V - estabeleçam foro de eleição que dificulte a defesa dos direitos do usuário;
                VI - obstem ou dificultem o acesso do usuário ao Poder Judiciário;
                VII - permitam à prestadora modificar unilateralmente o conteúdo ou a interpretação do contrato;
                VIII - tenham caráter abusivo ou coloquem o usuário em desvantagem exagerada.
                """,
                "document_type": "regulamento",
                "category": "telecom",
                "source": "ANATEL",
                "reference_number": "Resolução ANATEL 632/2014 - Art. 47",
                "authority_level": "high",
                "legal_area": ["direito das telecomunicacoes", "contratos"],
                "keywords": ["telecomunicacoes", "ANATEL", "clausulas abusivas", "usuarios"]
            },
            {
                "title": "Código Civil - Contratos - Art. 421 - Função Social",
                "content": """
                Art. 421. A liberdade contratual será exercida nos limites da função social do contrato.
                Parágrafo único. Nas relações contratuais privadas, prevalecerão o princípio da intervenção mínima e a excepcionalidade da revisão contratual.
                
                Art. 422. Os contratantes são obrigados a guardar, assim na conclusão do contrato, como em sua execução, os princípios de probidade e boa-fé.
                
                Art. 423. Quando houver no contrato de adesão cláusulas ambíguas ou contraditórias, dever-se-á adotar a interpretação mais favorável ao aderente.
                
                Art. 424. Nos contratos de adesão, são nulas as cláusulas que estipulem a renúncia antecipada do aderente a direito resultante da natureza do negócio.
                """,
                "document_type": "lei",
                "category": "geral",
                "source": "Código Civil - Lei 10.406/02",
                "reference_number": "Lei 10.406/02 - Arts. 421-424",
                "authority_level": "high",
                "legal_area": ["direito civil", "contratos"],
                "keywords": ["funcao social", "boa fe", "contrato adesao", "clausulas nulas"]
            },
            {
                "title": "Jurisprudência STJ - Contratos de Locação - Multa Abusiva",
                "content": """
                CIVIL E PROCESSUAL CIVIL. LOCAÇÃO. CLÁUSULA PENAL COMPENSATÓRIA. REDUÇÃO. 
                POSSIBILIDADE. ARTIGO 413 DO CÓDIGO CIVIL.
                
                1. A cláusula penal, ainda que previamente estipulada, pode ser reduzida pelo juiz se a obrigação principal tiver sido cumprida em parte, ou se o montante da penalidade for manifestamente excessivo, tendo-se em vista a natureza e a finalidade do negócio (art. 413 do CC).
                
                2. No caso de locação residencial, a multa compensatória equivalente a três aluguéis, em regra, não se mostra excessiva, devendo a redução ser analisada caso a caso.
                
                3. Precedentes do STJ: REsp 1.061.530/RS, REsp 1.024.478/PR.
                """,
                "document_type": "jurisprudencia",
                "category": "locacao",
                "source": "STJ",
                "reference_number": "REsp 1.355.554/SP",
                "authority_level": "high",
                "legal_area": ["direito imobiliario", "contratos"],
                "keywords": ["locacao", "clausula penal", "multa", "reducao", "STJ"]
            }
        ]
        
        async with AsyncSessionLocal() as db:
            for doc_data in basic_legal_docs:
                try:
                    logger.info(f"Indexing: {doc_data['title']}")
                    
                    document_id = await self.rag_service.index_legal_document(
                        title=doc_data["title"],
                        content=doc_data["content"],
                        document_type=doc_data["document_type"],
                        category=doc_data["category"],
                        source=doc_data["source"],
                        reference_number=doc_data["reference_number"],
                        authority_level=doc_data["authority_level"],
                        legal_area=doc_data["legal_area"],
                        keywords=doc_data["keywords"],
                        db=db
                    )
                    
                    logger.info(f"Successfully indexed document: {document_id}")
                    
                except Exception as e:
                    logger.error(f"Error indexing document {doc_data['title']}: {e}")
                    continue
    
    async def index_knowledge_base_guidelines(self):
        """Index general guidelines and best practices"""
        
        guidelines = [
            {
                "title": "Análise de Cláusulas de Multa em Contratos de Locação",
                "content": """
                DIRETRIZES PARA ANÁLISE DE CLÁUSULAS DE MULTA:
                
                1. MULTA COMPENSATÓRIA (Art. 413 CC):
                - Até 3 aluguéis: Geralmente aceita pelos tribunais
                - Acima de 3 aluguéis: Pode ser considerada excessiva
                - Deve ser proporcional ao prejuízo estimado
                
                2. MULTA MORATÓRIA:
                - Limite de 2% sobre o valor do débito (CDC)
                - Não pode ser cumulada com juros superiores a 1% a.m.
                
                3. FATORES DE ANÁLISE:
                - Finalidade do negócio
                - Poder econômico das partes
                - Cumprimento parcial da obrigação
                - Desproporcionalidade manifesta
                
                4. JURISPRUDÊNCIA CONSOLIDADA:
                - STJ admite redução judicial de multa excessiva
                - Análise caso a caso da proporcionalidade
                - Boa-fé objetiva como limite
                """,
                "category": "locacao",
                "subcategory": "multas",
                "tags": ["multa", "locacao", "clausula penal", "proporcionalidade"],
                "source": "guideline",
                "confidence_level": 0.95
            },
            {
                "title": "Identificação de Cláusulas Abusivas em Telecomunicações",
                "content": """
                PRINCIPAIS CLÁUSULAS ABUSIVAS EM TELECOM:
                
                1. FORO DE ELEIÇÃO:
                - Cláusula que dificulte acesso à Justiça
                - Obrigar usuário a litigar em comarca distante
                - Vedado pela ANATEL (Res. 632/2014)
                
                2. INVERSÃO DO ÔNUS DA PROVA:
                - Transferir ao usuário prova de falha do serviço
                - Contraria CDC e regulamentação
                
                3. MODIFICAÇÃO UNILATERAL:
                - Alteração de preços sem justificativa
                - Mudança de condições contratuais
                - Necessário aviso prévio mínimo de 30 dias
                
                4. RENOVAÇÃO AUTOMÁTICA:
                - Deve ser expressa e destacada
                - Usuário deve ter direito de cancelamento
                - Fidelização abusiva vedada
                
                5. COBRANÇA INDEVIDA:
                - Serviços não contratados
                - Taxas de adesão abusivas
                - Multa desproporcional
                """,
                "category": "telecom",
                "subcategory": "clausulas_abusivas",
                "tags": ["telecom", "ANATEL", "clausulas abusivas", "usuarios"],
                "source": "guideline",
                "confidence_level": 0.9
            },
            {
                "title": "Contratos Financeiros - Cláusulas de Risco",
                "content": """
                CLÁUSULAS DE ALTO RISCO EM CONTRATOS FINANCEIROS:
                
                1. JUROS ABUSIVOS:
                - Verificar taxa efetiva anual
                - Comparar com média de mercado
                - Atenção aos juros compostos
                
                2. CAPITALIZAÇÃO:
                - Capitalização mensal só permitida em casos específicos
                - Verificar autorização legal
                
                3. COMISSÃO DE PERMANÊNCIA:
                - Não pode ser cumulada com juros moratórios
                - Limitada à taxa do contrato
                
                4. VENCIMENTO ANTECIPADO:
                - Deve ter causa justificada
                - Não pode ser arbitrária
                
                5. GARANTIAS EXCESSIVAS:
                - Desproporcionalidade ao risco
                - Alienação de bem essencial
                
                6. INDEXADORES:
                - Índices permitidos por lei
                - Transparência na aplicação
                """,
                "category": "financeiro",
                "subcategory": "clausulas_risco",
                "tags": ["financeiro", "juros", "garantias", "bancario"],
                "source": "guideline",  
                "confidence_level": 0.85
            }
        ]
        
        async with AsyncSessionLocal() as db:
            for guideline in guidelines:
                try:
                    logger.info(f"Adding guideline: {guideline['title']}")
                    
                    kb_id = await self.rag_service.add_knowledge(
                        title=guideline["title"],
                        content=guideline["content"],
                        category=guideline["category"],
                        subcategory=guideline.get("subcategory"),
                        tags=guideline.get("tags", []),
                        source=guideline.get("source", "internal"),
                        confidence_level=guideline.get("confidence_level", 1.0),
                        db=db
                    )
                    
                    logger.info(f"Successfully added guideline: {kb_id}")
                    
                except Exception as e:
                    logger.error(f"Error adding guideline {guideline['title']}: {e}")
                    continue

async def main():
    """Main indexing function"""
    indexer = LegalKnowledgeIndexer()
    
    logger.info("Starting legal knowledge indexing...")
    
    try:
        # Index basic legal framework
        logger.info("Indexing basic legal framework...")
        await indexer.index_basic_legal_framework()
        
        # Index knowledge base guidelines
        logger.info("Indexing knowledge base guidelines...")
        await indexer.index_knowledge_base_guidelines()
        
        logger.info("Legal knowledge indexing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during indexing: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())