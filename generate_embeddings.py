"""
Gerar embeddings para todos os documentos na base de conhecimento
"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.services.rag_service import get_rag_service

async def generate_all_embeddings():
    print("\n" + "="*70)
    print("🔄 GERANDO EMBEDDINGS PARA TODA A BASE DE CONHECIMENTO")
    print("="*70)
    
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    rag = get_rag_service()
    
    print(f"\n📊 Provider: {rag.provider.value}")
    print(f"📏 Dimensão: {rag.embedding_dimension}d")
    
    # Buscar todos os documentos sem embedding
    result = session.execute(text("""
        SELECT id, content 
        FROM knowledge_base 
        WHERE embedding IS NULL
        ORDER BY created_at
    """))
    
    documents = result.fetchall()
    total = len(documents)
    
    print(f"\n📚 Documentos sem embeddings: {total}")
    
    if total == 0:
        print("✅ Todos os documentos já têm embeddings!")
        return
    
    print(f"\n🔄 Processando...")
    
    processed = 0
    for doc_id, content in documents:
        try:
            # Gerar embedding
            embeddings = await rag.create_embeddings([content])
            embedding_vector = embeddings[0]
            
            # Converter para string format do PostgreSQL
            vector_str = '[' + ','.join(map(str, embedding_vector)) + ']'
            
            # Atualizar no banco - usando f-string para evitar escape de ::
            with engine.connect() as conn:
                sql = f"UPDATE knowledge_base SET embedding = '{vector_str}'::vector WHERE id = '{str(doc_id)}'"
                conn.execute(text(sql))
                conn.commit()
            
            processed += 1
            print(f"   ✅ {processed}/{total} - {str(doc_id)[:8]}...")
            
        except Exception as e:
            print(f"   ❌ Erro no documento {doc_id}: {e}")
            session.rollback()
    
    session.close()
    
    print(f"\n✅ {processed}/{total} embeddings gerados com sucesso!")
    
    # Verificar total final
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(embedding) as with_embedding
            FROM knowledge_base
        """))
        row = result.fetchone()
        print(f"\n📊 Status Final:")
        print(f"   Total de documentos: {row.total}")
        print(f"   Com embeddings: {row.with_embedding}")
        print(f"   Sem embeddings: {row.total - row.with_embedding}")
    
    print("\n" + "="*70)
    print("✅ EMBEDDINGS GERADOS!")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(generate_all_embeddings())
