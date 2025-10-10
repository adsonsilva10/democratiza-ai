# 🔧 Troubleshooting - Instalação de Dependências

## Problemas Comuns e Soluções

### ❌ Erro: `contains-studio` não encontrado

**Problema**: Pacote `contains-studio-agents` não existe no PyPI

**Solução**: Removido do requirements.txt (não é necessário)

---

### ❌ Erro: `psycopg2-binary` falha ao instalar no Windows

**Problema**: Compilador C++ ausente

**Solução 1 (Recomendado)**:
```bash
pip install psycopg2-binary==2.9.9
```

**Solução 2 (Se ainda falhar)**:
```bash
# Baixar wheel pré-compilado
pip install https://download.lfd.uci.edu/pythonlibs/archived/psycopg2_binary-2.9.9-cp311-cp311-win_amd64.whl
```

**Solução 3 (Alternativa)**:
```bash
# Usar versão mais nova
pip install psycopg2-binary --upgrade
```

---

### ❌ Erro: `google-auth-oauthlib` conflito de versões

**Problema**: Dependências incompatíveis

**Solução**: Removido pacotes duplicados/desnecessários do requirements.txt

---

### ❌ Erro: `numpy` versão incompatível

**Problema**: Numpy 1.24.3 pode ter conflitos

**Solução**:
```bash
pip install numpy==1.26.0
```

---

### ❌ Erro: `Pillow` duplicado

**Problema**: Pillow aparece 2x no requirements.txt

**Solução**: Já corrigido no novo requirements.txt

---

### ❌ Erro: Falta compilador C/C++

**Sintoma**: Erro ao instalar pacotes com extensões C

**Solução Windows**:
1. Instalar Microsoft Visual C++ Build Tools
2. Ou usar wheels pré-compilados

**Link**: https://visualstudio.microsoft.com/visual-cpp-build-tools/

---

## 🔄 Processo de Instalação Limpa

### Opção 1: Script Automático (Recomendado)

```bash
cd c:\Users\adson.silva_contabil\democratiza-ai\democratiza-ai\backend

# Executar script de instalação
python install_dependencies.py
```

### Opção 2: Manual Passo a Passo

```bash
# 1. Atualizar pip
python -m pip install --upgrade pip setuptools wheel

# 2. Instalar pacotes críticos primeiro
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install sqlalchemy==2.0.23
pip install pydantic==2.5.0

# 3. Instalar AI packages
pip install anthropic==0.8.1
pip install openai==1.6.1
pip install google-generativeai==0.3.2

# 4. Instalar database
pip install asyncpg==0.29.0
pip install psycopg2-binary==2.9.9
pip install pgvector==0.2.3
pip install alembic==1.13.0

# 5. Instalar Google Cloud
pip install google-cloud-vision==3.4.5
pip install google-auth==2.23.4

# 6. Instalar storage
pip install boto3==1.34.0

# 7. Instalar utilitários
pip install python-dotenv==1.0.0
pip install PyMuPDF==1.23.8
pip install numpy==1.24.3

# 8. Instalar resto
pip install -r requirements.txt
```

### Opção 3: Instalação Individual (Debug)

Se algum pacote específico falhar:

```bash
# Tentar instalar individualmente
pip install --no-cache-dir nome-do-pacote

# Ver detalhes do erro
pip install --verbose nome-do-pacote

# Usar versão mais nova
pip install --upgrade nome-do-pacote
```

---

## ✅ Verificação Pós-Instalação

### Teste Rápido

```bash
python -c "import fastapi, anthropic, openai, sqlalchemy, pgvector; print('✅ Imports OK!')"
```

### Teste Completo

```bash
python -c "
from fastapi import FastAPI
from anthropic import Anthropic
from openai import OpenAI
import sqlalchemy
import pgvector
import boto3
from google.cloud import vision
print('✅ Todos os imports críticos funcionando!')
"
```

### Verificar Versões

```bash
pip list | findstr "fastapi anthropic openai sqlalchemy pgvector"
```

---

## 🐛 Erros Específicos

### Erro: `ModuleNotFoundError: No module named 'pgvector'`

```bash
pip uninstall pgvector -y
pip install pgvector==0.2.3
```

### Erro: `ImportError: cannot import name 'Anthropic'`

```bash
pip uninstall anthropic -y
pip install anthropic==0.8.1
```

### Erro: `SSL: CERTIFICATE_VERIFY_FAILED`

```bash
# Windows
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org nome-do-pacote
```

---

## 📊 Status Esperado

Depois da instalação bem-sucedida, você deve ter:

```
✅ Python 3.11+ instalado
✅ pip atualizado
✅ 45+ pacotes instalados
✅ Todos os imports críticos funcionando
✅ Sem conflitos de versão
```

---

## 💡 Dicas Úteis

### Criar Virtual Environment (Recomendado)

```bash
# Criar venv
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### Limpar Cache do Pip

```bash
pip cache purge
```

### Reinstalar Tudo

```bash
pip freeze > installed.txt
pip uninstall -r installed.txt -y
pip install -r requirements.txt
```

---

## 🆘 Se Nada Funcionar

1. **Verificar Python**: `python --version` (precisa ser 3.11+)
2. **Atualizar pip**: `python -m pip install --upgrade pip`
3. **Limpar cache**: `pip cache purge`
4. **Usar venv**: Criar ambiente virtual limpo
5. **Instalar um por um**: Identificar qual pacote está falhando

---

## 📞 Suporte

Se o erro persistir, me envie:

1. Versão do Python: `python --version`
2. Sistema Operacional
3. Mensagem de erro completa
4. Último pacote que falhou

**Exemplo de erro útil**:
```
ERROR: Could not find a version that satisfies the requirement package==X.X.X
```

Isso me ajuda a identificar o problema exato!
