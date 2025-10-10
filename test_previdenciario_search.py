"""
Teste rápido de busca semântica sobre direito previdenciário
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

async def test_previdenciario():
    print("\n" + "="*70)
    print("🔍 TESTE: BUSCA SEMÂNTICA - DIREITO PREVIDENCIÁRIO")
    print("="*70)
    
    # Setup database
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    
    rag = get_rag_service()
    
    # Queries de teste
    queries = [
        "aposentadoria por idade requisitos",
        "pensão por morte dependentes",
        "aposentadoria especial condições insalubres",
        "reforma da previdência idade mínima"
    ]
    
    for query in queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 70)
        
        # Gerar embedding da query
        query_embedding = await rag.generate_embeddings([query])
        
        # Buscar documentos similares diretamente
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    content,
                    metadata,
                    1 - (embedding <=> :query_embedding::vector) as similarity
                FROM knowledge_base
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> :query_embedding::vector
                LIMIT 2
            """), {"query_embedding": str(query_embedding[0])})
            
            for i, row in enumerate(result, 1):
                similarity = row.similarity
                content = row.content
                metadata = row.metadata or {}
                
                source = metadata.get("source", "N/A")
                article = metadata.get("article", "N/A")
                
                print(f"\n  {i}. Similaridade: {similarity:.4f}")
                print(f"     Fonte: {source}")
                print(f"     Artigo: {article}")
                print(f"     Conteúdo: {content[:150]}...")
    
    print("\n" + "="*70)
    print("✅ Teste de busca previdenciária concluído!")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(test_previdenciario())
