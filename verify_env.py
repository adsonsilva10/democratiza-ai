"""
Script para verificar se .env consolidado tem todas as credenciais
"""
from dotenv import load_dotenv
import os

# Carregar .env
load_dotenv()

print("\n" + "="*60)
print("🔍 VERIFICAÇÃO DE CREDENCIAIS - .ENV CONSOLIDADO")
print("="*60)

# Verificar cada credencial
credentials = {
    "DATABASE_URL": {
        "value": os.getenv("DATABASE_URL"),
        "check": lambda v: v and "brrehdlpiimawxiiswzq" in v,
        "desc": "Supabase Database"
    },
    "OPENAI_API_KEY": {
        "value": os.getenv("OPENAI_API_KEY"),
        "check": lambda v: v and len(v) > 50 and "sk-proj" in v,
        "desc": "OpenAI (Embeddings 1536d)"
    },
    "ANTHROPIC_API_KEY": {
        "value": os.getenv("ANTHROPIC_API_KEY"),
        "check": lambda v: v and "sk-ant" in v,
        "desc": "Anthropic Claude 3.5"
    },
    "GOOGLE_API_KEY": {
        "value": os.getenv("GOOGLE_API_KEY"),
        "check": lambda v: v and "AIza" in v,
        "desc": "Google Gemini"
    },
    "SUPABASE_URL": {
        "value": os.getenv("SUPABASE_URL"),
        "check": lambda v: v and "supabase.co" in v,
        "desc": "Supabase URL"
    },
    "SECRET_KEY": {
        "value": os.getenv("SECRET_KEY"),
        "check": lambda v: v and len(v) > 30,
        "desc": "JWT Secret"
    }
}

all_ok = True
for key, config in credentials.items():
    value = config["value"]
    is_ok = config["check"](value) if value else False
    status = "✅ OK" if is_ok else "❌ FALTA"
    
    if is_ok:
        # Mostrar preview seguro
        preview = f"{value[:15]}...{value[-10:]}" if len(value) > 30 else value[:20] + "..."
        print(f"\n{status} {key}")
        print(f"   {config['desc']}: {preview}")
    else:
        print(f"\n{status} {key}")
        print(f"   {config['desc']}: NÃO CONFIGURADO")
        all_ok = False

print("\n" + "="*60)
if all_ok:
    print("✅ CONSOLIDAÇÃO BEM-SUCEDIDA!")
    print("   Todas as credenciais essenciais estão configuradas.")
else:
    print("⚠️  ALGUMAS CREDENCIAIS FALTANDO")
    print("   Verifique o arquivo .env")

print("="*60)

# Testar nos backends também
print("\n📂 Testando backends...")
for backend_path in ["backend/.env", "democratiza-ai/backend/.env"]:
    if os.path.exists(backend_path):
        print(f"   ✅ {backend_path} existe")
    else:
        print(f"   ❌ {backend_path} NÃO ENCONTRADO")

print("\n✨ Verificação completa!\n")
