# ========================================
# 🧹 SCRIPT DE LIMPEZA E CONSOLIDAÇÃO DE .ENV
# ========================================
# Remove arquivos .env duplicados e cria um único master
# Data: 2025-10-10
# ========================================

Write-Host "`n" -NoNewline
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "🧹 CONSOLIDAÇÃO DE ARQUIVOS .ENV" -ForegroundColor Yellow
Write-Host "="*60 -ForegroundColor Cyan

# Diretórios
$root = "c:\Users\adson.silva_contabil\democratiza-ai"
$backend = "$root\backend"
$backendNew = "$root\democratiza-ai\backend"

Write-Host "`n📂 Analisando estrutura..." -ForegroundColor Cyan

# ====================
# PASSO 1: Backup
# ====================
Write-Host "`n🔄 PASSO 1: Criando backups..." -ForegroundColor Yellow

$backupDir = "$root\_env_backups_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -Path $backupDir -ItemType Directory -Force | Out-Null

# Backup de todos os .env encontrados
$envFiles = @(
    "$root\.env",
    "$root\.env.private",
    "$root\.env.llm.example",
    "$backend\.env",
    "$backend\.env.local",
    "$backend\.env.private",
    "$backend\.env.production"
)

foreach ($file in $envFiles) {
    if (Test-Path $file) {
        $fileName = Split-Path $file -Leaf
        $sourceDir = Split-Path $file -Parent | Split-Path -Leaf
        $backupName = "${sourceDir}_${fileName}"
        Copy-Item $file "$backupDir\$backupName" -Force
        Write-Host "  ✅ Backup: $backupName" -ForegroundColor Green
    }
}

Write-Host "`n✅ Backups salvos em: $backupDir" -ForegroundColor Green

# ====================
# PASSO 2: Consolidar
# ====================
Write-Host "`n🔧 PASSO 2: Criando .env MASTER..." -ForegroundColor Yellow

$masterEnv = @"
# ========================================
# 🚀 DEMOCRATIZA AI - CONFIGURAÇÃO MASTER
# ========================================
# Arquivo ÚNICO - Todas as configurações centralizadas
# Última atualização: $(Get-Date -Format 'yyyy-MM-dd HH:mm')
# ========================================

# ========================================
# 🗄️ DATABASE (Supabase)
# ========================================
DATABASE_URL="postgresql://postgres:Morena20.a@db.brrehdlpiimawxiiswzq.supabase.co:5432/postgres"
SUPABASE_DB_URL="postgresql://postgres:Morena20.a@db.brrehdlpiimawxiiswzq.supabase.co:5432/postgres"
SUPABASE_URL="https://brrehdlpiimawxiiswzq.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJycmVoZGxwaWltYXd4aWlzd3pxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNDUwMzAsImV4cCI6MjA3NDkyMTAzMH0.YBxqUB9AXUWq1dptUWgGBB4nIvDLES50Vs8l8A4o_4E"
SUPABASE_SERVICE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJycmVoZGxwaWltYXd4aWlzd3pxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTM0NTAzMCwiZXhwIjoyMDc0OTIxMDMwfQ.yLWjrYfhJ780Dt0ASmePE58Cf4nKNVQOeheFvmUW1kA"
SUPABASE_JWT_SECRET="VJd7jZ0z/1ApnyryCh8QmchewOVTZM2qkGhkYXpLOgQHYsCtywBjesx0EjUn0k5Uqox9kiuWtUOzbMhlsrQong=="

# ========================================
# 🔐 JWT & AUTHENTICATION
# ========================================
SECRET_KEY="_sSHeMX7o_yitMc_gKYSWIw72pkP7BJmH-8X5H2_mMgtmXCQSh0GQWGki9-TRikt2cKiLDZkaLXdqI8h0XvSgQ"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ========================================
# 🤖 AI SERVICES - CHAVES REAIS FUNCIONAIS
# ========================================
# OpenAI (Embeddings - 1536d) ✅ FUNCIONAL
OPENAI_API_KEY="sk-proj-YOUR_OPENAI_KEY_HERE"

# Anthropic Claude (Análises Premium) ✅ FUNCIONAL
ANTHROPIC_API_KEY="sk-ant-api03-YOUR_ANTHROPIC_KEY_HERE"
CLAUDE_MODEL="claude-3-5-sonnet-20240620"
MAX_TOKENS=4000

# Google Gemini (Análises Econômicas + Fallback) ✅ FUNCIONAL
GOOGLE_API_KEY="AIzaSyDerKvFkArJqq524PAeW-1lhCWT7zkJIrI"
GOOGLE_CLOUD_PROJECT_ID="[SUBSTITUA_SE_USAR_VISION_API]"
GOOGLE_APPLICATION_CREDENTIALS="./credentials/gcp-service-account.json"

# ========================================
# 🧠 LLM ROUTER - ROTEAMENTO INTELIGENTE
# ========================================
LLM_COMPLEXITY_THRESHOLD_SIMPLE=5
LLM_COMPLEXITY_THRESHOLD_MEDIUM=12
LLM_COMPLEXITY_THRESHOLD_COMPLEX=20
LLM_MAX_COST_PER_ANALYSIS=0.50
LLM_MONTHLY_BUDGET=500.00
LLM_MAX_RESPONSE_TIME=30
LLM_ENABLE_STREAMING=true
LLM_CACHE_RESPONSES=true
LLM_MIN_CONFIDENCE_SCORE=0.7
LLM_ENABLE_FALLBACK=true
LLM_QUALITY_THRESHOLD=0.8

# ========================================
# 📊 RAG (Retrieval Augmented Generation)
# ========================================
RAG_ENABLE=true
RAG_MAX_DOCUMENTS=5
RAG_SIMILARITY_THRESHOLD=0.7
RAG_EMBEDDING_MODEL="text-embedding-3-small"
RAG_EMBEDDING_PROVIDER="openai"

# ========================================
# ☁️ CLOUDFLARE R2 (File Storage) - CONFIGURAR QUANDO NECESSÁRIO
# ========================================
CLOUDFLARE_R2_ACCOUNT_ID="[SUBSTITUA]"
CLOUDFLARE_R2_ACCESS_KEY_ID="[SUBSTITUA]"
CLOUDFLARE_R2_SECRET_ACCESS_KEY="[SUBSTITUA]"
CLOUDFLARE_R2_BUCKET_NAME="democratiza-ai-contracts"
CLOUDFLARE_R2_PUBLIC_URL="[SUBSTITUA]"

# ========================================
# 📨 AWS SQS (Message Queue) - CONFIGURAR QUANDO NECESSÁRIO
# ========================================
AWS_ACCESS_KEY_ID="[SUBSTITUA]"
AWS_SECRET_ACCESS_KEY="[SUBSTITUA]"
AWS_REGION="sa-east-1"
AWS_SQS_QUEUE_URL="[SUBSTITUA]"

# ========================================
# 📧 SENDGRID (Email) - CONFIGURAR QUANDO NECESSÁRIO
# ========================================
SENDGRID_API_KEY="[SUBSTITUA]"
SENDGRID_FROM_EMAIL="noreply@democratiza.ai"
SENDGRID_FROM_NAME="Democratiza AI"

# ========================================
# 💳 MERCADO PAGO (Payments) - CONFIGURAR QUANDO NECESSÁRIO
# ========================================
MERCADO_PAGO_ACCESS_TOKEN="[SUBSTITUA]"
MERCADO_PAGO_PUBLIC_KEY="[SUBSTITUA]"
MERCADO_PAGO_WEBHOOK_SECRET="[SUBSTITUA]"

# ========================================
# ✍️ D4SIGN (E-signature) - CONFIGURAR QUANDO NECESSÁRIO
# ========================================
D4SIGN_API_KEY="[SUBSTITUA]"
D4SIGN_CRYPTO_KEY="[SUBSTITUA]"
D4SIGN_BASE_URL="https://secure.d4sign.com.br/api/v1"

# ========================================
# ⚙️ APPLICATION SETTINGS
# ========================================
ENVIRONMENT="development"
DEBUG="true"
API_V1_STR="/api/v1"
PROJECT_NAME="Democratiza AI"
BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_MINUTES=1
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES="pdf,jpg,jpeg,png,gif,txt,doc,docx"

# ========================================
# 📊 LOGGING & MONITORING
# ========================================
LOG_LEVEL="INFO"
SENTRY_DSN=""
LLM_ENABLE_METRICS=true
LLM_METRICS_INTERVAL=3600
LLM_COST_ALERTS=true
LLM_PERFORMANCE_ALERTS=true
LLM_DAILY_COST_ALERT=50.00
LLM_HOURLY_REQUEST_LIMIT=100

# ========================================
# 🎨 FRONTEND (Next.js)
# ========================================
NEXT_PUBLIC_APP_NAME="Democratiza AI"
NEXT_PUBLIC_APP_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_SUPABASE_URL="https://brrehdlpiimawxiiswzq.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJycmVoZGxwaWltYXd4aWlzd3pxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNDUwMzAsImV4cCI6MjA3NDkyMTAzMH0.YBxqUB9AXUWq1dptUWgGBB4nIvDLES50Vs8l8A4o_4E"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="_sSHeMX7o_yitMc_gKYSWIw72pkP7BJmH-8X5H2_mMgtmXCQSh0GQWGki9-TRikt2cKiLDZkaLXdqI8h0XvSgQ"

# ========================================
# 📝 STATUS DAS CONFIGURAÇÕES
# ========================================
# ✅ Database: CONECTADO (Supabase + pg_vector)
# ✅ OpenAI: FUNCIONAL (embeddings 1536d)
# ✅ Anthropic: FUNCIONAL (Claude 3.5 Sonnet)
# ✅ Gemini: FUNCIONAL (fallback econômico)
# ⏳ R2: Pendente (configurar quando necessário)
# ⏳ SQS: Pendente (configurar quando necessário)
# ⏳ SendGrid: Pendente (configurar quando necessário)
# ⏳ Mercado Pago: Pendente (configurar quando necessário)
# ⏳ D4Sign: Pendente (configurar quando necessário)
# ========================================
"@

# Criar .env master na raiz
Set-Content -Path "$root\.env" -Value $masterEnv -Force
Write-Host "  ✅ Criado: .env (raiz)" -ForegroundColor Green

# Copiar para backend/
Copy-Item "$root\.env" "$backend\.env" -Force
Write-Host "  ✅ Copiado: backend/.env" -ForegroundColor Green

# Copiar para democratiza-ai/backend/
if (Test-Path $backendNew) {
    Copy-Item "$root\.env" "$backendNew\.env" -Force
    Write-Host "  ✅ Copiado: democratiza-ai/backend/.env" -ForegroundColor Green
}

# ====================
# PASSO 3: Remover duplicatas
# ====================
Write-Host "`n🗑️  PASSO 3: Removendo arquivos duplicados..." -ForegroundColor Yellow

$toRemove = @(
    "$root\.env.private",
    "$root\.env.llm.example",
    "$backend\.env.local",
    "$backend\.env.private",
    "$backend\.env.production"
)

foreach ($file in $toRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        $fileName = Split-Path $file -Leaf
        Write-Host "  ✅ Removido: $fileName" -ForegroundColor Green
    }
}

# ====================
# PASSO 4: Manter apenas exemplos
# ====================
Write-Host "`n📋 PASSO 4: Mantendo arquivos .example..." -ForegroundColor Yellow

$exampleContent = @"
# ========================================
# .ENV.EXAMPLE - TEMPLATE DE CONFIGURAÇÃO
# ========================================
# Copie este arquivo para .env e preencha as credenciais
# Arquivo: .env.example
# ========================================

# Database (Supabase)
DATABASE_URL="postgresql://postgres:[SENHA]@db.[PROJECT_ID].supabase.co:5432/postgres"
SUPABASE_URL="https://[PROJECT_ID].supabase.co"
SUPABASE_ANON_KEY="[ANON_KEY]"
SUPABASE_SERVICE_KEY="[SERVICE_KEY]"
SUPABASE_JWT_SECRET="[JWT_SECRET]"

# AI Services
OPENAI_API_KEY="sk-proj-[SUA_CHAVE]"
ANTHROPIC_API_KEY="sk-ant-[SUA_CHAVE]"
GOOGLE_API_KEY="AIza[SUA_CHAVE]"

# Application
SECRET_KEY="[GERAR_COM_OPENSSL_RAND_BASE64_64]"
ENVIRONMENT="development"
DEBUG="true"

# Ver documentação completa no .env principal
"@

Set-Content -Path "$root\.env.example" -Value $exampleContent -Force
Write-Host "  ✅ Atualizado: .env.example (raiz)" -ForegroundColor Green

Copy-Item "$root\.env.example" "$backend\.env.example" -Force
Write-Host "  ✅ Copiado: backend/.env.example" -ForegroundColor Green

# ====================
# RESUMO
# ====================
Write-Host "`n" -NoNewline
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "✅ CONSOLIDAÇÃO COMPLETA!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Cyan

Write-Host "`n📊 Estrutura Final:" -ForegroundColor Yellow
Write-Host "  📂 democratiza-ai/" -ForegroundColor White
Write-Host "    ├── .env              ✅ MASTER (todas as chaves)" -ForegroundColor Green
Write-Host "    ├── .env.example      📋 Template" -ForegroundColor Gray
Write-Host "    └── backend/" -ForegroundColor White
Write-Host "        ├── .env          ✅ MASTER (cópia sincronizada)" -ForegroundColor Green
Write-Host "        └── .env.example  📋 Template" -ForegroundColor Gray

Write-Host "`n🔐 Credenciais Configuradas:" -ForegroundColor Yellow
Write-Host "  ✅ Database (Supabase + pg_vector)" -ForegroundColor Green
Write-Host "  ✅ OpenAI (embeddings 1536d)" -ForegroundColor Green
Write-Host "  ✅ Anthropic Claude 3.5 Sonnet" -ForegroundColor Green
Write-Host "  ✅ Google Gemini (fallback)" -ForegroundColor Green

Write-Host "`n💾 Backups salvos em:" -ForegroundColor Yellow
Write-Host "  $backupDir" -ForegroundColor Cyan

Write-Host "`n📝 Próximos passos:" -ForegroundColor Yellow
Write-Host "  1. Verificar .gitignore (garantir que .env está ignorado)" -ForegroundColor White
Write-Host "  2. Testar scripts com novo .env unificado" -ForegroundColor White
Write-Host "  3. Commitar apenas .env.example (NUNCA o .env!)" -ForegroundColor White

Write-Host "`n✨ Arquivos .env consolidados com sucesso!" -ForegroundColor Green
Write-Host ""
