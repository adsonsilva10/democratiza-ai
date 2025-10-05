# Scripts de Utilitários - Democratiza AI Backend

## Migração de Embeddings

### migrate_embeddings.py

Script para migrar embeddings entre diferentes providers (Gemini ↔ OpenAI ↔ Anthropic).

#### Casos de Uso

##### 1. Upgrade para Produção (Gemini → OpenAI)

Quando seu projeto crescer e você precisar de mais qualidade/volume:

```bash
# Dry run primeiro (recomendado)
python scripts/migrate_embeddings.py \
    --from gemini \
    --to openai \
    --batch-size 100 \
    --dry-run

# Migração real
python scripts/migrate_embeddings.py \
    --from gemini \
    --to openai \
    --batch-size 100
```

**Vantagens**:
- ✅ Maior qualidade de embeddings (1536d vs 768d)
- ✅ Sem limites de quota
- ✅ API mais rápida e estável
- ❌ Custo: ~$0.02 por 1M tokens

##### 2. Redução de Custos (OpenAI → Gemini)

Para economizar em ambiente de desenvolvimento:

```bash
python scripts/migrate_embeddings.py \
    --from openai \
    --to gemini \
    --batch-size 10  # Menor batch devido ao rate limit
```

**Vantagens**:
- ✅ Gratuito (free tier)
- ✅ Bom para português
- ❌ Limites: 1,500/dia, 15/minuto
- ❌ Menos dimensões (768d vs 1536d)

##### 3. Especialização Legal (Qualquer → Anthropic)

Futuro: quando Voyage AI estiver disponível:

```bash
python scripts/migrate_embeddings.py \
    --from gemini \
    --to anthropic \
    --batch-size 50
```

**Vantagens**:
- ✅ Embeddings especializados em domínio legal
- ✅ Melhor performance em contratos
- ⏳ Em desenvolvimento

#### Opções

```bash
Options:
  --from {gemini,openai,anthropic}
                        Source provider
  --to {gemini,openai,anthropic}
                        Target provider
  --batch-size BATCH_SIZE
                        Number of chunks per batch (default: 50)
  --dry-run             Simulate without making changes
  --validate {gemini,openai,anthropic}
                        Validate existing embeddings
  --verbose             Enable verbose logging
```

#### Validação Pós-Migração

Após migrar, valide se tudo está correto:

```bash
# Validar embeddings OpenAI
python scripts/migrate_embeddings.py --validate openai

# Validar embeddings Gemini
python scripts/migrate_embeddings.py --validate gemini
```

**Verificações**:
- ✅ Dimensões corretas
- ✅ Embeddings não-nulos
- ✅ Metadata atualizado
- ✅ Sample de chunks aleatórios

#### Performance

| Migração | Chunks/segundo | Batch Size | Tempo estimado (10k chunks) |
|----------|----------------|------------|------------------------------|
| Gemini → OpenAI | ~10/s | 100 | ~17 min |
| OpenAI → Gemini | ~2/s | 10 | ~83 min |
| Qualquer → Anthropic | ~5/s | 50 | ~33 min |

**Notas**:
- Gemini tem rate limits: máx 15/min no free tier
- OpenAI processa em batch: muito mais rápido
- Script adiciona delay automático para Gemini

#### Troubleshooting

##### Erro: "Quota exceeded" (Gemini)

```
google.api_core.exceptions.ResourceExhausted: 429 You exceeded your current quota
```

**Solução**:
1. Aguarde reset (meia-noite PST para diário, 60s para minuto)
2. Reduza `--batch-size` (tente 5)
3. Use OpenAI como target em vez de Gemini

##### Erro: "Dimension mismatch"

```
ERROR - Dimension mismatch for chunk 123: expected 768, got 1536
```

**Causa**: Chunk já tem embedding do provider errado

**Solução**:
```bash
# Re-migrate forçando
python scripts/migrate_embeddings.py \
    --from openai \
    --to gemini \
    --batch-size 10
# Script sobrescreve embeddings existentes
```

##### Migration Muito Lenta

**Diagnóstico**:
```bash
# Execute com --verbose para ver timing
python scripts/migrate_embeddings.py \
    --from gemini \
    --to openai \
    --verbose
```

**Soluções**:
- Aumente `--batch-size` se usar OpenAI (100-200)
- Diminua `--batch-size` se usar Gemini (5-10)
- Verifique sua conexão com a internet
- Para Gemini: execute fora de horário de pico

#### Metadata de Migração

O script adiciona metadata a cada chunk migrado:

```json
{
  "embedding_provider": "openai",
  "embedding_dimension": 1536,
  "migrated_from": "gemini",
  "migration_date": "2025-10-05T22:30:00"
}
```

**Uso**:
```python
# Filtrar chunks por provider
chunks = await db.query(LegalChunk).filter(
    LegalChunk.metadata['embedding_provider'] == 'openai'
).all()
```

#### Rollback

Se precisar desfazer uma migração:

```bash
# Voltar para provider anterior
python scripts/migrate_embeddings.py \
    --from openai \
    --to gemini
```

**Nota**: Não há rollback automático. O metadata guarda o provider anterior.

#### Melhores Práticas

1. **Sempre faça dry-run primeiro**
   ```bash
   python scripts/migrate_embeddings.py --from X --to Y --dry-run
   ```

2. **Faça backup do banco antes**
   ```bash
   pg_dump -Fc dbname > backup_before_migration.dump
   ```

3. **Valide após migração**
   ```bash
   python scripts/migrate_embeddings.py --validate openai
   ```

4. **Monitore custos (OpenAI)**
   - 10,000 chunks ≈ 500K tokens ≈ $0.01
   - Calcule antes: `num_chunks * avg_chars / 4 * 0.00002`

5. **Considere migração gradual**
   ```python
   # Migre apenas chunks novos
   # Mantenha chunks antigos no provider original
   # Sistema multi-provider suporta ambos simultaneamente
   ```

## Outros Scripts

### (Em desenvolvimento)

Mais scripts de utilitários serão adicionados conforme necessário.
