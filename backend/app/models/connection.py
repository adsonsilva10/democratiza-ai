"""
Database connection and session management for Supabase PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os
from typing import AsyncGenerator

# Importar configurações
from app.core.config_minimal import settings

# Base para modelos SQLAlchemy
Base = declarative_base()

# Engine síncrono para migrations e operações especiais
sync_engine = create_engine(
    settings.database_url_sync,
    poolclass=NullPool,
    echo=settings.DEBUG,
    future=True
)

# Engine assíncrono para operações normais da aplicação
async_engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    poolclass=NullPool,
    echo=settings.DEBUG,
    future=True
)

# Session makers
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para obter sessão assíncrona do banco de dados
    Para uso com FastAPI Dependency Injection
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db():
    """
    Dependency para obter sessão síncrona do banco de dados
    Para migrations e operações especiais
    """
    db = SyncSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


async def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas
    """
    from app.models.database_complete import Base
    
    # Importar todos os modelos para garantir que sejam registrados
    from app.models import database_complete
    
    async with async_engine.begin() as conn:
        # Criar todas as tabelas
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Todas as tabelas foram criadas com sucesso!")


async def check_db_connection():
    """
    Verifica se a conexão com o banco está funcionando
    """
    try:
        from sqlalchemy import text
        async with async_engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.fetchone()
            print(f"✅ Conexão com PostgreSQL: {version[0]}")
            return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False


async def check_extensions():
    """
    Verifica extensões habilitadas no PostgreSQL
    """
    try:
        from sqlalchemy import text
        async with async_engine.begin() as conn:
            # Verificar pg_vector para RAG
            result = await conn.execute(
                text("SELECT extname FROM pg_extension WHERE extname = 'vector'")
            )
            vector_ext = result.fetchone()
            
            if vector_ext:
                print("✅ Extensão pg_vector habilitada (RAG disponível)")
            else:
                print("⚠️  Extensão pg_vector não encontrada")
                print("   Execute: CREATE EXTENSION vector; no Supabase SQL Editor")
                
    except Exception as e:
        print(f"⚠️  Erro ao verificar extensões: {e}")


# Configurações de conexão otimizadas para Supabase
CONNECTION_CONFIG = {
    "pool_size": 5,
    "max_overflow": 10,
    "pool_pre_ping": True,
    "pool_recycle": 300,
}