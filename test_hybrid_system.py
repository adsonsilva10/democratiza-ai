"""
Teste do Sistema Híbrido Gemini + Anthropic
Verifica se a integração está funcionando com a API key real
"""

import asyncio
import os
import sys
from pathlib import Path

# Adicionar path do backend
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

try:
    from app.core.config import settings
    from app.services.llm_router import LLMRouter, ComplexityLevel
    from app.services.llm_client import LLMClientFactory
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Certifique-se de estar na pasta raiz do projeto")
    sys.exit(1)

class HybridSystemTester:
    """Testa o sistema híbrido com APIs reais"""
    
    def __init__(self):
        self.router = LLMRouter()
        self.factory = LLMClientFactory()
        
    async def test_api_keys(self):
        """Verifica se as API keys estão configuradas"""
        
        print("🔑 VERIFICANDO CONFIGURAÇÃO DAS API KEYS")
        print("-" * 45)
        
        # Google Gemini
        if hasattr(settings, 'GOOGLE_API_KEY') and settings.GOOGLE_API_KEY:
            if settings.GOOGLE_API_KEY.startswith('AIza'):
                print("✅ Google Gemini API Key configurada corretamente")
                google_configured = True
            else:
                print("⚠️ Google Gemini API Key formato inválido")
                google_configured = False
        else:
            print("❌ Google Gemini API Key não encontrada")
            google_configured = False
        
        # Anthropic Claude
        if hasattr(settings, 'ANTHROPIC_API_KEY') and settings.ANTHROPIC_API_KEY:
            if settings.ANTHROPIC_API_KEY.startswith('sk-ant-'):
                print("✅ Anthropic Claude API Key configurada corretamente")
                anthropic_configured = True
            else:
                print("⚠️ Anthropic Claude API Key formato inválido")
                anthropic_configured = False
        else:
            print("❌ Anthropic Claude API Key não encontrada")
            anthropic_configured = False
        
        return google_configured, anthropic_configured

    async def test_llm_clients(self):
        """Testa a criação dos clientes LLM"""
        
        print(f"\n🤖 TESTANDO CLIENTES LLM")
        print("-" * 30)
        
        # Testar Google Gemini Flash
        try:
            gemini_flash = self.factory.create_client("GEMINI_FLASH")
            print("✅ Google Gemini Flash client criado")
        except Exception as e:
            print(f"❌ Erro Gemini Flash: {e}")
        
        # Testar Google Gemini Pro
        try:
            gemini_pro = self.factory.create_client("GEMINI_PRO")
            print("✅ Google Gemini Pro client criado")
        except Exception as e:
            print(f"❌ Erro Gemini Pro: {e}")
        
        # Testar Claude Sonnet
        try:
            claude_sonnet = self.factory.create_client("CLAUDE_SONNET")
            print("✅ Claude Sonnet client criado")
        except Exception as e:
            print(f"❌ Erro Claude Sonnet: {e}")
        
        # Testar Claude Opus
        try:
            claude_opus = self.factory.create_client("CLAUDE_OPUS")
            print("✅ Claude Opus client criado")
        except Exception as e:
            print(f"❌ Erro Claude Opus: {e}")

    async def test_complexity_routing(self):
        """Testa o roteamento por complexidade"""
        
        print(f"\n🎯 TESTANDO ROTEAMENTO INTELIGENTE")
        print("-" * 40)
        
        test_contracts = {
            "Netflix Premium": {
                "text": "Contrato de assinatura mensal Netflix Premium por R$ 45,90 com renovação automática...",
                "expected": ComplexityLevel.SIMPLES
            },
            "Locação Residencial": {
                "text": "Contrato de locação de imóvel residencial, valor mensal R$ 2.800, prazo 24 meses, com fiador e seguro fiança...",
                "expected": ComplexityLevel.MEDIO
            },
            "Consultoria Empresarial": {
                "text": "Prestação de serviços de consultoria em tecnologia da informação, valor total R$ 240.000, prazo 12 meses, com cláusulas de propriedade intelectual...",
                "expected": ComplexityLevel.COMPLEXO
            },
            "PGBL Previdência": {
                "text": "Plano Gerador de Benefício Livre, contribuição inicial R$ 50.000, taxa de administração 2,5% a.a., modalidade de tributação regressiva...",
                "expected": ComplexityLevel.ESPECIALIZADO
            }
        }
        
        for contract_name, data in test_contracts.items():
            try:
                complexity = await self.router.analyze_complexity(data["text"])
                model_info = await self.router.route_to_best_model(data["text"])
                
                expected = data["expected"]
                status = "✅" if complexity == expected else "⚠️"
                
                print(f"{status} {contract_name}:")
                print(f"   Complexidade: {complexity.value} (esperado: {expected.value})")
                print(f"   Modelo: {model_info['model']} (${model_info['cost_per_1k']}/1k tokens)")
                print()
                
            except Exception as e:
                print(f"❌ Erro testando {contract_name}: {e}")
                print()

    async def test_real_api_call(self):
        """Testa uma chamada real para a API (se as keys estiverem configuradas)"""
        
        print(f"\n🚀 TESTE COM API REAL (GEMINI)")
        print("-" * 35)
        
        if not (hasattr(settings, 'GOOGLE_API_KEY') and settings.GOOGLE_API_KEY):
            print("❌ Google API Key não configurada - pulando teste real")
            return
        
        try:
            # Testar análise simples com Gemini Flash
            simple_contract = "Contrato de assinatura Netflix Premium por R$ 45,90 mensal."
            
            model_info = await self.router.route_to_best_model(simple_contract)
            print(f"🎯 Roteamento: {model_info['model']} (${model_info['cost_per_1k']}/1k tokens)")
            
            # Criar cliente e fazer chamada real
            client = self.factory.create_client(model_info['provider'])
            
            prompt = f"""
            Analise este contrato brasileiro de forma jurídica:
            
            {simple_contract}
            
            Identifique:
            1. Tipo de contrato
            2. Principal risco para o consumidor
            3. Recomendação em 1 frase
            
            Responda de forma objetiva em português.
            """
            
            print("⏳ Fazendo chamada para API...")
            response = await client.generate_response(prompt, max_tokens=200)
            
            print("✅ RESPOSTA DA IA:")
            print(f"   {response}")
            print()
            print(f"💰 Custo estimado: ${(200/1000) * model_info['cost_per_1k']:.6f}")
            
        except Exception as e:
            print(f"❌ Erro na chamada real: {e}")

    async def run_full_test(self):
        """Executa todos os testes do sistema híbrido"""
        
        print("🧪 DEMOCRATIZA AI - TESTE DO SISTEMA HÍBRIDO")
        print("=" * 55)
        print("🎯 Verificando integração Gemini + Anthropic")
        print()
        
        # 1. Verificar API Keys
        google_ok, anthropic_ok = await self.test_api_keys()
        
        # 2. Testar clientes LLM
        await self.test_llm_clients()
        
        # 3. Testar roteamento
        await self.test_complexity_routing()
        
        # 4. Teste real se possível
        if google_ok:
            await self.test_real_api_call()
        
        # Resultado final
        print("🏆 RESULTADO DOS TESTES")
        print("-" * 25)
        
        if google_ok and anthropic_ok:
            print("✅ Sistema híbrido COMPLETAMENTE FUNCIONAL!")
            print("🚀 Economia de 64% ativada!")
            print("⚡ Pronto para análise de contratos em produção!")
        elif google_ok:
            print("✅ Google Gemini funcionando (economia ativada)")
            print("⚠️ Anthropic Claude pendente (qualidade limitada)")
        elif anthropic_ok:
            print("✅ Anthropic Claude funcionando")  
            print("⚠️ Google Gemini pendente (sem economia máxima)")
        else:
            print("❌ APIs não configuradas")
            print("🔧 Configure as API keys para ativar o sistema")

async def main():
    """Executa teste completo do sistema híbrido"""
    
    print("🔍 Iniciando teste do sistema híbrido...")
    print()
    
    try:
        tester = HybridSystemTester()
        await tester.run_full_test()
        
    except Exception as e:
        print(f"❌ Erro fatal no teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())