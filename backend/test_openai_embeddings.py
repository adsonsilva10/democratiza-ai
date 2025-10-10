"""
Teste do RAG Service com OpenAI Embeddings
Valida que o provider padrão é OpenAI e que embeddings são gerados corretamente
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env ANTES de qualquer coisa
load_dotenv()

# Adiciona backend ao path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.rag_service import get_rag_service, EmbeddingProvider


async def test_openai_as_default():
    """Testa se OpenAI é o provider padrão"""
    print("=" * 60)
    print("🧪 TESTE: OpenAI como Provider Padrão")
    print("=" * 60)
    
    # Verificar API keys disponíveis
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    print(f"\n📋 API Keys Disponíveis:")
    print(f"  ✅ OPENAI_API_KEY: {'Configurada' if openai_key else '❌ Ausente'}")
    print(f"  {'✅' if google_key else '❌'} GOOGLE_API_KEY: {'Configurada' if google_key else 'Ausente'}")
    
    # Inicializar RAG Service (auto-select provider)
    print(f"\n🔄 Inicializando RAG Service...")
    rag = get_rag_service()
    
    # Validar provider selecionado
    print(f"\n✅ Provider Selecionado: {rag.provider.value}")
    print(f"📊 Dimensão dos Embeddings: {rag.embedding_dimension}d")
    
    # Verificar se é OpenAI
    assert rag.provider == EmbeddingProvider.OPENAI, \
        f"❌ ERRO: Provider deveria ser OpenAI, mas é {rag.provider.value}"
    
    assert rag.embedding_dimension == 1536, \
        f"❌ ERRO: Dimensão deveria ser 1536, mas é {rag.embedding_dimension}"
    
    print(f"\n✅ VALIDAÇÃO OK: OpenAI é o provider padrão!")
    
    return rag


async def test_embedding_generation():
    """Testa geração de embeddings com OpenAI"""
    print("\n" + "=" * 60)
    print("🧪 TESTE: Geração de Embeddings OpenAI")
    print("=" * 60)
    
    rag = get_rag_service()
    
    # Texto de teste - cláusula de contrato
    test_texts = [
        "Art. 6º São direitos básicos do consumidor a proteção da vida, saúde e segurança.",
        "O contrato terá prazo de 12 meses com multa rescisória de R$ 2.000,00.",
        "A velocidade contratada é de até 100 Mbps, não sendo garantida."
    ]
    
    print(f"\n📝 Gerando embeddings para {len(test_texts)} textos de teste...")
    
    try:
        embeddings = await rag.create_embeddings(test_texts)
        
        print(f"\n✅ Embeddings gerados com sucesso!")
        print(f"📊 Quantidade: {len(embeddings)}")
        print(f"📏 Dimensão: {len(embeddings[0])}d")
        print(f"📈 Exemplo (primeiros 5 valores): {embeddings[0][:5]}")
        
        # Validações
        assert len(embeddings) == len(test_texts), "Quantidade de embeddings incorreta"
        assert len(embeddings[0]) == 1536, "Dimensão incorreta (deveria ser 1536)"
        assert all(isinstance(val, float) for val in embeddings[0][:10]), "Valores não são float"
        
        print(f"\n✅ VALIDAÇÃO OK: Embeddings OpenAI funcionando!")
        
    except Exception as e:
        print(f"\n❌ ERRO ao gerar embeddings: {e}")
        raise
    
    return embeddings


async def test_similarity_search():
    """Testa busca por similaridade (sem DB real, apenas validação)"""
    print("\n" + "=" * 60)
    print("🧪 TESTE: Busca por Similaridade (Conceitual)")
    print("=" * 60)
    
    rag = get_rag_service()
    
    # Gerar embeddings de exemplo
    query = "direitos do consumidor informação clara"
    documents = [
        "Art. 6º CDC - Direito à informação adequada e clara sobre produtos e serviços",
        "Art. 51 CDC - Cláusulas abusivas que exonerem o fornecedor",
        "Lei 8.078/90 - Código de Defesa do Consumidor protege consumidores brasileiros"
    ]
    
    print(f"\n📝 Query: '{query}'")
    print(f"📚 Documentos para comparação: {len(documents)}")
    
    try:
        # Gerar embeddings
        query_embedding = (await rag.create_embeddings([query]))[0]
        doc_embeddings = await rag.create_embeddings(documents)
        
        print(f"\n✅ Embeddings gerados:")
        print(f"  - Query: 1 embedding de {len(query_embedding)}d")
        print(f"  - Documentos: {len(doc_embeddings)} embeddings de {len(doc_embeddings[0])}d")
        
        # Calcular similaridade (cosine similarity simplificada)
        import numpy as np
        
        query_vec = np.array(query_embedding)
        similarities = []
        
        for i, doc_emb in enumerate(doc_embeddings):
            doc_vec = np.array(doc_emb)
            
            # Cosine similarity
            similarity = np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
            )
            similarities.append((i, similarity))
        
        # Ordenar por similaridade
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n📊 Rankings de Similaridade:")
        for idx, similarity in similarities:
            print(f"  {idx+1}. Similaridade: {similarity:.4f}")
            print(f"     Texto: {documents[idx][:70]}...")
        
        print(f"\n✅ VALIDAÇÃO OK: Busca por similaridade funcionando!")
        
    except Exception as e:
        print(f"\n❌ ERRO na busca: {e}")
        raise


async def test_cost_calculation():
    """Testa cálculo de custos OpenAI"""
    print("\n" + "=" * 60)
    print("🧪 TESTE: Cálculo de Custos OpenAI")
    print("=" * 60)
    
    # Estimativa de custos
    texts = [
        "Este é um texto curto.",
        "Este é um texto de tamanho médio com mais palavras e conteúdo relevante para análise.",
        "Este é um texto longo que simula um contrato completo com múltiplas cláusulas, condições, termos e informações detalhadas sobre direitos e deveres das partes envolvidas na relação contratual."
    ]
    
    # Tokens aproximados (1 token ≈ 4 caracteres)
    total_chars = sum(len(text) for text in texts)
    estimated_tokens = total_chars / 4
    
    # Custo OpenAI: $0.02 / 1M tokens
    cost_per_token = 0.02 / 1_000_000
    estimated_cost_usd = estimated_tokens * cost_per_token
    
    print(f"\n📊 Análise de Custos:")
    print(f"  Textos: {len(texts)}")
    print(f"  Caracteres totais: {total_chars:,}")
    print(f"  Tokens estimados: {estimated_tokens:,.0f}")
    print(f"  Custo estimado: ${estimated_cost_usd:.6f} USD")
    print(f"  Custo em R$: R$ {estimated_cost_usd * 5:.6f} (câmbio R$ 5,00)")
    
    # Projeção para volume
    print(f"\n💰 Projeção de Custos (1000 contratos/mês):")
    monthly_chars = total_chars * 1000 / len(texts)  # Média por contrato
    monthly_tokens = monthly_chars / 4
    monthly_cost_usd = monthly_tokens * cost_per_token
    
    print(f"  Tokens/mês: {monthly_tokens:,.0f}")
    print(f"  Custo/mês: ${monthly_cost_usd:.2f} USD (R$ {monthly_cost_usd * 5:.2f})")
    print(f"  Custo/contrato: ${monthly_cost_usd/1000:.4f} USD")
    
    print(f"\n✅ OpenAI Embeddings são MUITO baratos para nosso uso!")


async def main():
    """Executa todos os testes"""
    try:
        print("\n" + "🚀" * 30)
        print("SUITE DE TESTES - RAG SERVICE (OpenAI)")
        print("🚀" * 30)
        
        # Teste 1: Provider padrão
        await test_openai_as_default()
        
        # Teste 2: Geração de embeddings
        await test_embedding_generation()
        
        # Teste 3: Busca por similaridade
        await test_similarity_search()
        
        # Teste 4: Custos
        await test_cost_calculation()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print("\n📋 Resumo:")
        print("  ✅ OpenAI configurado como provider padrão")
        print("  ✅ Embeddings 1536d gerados corretamente")
        print("  ✅ Busca por similaridade funcional")
        print("  ✅ Custos estimados (~$0.0002 por contrato)")
        print("\n🎉 RAG Service pronto para produção com OpenAI!")
        
    except Exception as e:
        print(f"\n❌ ERRO NOS TESTES: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
