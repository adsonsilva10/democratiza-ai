"""
Script para verificar estado atual do banco
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

# Carregar variáveis de ambiente
env_path = backend_path / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


def check_database_state():
    """Verifica estado atual do banco"""
    
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    if not database_url:
        print("❌ DATABASE_URL não configurado!")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("📊 ESTADO DO BANCO DE DADOS")
    print("="*60)
    
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
            
            print(f"\n📋 Tabelas existentes ({len(tables)}):")
            for table in tables:
                print(f"   ✅ {table}")
            
            # Verificar colunas da tabela users
            if 'users' in tables:
                print("\n👤 Colunas da tabela 'users':")
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = 'users'
                    ORDER BY ordinal_position
                """))
                for row in result.fetchall():
                    nullable = "NULL" if row[2] == 'YES' else "NOT NULL"
                    print(f"   - {row[0]}: {row[1]} ({nullable})")
            
            # Verificar colunas da tabela contracts
            if 'contracts' in tables:
                print("\n📄 Colunas da tabela 'contracts':")
                result = conn.execute(text("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = 'contracts'
                    AND column_name IN ('text_embedding', 'llm_model_used', 'llm_provider_used')
                    ORDER BY ordinal_position
                """))
                cols = result.fetchall()
                if cols:
                    for row in cols:
                        print(f"   - {row[0]}: {row[1]}")
                else:
                    print("   ⚠️  Colunas de AI não encontradas (precisa migration)")
            
            # Verificar pg_vector
            result = conn.execute(text("""
                SELECT * FROM pg_extension WHERE extname = 'vector'
            """))
            has_vector = result.fetchone()
            
            print(f"\n🎯 Extensão pg_vector: {'✅ INSTALADA' if has_vector else '❌ NÃO INSTALADA'}")
            
            # Verificar índices
            result = conn.execute(text("""
                SELECT indexname 
                FROM pg_indexes 
                WHERE tablename = 'contracts'
                AND indexname LIKE '%embedding%'
            """))
            indexes = [row[0] for row in result.fetchall()]
            
            if indexes:
                print(f"\n📊 Índices vetoriais:")
                for idx in indexes:
                    print(f"   ✅ {idx}")
            else:
                print("\n⚠️  Nenhum índice vetorial encontrado")
            
            # Verificar migrations aplicadas
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'alembic_version'
                )
            """))
            has_alembic = result.scalar()
            
            if has_alembic:
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                versions = [row[0] for row in result.fetchall()]
                if versions:
                    print(f"\n🔄 Migrations aplicadas:")
                    for v in versions:
                        print(f"   - {v}")
                else:
                    print("\n⚠️  Nenhuma migration aplicada (alembic_version vazio)")
            else:
                print("\n⚠️  Tabela alembic_version não existe")
            
            print("\n" + "="*60)
            return True
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    check_database_state()
