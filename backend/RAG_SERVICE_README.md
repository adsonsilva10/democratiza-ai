# RAG Service - Retrieval-Augmented Generation Multi-Provider

## Visão Geral

O RAG Service é o sistema de recuperação aumentada por geração que enriquece os agentes de IA com conhecimento jurídico especializado. Implementa uma **arquitetura multi-provider** que permite usar diferentes serviços de embeddings (Gemini, OpenAI, Anthropic) com fallback automático.

**✨ Novidade**: Implementação multi-provider com suporte a Google Gemini (gratuito), OpenAI (alta qualidade) e Anthropic/Voyage AI (especializado em domínio legal).

## Arquitetura Multi-Provider

### Componentes Principais

1. **Vector Database (pg_vector)**: Armazena embeddings de documentos legais
2. **Multi-Provider Engine**: Sistema de embeddings com fallback automático
3. **Legal Documents**: Leis, regulamentos, jurisprudência indexada
4. **Knowledge Base**: Diretrizes e melhores práticas
5. **Context Builder**: Constrói contexto relevante para agentes
6. **Search Service**: Busca por similaridade vetorial

### Providers Disponíveis

#### 🥇 Google Gemini (Default)
- **Modelo**: `models/embedding-001`
- **Dimensões**: 768
- **Custo**: Gratuito (com limites)
- **Vantagens**: 
  - Ótimo para português brasileiro
  - Gratuito no free tier
  - Boa performance em textos jurídicos
- **Limites Free Tier**:
  - 1,500 requests/dia
  - 15 requests/minuto
- **Status**: ✅ Implementado e testado

#### 🥈 OpenAI (Fallback)
- **Modelo**: `text-embedding-3-small`
- **Dimensões**: 1536
- **Custo**: Pago ($0.02 / 1M tokens)
- **Vantagens**:
  - Melhor qualidade geral
  - Mais dimensões (1536)
  - API estável e rápida
- **Status**: ✅ Implementado, aguardando OPENAI_API_KEY

#### 🥉 Anthropic/Voyage AI (Futuro)
- **Modelo**: Voyage AI (especializado)
- **Dimensões**: 1024
- **Custo**: A definir
- **Vantagens**:
  - Especializado em domínio legal
  - Alta precisão para contratos
- **Status**: 🔄 Placeholder implementado

### Fluxo de Dados

```
Consulta → [Provider Selection] → Embedding → Busca Vetorial → Contexto → Agente → Análise Enriquecida
                ↓
         Gemini > OpenAI > Anthropic
```

### Auto-Seleção de Provider

O sistema seleciona automaticamente o melhor provider disponível:

```python
Priority Chain:
1. Gemini (se GOOGLE_API_KEY disponível) → Free + Bom para PT-BR
2. OpenAI (se OPENAI_API_KEY disponível) → Melhor qualidade
3. Anthropic (placeholder) → Futuro especializado

Fallback automático se quota excedida ou API indisponível
```

## Configuração do Banco

### 1. Habilitar pg_vector

```sql
-- No PostgreSQL (Supabase)
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Executar Migrations

```bash
cd backend
alembic upgrade head
```

### 3. Verificar Tabelas

- `legal_documents`: Documentos legais completos
- `legal_chunks`: Chunks dos documentos com embeddings
- `knowledge_base`: Diretrizes e melhores práticas

## Configuração de Ambiente

### Variáveis de API Keys

O sistema suporta múltiplos providers. Configure pelo menos um:

```env
# Opção 1: Google Gemini (Recomendado para começar - FREE)
GOOGLE_API_KEY=your_google_api_key_here

# Opção 2: OpenAI (Melhor qualidade - PAGO)
OPENAI_API_KEY=your_openai_api_key_here

# Opção 3: Anthropic (Futuro - especializado legal)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Como Obter API Keys

#### Google Gemini (Gratuito)
1. Acesse: https://makersuite.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a key e adicione no `.env`
4. **Limites Free**: 1,500 requests/dia, 15/minuto

#### OpenAI (Pago)
1. Acesse: https://platform.openai.com/api-keys
2. Clique em "Create new secret key"
3. Copie a key e adicione no `.env`
4. **Custo**: ~$0.02 por 1M tokens

#### Anthropic (Futuro)
1. Em breve: integração com Voyage AI
2. Embeddings especializados em documentos legais

## Instalação de Dependências

### Pacotes Python Necessários

```bash
# Instalar todos os providers
pip install google-generativeai anthropic openai

# Ou apenas o que você vai usar:
pip install google-generativeai  # Para Gemini
pip install openai                # Para OpenAI
pip install anthropic             # Para Anthropic (futuro)
```

### Verificar Instalação

```python
# Test script
python -c "import google.generativeai; import anthropic; print('✅ Packages OK')"
```

## Uso Programático

### Exemplo Básico - Auto-Seleção de Provider

```python
from app.services.rag_service import get_rag_service

# O sistema escolhe automaticamente o melhor provider disponível
rag = get_rag_service()

# Criar embeddings
texts = [
    "Contrato de locação com cláusula abusiva",
    "Multa por rescisão antecipada de 3 meses"
]

embeddings = await rag.create_embeddings(texts)
print(f"Provider usado: {rag.provider}")  # gemini, openai ou anthropic
print(f"Dimensões: {len(embeddings[0])}")  # 768, 1536 ou 1024
```

### Exemplo Avançado - Provider Específico

```python
from app.services.rag_service import RAGService, EmbeddingProvider

# Forçar uso do Gemini
rag_gemini = RAGService(provider=EmbeddingProvider.GEMINI)

# Forçar uso do OpenAI (se disponível)
rag_openai = RAGService(provider=EmbeddingProvider.OPENAI)

# Verificar qual provider está ativo
print(f"Provider: {rag_gemini.provider.value}")
print(f"Model: {rag_gemini.embedding_model}")
print(f"Dimensions: {rag_gemini.embedding_dimension}")
```

### Busca Semântica com RAG

```python
from app.services.rag_service import get_rag_service
from app.db.session import get_session

async def search_legal_knowledge():
    rag = get_rag_service()
    
    async with get_session() as db:
        results = await rag.search_legal_knowledge(
            query="cláusulas abusivas em contratos de locação",
            contract_category="locacao",
            document_types=["lei", "jurisprudencia"],
            authority_level="high",
            limit=10,
            similarity_threshold=0.75,
            db=db
        )
    
    print(f"Found {len(results['legal_chunks'])} relevant chunks")
    for chunk in results['legal_chunks']:
        print(f"- {chunk.content[:100]}... (similarity: {chunk.similarity:.2f})")
```

### Tratamento de Erros e Fallback

```python
from app.services.rag_service import get_rag_service
from google.api_core.exceptions import ResourceExhausted

async def safe_embedding_creation(texts):
    """Criação de embeddings com tratamento de quota"""
    rag = get_rag_service()
    
    try:
        embeddings = await rag.create_embeddings(texts)
        return embeddings
    
    except ResourceExhausted:
        # Quota do Gemini excedida
        print("⚠️ Gemini quota exceeded, sistema tentará fallback automático")
        
        # Se tiver OpenAI configurado, o sistema usa automaticamente
        # Caso contrário, você pode configurar OpenAI:
        # 1. Adicione OPENAI_API_KEY no .env
        # 2. Reinicie o serviço
        # 3. Sistema fará fallback automaticamente
        
        raise Exception("Configure OPENAI_API_KEY para fallback automático")
```

## Comparação de Providers

### Performance Benchmark

| Provider | Dimensões | Custo/1M tokens | Tempo/embed | Qualidade PT-BR |
|----------|-----------|-----------------|-------------|-----------------|
| **Gemini** | 768 | 🆓 Gratuito* | ~0.3s | ⭐⭐⭐⭐ Excelente |
| **OpenAI** | 1536 | $0.02 | ~0.1s | ⭐⭐⭐⭐⭐ Superior |
| **Anthropic** | 1024 | TBD | TBD | ⭐⭐⭐⭐⭐ Legal-specific |

*Sujeito a limites: 1,500/dia, 15/minuto no free tier

### Quando Usar Cada Provider

#### Use Gemini quando:
- ✅ Começando o projeto (gratuito)
- ✅ Desenvolvimento e testes
- ✅ Volume moderado (< 1,500 requests/dia)
- ✅ Textos em português brasileiro
- ✅ Orçamento limitado

#### Use OpenAI quando:
- ✅ Produção com alto volume
- ✅ Máxima qualidade necessária
- ✅ Orçamento disponível
- ✅ Busca mais precisa
- ✅ Quota do Gemini excedida

#### Use Anthropic quando:
- ✅ Domínio legal específico (futuro)
- ✅ Análise de contratos complexos
- ✅ Necessita embeddings especializados

## Indexação de Conhecimento

### Executar Indexação Inicial

```bash
cd backend
python -m app.workers.legal_indexer
```

### Documentos Incluídos

- Lei do Inquilinato (8.245/91)
- Código de Defesa do Consumidor
- Regulamentação ANATEL
- Código Civil - Contratos
- Jurisprudência STJ relevante

## API Endpoints

### Busca no Knowledge Base

```http
POST /api/v1/contracts/rag/search
Content-Type: application/json

{
  "query": "cláusula de multa contrato locação",
  "contract_category": "locacao", 
  "document_types": ["lei", "jurisprudencia"],
  "authority_level": "high",
  "limit": 10,
  "similarity_threshold": 0.75
}
```

### Análise Enriquecida

```http
POST /api/v1/contracts/{contract_id}/enhanced-analysis
Content-Type: application/json

{
  "contract_text": "texto do contrato...",
  "contract_category": "locacao",
  "analysis_type": "risk_assessment"
}
```

### Precedentes Legais

```http
POST /api/v1/contracts/legal-precedents
Content-Type: application/json

{
  "contract_clause": "multa compensatória três aluguéis",
  "contract_type": "locacao"
}
```

### Estatísticas

```http
GET /api/v1/contracts/rag/stats
```

## Uso nos Agentes

### Integração Básica

```python
from app.agents.rental_agent import RentalAgent
from app.services.rag_service import rag_service

# Criar agente com RAG
agent = RentalAgent(claude_client, rag_service, db_session)

# Análise com contexto enriquecido
analysis = await agent.analyze_contract(contract_text)
```

### Contexto Enriquecido

```python
# Obter contexto legal relevante
enriched_context = await agent.get_enriched_context(
    contract_text, 
    analysis_type="risk_assessment"
)

# Precedentes para cláusula específica
precedents = await agent.get_legal_precedents(
    "cláusula de multa compensatória"
)
```

## Tipos de Análise

### 1. Análise de Risco (`risk_assessment`)
- Identifica cláusulas de alto risco
- Compara com precedentes jurisprudenciais
- Sugere mitigações

### 2. Análise de Conformidade (`compliance_analysis`) 
- Verifica conformidade com legislação
- Identifica cláusulas potencialmente ilegais
- Sugere adequações

### 3. Análise Comparativa (`comparative_analysis`)
- Compara com padrões de mercado
- Identifica cláusulas atípicas
- Sugere melhorias

## Categorias Suportadas

### Contratos de Locação (`locacao`)
- Lei do Inquilinato (8.245/91)
- Jurisprudência específica
- Melhores práticas de mercado

### Telecomunicações (`telecom`)
- Regulamentação ANATEL
- Direitos dos usuários
- Cláusulas típicas abusivas

### Financeiro (`financeiro`)
- Regulamentação BACEN
- Código de Defesa do Consumidor
- Limites legais de juros

### Geral (`geral`)
- Código Civil
- Princípios contratuais
- Direitos fundamentais

## Troubleshooting

### Erro: "Quota exceeded" (Gemini)

**Problema**: Quota do Gemini Free Tier excedida

```
google.api_core.exceptions.ResourceExhausted: 429 You exceeded your current quota
```

**Soluções**:

1. **Opção A - Aguardar reset** (recomendado para dev):
   - Quota diária: Reset à meia-noite (PST)
   - Quota por minuto: Reset após 60 segundos

2. **Opção B - Configurar OpenAI** (recomendado para prod):
   ```bash
   # Adicione no .env
   OPENAI_API_KEY=sk-your-key-here
   
   # Reinicie o serviço
   # Sistema fará fallback automático para OpenAI
   ```

3. **Opção C - Upgrade Gemini** (futuro):
   - Google oferecerá plano pago com quotas maiores

### Erro: "GOOGLE_API_KEY not found"

**Problema**: API key não configurada

**Solução**:
```bash
# 1. Obtenha a key em https://makersuite.google.com/app/apikey
# 2. Adicione no backend/.env
echo "GOOGLE_API_KEY=your_key_here" >> backend/.env

# 3. Reinicie o servidor
cd backend
python -m uvicorn main:app --reload
```

### Erro: "Import google.generativeai could not be resolved"

**Problema**: Pacote não instalado

**Solução**:
```bash
pip install google-generativeai anthropic
```

### Embeddings com Dimensões Erradas

**Problema**: Mistura de embeddings de providers diferentes

**Sintomas**:
- Busca vetorial retorna resultados irrelevantes
- Erro: "dimension mismatch" no pg_vector

**Solução**: Use o script de migração (ver seção abaixo)

### Performance Lenta

**Problema**: Embeddings demorando muito

**Diagnóstico**:
```python
import time
from app.services.rag_service import get_rag_service

rag = get_rag_service()
start = time.time()
await rag.create_embeddings(["test"])
print(f"Time: {time.time() - start:.2f}s")
```

**Soluções**:
- **Gemini**: ~0.3s/embedding (sequencial)
- **OpenAI**: ~0.1s/embedding (batch de 100)
- Para alto volume, use OpenAI

## Melhores Práticas

### 1. Lazy Initialization

```python
# ✅ CORRETO: Usa get_rag_service()
from app.services.rag_service import get_rag_service

rag = get_rag_service()  # Lazy loading
```

```python
# ❌ ERRADO: Importação global
from app.services.rag_service import rag_service  # Antigo, deprecated

# Causará erro se API key não estiver configurada no startup
```

### 2. Batch Processing

```python
# ✅ CORRETO: Processa em batch
texts = [...]  # 100 textos
embeddings = await rag.create_embeddings(texts)  # Uma chamada

# ❌ ERRADO: Um por um
for text in texts:
    emb = await rag.create_embeddings([text])  # 100 chamadas!
```

### 3. Cache de Embeddings

```python
# ✅ CORRETO: Cache em database
async def get_cached_embedding(text: str, db):
    # Verifica se já existe
    cached = await db.query(LegalChunk).filter_by(content=text).first()
    if cached:
        return cached.embedding
    
    # Se não existe, cria e salva
    embedding = await rag.create_embeddings([text])
    chunk = LegalChunk(content=text, embedding=embedding[0])
    db.add(chunk)
    await db.commit()
    return embedding[0]
```

### 4. Tratamento de Erros

```python
# ✅ CORRETO: Try/catch com fallback
try:
    embeddings = await rag.create_embeddings(texts)
except ResourceExhausted:
    # Log erro e tenta provider alternativo
    logger.warning("Gemini quota exceeded")
    # Sistema já tenta fallback automático
    raise
except Exception as e:
    logger.error(f"Embedding error: {e}")
    # Seu código de recuperação aqui
```

### 5. Monitoramento de Quota

```python
# Implementar contador de requests
import redis

async def check_gemini_quota():
    """Verifica se está próximo do limite"""
    r = redis.Redis()
    count = r.incr('gemini_requests_today')
    r.expire('gemini_requests_today', 86400)  # 24h
    
    if count > 1400:  # 93% do limite de 1500
        logger.warning(f"Gemini quota quase excedida: {count}/1500")
        # Mudar para OpenAI
        return False
    return True
```

## Migração Entre Providers

Ver script detalhado em: `backend/scripts/migrate_embeddings.py`

### Cenários de Migração

#### 1. Gemini → OpenAI (Upgrade para Produção)

```bash
# Motivo: Maior qualidade e sem limites de quota
python backend/scripts/migrate_embeddings.py \
    --from gemini \
    --to openai \
    --batch-size 100
```

#### 2. OpenAI → Gemini (Redução de Custos)

```bash
# Motivo: Economizar em ambiente de desenvolvimento
python backend/scripts/migrate_embeddings.py \
    --from openai \
    --to gemini \
    --batch-size 10  # Menor batch por causa do rate limit
```

#### 3. Qualquer → Anthropic (Futu ro - Legal Specific)

```bash
# Quando Voyage AI estiver disponível
python backend/scripts/migrate_embeddings.py \
    --from gemini \
    --to anthropic \
    --batch-size 50
```

### Validação Pós-Migração

```python
# Verificar consistência após migração
from app.services.rag_service import get_rag_service

rag = get_rag_service()

# Test query
results = await rag.search_legal_knowledge(
    query="cláusula abusiva",
    db=db,
    limit=10
)

print(f"Found {len(results['legal_chunks'])} results")
# Se retornar 0 ou resultados irrelevantes, houve problema na migração
```

## Métricas de Qualidade

### Similarity Score
- `> 0.9`: Alta relevância
- `0.7 - 0.9`: Relevância média
- `< 0.7`: Baixa relevância

### Authority Level
- `high`: STF, STJ, Leis federais
- `medium`: TJs, Regulamentos
- `low`: Doutrinas, Pareceres

## Testes

### Executar Testes

```bash
cd backend
python test_rag.py
```

### Verificações

1. ✅ Criação de embeddings
2. ✅ Adição ao knowledge base
3. ✅ Busca por similaridade
4. ✅ Indexação de documentos
5. ✅ Construção de contexto

## Monitoramento

### Métricas Importantes

- Número de documentos indexados
- Tempo de resposta das buscas
- Qualidade dos similarity scores
- Taxa de uso por categoria

### Logs

```bash
# Ver logs do RAG Service
grep "RAGService" backend/logs/app.log

# Ver performance
grep "similarity_search" backend/logs/app.log
```

## Manutenção

### Adicionar Novos Documentos

```python
# Via API ou script
await rag_service.index_legal_document(
    title="Nova Lei - Artigo X",
    content="conteúdo da lei...",
    document_type="lei",
    category="locacao",
    source="Lei X/2024",
    authority_level="high"
)
```

### Atualizar Knowledge Base

```python
# Atualizar entrada existente
await rag_service.update_knowledge(
    knowledge_id="uuid",
    content="novo conteúdo...",
    title="Título Atualizado"
)
```

### Reindexar Documentos

```bash
# Reprocessar todos os documentos
python -m app.workers.legal_indexer --reindex-all
```

## Performance

### Otimizações Implementadas

- Índices IVFFlat para busca vetorial rápida
- Chunking inteligente por parágrafos
- Cache de embeddings
- Busca paralela por tipo de documento

### Configurações Recomendadas

```python
# Configurações ótimas
CHUNK_SIZE = 1000        # Tamanho do chunk
CHUNK_OVERLAP = 200      # Sobreposição
EMBEDDING_DIMENSION = 1536  # OpenAI text-embedding-3-small
SIMILARITY_THRESHOLD = 0.75  # Limite de relevância
```

## Roadmap

### Próximas Funcionalidades

- [ ] Indexação automática de novas leis
- [ ] Cache inteligente de buscas
- [ ] Análise de sentimentos em jurisprudência
- [ ] Integração com sistemas jurídicos externos
- [ ] Dashboard de analytics do RAG
- [ ] Fine-tuning de embeddings específicos

### Melhorias Planejadas

- [ ] Suporte a mais tipos de contrato
- [ ] Análise de precedentes por região
- [ ] Integração com bases de dados jurídicas
- [ ] ML para ranking de relevância
- [ ] API GraphQL para consultas complexas