"""
Script para resetar migrations do Alembic no Supabase
Limpa a tabela alembic_version e permite aplicar migrations do zero
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


def reset_migrations():
    """Remove histórico de migrations antigas"""
    
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    if not database_url:
        print("❌ DATABASE_URL não configurado!")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🔄 RESET DE MIGRATIONS")
    print("="*60)
    print(f"\n📊 Database: {database_url[:50]}...")
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Verificar se tabela alembic_version existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'alembic_version'
                )
            """))
            exists = result.scalar()
            
            if not exists:
                print("✅ Tabela alembic_version não existe (banco limpo)")
                return True
            
            # Ver versões atuais
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            versions = [row[0] for row in result.fetchall()]
            
            if versions:
                print(f"\n⚠️  Versões de migration encontradas:")
                for v in versions:
                    print(f"   - {v}")
                
                print("\n❓ Deseja remover todas as versões antigas? (s/n): ", end="")
                confirm = input().strip().lower()
                
                if confirm == 's':
                    # Deletar todas as versões
                    conn.execute(text("DELETE FROM alembic_version"))
                    conn.commit()
                    print("\n✅ Histórico de migrations limpo!")
                    print("   Agora você pode executar: python setup_database.py")
                    return True
                else:
                    print("\n❌ Operação cancelada.")
                    return False
            else:
                print("✅ Nenhuma versão de migration encontrada (já limpo)")
                return True
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def drop_all_tables():
    """Remove TODAS as tabelas (cuidado!)"""
    
    database_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    
    print("\n" + "="*60)
    print("⚠️  DROP ALL TABLES (CUIDADO!)")
    print("="*60)
    print("\n🚨 Esta operação vai DELETAR todas as tabelas!")
    print("   Isso inclui: users, contracts, chat_messages, audit_logs")
    print("\n❓ Tem CERTEZA que deseja continuar? (digite 'SIM' em maiúsculas): ", end="")
    
    confirm = input().strip()
    
    if confirm != "SIM":
        print("\n✅ Operação cancelada (bom!).")
        return False
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Pegar todas as tabelas
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if not tables:
                print("\n✅ Nenhuma tabela encontrada.")
                return True
            
            print(f"\n📋 Tabelas a serem removidas ({len(tables)}):")
            for table in tables:
                print(f"   - {table}")
            
            # Drop em cascata
            for table in tables:
                print(f"   Removendo {table}...")
                conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
            
            conn.commit()
            print("\n✅ Todas as tabelas foram removidas!")
            print("   Execute: python setup_database.py para recriar")
            return True
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Menu principal"""
    print("\n" + "🔧"*30)
    print("RESET DE MIGRATIONS - DEMOCRATIZA AI")
    print("🔧"*30)
    print("\nEscolha uma opção:")
    print("  1. Limpar histórico de migrations (recomendado)")
    print("  2. Drop de todas as tabelas (CUIDADO!)")
    print("  3. Cancelar")
    print("\nOpção: ", end="")
    
    choice = input().strip()
    
    if choice == "1":
        reset_migrations()
    elif choice == "2":
        drop_all_tables()
    else:
        print("\n✅ Cancelado.")


if __name__ == "__main__":
    main()
