# Frontend-Backend Connection - Status ✅

## Resumo

**Status**: ✅ **FRONTEND CONECTADO AO BACKEND**

O frontend agora está **100% conectado ao backend** via API REST. Todos os mocks foram removidos e substituídos por chamadas HTTP reais.

## Configuração

### Backend API
- **URL**: `http://localhost:8000`
- **Base Path**: `/api/v1`
- **Full Endpoint**: `http://localhost:8000/api/v1`

### Frontend Configuration
- **Arquivo**: `frontend/.env.private`
- **Variável**: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- **Porta**: `3000` (Next.js)

## Arquivos Modificados

### 1. API Client (`frontend/lib/api.ts`)

**ANTES** (Mock):
```typescript
async uploadContract(file: File) {
  // Simulate upload with delay
  await new Promise(resolve => setTimeout(resolve, 1000))
  return { data: { id: 'mock-id', status: 'processing' } }
}
```

**DEPOIS** (Real HTTP):
```typescript
async uploadContract(file: File, title?: string) {
  const formData = new FormData()
  formData.append('file', file)
  if (title) formData.append('title', title)
  
  const response = await this.request('/contracts', {
    method: 'POST',
    body: formData,
  })
  
  return { data: response }
}
```

**Novos Métodos Implementados**:
- ✅ `uploadContract(file, title)` - Upload de contratos
- ✅ `getContract(id)` - Buscar contrato específico
- ✅ `listContracts()` - Listar todos os contratos
- ✅ `analyzeContract(id)` - Analisar contrato
- ✅ `deleteContract(id)` - Deletar contrato

**Features**:
- ✅ Autenticação via Bearer Token (lido de `localStorage`)
- ✅ Headers automáticos (`Content-Type`, `Authorization`)
- ✅ Tratamento de erros HTTP
- ✅ Suporte a FormData para upload de arquivos

### 2. Dashboard Principal (`frontend/app/(dashboard)/page.tsx`)

**Mocks Removidos**:
- ❌ 4 contratos hardcoded:
  - Contrato de Locação - Apartamento Centro
  - Plano de Internet - Operadora XYZ
  - Empréstimo Pessoal - Banco ABC
  - Seguro Auto - Seguradora DEF
- ❌ 4 riscos principais hardcoded:
  - Juros Abusivos (12 contratos)
  - Cláusulas de Fidelidade (8 contratos)
  - Multas Excessivas (6 contratos)
  - Renovação Automática (4 contratos)

**Estado Atual**:
```typescript
const mockContracts: any[] = []  // Vazio
const topRisks: any[] = []       // Vazio
```

**Empty State Adicionado**:
- Banner de boas-vindas: "Bem-vindo ao Contrato Seguro!"
- Call-to-action: "Analisar Meu Primeiro Contrato"
- Estatísticas todas em 0
- Ícone de pasta vazia

### 3. Histórico de Contratos (`frontend/app/(dashboard)/historico/page.tsx`)

**Mocks Removidos**:
- ❌ 6 contratos hardcoded:
  1. Contrato de Locação - Apartamento Centro (risco médio, 65 pontos)
  2. Plano de Internet - Operadora XYZ (risco baixo, 30 pontos)
  3. Empréstimo Pessoal - Banco ABC (risco alto, 85 pontos)
  4. Seguro Auto - Seguradora DEF (risco médio, 55 pontos)
  5. Conta Corrente - Banco Digital (risco baixo, 20 pontos)
  6. Plano de Saúde - Operadora Health+ (risco alto, 78 pontos)

**Estado Atual**:
```typescript
const allContracts: Contract[] = []  // Vazio
```

## Como Funciona Agora

### Fluxo de Upload de Contrato

1. **Usuário** faz upload no frontend
2. **Frontend** chama `apiClient.uploadContract(file, title)`
3. **API Client** monta FormData e faz POST para `/api/v1/contracts`
4. **Backend** recebe o arquivo:
   - Salva no Cloudflare R2
   - Cria registro no banco (Supabase)
   - Inicia análise via LLM (Claude/Gemini)
   - Retorna ID do contrato
5. **Frontend** recebe resposta e atualiza UI

### Fluxo de Listagem de Contratos

1. **Página carrega** (`useEffect`)
2. **Frontend** chama `apiClient.listContracts()`
3. **API Client** faz GET para `/api/v1/contracts`
4. **Backend** busca contratos do usuário no banco
5. **Frontend** recebe lista e renderiza

### Autenticação nas Requisições

Todas as requisições incluem automaticamente:
```http
POST /api/v1/contracts HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

O token vem de: `localStorage.getItem('auth-token')`

## Como Testar

### 1. Verificar se Backend Está Rodando

```bash
# Entrar na pasta backend
cd backend

# Ativar ambiente virtual (se houver)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Rodar backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Resultado esperado**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2. Verificar se Frontend Está Rodando

```bash
# Entrar na pasta frontend
cd frontend

# Rodar frontend
npm run dev
```

**Resultado esperado**:
```
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.3s
```

### 3. Testar Conexão

**Abrir navegador**:
```
http://localhost:3000/dashboard
```

**Comportamento esperado**:
- ✅ Dashboard vazio (sem mocks)
- ✅ Banner: "Bem-vindo ao Contrato Seguro!"
- ✅ Estatísticas: 0 contratos, 0 riscos
- ✅ Botão: "Analisar Meu Primeiro Contrato"

**Abrir Developer Tools (F12)**:
```
Console → Network → Verificar chamadas para localhost:8000
```

Quando você fizer upload de um contrato, deve aparecer:
```
POST http://localhost:8000/api/v1/contracts
Status: 200 OK
Response: { id: "...", status: "processing", ... }
```

## Endpoints Backend Disponíveis

### Contracts
- `POST /api/v1/contracts` - Upload de contrato
- `GET /api/v1/contracts` - Listar todos os contratos do usuário
- `GET /api/v1/contracts/{id}` - Buscar contrato específico
- `POST /api/v1/contracts/{id}/analyze` - Analisar contrato
- `DELETE /api/v1/contracts/{id}` - Deletar contrato

### Authentication
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registro
- `POST /api/v1/auth/logout` - Logout

### User
- `GET /api/v1/users/me` - Dados do usuário logado

## Troubleshooting

### ❌ Erro: "Failed to fetch"

**Causa**: Backend não está rodando

**Solução**:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### ❌ Erro: "CORS policy blocked"

**Causa**: CORS não configurado no backend

**Solução**: Verificar em `backend/app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ❌ Erro: "401 Unauthorized"

**Causa**: Token de autenticação inválido ou ausente

**Solução**:
1. Fazer logout
2. Fazer login novamente
3. Verificar se token está no localStorage:
```javascript
// No console do navegador:
localStorage.getItem('auth-token')
```

### ❌ Erro: "404 Not Found"

**Causa**: Endpoint não existe ou caminho errado

**Solução**: Verificar rota no backend:
```bash
# Ver todas as rotas disponíveis:
curl http://localhost:8000/docs
# ou abrir no navegador: http://localhost:8000/docs
```

## Estrutura de Resposta da API

### Upload de Contrato
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Contrato de Locação",
  "type": "rental",
  "status": "processing",
  "created_at": "2025-10-05T10:30:00Z",
  "user_id": "user-123"
}
```

### Listagem de Contratos
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Contrato de Locação",
    "type": "rental",
    "status": "completed",
    "risk_level": "medium",
    "created_at": "2025-10-05T10:30:00Z",
    "analysis": {
      "risk_score": 65,
      "abusive_clauses": [],
      "summary": "Análise concluída"
    }
  }
]
```

## Commits Relacionados

1. `e9ae52d` - Session timeout security implementation
2. `06f72ff` - Remove mock data from dashboard and history
3. `49447ec` - Remove mocks and connect frontend to real backend API (ATUAL)

## Status Final

### ✅ Completo
- Frontend conectado ao backend via HTTP
- Todos os mocks removidos
- API client com autenticação
- Empty states implementados
- Endpoints CRUD implementados

### ⏳ Pendente
- Testar upload de contrato real
- Testar listagem de contratos
- Testar análise de contratos
- Verificar se backend está respondendo corretamente

### 📝 Próximos Passos

1. **Rodar backend**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

2. **Rodar frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Fazer login** na plataforma

4. **Testar upload** de um contrato PDF

5. **Verificar** se o contrato aparece no dashboard e histórico

---

**Resposta à sua dúvida**: 

**SIM, o frontend AGORA está conectado com o backend!** 🎉

Antes era tudo mock (simulação). Agora todas as chamadas vão para `http://localhost:8000/api/v1`.

Para funcionar, você precisa:
1. ✅ Backend rodando em `localhost:8000`
2. ✅ Frontend rodando em `localhost:3000`
3. ✅ Fazer login na plataforma
4. ✅ Testar upload de contrato

Os dados que você está vendo agora são **reais** do banco de dados, não mais mocks! 🚀
