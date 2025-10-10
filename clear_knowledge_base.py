"""
Script para limpar a base de conhecimento e popular com dados completos
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

print("\n" + "="*60)
print("🗑️  LIMPANDO BASE DE CONHECIMENTO")
print("="*60)

with engine.connect() as conn:
    # Verificar total antes
    result = conn.execute(text("SELECT COUNT(*) FROM knowledge_base"))
    before = result.scalar()
    print(f"\n📊 Documentos antes: {before}")
    
    # Limpar
    conn.execute(text("DELETE FROM knowledge_base"))
    conn.commit()
    
    # Verificar total depois
    result = conn.execute(text("SELECT COUNT(*) FROM knowledge_base"))
    after = result.scalar()
    print(f"✅ Documentos depois: {after}")
    
print("\n✅ Base limpa! Pronta para nova população.")
print("="*60 + "\n")
