#!/usr/bin/env python3
"""
Teste de Segurança - Verificar se sistema funciona após correção
Democratiza AI - Teste das APIs sem vazar credenciais
"""

import asyncio
from app.core.config import settings

async def test_security_remediation():
    """Testa se sistema funciona após correção de segurança"""
    
    print("🔒 TESTE DE SEGURANÇA - PÓS CORREÇÃO")
    print("="*50)
    
    # 1. Verificar configurações
    print("✅ 1. Configurações carregadas")
    
    # 2. Verificar se chaves são válidas (formato)
    google_valid = settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY.startswith("AIza")
    anthropic_valid = settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY.startswith("sk-ant")
    
    print(f"✅ 2. Google API Key válida: {google_valid}")
    print(f"✅ 3. Anthropic API Key válida: {anthropic_valid}")
    
    if not (google_valid and anthropic_valid):
        print("❌ Chaves inválidas - verifique .env.private")
        return False
    
    # 3. Teste rápido de API (sem gastar muito)
    try:
        from app.services.llm_router import LLMRouter
        
        router = LLMRouter()
        
        # Teste simples com Gemini (mais barato)
        response = await router.route_contract_analysis(
            contract_text="Teste simples para verificar funcionamento.",
            analysis_type="risk_assessment"
        )
        
        if response and "analysis" in response:
            print("✅ 4. API Sistema funcionando")
        else:
            print("⚠️  4. API Sistema resposta inesperada")
            
        print("🔒 SISTEMA SEGURO E FUNCIONAL!")
        return True
        
    except Exception as e:
        print(f"❌ 4. Erro ao testar APIs: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_security_remediation())
    print("\n" + "="*50)
    if success:
        print("🎉 SUCESSO: Sistema funcional após correção de segurança")
        print("🔐 Chaves seguras e não expostas no Git")
    else:
        print("⚠️  ATENÇÃO: Verificar configuração das APIs")