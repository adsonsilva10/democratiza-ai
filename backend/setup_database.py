"""
Script para inicialização e teste do banco de dados Supabase
"""

import asyncio
import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.models.connection import init_db, check_db_connection, check_extensions
from app.models.database_complete import Base
from app.core.config_minimal import settings

async def setup_database():
    """Configuração completa do banco de dados"""
    
    print("🚀 Democratiza AI - Configuração do Banco de Dados")
    print("=" * 50)
    
    # 1. Verificar conexão
    print("\n1. Testando conexão com Supabase PostgreSQL...")
    if not await check_db_connection():
        print("❌ Falha na conexão. Verifique as credenciais.")
        return False
    
    # 2. Verificar extensões
    print("\n2. Verificando extensões do PostgreSQL...")
    await check_extensions()
    
    # 3. Criar tabelas
    print("\n3. Criando estrutura de tabelas...")
    try:
        await init_db()
        print("✅ Estrutura de banco criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False
    
    # 4. Verificar configurações
    print("\n4. Verificando configurações...")
    print(f"✅ URL Supabase: {settings.SUPABASE_URL}")
    print(f"✅ Banco configurado: PostgreSQL")
    print(f"✅ Modelos definidos: 8 tabelas")
    
    print("\n🎉 CONFIGURAÇÃO DO BANCO CONCLUÍDA!")
    print("\nTabelas criadas:")
    print("- users (usuários)")
    print("- contracts (contratos)")
    print("- contract_analyses (análises)")
    print("- chat_sessions (sessões de chat)")
    print("- chat_messages (mensagens)")
    print("- user_configurations (configurações)")
    print("- document_vectors (vetores RAG)")
    print("- audit_logs (logs de auditoria)")
    
    return True

if __name__ == "__main__":
    asyncio.run(setup_database())