#!/usr/bin/env python3
"""
Democratiza AI - Environment Validation Script
Valida se todas as variáveis de ambiente necessárias estão configuradas
"""

import os
import sys
from typing import List, Dict, Any
import json
from pathlib import Path

# Cores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_status(message: str, status: str = "INFO"):
    """Imprime mensagem colorida baseada no status"""
    color_map = {
        "SUCCESS": Colors.GREEN,
        "ERROR": Colors.RED,
        "WARNING": Colors.YELLOW,
        "INFO": Colors.BLUE
    }
    color = color_map.get(status, Colors.BLUE)
    print(f"{color}{Colors.BOLD}[{status}]{Colors.END} {message}")

def check_env_var(var_name: str, required: bool = True) -> Dict[str, Any]:
    """Verifica se uma variável de ambiente existe e não é placeholder"""
    value = os.getenv(var_name, "")
    is_set = bool(value)
    is_placeholder = value.startswith("[SUBSTITUA_") or not value
    
    return {
        "name": var_name,
        "set": is_set,
        "placeholder": is_placeholder,
        "required": required,
        "value_preview": value[:20] + "..." if len(value) > 20 else value
    }

def validate_backend_env() -> List[Dict[str, Any]]:
    """Valida variáveis do backend"""
    print_status("Validando Backend Environment (.env.local)", "INFO")
    
    required_vars = [
        # Database
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_KEY", 
        "SUPABASE_JWT_SECRET",
        "DATABASE_URL",
        "DATABASE_PASSWORD",
        
        # AI Services
        "ANTHROPIC_API_KEY",
        "GOOGLE_CLOUD_PROJECT_ID",
        "GOOGLE_APPLICATION_CREDENTIALS_JSON",
        
        # File Storage
        "CLOUDFLARE_R2_ACCESS_KEY_ID",
        "CLOUDFLARE_R2_SECRET_ACCESS_KEY",
        "CLOUDFLARE_R2_BUCKET_NAME",
        "CLOUDFLARE_R2_PUBLIC_URL",
        
        # Message Queue
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SQS_QUEUE_URL",
        
        # Email
        "SENDGRID_API_KEY",
        "SENDGRID_FROM_EMAIL",
        
        # Payments
        "MERCADO_PAGO_ACCESS_TOKEN",
        "MERCADO_PAGO_PUBLIC_KEY",
        "D4SIGN_API_TOKEN",
        "D4SIGN_CRYPT_KEY",
        
        # Security
        "SECRET_KEY"
    ]
    
    optional_vars = [
        "MERCADO_PAGO_WEBHOOK_SECRET",
        "SENTRY_DSN"
    ]
    
    results = []
    
    # Check required variables
    for var in required_vars:
        result = check_env_var(var, required=True)
        results.append(result)
        
        if not result["set"]:
            print_status(f"❌ {var}: NÃO DEFINIDA", "ERROR")
        elif result["placeholder"]:
            print_status(f"⚠️  {var}: PLACEHOLDER - {result['value_preview']}", "WARNING")
        else:
            print_status(f"✅ {var}: CONFIGURADA", "SUCCESS")
    
    # Check optional variables
    for var in optional_vars:
        result = check_env_var(var, required=False)
        results.append(result)
        
        if result["set"] and not result["placeholder"]:
            print_status(f"✅ {var}: CONFIGURADA (opcional)", "SUCCESS")
        else:
            print_status(f"ℹ️  {var}: NÃO CONFIGURADA (opcional)", "INFO")
    
    return results

def validate_frontend_env() -> List[Dict[str, Any]]:
    """Valida variáveis do frontend"""
    print_status("\nValidando Frontend Environment (.env.local)", "INFO")
    
    required_vars = [
        "NEXT_PUBLIC_SUPABASE_URL",
        "NEXT_PUBLIC_SUPABASE_ANON_KEY",
        "NEXT_PUBLIC_API_URL",
        "NEXTAUTH_SECRET"
    ]
    
    optional_vars = [
        "NEXT_PUBLIC_MERCADO_PAGO_PUBLIC_KEY",
        "NEXT_PUBLIC_GOOGLE_ANALYTICS_ID",
        "NEXT_PUBLIC_SENTRY_DSN"
    ]
    
    results = []
    
    # Check required variables
    for var in required_vars:
        result = check_env_var(var, required=True)
        results.append(result)
        
        if not result["set"]:
            print_status(f"❌ {var}: NÃO DEFINIDA", "ERROR")
        elif result["placeholder"]:
            print_status(f"⚠️  {var}: PLACEHOLDER - {result['value_preview']}", "WARNING")
        else:
            print_status(f"✅ {var}: CONFIGURADA", "SUCCESS")
    
    # Check optional variables  
    for var in optional_vars:
        result = check_env_var(var, required=False)
        results.append(result)
        
        if result["set"] and not result["placeholder"]:
            print_status(f"✅ {var}: CONFIGURADA (opcional)", "SUCCESS")
        else:
            print_status(f"ℹ️  {var}: NÃO CONFIGURADA (opcional)", "INFO")
    
    return results

def generate_summary(backend_results: List[Dict], frontend_results: List[Dict]):
    """Gera resumo da validação"""
    print_status("\n" + "="*50, "INFO")
    print_status("RESUMO DA VALIDAÇÃO", "INFO")
    print_status("="*50, "INFO")
    
    all_results = backend_results + frontend_results
    
    total_required = len([r for r in all_results if r["required"]])
    configured_required = len([r for r in all_results if r["required"] and r["set"] and not r["placeholder"]])
    placeholders_required = len([r for r in all_results if r["required"] and r["placeholder"]])
    missing_required = len([r for r in all_results if r["required"] and not r["set"]])
    
    print_status(f"📊 Variáveis obrigatórias: {total_required}", "INFO")
    print_status(f"✅ Configuradas corretamente: {configured_required}", "SUCCESS")
    print_status(f"⚠️  Ainda são placeholders: {placeholders_required}", "WARNING")
    print_status(f"❌ Faltando definir: {missing_required}", "ERROR")
    
    if configured_required == total_required:
        print_status("\n🎉 TODAS AS VARIÁVEIS ESTÃO CONFIGURADAS!", "SUCCESS")
        print_status("Você pode iniciar a aplicação com segurança.", "SUCCESS")
    elif placeholders_required > 0:
        print_status(f"\n⚠️  ATENÇÃO: {placeholders_required} variáveis ainda são placeholders", "WARNING")
        print_status("Consulte o CREDENTIALS_GUIDE.md para obter as credenciais reais", "WARNING")
    else:
        print_status(f"\n❌ ERRO: {missing_required} variáveis obrigatórias não configuradas", "ERROR")
        print_status("Configure todas as variáveis antes de continuar", "ERROR")
    
    # Lista variáveis problemáticas
    problematic = [r for r in all_results if r["required"] and (not r["set"] or r["placeholder"])]
    if problematic:
        print_status("\n🔧 VARIÁVEIS QUE PRECISAM DE ATENÇÃO:", "WARNING")
        for var in problematic:
            if not var["set"]:
                print(f"   ❌ {var['name']}: Não definida")
            elif var["placeholder"]:
                print(f"   ⚠️  {var['name']}: Ainda é placeholder")

def check_file_exists(filepath: str) -> bool:
    """Verifica se arquivo existe"""
    return Path(filepath).exists()

def main():
    """Função principal"""
    print_status("Democratiza AI - Validador de Ambiente", "INFO")
    print_status("Verificando configuração das variáveis de ambiente...\n", "INFO")
    
    # Verificar se arquivos .env existem
    backend_env = "backend/.env.local"
    frontend_env = "frontend/.env.local"
    
    if not check_file_exists(backend_env):
        print_status(f"❌ Arquivo {backend_env} não encontrado!", "ERROR")
        sys.exit(1)
        
    if not check_file_exists(frontend_env):
        print_status(f"❌ Arquivo {frontend_env} não encontrado!", "ERROR")
        sys.exit(1)
    
    # Carregar variáveis dos arquivos .env
    try:
        # Para o backend
        with open(backend_env, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"')
        
        # Para o frontend  
        with open(frontend_env, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"')
                    
    except Exception as e:
        print_status(f"Erro ao carregar arquivos .env: {e}", "ERROR")
        sys.exit(1)
    
    # Validar ambientes
    backend_results = validate_backend_env()
    frontend_results = validate_frontend_env()
    
    # Gerar resumo
    generate_summary(backend_results, frontend_results)

if __name__ == "__main__":
    main()