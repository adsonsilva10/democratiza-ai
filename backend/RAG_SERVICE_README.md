# RAG Service - Retrieval-Augmented Generation

## Visão Geral

O RAG Service é o sistema de recuperação aumentada por geração que enriquece os agentes de IA com conhecimento jurídico especializado. Permite que os agentes façam análises mais precisas e fundamentadas em legislação brasileira, jurisprudência e melhores práticas.

## Arquitetura

### Componentes Principais

1. **Vector Database (pg_vector)**: Armazena embeddings de documentos legais
2. **Legal Documents**: Leis, regulamentos, jurisprudência indexada
3. **Knowledge Base**: Diretrizes e melhores práticas
4. **Context Builder**: Constrói contexto relevante para agentes
5. **Search Service**: Busca por similaridade vetorial

### Fluxo de Dados

```
Consulta → Embedding → Busca Vetorial → Contexto → Agente → Análise Enriquecida
```

## Configuração do Banco

### 1. Habilitar pg_vector

```sql
-- No PostgreSQL
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

### Variáveis Necessárias

```env
# OpenAI para embeddings
OPENAI_API_KEY=sk-your-openai-key

# Database com pg_vector
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db

# Claude para análise
CLAUDE_API_KEY=your-claude-key
```

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