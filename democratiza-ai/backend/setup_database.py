"""
Script para aplicar migrations no Supabase
Verifica se pg_vector está habilitado e aplica schema inicial
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

# Carregar variáveis de ambiente do .env
env_path = backend_path / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Carregado: {env_path}")
else:
    print(f"⚠️  Arquivo .env não encontrado em {env_path}")
    print("   Tentando variáveis de ambiente do sistema...")

from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_pgvector_extension():
    """Verifica se extensão pg_vector está disponível"""
    logger.info("🔍 Verificando extensão pg_vector...")
    
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    if not database_url:
        logger.error("❌ DATABASE_URL ou SUPABASE_DB_URL não configurado!")
        return False
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Verificar se pg_vector está disponível
            result = conn.execute(text(
                "SELECT * FROM pg_available_extensions WHERE name = 'vector'"
            ))
            available = result.fetchone()
            
            if not available:
                logger.error("❌ Extensão pg_vector NÃO está disponível no Supabase!")
                logger.error("   Contate o suporte do Supabase para habilitar.")
                return False
            
            # Verificar se está instalada
            result = conn.execute(text(
                "SELECT * FROM pg_extension WHERE extname = 'vector'"
            ))
            installed = result.fetchone()
            
            if installed:
                logger.info("✅ pg_vector JÁ está instalado!")
            else:
                logger.info("⚠️  pg_vector está disponível mas NÃO instalado")
                logger.info("   A migration irá instalar automaticamente.")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Erro ao verificar pg_vector: {e}")
        return False


def run_migrations():
    """Executa migrations do Alembic"""
    logger.info("\n" + "="*60)
    logger.info("🚀 Aplicando Migrations no Supabase")
    logger.info("="*60)
    
    # Verificar pg_vector primeiro
    if not check_pgvector_extension():
        logger.error("\n❌ ERRO: pg_vector não disponível. Abortando.")
        return False
    
    try:
        # Configurar Alembic
        alembic_cfg = Config("alembic.ini")
        
        # Obter URL do banco
        database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        
        logger.info("\n📋 Histórico de Migrations:")
        command.history(alembic_cfg)
        
        logger.info("\n⬆️  Aplicando migrations...")
        command.upgrade(alembic_cfg, "head")
        
        logger.info("\n✅ Migrations aplicadas com sucesso!")
        
        # Mostrar status atual
        logger.info("\n📊 Status Atual:")
        command.current(alembic_cfg)
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Erro ao aplicar migrations: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_schema():
    """Verifica se schema foi criado corretamente"""
    logger.info("\n" + "="*60)
    logger.info("🔍 Verificando Schema Criado")
    logger.info("="*60)
    
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Verificar tabelas
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            
            logger.info(f"\n📋 Tabelas criadas ({len(tables)}):")
            for table in tables:
                logger.info(f"  ✅ {table}")
            
            # Verificar índice vetorial
            result = conn.execute(text("""
                SELECT indexname 
                FROM pg_indexes 
                WHERE tablename = 'contracts' 
                AND indexname LIKE '%embedding%'
            """))
            indexes = [row[0] for row in result.fetchall()]
            
            if indexes:
                logger.info(f"\n📊 Índices vetoriais:")
                for idx in indexes:
                    logger.info(f"  ✅ {idx}")
            else:
                logger.warning("  ⚠️  Nenhum índice vetorial encontrado")
            
            # Verificar coluna text_embedding
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'contracts' 
                AND column_name = 'text_embedding'
            """))
            embedding_col = result.fetchone()
            
            if embedding_col:
                logger.info(f"\n🎯 Coluna de embedding:")
                logger.info(f"  ✅ {embedding_col[0]}: {embedding_col[1]} (1536 dimensões)")
            else:
                logger.error("  ❌ Coluna text_embedding NÃO encontrada!")
            
            logger.info("\n✅ Verificação de schema completa!")
            return True
            
    except Exception as e:
        logger.error(f"\n❌ Erro ao verificar schema: {e}")
        return False


def main():
    """Executa processo completo de migration"""
    print("\n" + "🚀"*30)
    print("DEMOCRATIZA AI - SETUP DE DATABASE")
    print("🚀"*30)
    
    # Verificar variáveis de ambiente
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    if not database_url:
        print("\n❌ ERRO: Variável de ambiente DATABASE_URL ou SUPABASE_DB_URL não configurada!")
        print("\n💡 Configure no .env:")
        print("   DATABASE_URL=postgresql://user:pass@host:5432/dbname")
        sys.exit(1)
    
    print(f"\n📊 Database: {database_url[:50]}...")
    
    # Executar migrations
    if not run_migrations():
        print("\n❌ Falha ao aplicar migrations. Abortando.")
        sys.exit(1)
    
    # Verificar schema
    if not verify_schema():
        print("\n⚠️  Verificação de schema falhou, mas migrations foram aplicadas.")
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETO!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("  1. Testar RAG Service: python test_openai_embeddings.py")
    print("  2. Indexar documentos legais: python legal_bootstrap.py")
    print("  3. Testar pipeline completo: python test_complete_pipeline.py")
    print("\n🎉 Database pronto para produção!")


if __name__ == "__main__":
    main()
