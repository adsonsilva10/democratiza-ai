"""
Script automatizado para limpar histórico de migrations
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
    print(f"✅ Carregado: {env_path}")


def clean_alembic_version():
    """Limpa tabela alembic_version automaticamente"""
    
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    if not database_url:
        print("❌ DATABASE_URL não configurado!")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🔄 LIMPANDO HISTÓRICO DE MIGRATIONS")
    print("="*60)
    print(f"\n📊 Database: {database_url[:50]}...")
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Verificar se tabela existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'alembic_version'
                )
            """))
            exists = result.scalar()
            
            if not exists:
                print("✅ Tabela alembic_version não existe (OK)")
                return True
            
            # Ver versões atuais
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            versions = [row[0] for row in result.fetchall()]
            
            if versions:
                print(f"\n⚠️  Versões de migration antigas encontradas:")
                for v in versions:
                    print(f"   - {v}")
                
                # Deletar todas as versões
                print("\n🔄 Removendo versões antigas...")
                conn.execute(text("DELETE FROM alembic_version"))
                conn.commit()
                print("✅ Histórico de migrations limpo!")
            else:
                print("✅ Nenhuma versão antiga encontrada")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "🧹"*30)
    print("CLEAN MIGRATIONS - DEMOCRATIZA AI")
    print("🧹"*30)
    
    if clean_alembic_version():
        print("\n" + "="*60)
        print("✅ PRONTO!")
        print("="*60)
        print("\n📋 Próximo passo:")
        print("   python setup_database.py")
    else:
        print("\n❌ Erro ao limpar migrations.")
        sys.exit(1)
