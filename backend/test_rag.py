"""
Test script for RAG Service functionality
"""
import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rag_service import rag_service
from app.db.database import AsyncSessionLocal

async def test_rag_service():
    """Test basic RAG Service functionality"""
    
    print("🧪 Testing RAG Service...")
    
    try:
        # Test 1: Create embeddings
        print("\n1️⃣ Testing embedding creation...")
        test_texts = [
            "Este é um contrato de locação residencial",
            "Cláusula de multa compensatória",
            "Direitos do consumidor em telecomunicações"
        ]
        
        embeddings = await rag_service.create_embeddings(test_texts)
        print(f"✅ Created embeddings for {len(embeddings)} texts")
        print(f"   Embedding dimension: {len(embeddings[0])}")
        
        # Test 2: Add knowledge to knowledge base
        print("\n2️⃣ Testing knowledge base addition...")
        async with AsyncSessionLocal() as db:
            
            kb_id = await rag_service.add_knowledge(
                title="Teste de Conhecimento Legal",
                content="Este é um teste de adição de conhecimento jurídico ao sistema RAG. Inclui informações sobre contratos de locação e direitos do consumidor.",
                category="geral",
                subcategory="teste",
                tags=["teste", "rag", "conhecimento"],
                source="teste_automatizado",
                confidence_level=0.8,
                db=db
            )
            
            print(f"✅ Added knowledge entry with ID: {kb_id}")
            
            # Test 3: Search knowledge
            print("\n3️⃣ Testing knowledge search...")
            search_results = await rag_service.search(
                query="contrato de locação multa",
                contract_type="geral",
                limit=3,
                similarity_threshold=0.5,
                db=db
            )
            
            print(f"✅ Found {len(search_results)} results")
            for i, result in enumerate(search_results):
                print(f"   Result {i+1}: {result['title'][:50]}... (Score: {result['similarity_score']:.3f})")
            
            # Test 4: Get knowledge stats
            print("\n4️⃣ Testing knowledge statistics...")
            stats = await rag_service.get_knowledge_stats(db)
            print(f"✅ Knowledge base stats:")
            print(f"   Total entries: {stats['total_entries']}")
            print(f"   Categories: {stats['categories']}")
            print(f"   Embedding dimension: {stats['embedding_dimension']}")
        
        print("\n🎉 All RAG Service tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_legal_document_indexing():
    """Test legal document indexing functionality"""
    
    print("\n📚 Testing Legal Document Indexing...")
    
    try:
        async with AsyncSessionLocal() as db:
            
            # Test document indexing
            doc_id = await rag_service.index_legal_document(
                title="Lei de Teste - Artigo 1º",
                content="""
                Art. 1º Esta é uma lei de teste para verificar o funcionamento do sistema de indexação.
                § 1º O sistema deve processar corretamente este texto.
                § 2º Deve criar chunks apropriados e gerar embeddings.
                § 3º A busca deve encontrar este documento quando relevante.
                
                Art. 2º Este artigo testa a divisão em chunks.
                Parágrafo único. Deve manter a coerência do contexto legal.
                """,
                document_type="lei",
                category="geral",
                source="Sistema de Teste",
                reference_number="Lei Teste/2024 - Art. 1º",
                authority_level="medium",
                legal_area=["teste", "sistema"],
                keywords=["teste", "indexacao", "rag"],
                chunk_size=200,
                chunk_overlap=50,
                db=db
            )
            
            print(f"✅ Indexed legal document with ID: {doc_id}")
            
            # Test advanced search
            print("\n🔍 Testing advanced legal search...")
            legal_results = await rag_service.search_legal_knowledge(
                query="lei teste artigo sistema",
                contract_category="geral",
                document_types=["lei"],
                authority_level="medium",
                limit=5,
                similarity_threshold=0.6,
                db=db
            )
            
            print(f"✅ Advanced search results:")
            print(f"   Legal chunks found: {len(legal_results['legal_chunks'])}")
            print(f"   Knowledge base entries: {len(legal_results['knowledge_base'])}")
            
            # Test context building
            print("\n🏗️  Testing context building for agents...")
            context = await rag_service.build_context_for_agent(
                query="análise de contrato com cláusula de teste",
                contract_type="geral",
                context_type="analysis",
                max_context_length=1000,
                db=db
            )
            
            print(f"✅ Built context for agent:")
            print(f"   Legal framework entries: {len(context['legal_framework'])}")
            print(f"   Jurisprudence entries: {len(context['jurisprudence'])}")
            print(f"   Recommendations: {len(context['recommendations'])}")
            print(f"   Context length: {context['metadata']['context_length']} chars")
        
        print("\n🎉 Legal document indexing tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Legal document test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting RAG Service Tests\n")
    
    # Test basic RAG functionality
    basic_test_passed = await test_rag_service()
    
    if basic_test_passed:
        # Test advanced legal document features
        legal_test_passed = await test_legal_document_indexing()
    else:
        legal_test_passed = False
    
    print("\n" + "="*50)
    print("📊 TEST SUMMARY:")
    print(f"   Basic RAG Service: {'✅ PASSED' if basic_test_passed else '❌ FAILED'}")
    print(f"   Legal Document Indexing: {'✅ PASSED' if legal_test_passed else '❌ FAILED'}")
    
    if basic_test_passed and legal_test_passed:
        print("\n🎉 All tests completed successfully!")
        print("✅ RAG Service is ready for production use!")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())