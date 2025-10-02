# Democratiza AI - Guia Completo de Credenciais

## 🔐 Credenciais Necessárias por Serviço

### 📊 SUPABASE (Database + Auth + Storage)
**Localização**: [https://supabase.com/dashboard](https://supabase.com/dashboard)

**Onde encontrar**:
1. **Project URL**: Dashboard → Settings → API → Project URL
2. **Anon Key**: Dashboard → Settings → API → Project API keys → anon/public
3. **Service Role Key**: Dashboard → Settings → API → Project API keys → service_role (⚠️ SECRETO)
4. **JWT Secret**: Dashboard → Settings → API → JWT Settings → JWT Secret
5. **Database Password**: Definido na criação do projeto

**Substitua em**:
```bash
# Backend
SUPABASE_URL="[SUBSTITUA_SUPABASE_PROJECT_URL]"
SUPABASE_KEY="[SUBSTITUA_SUPABASE_SERVICE_ROLE_KEY]"
SUPABASE_JWT_SECRET="[SUBSTITUA_SUPABASE_JWT_SECRET]"
DATABASE_PASSWORD="[SUBSTITUA_SUPABASE_DB_PASSWORD]"

# Frontend
NEXT_PUBLIC_SUPABASE_URL="[SUBSTITUA_SUPABASE_PROJECT_URL]"
NEXT_PUBLIC_SUPABASE_ANON_KEY="[SUBSTITUA_SUPABASE_ANON_PUBLIC_KEY]"
```

---

### 🤖 ANTHROPIC CLAUDE (AI)
**Localização**: [https://console.anthropic.com/](https://console.anthropic.com/)

**Onde encontrar**:
1. Acesse Console → API Keys
2. Clique "Create Key"
3. Nomeie como "democratiza-ai-production"
4. Copie a chave (formato: `sk-ant-...`)

**Substitua em**:
```bash
# Backend
ANTHROPIC_API_KEY="[SUBSTITUA_ANTHROPIC_API_KEY]"
```

---

### 🔍 GOOGLE CLOUD VISION (OCR)
**Localização**: [https://console.cloud.google.com/](https://console.cloud.google.com/)

**Onde encontrar**:
1. Crie projeto ou selecione existente
2. APIs & Services → Enable APIs → Cloud Vision API
3. Credentials → Create Credentials → Service Account
4. Download JSON key file
5. Copie conteúdo do JSON

**Substitua em**:
```bash
# Backend
GOOGLE_CLOUD_PROJECT_ID="[SUBSTITUA_GCP_PROJECT_ID]"
GOOGLE_APPLICATION_CREDENTIALS_JSON='[SUBSTITUA_COMPLETE_JSON_CONTENT]'
```

---

### ☁️ CLOUDFLARE R2 (File Storage)
**Localização**: [https://dash.cloudflare.com/](https://dash.cloudflare.com/)

**Onde encontrar**:
1. R2 Object Storage → Create bucket → "democratiza-ai-files"
2. Manage R2 API Tokens → Create API Token
3. Permissions: Object Read, Object Write
4. Note: Access Key ID, Secret Access Key
5. Custom Domain (opcional): R2 → Custom Domains

**Substitua em**:
```bash
# Backend
CLOUDFLARE_R2_ACCESS_KEY_ID="[SUBSTITUA_R2_ACCESS_KEY]"
CLOUDFLARE_R2_SECRET_ACCESS_KEY="[SUBSTITUA_R2_SECRET_KEY]"
CLOUDFLARE_R2_BUCKET_NAME="democratiza-ai-files"
CLOUDFLARE_R2_PUBLIC_URL="[SUBSTITUA_R2_PUBLIC_DOMAIN]"

# Frontend
NEXT_PUBLIC_CLOUDFLARE_R2_PUBLIC_URL="[SUBSTITUA_CLOUDFLARE_R2_PUBLIC_DOMAIN]"
```

---

### 📨 AWS SQS (Message Queue)
**Localização**: [https://aws.amazon.com/console/](https://aws.amazon.com/console/)

**Onde encontrar**:
1. SQS → Create Queue → "democratiza-ai-processing"
2. IAM → Users → Create User → "democratiza-ai-sqs"
3. Attach Policy: AmazonSQSFullAccess
4. Security Credentials → Create Access Key
5. Note: Access Key, Secret Key, Queue URL

**Substitua em**:
```bash
# Backend
AWS_ACCESS_KEY_ID="[SUBSTITUA_AWS_ACCESS_KEY]"
AWS_SECRET_ACCESS_KEY="[SUBSTITUA_AWS_SECRET_KEY]"
AWS_REGION="sa-east-1"
AWS_SQS_QUEUE_URL="[SUBSTITUA_SQS_QUEUE_URL]"
```

---

### 📧 SENDGRID (Email)
**Localização**: [https://app.sendgrid.com/](https://app.sendgrid.com/)

**Onde encontrar**:
1. Settings → API Keys → Create API Key
2. Full Access permissions
3. Settings → Sender Authentication → Single Sender Verification
4. Verifique email que será usado como remetente

**Substitua em**:
```bash
# Backend
SENDGRID_API_KEY="[SUBSTITUA_SENDGRID_API_KEY]"
SENDGRID_FROM_EMAIL="[SUBSTITUA_EMAIL_VERIFICADO]"
SENDGRID_FROM_NAME="Democratiza AI"
```

---

### 💳 MERCADO PAGO (Payments)
**Localização**: [https://www.mercadopago.com.br/developers/](https://www.mercadopago.com.br/developers/)

**Onde encontrar**:
1. Suas integrações → Criar aplicação
2. Nome: "Democratiza AI"
3. Credenciais de teste/produção:
   - Public Key (frontend)
   - Access Token (backend)
4. Webhooks → Configurar URL de notificação

**Substitua em**:
```bash
# Backend
MERCADO_PAGO_ACCESS_TOKEN="[SUBSTITUA_MP_ACCESS_TOKEN]"
MERCADO_PAGO_PUBLIC_KEY="[SUBSTITUA_MP_PUBLIC_KEY]"
MERCADO_PAGO_WEBHOOK_SECRET="[SUBSTITUA_MP_WEBHOOK_SECRET]"

# Frontend
NEXT_PUBLIC_MERCADO_PAGO_PUBLIC_KEY="[SUBSTITUA_MERCADO_PAGO_PUBLIC_KEY]"
```

---

### ✍️ D4SIGN (E-signature)
**Localização**: [https://www.d4sign.com.br/](https://www.d4sign.com.br/)

**Onde encontrar**:
1. Painel → Integrações → Chaves de API
2. Gere nova chave para "Democratiza AI"
3. Anote Token Key e Crypt Key

**Substitua em**:
```bash
# Backend
D4SIGN_API_TOKEN="[SUBSTITUA_D4SIGN_TOKEN]"
D4SIGN_CRYPT_KEY="[SUBSTITUA_D4SIGN_CRYPT_KEY]"
D4SIGN_BASE_URL="https://secure.d4sign.com.br/api/v1"
```

---

### 🔐 SECRETS & SECURITY
**Geração Local**:

```bash
# JWT Secrets (use diferentes para dev/prod)
python -c "import secrets; print(secrets.token_urlsafe(64))"

# NextAuth Secret
openssl rand -base64 32
```

**Substitua em**:
```bash
# Backend
SECRET_KEY="[SUBSTITUA_JWT_SECRET_BACKEND]"

# Frontend
NEXTAUTH_SECRET="[SUBSTITUA_NEXTAUTH_SECRET_KEY]"
```

---

### 📈 ANALYTICS (Opcional)
**Google Analytics**: [https://analytics.google.com/](https://analytics.google.com/)
**HotJar**: [https://www.hotjar.com/](https://www.hotjar.com/)
**Sentry**: [https://sentry.io/](https://sentry.io/)

---

## 🚀 Próximos Passos

1. **Obter todas as credenciais** listadas acima
2. **Substituir placeholders** nos arquivos `.env.local` e `.env.production`
3. **Testar conexões** executando o backend com `uvicorn app.main:app --reload`
4. **Configurar Supabase** com as tabelas necessárias
5. **Deploy** quando tudo estiver funcionando

## ⚠️ IMPORTANTE

- **NUNCA** commit arquivos `.env` com credenciais reais
- Use **credenciais de teste** primeiro, depois migre para produção
- Rotacione chaves regularmente
- Monitore logs para vazamentos acidentais de credenciais