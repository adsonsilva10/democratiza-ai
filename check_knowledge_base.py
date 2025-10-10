"""
Script para verificar o estado da base de conhecimento jurídico
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Carregar .env
load_dotenv()

def check_knowledge_base():
    """Verifica estado da base de conhecimento"""
    
    print("\n" + "="*60)
    print("📚 VERIFICAÇÃO DA BASE DE CONHECIMENTO JURÍDICO")
    print("="*60)
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL não configurado!")
        return False
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Verificar se tabela existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'knowledge_base'
                )
            """))
            table_exists = result.scalar()
            
            if not table_exists:
                print("\n❌ Tabela 'knowledge_base' NÃO EXISTE!")
                print("   Execute as migrations primeiro.")
                return False
            
            print("\n✅ Tabela 'knowledge_base' existe")
            
            # Contar documentos
            result = conn.execute(text("SELECT COUNT(*) FROM knowledge_base"))
            total_docs = result.scalar()
            
            print(f"\n📊 Total de documentos: {total_docs}")
            
            if total_docs == 0:
                print("\n⚠️  BASE VAZIA! Necessário popular com documentos legais.")
                print("\n📋 Para popular a base, execute:")
                print("   cd backend")
                print("   python legal_bootstrap.py")
                print("   OU")
                print("   python populate_complete_knowledge.py")
                return False
            
            # Estatísticas por categoria
            result = conn.execute(text("""
                SELECT 
                    category,
                    COUNT(*) as count,
                    COUNT(DISTINCT source) as sources
                FROM knowledge_base 
                GROUP BY category
                ORDER BY count DESC
            """))
            
            categories = result.fetchall()
            
            if categories:
                print("\n📂 Documentos por categoria:")
                for cat, count, sources in categories:
                    print(f"   • {cat}: {count} docs ({sources} fontes)")
            
            # Verificar embeddings
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM knowledge_base 
                WHERE embedding IS NOT NULL
            """))
            with_embeddings = result.scalar()
            
            print(f"\n🎯 Documentos com embeddings: {with_embeddings}/{total_docs}")
            
            if with_embeddings < total_docs:
                print(f"   ⚠️  {total_docs - with_embeddings} documentos SEM embeddings!")
                print("   Execute: python populate_complete_knowledge.py --regenerate-embeddings")
            
            # Fontes de legislação
            result = conn.execute(text("""
                SELECT DISTINCT source 
                FROM knowledge_base 
                ORDER BY source
                LIMIT 20
            """))
            sources = [row[0] for row in result.fetchall()]
            
            if sources:
                print(f"\n📖 Fontes de legislação ({len(sources)} primeiras):")
                for source in sources:
                    print(f"   • {source}")
            
            # Data da última atualização
            result = conn.execute(text("""
                SELECT MAX(created_at) 
                FROM knowledge_base
            """))
            last_update = result.scalar()
            
            if last_update:
                print(f"\n🕐 Última atualização: {last_update}")
            
            print("\n" + "="*60)
            if total_docs > 0 and with_embeddings == total_docs:
                print("✅ BASE DE CONHECIMENTO COMPLETA E PRONTA!")
                return True
            else:
                print("⚠️  BASE INCOMPLETA - AÇÃO NECESSÁRIA")
                return False
            
    except Exception as e:
        print(f"\n❌ Erro ao verificar base: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_populate_scripts():
    """Verifica scripts de população disponíveis"""
    
    print("\n" + "="*60)
    print("🔧 SCRIPTS DE POPULAÇÃO DISPONÍVEIS")
    print("="*60)
    
    scripts = [
        ("legal_bootstrap.py", "Bootstrap rápido com dados essenciais"),
        ("populate_complete_knowledge.py", "População completa com toda legislação"),
    ]
    
    backend_path = Path("backend")
    if not backend_path.exists():
        backend_path = Path(".")
    
    for script, desc in scripts:
        script_path = backend_path / script
        if script_path.exists():
            print(f"\n✅ {script}")
            print(f"   {desc}")
            print(f"   Comando: python {script}")
        else:
            print(f"\n❌ {script} NÃO ENCONTRADO")


if __name__ == "__main__":
    print("\n" + "🔍"*30)
    print("DEMOCRATIZA AI - VERIFICAÇÃO DE BASE DE CONHECIMENTO")
    print("🔍"*30)
    
    is_complete = check_knowledge_base()
    check_populate_scripts()
    
    print("\n" + "="*60)
    if is_complete:
        print("✅ TUDO OK! Pode prosseguir com os testes.")
    else:
        print("⚠️  POPULAR BASE ANTES DE TESTAR RAG SERVICE")
        print("\n📋 Passos recomendados:")
        print("  1. cd backend")
        print("  2. python populate_complete_knowledge.py")
        print("  3. python check_knowledge_base.py  # Verificar novamente")
    print("="*60)
    print()
