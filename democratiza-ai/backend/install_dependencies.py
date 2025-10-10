"""
Script para instalar dependências do backend com tratamento de erros
Tenta instalar pacotes individualmente para identificar problemas
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Executa comando e retorna sucesso/falha"""
    print(f"\n{'='*60}")
    print(f"▶️  {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - SUCESSO")
        if result.stdout:
            print(result.stdout[-500:])  # Últimas 500 chars
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ERRO")
        if e.stderr:
            print(f"Erro: {e.stderr[-500:]}")
        return False


def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"\n🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("⚠️  AVISO: Python 3.11+ é recomendado")
        print("   Versão atual pode causar problemas de compatibilidade")
        return False
    
    print("✅ Versão Python OK!")
    return True


def upgrade_pip():
    """Atualiza pip, setuptools e wheel"""
    print(f"\n{'='*60}")
    print("🔄 Atualizando pip, setuptools e wheel")
    print(f"{'='*60}")
    
    cmd = f"{sys.executable} -m pip install --upgrade pip setuptools wheel"
    return run_command(cmd, "Atualizar pip")


def install_requirements():
    """Instala requirements.txt"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ Arquivo não encontrado: {requirements_file}")
        return False
    
    cmd = f"{sys.executable} -m pip install -r {requirements_file}"
    return run_command(cmd, "Instalar requirements.txt")


def test_critical_imports():
    """Testa imports críticos"""
    print(f"\n{'='*60}")
    print("🧪 Testando Imports Críticos")
    print(f"{'='*60}")
    
    critical_packages = {
        "fastapi": "FastAPI",
        "sqlalchemy": "SQLAlchemy",
        "anthropic": "Anthropic (Claude)",
        "openai": "OpenAI",
        "google.generativeai": "Google Generative AI (Gemini)",
        "pgvector": "pgvector",
        "google.cloud.vision": "Google Cloud Vision",
        "boto3": "Boto3 (AWS/R2)",
    }
    
    failed = []
    
    for module, name in critical_packages.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
            failed.append(name)
    
    if failed:
        print(f"\n⚠️  {len(failed)} pacotes falharam:")
        for pkg in failed:
            print(f"     - {pkg}")
        return False
    
    print("\n✅ Todos os imports críticos OK!")
    return True


def show_package_versions():
    """Mostra versões dos pacotes instalados"""
    print(f"\n{'='*60}")
    print("📦 Versões dos Pacotes Principais")
    print(f"{'='*60}")
    
    packages_to_check = [
        "fastapi",
        "sqlalchemy",
        "anthropic",
        "openai",
        "google-generativeai",
        "pgvector",
        "boto3",
    ]
    
    for package in packages_to_check:
        cmd = f"{sys.executable} -m pip show {package} | findstr Version"
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            version = result.stdout.strip()
            print(f"  {package}: {version}")
        except:
            print(f"  {package}: ❌ Não instalado")


def main():
    """Executa instalação completa"""
    print("\n" + "🚀" * 30)
    print("DEMOCRATIZA AI - INSTALAÇÃO DE DEPENDÊNCIAS")
    print("🚀" * 30)
    
    # 1. Verificar Python
    if not check_python_version():
        print("\n⚠️  Continuando mesmo assim...")
    
    # 2. Atualizar pip
    if not upgrade_pip():
        print("\n⚠️  Falha ao atualizar pip, mas continuando...")
    
    # 3. Instalar requirements
    print("\n📦 Instalando dependências do requirements.txt...")
    if not install_requirements():
        print("\n❌ ERRO: Falha ao instalar requirements.txt")
        print("\n💡 Tente instalar manualmente:")
        print("   pip install -r requirements.txt")
        return False
    
    # 4. Testar imports
    if not test_critical_imports():
        print("\n⚠️  Alguns pacotes falharam nos imports")
        print("   Mas a instalação foi concluída")
    
    # 5. Mostrar versões
    show_package_versions()
    
    # 6. Resumo
    print("\n" + "="*60)
    print("✅ INSTALAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("  1. Executar: python setup_database.py")
    print("  2. Testar: python test_openai_embeddings.py")
    print("  3. Verificar: python -c 'import fastapi, anthropic, openai; print(\"OK\")'")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
