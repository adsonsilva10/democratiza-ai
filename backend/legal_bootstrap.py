"""
Legal Knowledge Bootstrap System
Sistema completo de inicialização da base de conhecimento jurídico brasileiro
"""
import asyncio
import sys
import os
from typing import List, Dict, Optional
from datetime import datetime
import json
import logging

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.legal_data_collector import LegalDataCollector, run_legal_data_collection
from app.services.regulatory_data_collector import RegulatoryDataCollector, run_regulatory_collection
from app.services.rag_service import rag_service
from app.db.database import AsyncSessionLocal
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('legal_bootstrap.log')
    ]
)
logger = logging.getLogger(__name__)

class LegalKnowledgeBootstrap:
    """Sistema completo de bootstrap da base de conhecimento jurídico"""
    
    def __init__(self):
        self.rag_service = rag_service
        self.total_indexed = 0
        self.errors = []
        
    async def run_complete_bootstrap(self):
        """Executa bootstrap completo da base jurídica"""
        
        logger.info("🚀 INICIANDO BOOTSTRAP COMPLETO DA BASE JURÍDICA BRASILEIRA")
        logger.info("="*70)
        
        start_time = datetime.now()
        
        try:
            # 1. Verificar pré-requisitos
            await self._check_prerequisites()
            
            # 2. Coletar dados das fontes oficiais
            all_legal_data = await self._collect_all_legal_data()
            
            # 3. Indexar no RAG Service
            await self._index_collected_data(all_legal_data)
            
            # 4. Adicionar conhecimento base especializado
            await self._add_specialized_knowledge()
            
            # 5. Verificar integridade dos dados
            await self._verify_data_integrity()
            
            # 6. Gerar relatório final
            await self._generate_final_report(start_time)
            
            logger.info("🎉 BOOTSTRAP CONCLUÍDO COM SUCESSO!")
            
        except Exception as e:
            logger.error(f"❌ ERRO CRÍTICO NO BOOTSTRAP: {str(e)}")
            raise
    
    async def _check_prerequisites(self):
        """Verifica pré-requisitos do sistema"""
        
        logger.info("🔍 Verificando pré-requisitos...")
        
        # Verificar conexão com banco
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(text("SELECT 1"))
                logger.info("✅ Conexão com banco de dados OK")
        except Exception as e:
            logger.error(f"❌ Erro de conexão com banco: {str(e)}")
            raise
        
        # Verificar extensão pg_vector
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector'"))
                if result.fetchone():
                    logger.info("✅ Extensão pg_vector ativa")
                else:
                    logger.warning("⚠️  Extensão pg_vector não encontrada - tentando criar...")
                    await db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                    await db.commit()
                    logger.info("✅ Extensão pg_vector criada")
        except Exception as e:
            logger.error(f"❌ Erro com pg_vector: {str(e)}")
            raise
        
        # Verificar tabelas RAG
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(text("SELECT tablename FROM pg_tables WHERE tablename IN ('legal_documents', 'legal_chunks', 'knowledge_base')"))
                tables = [row[0] for row in result.fetchall()]
                
                expected_tables = ['legal_documents', 'legal_chunks', 'knowledge_base']
                missing_tables = [t for t in expected_tables if t not in tables]
                
                if missing_tables:
                    logger.warning(f"⚠️  Tabelas faltando: {missing_tables}")
                    logger.info("💡 Execute: alembic upgrade head")
                else:
                    logger.info("✅ Todas as tabelas RAG existem")
        except Exception as e:
            logger.error(f"❌ Erro verificando tabelas: {str(e)}")
            raise
        
        # Verificar OpenAI API Key
        from app.core.config import settings
        if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
            logger.info("✅ OpenAI API Key configurada")
        else:
            logger.error("❌ OpenAI API Key não configurada")
            logger.info("💡 Configure OPENAI_API_KEY no arquivo .env")
            raise ValueError("OpenAI API Key necessária")
        
        logger.info("✅ Todos os pré-requisitos atendidos")
    
    async def _collect_all_legal_data(self) -> List[Dict]:
        """Coleta dados de todas as fontes jurídicas"""
        
        logger.info("\\n📚 INICIANDO COLETA DE DADOS JURÍDICOS")
        logger.info("="*50)
        
        all_data = []
        
        try:
            # 1. Coletar leis federais e jurisprudência
            logger.info("🏛️ Coletando leis federais e jurisprudência...")
            legal_data, _ = await run_legal_data_collection()
            all_data.extend(legal_data)
            logger.info(f"✅ Coletados {len(legal_data)} documentos legais")
            
            # 2. Coletar dados regulatórios
            logger.info("🏢 Coletando regulamentações de órgãos...")
            regulatory_data, _ = await run_regulatory_collection()
            all_data.extend(regulatory_data)
            logger.info(f"✅ Coletados {len(regulatory_data)} documentos regulatórios")
            
            logger.info(f"📊 Total de documentos coletados: {len(all_data)}")
            
            return all_data
            
        except Exception as e:
            logger.error(f"❌ Erro na coleta de dados: {str(e)}")
            raise
    
    async def _index_collected_data(self, legal_data: List[Dict]):
        """Indexa todos os dados coletados no RAG Service"""
        
        logger.info("\\n🔄 INICIANDO INDEXAÇÃO NO RAG SERVICE")
        logger.info("="*50)
        
        indexed_count = 0
        errors_count = 0
        
        async with AsyncSessionLocal() as db:
            for i, doc_data in enumerate(legal_data, 1):
                try:
                    logger.info(f"📄 Indexando ({i}/{len(legal_data)}): {doc_data['title'][:60]}...")
                    
                    # Indexar documento legal
                    document_id = await self.rag_service.index_legal_document(
                        title=doc_data["title"],
                        content=doc_data["content"],
                        document_type=doc_data["document_type"],
                        category=doc_data["category"],
                        source=doc_data["source"],
                        reference_number=doc_data.get("reference_number", ""),
                        authority_level=doc_data.get("authority_level", "medium"),
                        legal_area=doc_data.get("legal_area", []),
                        keywords=doc_data.get("keywords", []),
                        chunk_size=1000,
                        chunk_overlap=200,
                        db=db
                    )
                    
                    indexed_count += 1
                    logger.info(f"✅ Indexado: {document_id}")
                    
                    # Rate limiting para não sobrecarregar OpenAI
                    if i % 5 == 0:
                        logger.info("⏱️  Pausa para rate limiting...")
                        await asyncio.sleep(2)
                    
                except Exception as e:
                    errors_count += 1
                    error_msg = f"Erro ao indexar {doc_data['title']}: {str(e)}"
                    logger.error(f"❌ {error_msg}")
                    self.errors.append(error_msg)
                    continue
        
        logger.info(f"📊 RESULTADO DA INDEXAÇÃO:")
        logger.info(f"   ✅ Documentos indexados: {indexed_count}")
        logger.info(f"   ❌ Erros: {errors_count}")
        
        self.total_indexed = indexed_count
    
    async def _add_specialized_knowledge(self):
        """Adiciona conhecimento base especializado"""
        
        logger.info("\\n🧠 ADICIONANDO CONHECIMENTO ESPECIALIZADO")
        logger.info("="*50)
        
        specialized_guidelines = [
            {
                "title": "Diretrizes para Análise de Contratos de Locação",
                "content": """
                GUIA COMPLETO PARA ANÁLISE DE CONTRATOS DE LOCAÇÃO
                
                1. CLÁUSULAS ESSENCIAIS
                - Identificação das partes (locador e locatário)
                - Descrição detalhada do imóvel
                - Prazo de locação (mínimo 30 meses para residencial)
                - Valor do aluguel e data de vencimento
                - Forma de reajuste (IGP-M, IPCA ou outro índice)
                - Garantias oferecidas (caução, fiador, seguro)
                
                2. CLÁUSULAS DE RISCO ALTO
                - Multa compensatória superior a 3 aluguéis
                - Cobrança antecipada de mais de 1 aluguel
                - Responsabilização do locatário por reformas estruturais
                - Foro de eleição em comarca diferente do imóvel
                - Renúncia antecipada a direitos do locatário
                - Cláusula de não indenizar benfeitorias necessárias
                
                3. VERIFICAÇÕES JURISPRUDENCIAIS
                - STJ: Multa compensatória limitada a 3 aluguéis (Precedente consolidado)
                - STJ: Benfeitorias necessárias são sempre indenizáveis
                - STJ: Reforma estrutural é responsabilidade do locador
                
                4. ALERTAS PARA CDC (Locação não residencial)
                - Aplicação subsidiária em locações comerciais
                - Cláusulas abusivas segundo Art. 51 do CDC
                - Princípio da boa-fé objetiva
                """,
                "category": "locacao",
                "subcategory": "diretrizes",
                "tags": ["locacao", "analise", "clausulas", "risco"],
                "source": "knowledge_base",
                "confidence_level": 0.95
            },
            {
                "title": "Identificação de Práticas Abusivas em Telecomunicações",
                "content": """
                PRÁTICAS ABUSIVAS COMUNS EM CONTRATOS DE TELECOMUNICAÇÕES
                
                1. CLÁUSULAS VEDADAS PELA ANATEL (Resolução 632/2014)
                - Foro de eleição que dificulte defesa do usuário
                - Inversão do ônus da prova contra o consumidor
                - Modificação unilateral sem aviso prévio de 30 dias
                - Cobrança por serviços não solicitados
                - Dificuldades excessivas para cancelamento
                
                2. DIREITOS GARANTIDOS AO USUÁRIO
                - Cancelamento gratuito em 7 dias (direito de arrependimento)
                - Atendimento gratuito em canais da prestadora
                - Compensação por indisponibilidade do serviço
                - Informações claras sobre velocidade de internet
                - Portabilidade numérica gratuita
                
                3. ALERTAS DE COMPLIANCE
                - Verificar se há cláusula de permanência superior a 12 meses
                - Confirmar transparência nas informações de cobrança
                - Validar procedimentos de cancelamento
                - Verificar compensações por falha no serviço
                
                4. PRECEDENTES RELEVANTES
                - Cancelamento deve ser no mesmo canal de contratação
                - Multa por fidelização limitada ao benefício recebido
                - Cobrança indevida gera restituição em dobro
                """,
                "category": "telecom",
                "subcategory": "compliance",
                "tags": ["telecom", "ANATEL", "abusivas", "usuarios"],
                "source": "knowledge_base", 
                "confidence_level": 0.90
            },
            {
                "title": "Análise de Contratos Financeiros - Principais Riscos",
                "content": """
                GUIA DE ANÁLISE PARA CONTRATOS FINANCEIROS E BANCÁRIOS
                
                1. VERIFICAÇÕES OBRIGATÓRIAS
                - Taxa Efetiva Anual (TEA) claramente informada
                - Valor total do financiamento
                - Número e valor das prestações
                - Seguros obrigatórios discriminados
                - IOF e outras taxas especificadas
                
                2. PRÁTICAS ABUSIVAS COMUNS
                - Capitalização mensal de juros sem autorização legal
                - Cumulação de comissão de permanência com juros
                - Anatocismo (juros sobre juros) não autorizado
                - Cobrança de tarifa não prevista em regulamentação
                - Venda casada de produtos não relacionados
                
                3. LIMITES LEGAIS E JURISPRUDENCIAIS
                - Taxa de juros: verificar se está dentro da média do mercado
                - Multa moratória: limitada a 2% sobre valor devido
                - Juros moratórios: máximo 1% ao mês após vencimento
                - Comissão de permanência: não cumulável com correção
                
                4. GARANTIAS E RISCOS
                - Avaliar proporcionalidade das garantias exigidas
                - Verificar se bem dado em garantia é essencial à família
                - Validar procedimentos de execução de garantias
                - Confirmar direito de quitação antecipada com desconto
                
                5. COMPLIANCE BACEN
                - Transparência nas informações (Resolução 4.753/19)
                - Procedimentos de reclamação disponíveis
                - Canais de atendimento adequados
                """,
                "category": "financeiro",
                "subcategory": "analise_risco", 
                "tags": ["financeiro", "BACEN", "juros", "garantias"],
                "source": "knowledge_base",
                "confidence_level": 0.88
            }
        ]
        
        guidelines_added = 0
        
        async with AsyncSessionLocal() as db:
            for guideline in specialized_guidelines:
                try:
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
                    
                    guidelines_added += 1
                    logger.info(f"✅ Diretriz adicionada: {guideline['title']}")
                    
                except Exception as e:
                    error_msg = f"Erro ao adicionar diretriz {guideline['title']}: {str(e)}"
                    logger.error(f"❌ {error_msg}")
                    self.errors.append(error_msg)
        
        logger.info(f"📊 Diretrizes especializadas adicionadas: {guidelines_added}")
    
    async def _verify_data_integrity(self):
        """Verifica integridade dos dados indexados"""
        
        logger.info("\\n🔍 VERIFICANDO INTEGRIDADE DOS DADOS")
        logger.info("="*50)
        
        async with AsyncSessionLocal() as db:
            try:
                # Verificar estatísticas do RAG
                stats = await self.rag_service.get_knowledge_stats(db)
                
                logger.info("📊 ESTATÍSTICAS DO KNOWLEDGE BASE:")
                logger.info(f"   📄 Total de entradas: {stats['total_entries']}")
                logger.info(f"   📁 Categorias: {stats['categories']}")
                logger.info(f"   🔢 Dimensão dos embeddings: {stats['embedding_dimension']}")
                
                # Verificar documentos legais indexados
                legal_docs_result = await db.execute(text("SELECT COUNT(*) FROM legal_documents WHERE processing_status = 'indexed'"))
                legal_docs_count = legal_docs_result.scalar()
                logger.info(f"   📚 Documentos legais indexados: {legal_docs_count}")
                
                # Verificar chunks gerados
                chunks_result = await db.execute(text("SELECT COUNT(*) FROM legal_chunks WHERE embedding IS NOT NULL"))
                chunks_count = chunks_result.scalar()
                logger.info(f"   🧩 Chunks com embeddings: {chunks_count}")
                
                # Teste de busca
                logger.info("\\n🧪 Testando busca vetorial...")
                test_results = await self.rag_service.search(
                    query="cláusula abusiva contrato",
                    limit=3,
                    db=db
                )
                
                logger.info(f"   🔍 Resultados de teste: {len(test_results)} encontrados")
                for i, result in enumerate(test_results[:3], 1):
                    score = result.get('similarity_score', 0)
                    logger.info(f"   {i}. {result['title'][:40]}... (Score: {score:.3f})")
                
                logger.info("✅ Integridade dos dados verificada")
                
            except Exception as e:
                logger.error(f"❌ Erro na verificação de integridade: {str(e)}")
                raise
    
    async def _generate_final_report(self, start_time: datetime):
        """Gera relatório final do bootstrap"""
        
        logger.info("\\n📋 GERANDO RELATÓRIO FINAL")
        logger.info("="*50)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Estatísticas finais
        async with AsyncSessionLocal() as db:
            stats = await self.rag_service.get_knowledge_stats(db)
            
            legal_docs_result = await db.execute(text("SELECT COUNT(*) FROM legal_documents"))
            legal_docs_total = legal_docs_result.scalar()
            
            chunks_result = await db.execute(text("SELECT COUNT(*) FROM legal_chunks"))
            chunks_total = chunks_result.scalar()
        
        report = {
            "bootstrap_info": {
                "inicio": start_time.isoformat(),
                "fim": end_time.isoformat(), 
                "duracao_minutos": duration.total_seconds() / 60,
                "status": "CONCLUÍDO"
            },
            "estatisticas": {
                "documentos_indexados": self.total_indexed,
                "knowledge_base_entries": stats['total_entries'],
                "legal_documents": legal_docs_total,
                "legal_chunks": chunks_total,
                "categorias": stats['categories']
            },
            "erros": {
                "total_erros": len(self.errors),
                "detalhes": self.errors
            },
            "verificacao": {
                "integridade_ok": len(self.errors) < self.total_indexed * 0.1,  # Menos de 10% de erros
                "busca_funcionando": True,
                "embeddings_ok": chunks_total > 0
            }
        }
        
        # Salvar relatório
        report_filename = f"bootstrap_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("reports", exist_ok=True)
        
        with open(f"reports/{report_filename}", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Log do relatório
        logger.info("🎯 RELATÓRIO FINAL DO BOOTSTRAP")
        logger.info(f"⏱️  Duração: {duration.total_seconds()/60:.1f} minutos")
        logger.info(f"📄 Documentos processados: {self.total_indexed}")
        logger.info(f"📊 Knowledge Base entries: {stats['total_entries']}")
        logger.info(f"🧩 Chunks gerados: {chunks_total}")
        logger.info(f"❌ Erros encontrados: {len(self.errors)}")
        logger.info(f"💾 Relatório salvo: reports/{report_filename}")
        
        if len(self.errors) == 0:
            logger.info("🎉 BOOTSTRAP 100% SUCESSFUL!")
        elif len(self.errors) < self.total_indexed * 0.1:
            logger.info("✅ BOOTSTRAP CONCLUÍDO COM SUCESSO (poucos erros)")
        else:
            logger.warning("⚠️  BOOTSTRAP CONCLUÍDO COM ERROS SIGNIFICATIVOS")
        
        logger.info("\\n🚀 BASE JURÍDICA BRASILEIRA PRONTA PARA USO!")

async def main():
    """Função principal para executar o bootstrap"""
    
    print("🇧🇷 DEMOCRATIZA AI - BOOTSTRAP DA BASE JURÍDICA BRASILEIRA")
    print("="*70)
    print("Inicializando base de conhecimento com fontes oficiais do Brasil")
    print("- Leis Federais (Planalto.gov.br)")
    print("- Jurisprudência (STJ)")  
    print("- Regulamentações (ANATEL, BACEN, SENACON)")
    print("- Diretrizes Especializadas")
    print("="*70)
    
    # Confirmação do usuário
    response = input("\\nDeseja continuar com o bootstrap completo? (s/n): ")
    if response.lower() != 's':
        print("❌ Bootstrap cancelado pelo usuário")
        return
    
    try:
        bootstrap = LegalKnowledgeBootstrap()
        await bootstrap.run_complete_bootstrap()
        
        print("\\n" + "="*70)
        print("🎉 BOOTSTRAP CONCLUÍDO COM SUCESSO!")
        print("✅ Base jurídica brasileira está pronta para uso")
        print("📚 Agentes de IA agora têm acesso a conhecimento jurídico especializado")
        print("⚖️ Análises de contratos serão mais precisas e fundamentadas")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\\n⏹️  Bootstrap interrompido pelo usuário")
    except Exception as e:
        print(f"\\n❌ ERRO CRÍTICO: {str(e)}")
        print("💡 Verifique os logs e pré-requisitos antes de tentar novamente")
        raise

if __name__ == "__main__":
    asyncio.run(main())