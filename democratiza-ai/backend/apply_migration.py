"""
Aplicar migration ALTER TABLE para adicionar colunas AI
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

# Carregar .env
env_path = backend_path / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Carregado: {env_path}")

from alembic.config import Config
from alembic import command


def apply_migration():
    """Aplica migration 002_add_ai_columns"""
    
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    if not database_url:
        print("❌ DATABASE_URL não configurado!")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🚀 APLICANDO MIGRATION: ADD AI COLUMNS")
    print("="*60)
    print(f"\n📊 Database: {database_url[:50]}...")
    
    try:
        # Configurar Alembic
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        
        print("\n⬆️  Aplicando migration 002_add_ai_columns...")
        command.upgrade(alembic_cfg, "head")
        
        print("\n✅ Migration aplicada com sucesso!")
        
        # Mostrar status
        print("\n📊 Status atual:")
        command.current(alembic_cfg)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "🔧"*30)
    print("ALTER TABLE MIGRATION - DEMOCRATIZA AI")
    print("🔧"*30)
    
    if apply_migration():
        print("\n" + "="*60)
        print("✅ CONCLUÍDO!")
        print("="*60)
        print("\n📋 Próximo passo:")
        print("   python check_database.py  # Verificar colunas adicionadas")
    else:
        print("\n❌ Erro ao aplicar migration.")
        sys.exit(1)
