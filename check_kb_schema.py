"""
Verificar schema real da tabela knowledge_base no Supabase
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

print("\n" + "="*70)
print("🔍 SCHEMA DA TABELA knowledge_base")
print("="*70)

inspector = inspect(engine)

if "knowledge_base" in inspector.get_table_names():
    print("\n✅ Tabela 'knowledge_base' existe")
    
    columns = inspector.get_columns("knowledge_base")
    print(f"\n📋 Colunas ({len(columns)} total):")
    for col in columns:
        nullable = "NULL" if col["nullable"] else "NOT NULL"
        default = f" DEFAULT {col['default']}" if col.get("default") else ""
        print(f"   • {col['name']:<25} {col['type']!s:<30} {nullable}{default}")
    
    indexes = inspector.get_indexes("knowledge_base")
    if indexes:
        print(f"\n📊 Índices ({len(indexes)} total):")
        for idx in indexes:
            print(f"   • {idx['name']:<35} em {idx['column_names']}")
    
    # Verificar conteúdo
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM knowledge_base"))
        count = result.scalar()
        print(f"\n📈 Total de registros: {count}")
        
        if count > 0:
            result = conn.execute(text("SELECT * FROM knowledge_base LIMIT 1"))
            sample = result.fetchone()
            print(f"\n📄 Exemplo de registro:")
            for key, value in zip(result.keys(), sample):
                print(f"   {key}: {value}")
else:
    print("\n❌ Tabela 'knowledge_base' NÃO EXISTE!")
    print("\nTabelas disponíveis:")
    for table in inspector.get_table_names():
        print(f"   • {table}")

print("\n" + "="*70 + "\n")
