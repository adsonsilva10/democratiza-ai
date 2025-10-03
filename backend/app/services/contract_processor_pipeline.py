"""
Document Processor Worker - Pipeline Completo
Integra OCR + LLM Router + Agent Factory + RAG Service
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import json
import traceback

# Imports dos nossos serviços
from app.services.simple_ocr_service import SimpleOCRService
from app.services.llm_router import LLMRouter, ComplexityLevel
from app.services.llm_client import LLMClientFactory
from app.agents.factory import AgentFactory
from app.services.rag_service import RAGService
from app.core.config import settings

logger = logging.getLogger(__name__)

class ContractProcessorPipeline:
    """
    Pipeline completo para processamento de contratos
    Upload → OCR → Classification → Analysis → Response
    """
    
    def __init__(self):
        # Inicializar serviços
        self.ocr_service = SimpleOCRService()
        self.llm_router = LLMRouter()
        self.llm_factory = LLMClientFactory()
        self.rag_service = RAGService()
        
        # Agent factory será inicializado conforme necessário
        self.agent_factory = None
        
        print("🚀 Pipeline de processamento inicializado")
    
    async def process_contract_file(
        self, 
        file_content: bytes, 
        filename: str, 
        contract_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processa arquivo de contrato completo
        
        Args:
            file_content: Conteúdo binário do arquivo
            filename: Nome do arquivo original
            contract_id: ID do contrato (opcional)
            
        Returns:
            Dict com resultado completo do processamento
        """
        
        print(f"📋 Iniciando processamento: {filename}")
        start_time = asyncio.get_event_loop().time()
        
        try:
            # 1. EXTRAÇÃO DE TEXTO (OCR)
            print("1️⃣ Extraindo texto...")
            ocr_result = await self.ocr_service.process_contract_document(
                file_content, filename
            )
            
            if not ocr_result.get('success'):
                return {
                    'success': False,
                    'error': f"OCR falhou: {ocr_result.get('error')}",
                    'stage': 'ocr'
                }
            
            contract_text = ocr_result['text']
            if len(contract_text.strip()) < 50:
                return {
                    'success': False,
                    'error': 'Texto insuficiente extraído do documento',
                    'stage': 'ocr'
                }
            
            print(f"✅ Texto extraído: {len(contract_text)} caracteres")
            
            # 2. ANÁLISE DE COMPLEXIDADE
            print("2️⃣ Analisando complexidade...")
            complexity = await self.llm_router.analyze_complexity(contract_text)
            routing_info = await self.llm_router.route_to_best_model(contract_text)
            
            print(f"✅ Complexidade: {complexity.value} → {routing_info['model']}")
            
            # 3. CLASSIFICAÇÃO DO CONTRATO
            print("3️⃣ Classificando tipo de contrato...")
            classification_result = await self._classify_contract(contract_text, routing_info)
            
            if not classification_result.get('success'):
                return {
                    'success': False,
                    'error': f"Classificação falhou: {classification_result.get('error')}",
                    'stage': 'classification'
                }
            
            contract_type = classification_result['contract_type']
            print(f"✅ Tipo identificado: {contract_type}")
            
            # 4. ANÁLISE ESPECIALIZADA
            print("4️⃣ Realizando análise jurídica especializada...")
            analysis_result = await self._analyze_with_specialist(
                contract_text, contract_type, routing_info
            )
            
            if not analysis_result.get('success'):
                return {
                    'success': False,
                    'error': f"Análise falhou: {analysis_result.get('error')}",
                    'stage': 'analysis'
                }
            
            print(f"✅ Análise concluída: {analysis_result['risk_level']} risco")
            
            # 5. COMPILAR RESULTADO FINAL
            processing_time = asyncio.get_event_loop().time() - start_time
            
            final_result = {
                'success': True,
                'contract_id': contract_id,
                'filename': filename,
                'processing_time_seconds': round(processing_time, 2),
                
                # Dados do OCR
                'ocr_data': {
                    'extracted_chars': len(contract_text),
                    'processing_time': ocr_result.get('processing_time_seconds', 0),
                    'estimated_tokens': ocr_result.get('estimated_tokens', 0),
                    'file_type': ocr_result.get('file_type', 'unknown')
                },
                
                # Dados do roteamento
                'routing_data': {
                    'complexity': complexity.value,
                    'selected_model': routing_info['model'],
                    'cost_per_1k_tokens': routing_info['cost_per_1k'],
                    'estimated_cost': (ocr_result.get('estimated_tokens', 0) / 1000) * routing_info['cost_per_1k']
                },
                
                # Dados da classificação
                'classification': {
                    'contract_type': contract_type,
                    'confidence': classification_result.get('confidence', 0.0)
                },
                
                # Dados da análise
                'analysis': analysis_result['analysis'],
                
                # Texto completo (pode ser grande)
                'extracted_text': contract_text
            }
            
            print(f"🎉 Processamento concluído em {processing_time:.2f}s")
            return final_result
            
        except Exception as e:
            error_msg = f"Erro no pipeline: {str(e)}"
            print(f"❌ {error_msg}")
            print(traceback.format_exc())
            
            return {
                'success': False,
                'error': error_msg,
                'stage': 'pipeline',
                'traceback': traceback.format_exc()
            }
    
    async def _classify_contract(self, contract_text: str, routing_info: Dict) -> Dict[str, Any]:
        """Classifica o tipo de contrato usando IA"""
        
        try:
            # Criar cliente LLM apropriado
            client = self.llm_factory.create_client(routing_info['provider'])
            
            # Prompt de classificação
            classification_prompt = f"""
Você é um especialista em direito brasileiro. Analise este contrato e identifique seu tipo.

CONTRATO:
{contract_text[:2000]}...

TIPOS POSSÍVEIS:
- locacao (contratos de aluguel/locação)  
- telecom (telecomunicações, internet, TV)
- financeiro (empréstimos, financiamentos, cartão)
- trabalhista (CLT, prestação de serviços)
- seguro (seguros diversos)
- consumo (compra e venda, e-commerce)
- outros (outros tipos)

RESPOSTA OBRIGATÓRIA:
Responda APENAS com JSON válido no formato:
{{"contract_type": "tipo", "confidence": 0.95, "reasoning": "explicação breve"}}
"""
            
            response = await client.generate_response(
                prompt=classification_prompt,
                max_tokens=200,
                temperature=0.1
            )
            
            # Tentar parsear resposta JSON
            try:
                # Limpar resposta (remover markdown se houver)
                clean_response = response.strip()
                if clean_response.startswith('```'):
                    lines = clean_response.split('\n')
                    clean_response = '\n'.join([line for line in lines if not line.startswith('```')])
                
                result = json.loads(clean_response)
                
                return {
                    'success': True,
                    'contract_type': result.get('contract_type', 'outros'),
                    'confidence': result.get('confidence', 0.0),
                    'reasoning': result.get('reasoning', ''),
                    'raw_response': response
                }
                
            except json.JSONDecodeError:
                # Fallback: tentar extrair tipo da resposta
                response_lower = response.lower()
                if 'locacao' in response_lower or 'aluguel' in response_lower:
                    contract_type = 'locacao'
                elif 'telecom' in response_lower or 'internet' in response_lower:
                    contract_type = 'telecom'
                elif 'financeiro' in response_lower or 'emprestimo' in response_lower:
                    contract_type = 'financeiro'
                else:
                    contract_type = 'outros'
                
                return {
                    'success': True,
                    'contract_type': contract_type,
                    'confidence': 0.7,
                    'reasoning': 'Classificação por palavras-chave (fallback)',
                    'raw_response': response
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'contract_type': 'outros'
            }
    
    async def _analyze_with_specialist(
        self, 
        contract_text: str, 
        contract_type: str, 
        routing_info: Dict
    ) -> Dict[str, Any]:
        """Realiza análise especializada do contrato"""
        
        try:
            # Criar cliente LLM apropriado
            client = self.llm_factory.create_client(routing_info['provider'])
            
            # Prompt especializado baseado no tipo
            analysis_prompt = self._get_specialized_prompt(contract_text, contract_type)
            
            response = await client.generate_response(
                prompt=analysis_prompt,
                max_tokens=1000,
                temperature=0.1
            )
            
            # Tentar parsear resposta estruturada
            try:
                # Limpar resposta
                clean_response = response.strip()
                if clean_response.startswith('```'):
                    lines = clean_response.split('\n')
                    clean_response = '\n'.join([line for line in lines if not line.startswith('```')])
                
                result = json.loads(clean_response)
                
                return {
                    'success': True,
                    'analysis': result,
                    'raw_response': response,
                    'risk_level': result.get('risk_level', 'medio')
                }
                
            except json.JSONDecodeError:
                # Fallback: análise básica
                return {
                    'success': True,
                    'analysis': {
                        'risk_level': 'medio',
                        'summary': response[:500] + '...' if len(response) > 500 else response,
                        'risk_factors': [],
                        'recommendations': ['Análise detalhada disponível na resposta completa'],
                        'confidence_score': 0.7
                    },
                    'raw_response': response,
                    'risk_level': 'medio'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis': {
                    'risk_level': 'alto',
                    'summary': f'Erro na análise: {str(e)}',
                    'risk_factors': [],
                    'recommendations': [],
                    'confidence_score': 0.0
                }
            }
    
    def _get_specialized_prompt(self, contract_text: str, contract_type: str) -> str:
        """Gera prompt especializado baseado no tipo de contrato"""
        
        base_prompt = f"""
Você é um advogado especialista em direito brasileiro. Analise este contrato de {contract_type} e identifique riscos jurídicos.

CONTRATO:
{contract_text[:3000]}...

ANÁLISE OBRIGATÓRIA:
1. Identifique cláusulas abusivas ou problemáticas
2. Avalie riscos para o consumidor/contratante
3. Verifique conformidade com leis brasileiras
4. Sugira recomendações práticas

RESPOSTA EM JSON:
{{
  "risk_level": "baixo|medio|alto",
  "summary": "resumo em 2-3 frases",
  "risk_factors": [
    {{
      "type": "clausula_abusiva|preco|prazo|garantia|outros",
      "description": "descrição do risco",
      "severity": "baixa|media|alta",
      "legal_basis": "lei ou código aplicável"
    }}
  ],
  "recommendations": ["lista de recomendações práticas"],
  "confidence_score": 0.95
}}
"""
        
        # Adicionar especializações por tipo
        if contract_type == 'locacao':
            specialization = """
FOQUE EM:
- Lei do Inquilinato (Lei 8.245/91)
- Garantias exigidas (fiador, seguro, caução)
- Reajustes e índices aplicados
- Cláusulas de rescisão antecipada
- Responsabilidades do locador e locatário
"""
        elif contract_type == 'telecom':
            specialization = """
FOQUE EM:
- Lei Geral de Telecomunicações
- ANATEL - regulamentações
- Fidelidade e multas de rescisão
- Velocidades prometidas vs. entregues
- Cobrança de serviços não solicitados
"""
        elif contract_type == 'financeiro':
            specialization = """
FOQUE EM:
- Código de Defesa do Consumidor
- Taxas de juros e CET
- Seguros opcionais
- Cláusulas de vencimento antecipado
- Proteção de dados (LGPD)
"""
        else:
            specialization = """
FOQUE EM:
- Código de Defesa do Consumidor
- Cláusulas abusivas gerais
- Direitos básicos do consumidor
- Foro de eleição
"""
        
        return base_prompt + "\n" + specialization

# Classe utilitária para testes
class PipelineTestManager:
    """Gerencia testes do pipeline"""
    
    def __init__(self):
        self.pipeline = ContractProcessorPipeline()
    
    async def test_with_sample_contracts(self):
        """Testa pipeline com contratos de exemplo"""
        
        print("🧪 TESTANDO PIPELINE COMPLETO")
        print("=" * 50)
        
        # Contratos de teste
        test_contracts = {
            'netflix.txt': """
CONTRATO DE ASSINATURA NETFLIX PREMIUM

CONTRATANTE: Netflix Brasil Entretenimento Ltda
ASSINANTE: João Silva

PLANO: Netflix Premium - R$ 45,90/mês
RENOVAÇÃO: Automática mensal
CANCELAMENTO: A qualquer momento
DISPOSITIVOS: Até 4 simultâneos
""",
            
            'locacao.txt': """
CONTRATO DE LOCAÇÃO RESIDENCIAL

LOCADOR: Maria Santos
LOCATÁRIO: João Silva  
IMÓVEL: Apartamento Rua das Flores, 123
VALOR: R$ 2.800,00 mensais
PRAZO: 24 meses
GARANTIA: Fiador + Seguro Fiança
REAJUSTE: IGPM anual
MULTA RESCISÃO: 3 aluguéis
""",
            
            'emprestimo.txt': """
CONTRATO DE EMPRÉSTIMO PESSOAL

BANCO: Banco XYZ S.A.
CLIENTE: João Silva
VALOR: R$ 50.000,00
PRAZO: 36 meses
TAXA: 2,5% a.m. + IOF
PRESTAÇÃO: R$ 2.847,00
SEGURO: Prestamista obrigatório R$ 180,00/mês
GARANTIA: Avalista obrigatório
"""
        }
        
        results = []
        
        for filename, content in test_contracts.items():
            print(f"\n🔍 Testando: {filename}")
            print("-" * 30)
            
            # Simular arquivo
            file_content = content.encode('utf-8')
            
            # Processar
            result = await self.pipeline.process_contract_file(
                file_content=file_content,
                filename=filename,
                contract_id=f"test_{filename.split('.')[0]}"
            )
            
            # Mostrar resultado
            if result['success']:
                print(f"✅ Processado com sucesso!")
                print(f"   Tipo: {result['classification']['contract_type']}")
                print(f"   Risco: {result['analysis']['risk_level']}")
                print(f"   Modelo usado: {result['routing_data']['selected_model']}")
                print(f"   Custo estimado: ${result['routing_data']['estimated_cost']:.6f}")
                print(f"   Tempo: {result['processing_time_seconds']:.2f}s")
            else:
                print(f"❌ Falha: {result['error']}")
            
            results.append(result)
        
        # Resumo final
        print(f"\n📊 RESUMO DOS TESTES")
        print("=" * 30)
        
        successful = sum(1 for r in results if r['success'])
        total = len(results)
        
        print(f"✅ Sucessos: {successful}/{total}")
        
        if successful > 0:
            avg_time = sum(r.get('processing_time_seconds', 0) for r in results if r['success']) / successful
            total_cost = sum(r.get('routing_data', {}).get('estimated_cost', 0) for r in results if r['success'])
            
            print(f"⏱️ Tempo médio: {avg_time:.2f}s")
            print(f"💰 Custo total: ${total_cost:.6f}")
        
        return results

# Função principal para testes
async def main():
    """Executa testes do pipeline"""
    
    tester = PipelineTestManager()
    await tester.test_with_sample_contracts()

if __name__ == "__main__":
    asyncio.run(main())