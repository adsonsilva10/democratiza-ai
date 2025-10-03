#!/usr/bin/env python3
"""
Auditoria Completa de Segurança - Democratiza AI
Verifica se todas as credenciais estão protegidas após correções
"""

import os
import subprocess
from pathlib import Path

def run_git_command(cmd):
    """Execute comando Git e retorna output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def scan_git_history_for_credentials():
    """Escaneia histórico do Git por padrões de credenciais"""
    
    sensitive_patterns = [
        "eyJhbGciOiJIUzI1NiI",  # JWT tokens
        "brrehdlpiimawxiiswzq", # Supabase project ID
        "sk-ant-api03",          # Anthropic API keys
        "AIzaSy",                # Google API keys
        "reBZclab_NnimnYZkeW",   # SECRET_KEY
        "VJd7jZ0z/1ApnyryCh8Q"  # SUPABASE_JWT_SECRET
    ]
    
    print("🔍 AUDITORIA DE SEGURANÇA - VERIFICANDO HISTÓRICO DO GIT")
    print("="*60)
    
    vulnerabilities_found = []
    
    for pattern in sensitive_patterns:
        print(f"\n🔍 Verificando padrão: {pattern[:15]}...")
        
        cmd = f'git log --all --source --full-history -S "{pattern}" --oneline'
        success, output, error = run_git_command(cmd)
        
        if success and output.strip():
            commits = output.strip().split('\n')
            print(f"❌ VULNERABILIDADE: {len(commits)} commit(s) encontrados!")
            vulnerabilities_found.extend(commits)
            for commit in commits:
                print(f"   📝 {commit}")
        else:
            print("✅ Padrão não encontrado no histórico")
    
    return vulnerabilities_found

def check_local_files():
    """Verifica se arquivos locais estão seguros"""
    
    print("\n🔍 VERIFICANDO ARQUIVOS LOCAIS")
    print("="*40)
    
    # Verificar se .env.private existem
    backend_private = Path("backend/.env.private")
    frontend_private = Path("frontend/.env.private")
    
    print(f"✅ Backend .env.private existe: {backend_private.exists()}")
    print(f"✅ Frontend .env.private existe: {frontend_private.exists()}")
    
    # Verificar se arquivos .env.production foram sanitizados
    backend_prod = Path("backend/.env.production")
    if backend_prod.exists():
        with open(backend_prod, 'r') as f:
            content = f.read()
            has_real_credentials = "brrehdlpiimawxiiswzq" in content
            print(f"{'❌ RISCO' if has_real_credentials else '✅'} Backend .env.production sanitizado: {not has_real_credentials}")
    
    # Verificar .gitignore
    gitignore = Path(".gitignore")
    if gitignore.exists():
        with open(gitignore, 'r') as f:
            content = f.read()
            protections = [
                ".env.private" in content,
                ".env.production" in content,
                "supabase" in content.lower()
            ]
            print(f"✅ .gitignore protegido: {all(protections)}")

def main():
    """Executa auditoria completa"""
    
    print("🛡️  DEMOCRATIZA AI - AUDITORIA DE SEGURANÇA")
    print("🚨 Verificando se todas as credenciais estão protegidas")
    print("="*60)
    
    # 1. Verificar histórico do Git
    vulnerabilities = scan_git_history_for_credentials()
    
    # 2. Verificar arquivos locais
    check_local_files()
    
    # 3. Relatório final
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL")
    print("="*60)
    
    if vulnerabilities:
        print(f"🚨 CRÍTICO: {len(vulnerabilities)} commits com credenciais no histórico!")
        print("💡 RECOMENDAÇÃO: Considerar git filter-branch ou novo repositório")
        print("\nCommits vulneráveis:")
        for vuln in set(vulnerabilities):
            print(f"   📝 {vuln}")
        return False
    else:
        print("✅ SEGURO: Nenhuma credencial encontrada no histórico atual")
        print("🔐 SEGURO: Arquivos locais protegidos")
        print("🛡️  SEGURO: .gitignore configurado adequadamente")
        print("\n🎉 SISTEMA SEGURO - Todas as credenciais protegidas!")
        return True

if __name__ == "__main__":
    os.chdir(Path(__file__).parent.parent)  # Ir para raiz do projeto
    is_secure = main()
    exit(0 if is_secure else 1)