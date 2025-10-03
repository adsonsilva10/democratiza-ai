"""
Pipeline de Teste Simples
Testa o fluxo básico sem dependências complexas
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any
import httpx

# Adicionar path do backend
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

from app.core.config import settings
from app.services.simple_ocr_service import SimpleOCRService

class SimplePipeline:
    """Pipeline simplificado para testes"""
    
    def __init__(self):
        self.ocr_service = SimpleOCRService()
        print("🚀 Pipeline simplificado inicializado")
    
    async def process_contract(self, contract_text: str, filename: str) -> Dict[str, Any]:
        """Processa contrato usando APIs diretas"""
        
        print(f"📋 Processando: {filename}")
        
        try:
            # 1. Simular OCR (já temos o texto)
            print("1️⃣ Texto fornecido diretamente")
            
            # 2. Determinar complexidade (análise simples)
            complexity = self._analyze_complexity_simple(contract_text)
            print(f"2️⃣ Complexidade: {complexity}")
            
            # 3. Classificar contrato
            print("3️⃣ Classificando contrato...")
            contract_type = await self._classify_contract_simple(contract_text)
            print(f"✅ Tipo: {contract_type}")
            
            # 4. Analisar riscos
            print("4️⃣ Analisando riscos...")
            analysis = await self._analyze_risks_simple(contract_text, contract_type)
            print(f"✅ Risco: {analysis['risk_level']}")
            
            return {
                'success': True,
                'filename': filename,
                'complexity': complexity,
                'contract_type': contract_type,
                'analysis': analysis,
                'text_length': len(contract_text)
            }
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_complexity_simple(self, text: str) -> str:
        """Análise simples de complexidade baseada em palavras-chave"""
        
        text_lower = text.lower()
        
        # Palavras que indicam complexidade
        complex_terms = [
            'aditivo', 'garantia', 'avalista', 'fiador', 'penalidade',
            'rescisão', 'multa', 'juros', 'correção monetária', 'foro',
            'cláusula penal', 'vencimento antecipado'
        ]
        
        specialized_terms = [
            'ipo', 'm&a', 'due diligence', 'compliance', 'auditoria',
            'previdência', 'pgbl', 'vgbl', 'fundos', 'derivativos'
        ]
        
        complex_count = sum(1 for term in complex_terms if term in text_lower)
        specialized_count = sum(1 for term in specialized_terms if term in text_lower)
        
        if specialized_count > 0:
            return 'especializado'
        elif complex_count >= 3:
            return 'complexo'
        elif complex_count >= 1:
            return 'medio'
        else:
            return 'simples'
    
    async def _classify_contract_simple(self, text: str) -> str:
        """Classificação simples baseada em palavras-chave"""
        
        text_lower = text.lower()
        
        # Mapear tipos por palavras-chave
        type_keywords = {
            'locacao': ['locação', 'aluguel', 'locador', 'locatário', 'imóvel', 'inquilinato'],
            'telecom': ['internet', 'telefone', 'tv', 'cabo', 'fibra', 'anatel', 'telecom'],
            'financeiro': ['empréstimo', 'financiamento', 'juros', 'banco', 'cet', 'crédito'],
            'trabalhista': ['trabalho', 'clt', 'salário', 'funcionário', 'empregado'],
            'seguro': ['seguro', 'apólice', 'prêmio', 'sinistro', 'cobertura'],
            'consumo': ['compra', 'venda', 'produto', 'entrega', 'garantia', 'troca'],
            'assinatura': ['assinatura', 'mensalidade', 'plano', 'netflix', 'spotify']
        }
        
        # Contar matches por tipo
        type_scores = {}
        for contract_type, keywords in type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                type_scores[contract_type] = score
        
        if type_scores:
            return max(type_scores.items(), key=lambda x: x[1])[0]
        else:
            return 'outros'
    
    async def _analyze_risks_simple(self, text: str, contract_type: str) -> Dict[str, Any]:
        """Análise simplificada de riscos"""
        
        if not settings.GOOGLE_API_KEY:
            # Fallback sem IA
            return {
                'risk_level': 'medio',
                'summary': 'Análise básica - configure APIs para análise completa',
                'risk_factors': ['Renovação automática', 'Cláusulas de cancelamento'],
                'recommendations': ['Ler atentamente antes de assinar', 'Verificar condições de cancelamento'],
                'confidence': 0.5
            }
        
        try:
            # Usar Gemini para análise
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={settings.GOOGLE_API_KEY}"
            
            prompt = f"""
Analise este contrato brasileiro de {contract_type} e identifique os principais riscos:

CONTRATO:
{text[:1500]}

Responda em JSON:
{{
  "risk_level": "baixo|medio|alto",
  "summary": "resumo em 1 frase",
  "risk_factors": ["risco1", "risco2", "risco3"],
  "recommendations": ["recomendação1", "recomendação2"],
  "confidence": 0.9
}}
"""
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 400, "temperature": 0.1}
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'candidates' in data and data['candidates']:
                        text_response = data['candidates'][0]['content']['parts'][0]['text']
                        
                        # Tentar parsear JSON
                        try:
                            # Limpar resposta
                            clean_text = text_response.strip()
                            if clean_text.startswith('```'):
                                lines = clean_text.split('\n')
                                clean_text = '\n'.join([line for line in lines if not line.startswith('```')])
                            
                            result = json.loads(clean_text)
                            return result
                            
                        except json.JSONDecodeError:
                            # Fallback com texto da resposta
                            return {
                                'risk_level': 'medio',
                                'summary': text_response[:100] + '...' if len(text_response) > 100 else text_response,
                                'risk_factors': ['Análise disponível na resposta completa'],
                                'recommendations': ['Consultar advogado especializado'],
                                'confidence': 0.7,
                                'raw_response': text_response
                            }
                    
        except Exception as e:
            print(f"⚠️ Erro na análise IA: {e}")
            
        # Fallback básico
        return {
            'risk_level': 'medio',
            'summary': f'Contrato de {contract_type} requer atenção às cláusulas',
            'risk_factors': ['Verificar condições de cancelamento', 'Analisar valores e prazos'],
            'recommendations': ['Ler integralmente', 'Consultar advogado se necessário'],
            'confidence': 0.6
        }

async def test_simple_pipeline():
    """Testa o pipeline simplificado"""
    
    pipeline = SimplePipeline()
    
    print("🧪 TESTANDO PIPELINE SIMPLIFICADO")
    print("=" * 50)
    
    # Contratos de teste
    test_contracts = [
        {
            'filename': 'netflix_premium.txt',
            'text': """
CONTRATO DE ASSINATURA NETFLIX PREMIUM

Assinante: João Silva
Plano: Netflix Premium 
Valor: R$ 45,90 por mês
Renovação: Automática mensal
Cancelamento: A qualquer momento pelo app
Dispositivos: Até 4 simultâneos
Qualidade: 4K Ultra HD

Termos:
- Cobrança mensal automática no cartão
- Cancelamento sem multa
- Conteúdo sujeito a disponibilidade
- Idade mínima 18 anos
"""
        },
        {
            'filename': 'locacao_apartamento.txt', 
            'text': """
CONTRATO DE LOCAÇÃO RESIDENCIAL

Locador: Maria Santos da Silva
Locatário: João Pereira dos Santos
Imóvel: Apartamento 203, Rua das Flores, 123, São Paulo/SP
Valor: R$ 2.800,00 mensais
Prazo: 24 meses (renovável)
Vencimento: Dia 10 de cada mês

Garantias:
- Fiador: Pedro Santos (pai do locatário)  
- Seguro Fiança: R$ 150,00 mensais

Cláusulas:
- Reajuste anual pelo IGPM
- Multa por rescisão antecipada: 3 aluguéis
- Uso exclusivo residencial
- Proibido animais de estimação
- Reformas apenas com autorização
"""
        },
        {
            'filename': 'emprestimo_pessoal.txt',
            'text': """
CONTRATO DE EMPRÉSTIMO PESSOAL

Banco: XYZ Bank S.A.
Cliente: João Silva, CPF 123.456.789-00
Valor liberado: R$ 50.000,00
Prazo: 36 meses
Taxa de juros: 2,99% ao mês
CET: 45,8% ao ano
Prestação: R$ 2.847,22

Encargos adicionais:
- IOF: R$ 275,00 (já descontado)
- Seguro Prestamista: R$ 189,00/mês (obrigatório)
- Taxa de abertura: R$ 350,00

Garantias:
- Avalista obrigatório
- Renda mínima comprovada R$ 8.000,00

Cláusulas importantes:
- Vencimento antecipado em caso de atraso > 60 dias
- Negativação a partir de 15 dias de atraso
- Juros de mora: 1% ao mês + multa 2%
"""
        }
    ]
    
    results = []
    
    for contract in test_contracts:
        print(f"\n🔍 Testando: {contract['filename']}")
        print("-" * 40)
        
        result = await pipeline.process_contract(
            contract_text=contract['text'],
            filename=contract['filename']
        )
        
        if result['success']:
            print(f"✅ Sucesso!")
            print(f"   📊 Complexidade: {result['complexity']}")
            print(f"   📋 Tipo: {result['contract_type']}")
            print(f"   ⚠️ Risco: {result['analysis']['risk_level']}")
            print(f"   📝 Resumo: {result['analysis']['summary']}")
            print(f"   🔤 Caracteres: {result['text_length']}")
            
            if 'raw_response' in result['analysis']:
                print(f"   🤖 IA respondeu diretamente")
        else:
            print(f"❌ Falha: {result['error']}")
        
        results.append(result)
    
    # Resumo final
    print(f"\n📊 RESUMO FINAL")
    print("=" * 30)
    
    successful = sum(1 for r in results if r['success'])
    print(f"✅ Sucessos: {successful}/{len(results)}")
    
    if successful > 0:
        types_found = [r['contract_type'] for r in results if r['success']]
        print(f"📋 Tipos identificados: {', '.join(set(types_found))}")
        
        risks_found = [r['analysis']['risk_level'] for r in results if r['success']]
        print(f"⚠️ Níveis de risco: {', '.join(risks_found)}")
    
    print(f"\n🎉 Teste do pipeline concluído!")
    return results

if __name__ == "__main__":
    asyncio.run(test_simple_pipeline())