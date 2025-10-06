"""Test RAG multi-provider implementation"""
import asyncio
from app.services.rag_service import get_rag_service, EmbeddingProvider

async def test_rag_multiprovider():
    """Test multi-provider RAG service"""
    
    # Get RAG service instance (should auto-select Gemini)
    rag = get_rag_service()
    
    print(f"\n{'='*60}")
    print(f"🔍 RAG Multi-Provider Test")
    print(f"{'='*60}\n")
    
    print(f"✅ Provider selected: {rag.provider}")
    print(f"✅ Embedding model: {rag.embedding_model}")
    print(f"✅ Embedding dimension: {rag.embedding_dimension}")
    
    # Test embedding creation
    test_texts = [
        "Contrato de locação residencial no Brasil",
        "Cláusula abusiva em contrato de telecomunicações",
        "Direitos do consumidor em contratos bancários"
    ]
    
    print(f"\n📝 Testing embeddings with {len(test_texts)} texts...")
    
    try:
        embeddings = await rag.create_embeddings(test_texts)
        print(f"✅ Successfully created {len(embeddings)} embeddings")
        print(f"✅ Embedding shape: {len(embeddings[0])} dimensions")
        print(f"✅ First 5 values of first embedding: {embeddings[0][:5]}")
        
        # Validate dimensions
        if len(embeddings[0]) == rag.embedding_dimension:
            print(f"\n✅ Dimension validation passed!")
        else:
            print(f"\n❌ Dimension mismatch: expected {rag.embedding_dimension}, got {len(embeddings[0])}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating embeddings: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_rag_multiprovider())
    
    if result:
        print(f"\n{'='*60}")
        print(f"🎉 RAG Multi-Provider Implementation: SUCCESS!")
        print(f"{'='*60}\n")
        exit(0)
    else:
        print(f"\n{'='*60}")
        print(f"❌ RAG Multi-Provider Implementation: FAILED")
        print(f"{'='*60}\n")
        exit(1)
