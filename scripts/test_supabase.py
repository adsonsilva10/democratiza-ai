#!/usr/bin/env python3
"""
Democratiza AI - Teste de Conexão com Supabase
Valida se as credenciais do Supabase estão funcionando corretamente
"""

import os
import sys
import asyncio
import asyncpg
from pathlib import Path
import json

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

def load_env_file(filepath: str):
    """Carrega variáveis de ambiente de um arquivo .env"""
    if not Path(filepath).exists():
        print_status(f"Arquivo {filepath} não encontrado!", "ERROR")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove aspas se existirem
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value
        return True
    except Exception as e:
        print_status(f"Erro ao carregar {filepath}: {e}", "ERROR")
        return False

async def test_database_connection():
    """Testa conexão com o banco de dados PostgreSQL"""
    print_status("Testando conexão com banco de dados PostgreSQL...", "INFO")
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url or "[SUBSTITUA" in database_url:
        print_status("❌ DATABASE_URL não configurada ou é placeholder", "ERROR")
        return False
    
    try:
        # Extrair informações da URL de conexão
        # Format: postgresql://user:password@host:port/database
        print_status(f"Conectando em: {database_url.replace(database_url.split('@')[0].split('://')[1], '***:***')}", "INFO")
        
        conn = await asyncpg.connect(database_url)
        
        # Teste básico de query
        result = await conn.fetchval("SELECT version()")
        print_status(f"✅ Conexão PostgreSQL bem-sucedida!", "SUCCESS")
        print_status(f"Versão: {result.split(' on ')[0]}", "INFO")
        
        # Testar se tem extensão pg_vector (necessária para RAG)
        try:
            extensions = await conn.fetch("SELECT extname FROM pg_extension WHERE extname = 'vector'")
            if extensions:
                print_status("✅ Extensão pg_vector encontrada (RAG habilitado)", "SUCCESS")
            else:
                print_status("⚠️  Extensão pg_vector não encontrada (RAG desabilitado)", "WARNING")
        except Exception as e:
            print_status(f"⚠️  Não foi possível verificar pg_vector: {e}", "WARNING")
        
        await conn.close()
        return True
        
    except asyncpg.InvalidPasswordError:
        print_status("❌ Senha do banco de dados incorreta", "ERROR")
        return False
    except asyncpg.InvalidCatalogNameError:
        print_status("❌ Nome do banco de dados incorreto", "ERROR")
        return False
    except Exception as e:
        print_status(f"❌ Erro na conexão: {e}", "ERROR")
        return False

def test_supabase_config():
    """Testa configurações básicas do Supabase"""
    print_status("Validando configurações do Supabase...", "INFO")
    
    # Verificar variáveis essenciais
    supabase_url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
    
    success = True
    
    if not supabase_url or "[SUBSTITUA" in supabase_url:
        print_status("❌ SUPABASE_URL não configurada", "ERROR")
        success = False
    else:
        print_status(f"✅ SUPABASE_URL: {supabase_url}", "SUCCESS")
    
    if not anon_key or "[SUBSTITUA" in anon_key:
        print_status("❌ SUPABASE_ANON_KEY não configurada", "ERROR")
        success = False
    else:
        print_status("✅ SUPABASE_ANON_KEY: Configurada", "SUCCESS")
    
    if not service_key or "[SUBSTITUA" in service_key:
        print_status("❌ SUPABASE_SERVICE_KEY não configurada", "ERROR")
        success = False
    else:
        print_status("✅ SUPABASE_SERVICE_KEY: Configurada", "SUCCESS")
    
    if not jwt_secret or "[SUBSTITUA" in jwt_secret:
        print_status("❌ SUPABASE_JWT_SECRET não configurada", "ERROR")
        success = False
    else:
        print_status("✅ SUPABASE_JWT_SECRET: Configurada", "SUCCESS")
    
    return success

async def test_supabase_api():
    """Testa acesso à API do Supabase"""
    print_status("Testando acesso à API do Supabase...", "INFO")
    
    try:
        import aiohttp
        
        supabase_url = os.getenv("SUPABASE_URL")
        service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not supabase_url or not service_key:
            print_status("❌ Credenciais do Supabase não configuradas", "ERROR")
            return False
        
        headers = {
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            # Testar endpoint básico de saúde
            async with session.get(f"{supabase_url}/rest/v1/", headers=headers) as response:
                if response.status == 200:
                    print_status("✅ API Supabase REST acessível", "SUCCESS")
                    return True
                else:
                    print_status(f"❌ API Supabase retornou status: {response.status}", "ERROR")
                    return False
                    
    except ImportError:
        print_status("⚠️  aiohttp não instalado, pulando teste de API", "WARNING")
        return None
    except Exception as e:
        print_status(f"❌ Erro ao testar API: {e}", "ERROR")
        return False

async def main():
    """Função principal"""
    print_status("=== TESTE DE CONFIGURAÇÃO SUPABASE ===", "INFO")
    print_status("Democratiza AI - Validação de Conexões\n", "INFO")
    
    # Carregar variáveis de ambiente
    if not load_env_file("backend/.env.local"):
        sys.exit(1)
    
    success_count = 0
    total_tests = 3
    
    # Teste 1: Configurações básicas
    print_status("1. Validando configurações...", "INFO")
    if test_supabase_config():
        success_count += 1
        print_status("✅ Configurações válidas\n", "SUCCESS")
    else:
        print_status("❌ Configurações inválidas\n", "ERROR")
    
    # Teste 2: Conexão com banco
    print_status("2. Testando conexão com banco...", "INFO")
    try:
        if await test_database_connection():
            success_count += 1
            print_status("✅ Banco de dados acessível\n", "SUCCESS")
        else:
            print_status("❌ Falha na conexão com banco\n", "ERROR")
    except Exception as e:
        print_status(f"❌ Erro no teste de banco: {e}\n", "ERROR")
    
    # Teste 3: API Supabase
    print_status("3. Testando API REST...", "INFO")
    api_result = await test_supabase_api()
    if api_result is True:
        success_count += 1
        print_status("✅ API REST funcionando\n", "SUCCESS")
    elif api_result is False:
        print_status("❌ Falha na API REST\n", "ERROR")
    else:
        print_status("⚠️  Teste de API pulado\n", "WARNING")
        total_tests -= 1
    
    # Resumo final
    print_status("=== RESUMO DOS TESTES ===", "INFO")
    print_status(f"Testes executados: {total_tests}", "INFO")
    print_status(f"Sucessos: {success_count}", "SUCCESS" if success_count == total_tests else "WARNING")
    print_status(f"Falhas: {total_tests - success_count}", "ERROR" if success_count < total_tests else "INFO")
    
    if success_count == total_tests:
        print_status("\n🎉 SUPABASE CONFIGURADO CORRETAMENTE!", "SUCCESS")
        print_status("Você pode iniciar o desenvolvimento da aplicação.", "SUCCESS")
    elif success_count > 0:
        print_status(f"\n⚠️  CONFIGURAÇÃO PARCIAL ({success_count}/{total_tests})", "WARNING")
        print_status("Alguns recursos podem não funcionar corretamente.", "WARNING")
    else:
        print_status("\n❌ CONFIGURAÇÃO FALHHOU COMPLETAMENTE", "ERROR")
        print_status("Verifique as credenciais e tente novamente.", "ERROR")
    
    return success_count == total_tests

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print_status("\nTeste interrompido pelo usuário", "WARNING")
        sys.exit(1)
    except Exception as e:
        print_status(f"Erro inesperado: {e}", "ERROR")
        sys.exit(1)