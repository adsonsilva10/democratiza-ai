"""
Democratiza AI - Demonstração Completa do Roteador de LLMs
Simula análises de contratos com diferentes níveis de complexidade
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List

# Simulação das classes (na implementação real, importar dos módulos)
from app.services.llm_router import LLMRouter, ComplexityLevel, LLMProvider
from app.services.contract_analysis_service import ContractAnalysisService

class LLMRouterDemo:
    """Demonstração completa do sistema de roteamento inteligente"""
    
    def __init__(self):
        print("🤖 DEMOCRATIZA AI - SISTEMA DE ROTEAMENTO INTELIGENTE DE LLMs")
        print("=" * 70)
        print()
        
        # Contratos de exemplo com diferentes complexidades
        self.sample_contracts = {
            ComplexityLevel.SIMPLES: {
                'title': 'Contrato de Streaming Netflix',
                'text': """
                CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE STREAMING
                
                CONTRATANTE: João Silva
                CONTRATADA: Netflix Brasil
                
                O CONTRATANTE concorda em pagar mensalidade de R$ 25,90 pelo acesso ao catálogo de filmes e séries.
                
                1. PAGAMENTO: Cobrança mensal automática no cartão de crédito
                2. CANCELAMENTO: Pode ser feito a qualquer momento
                3. PRAZO: Indeterminado, renovação automática
                4. USO: Streaming de conteúdo para entretenimento pessoal
                """,
                'metadata': {
                    'valor': 25.90,
                    'duracao_meses': 12,
                    'tipo': 'streaming'
                }
            },
            
            ComplexityLevel.MEDIO: {
                'title': 'Contrato de Locação Residencial',
                'text': """
                CONTRATO DE LOCAÇÃO DE IMÓVEL RESIDENCIAL
                
                LOCADOR: Maria Santos
                LOCATÁRIO: Pedro Oliveira
                IMÓVEL: Apartamento Rua das Flores, 123
                
                Cláusula 1ª - DO OBJETO: Locação de apartamento mobiliado com 2 quartos
                Cláusula 2ª - DO PRAZO: 24 meses, iniciando em 01/01/2024
                Cláusula 3ª - DO VALOR: R$ 1.500,00 mensais, reajuste anual pelo IGPM
                Cláusula 4ª - DAS GARANTIAS: Caução de R$ 3.000,00 + Fiador
                Cláusula 5ª - DAS OBRIGAÇÕES: Manutenção preventiva por conta do locatário
                Cláusula 6ª - DA RESCISÃO: Multa de 3 aluguéis para rescisão antecipada
                
                Art. 22 da Lei 8.245/91 - Obrigações do locador
                """,
                'metadata': {
                    'valor': 1500.00,
                    'duracao_meses': 24,
                    'tipo': 'locacao_residencial'
                }
            },
            
            ComplexityLevel.COMPLEXO: {
                'title': 'Contrato de Prestação de Serviços Empresariais',
                'text': """
                CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE CONSULTORIA EMPRESARIAL
                
                CONTRATANTE: Tech Solutions Ltda (CNPJ 12.345.678/0001-90)
                CONTRATADA: Consulting Group S/A (CNPJ 98.765.432/0001-10)
                
                Cláusula 1ª - OBJETO: Prestação de serviços especializados de consultoria em transformação digital
                
                Cláusula 2ª - ESCOPO DOS SERVIÇOS:
                a) Diagnóstico organizacional completo
                b) Implementação de ERP integrado
                c) Treinamento de equipes técnicas
                d) Suporte técnico por 12 meses
                
                Cláusula 3ª - VALOR E FORMA DE PAGAMENTO:
                - Valor total: R$ 180.000,00 (cento e oitenta mil reais)
                - 30% na assinatura (R$ 54.000,00)
                - 40% na entrega do diagnóstico (R$ 72.000,00)
                - 30% na conclusão da implementação (R$ 54.000,00)
                
                Cláusula 4ª - PRAZO DE EXECUÇÃO: 18 meses, prorrogável por mútuo acordo
                
                Cláusula 5ª - CLÁUSULA PENAL: 
                - Atraso: 0,5% ao dia sobre valor em aberto
                - Rescisão unilateral: 20% sobre valor total do contrato
                
                Cláusula 6ª - CONFIDENCIALIDADE: Sigilo absoluto sobre informações técnicas e comerciais
                
                Cláusula 7ª - PROPRIEDADE INTELECTUAL: Desenvolvimentos customizados permanecem com a CONTRATANTE
                
                Cláusula 8ª - FORÇA MAIOR: Suspensão de obrigações em casos de força maior ou caso fortuito
                
                Cláusula 9ª - FORO: Comarca de São Paulo/SP, com renúncia a qualquer outro
                """,
                'metadata': {
                    'valor': 180000.00,
                    'duracao_meses': 18,
                    'tipo': 'prestacao_servicos_empresarial'
                }
            },
            
            ComplexityLevel.ESPECIALIZADO: {
                'title': 'Contrato de Previdência Privada PGBL',
                'text': """
                CONTRATO DE PLANO GERADOR DE BENEFÍCIO LIVRE - PGBL
                
                PARTICIPANTE: Carlos Eduardo Mendes (CPF 123.456.789-00)
                ENTIDADE: Brasilprev Seguros e Previdência S.A. (CNPJ 27.055.699/0001-02)
                
                PLANO: PGBL Crescimento Moderado
                
                Cláusula 1ª - DO REGIME PREVIDENCIÁRIO:
                Este contrato rege-se pela Lei Complementar nº 109/2001 e regulamentação da SUSEP
                
                Cláusula 2ª - DAS CONTRIBUIÇÕES:
                - Contribuição inicial: R$ 50.000,00
                - Contribuições mensais: R$ 2.000,00 (indexadas ao INPC)
                - Contribuições extras: Permitidas sem limite
                - Portabilidade: Permitida após 60 dias da adesão
                
                Cláusula 3ª - DO REGIME TRIBUTÁRIO:
                Tributação regressiva conforme tabela da Receita Federal:
                - Até 2 anos: 35%
                - 2 a 4 anos: 30%
                - 4 a 6 anos: 25%
                - 6 a 8 anos: 20%
                - 8 a 10 anos: 15%
                - Acima de 10 anos: 10%
                
                Cláusula 4ª - DAS TAXAS:
                - Taxa de administração: 2,5% a.a. sobre patrimônio acumulado
                - Taxa de carregamento: 3% sobre aportes até R$ 10.000/ano
                - Taxa de performance: 20% sobre rendimento que exceder 100% do CDI
                
                Cláusula 5ª - DOS BENEFÍCIOS:
                - Renda mensal vitalícia
                - Renda mensal temporária (10, 15 ou 20 anos)
                - Pecúlio por morte
                - Resgate total ou parcial (sujeito à tributação)
                
                Cláusula 6ª - DA COMPOSIÇÃO DA CARTEIRA:
                - Até 70% em Renda Fixa (títulos públicos e privados)
                - Até 30% em Renda Variável (ações e fundos de investimento)
                - Até 20% no Exterior (fundos cambiais)
                
                Cláusula 7ª - DAS GARANTIAS ATUARIAIS:
                Tábua de mortalidade AT-2000 Basic masculina e feminina, com taxa de juros de 6% a.a.
                
                Cláusula 8ª - DA ALTERAÇÃO UNILATERAL:
                A Entidade poderá alterar taxas e condições mediante comunicação prévia de 60 dias
                e aprovação da SUSEP.
                
                Fundamentação Legal:
                - Lei Complementar 109/2001 (Regime de Previdência Complementar)
                - Resolução CNSP 139/2005 (Planos PGBL)
                - Circular SUSEP 302/2005 (Taxas e Regulamentação)
                """,
                'metadata': {
                    'valor': 50000.00,
                    'duracao_meses': 360,  # 30 anos
                    'tipo': 'previdencia_privada_pgbl'
                }
            }
        }
    
    async def run_complete_demo(self):
        """Executa demonstração completa do sistema"""
        
        print("📊 DEMONSTRAÇÃO POR NÍVEL DE COMPLEXIDADE")
        print("-" * 50)
        
        total_cost_with_routing = 0.0
        total_cost_without_routing = 0.0
        
        for complexity_level, contract_info in self.sample_contracts.items():
            print(f"\n🔍 ANÁLISE: {contract_info['title']}")
            print(f"📈 Complexidade: {complexity_level.value.upper()}")
            print(f"📄 Tamanho: {len(contract_info['text'])} caracteres")
            
            # Simular análise de complexidade
            complexity_analysis = self._analyze_complexity_mock(
                contract_info['text'], 
                contract_info['metadata']
            )
            
            print(f"🎯 Score de Complexidade: {complexity_analysis['total_score']}")
            print(f"💡 Reasoning: {complexity_analysis['reasoning']}")
            
            # Simular roteamento
            routing_decision = self._simulate_routing(complexity_level, len(contract_info['text']))
            
            print(f"🤖 Modelo Selecionado: {routing_decision['selected_model']}")
            print(f"💰 Custo Estimado: ${routing_decision['estimated_cost']:.4f}")
            print(f"⚡ Tempo Estimado: {routing_decision['estimated_time']}s")
            
            # Comparar com custo se usasse sempre Opus
            opus_cost = routing_decision['opus_cost']
            savings = opus_cost - routing_decision['estimated_cost']
            savings_pct = (savings / opus_cost) * 100 if opus_cost > 0 else 0
            
            print(f"💸 Economia vs Opus: ${savings:.4f} ({savings_pct:.1f}%)")
            
            total_cost_with_routing += routing_decision['estimated_cost']
            total_cost_without_routing += opus_cost
            
            # Simular resultado da análise
            analysis_preview = self._simulate_analysis_result(complexity_level, contract_info)
            print(f"📋 Preview da Análise:")
            print(f"   Risk Level: {analysis_preview['risk_level']}")
            print(f"   Key Issues: {len(analysis_preview['issues'])} identificados")
            print(f"   Recommendations: {len(analysis_preview['recommendations'])} sugestões")
        
        # Resumo final
        print(f"\n🎉 RESUMO FINAL DA DEMONSTRAÇÃO")
        print("=" * 50)
        print(f"💰 Custo total com roteamento: ${total_cost_with_routing:.4f}")
        print(f"💸 Custo sem roteamento (só Opus): ${total_cost_without_routing:.4f}")
        
        total_savings = total_cost_without_routing - total_cost_with_routing
        savings_percentage = (total_savings / total_cost_without_routing) * 100 if total_cost_without_routing > 0 else 0
        
        print(f"🏆 Economia Total: ${total_savings:.4f} ({savings_percentage:.1f}%)")
        print(f"📊 Eficiência do Sistema: {100 - (total_cost_with_routing/total_cost_without_routing*100):.1f}% de redução de custos")
        
        # Demonstrar estatísticas de uso
        print(f"\n📈 ESTATÍSTICAS SIMULADAS DE USO")
        print("-" * 40)
        
        usage_stats = {
            'groq_llama': {'requests': 1, 'cost': 0.0025, 'avg_time': '2.3s'},
            'anthropic_haiku': {'requests': 1, 'cost': 0.0180, 'avg_time': '4.1s'},
            'anthropic_sonnet': {'requests': 1, 'cost': 0.0420, 'avg_time': '6.8s'},
            'anthropic_opus': {'requests': 1, 'cost': 0.1850, 'avg_time': '9.2s'}
        }
        
        for model, stats in usage_stats.items():
            print(f"🤖 {model:<18}: {stats['requests']:>3} req | ${stats['cost']:>7.4f} | {stats['avg_time']:>6}")
        
        print(f"\n✨ BENEFÍCIOS DO SISTEMA:")
        print(f"   🎯 Roteamento inteligente baseado em complexidade")
        print(f"   💰 Redução significativa de custos operacionais")
        print(f"   ⚡ Otimização de tempo de resposta")
        print(f"   🧠 Qualidade adequada para cada tipo de análise")
        print(f"   📊 Métricas detalhadas de performance e custos")
    
    def _analyze_complexity_mock(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Simula análise de complexidade"""
        
        text_length = len(text)
        word_count = len(text.split())
        
        # Score baseado em tamanho
        size_score = min(word_count // 100, 10)
        
        # Score baseado em termos especializados
        specialized_terms = [
            'previdência', 'aposentadoria', 'susep', 'pgbl', 'vgbl',
            'cláusula penal', 'força maior', 'arbitragem',
            'propriedade intelectual', 'confidencialidade'
        ]
        
        specialized_score = sum(1 for term in specialized_terms if term.lower() in text.lower()) * 2
        
        # Score baseado em metadados
        metadata_score = 0
        if metadata.get('valor', 0) > 50000:
            metadata_score += 3
        if metadata.get('duracao_meses', 0) > 24:
            metadata_score += 2
        
        total_score = size_score + specialized_score + metadata_score
        
        reasoning_parts = []
        if specialized_score > 0:
            reasoning_parts.append(f"{specialized_score//2} termos especializados")
        if metadata_score > 0:
            reasoning_parts.append("Alto valor/longo prazo")
        if size_score > 5:
            reasoning_parts.append("Documento extenso")
        
        reasoning = '; '.join(reasoning_parts) if reasoning_parts else "Análise básica"
        
        return {
            'total_score': total_score,
            'breakdown': {
                'size_score': size_score,
                'specialized_score': specialized_score,
                'metadata_score': metadata_score
            },
            'reasoning': reasoning
        }
    
    def _simulate_routing(self, complexity: ComplexityLevel, text_length: int) -> Dict[str, Any]:
        """Simula decisão de roteamento"""
        
        # Mapear complexidade para modelo e custos
        routing_map = {
            ComplexityLevel.SIMPLES: {
                'model': 'groq_llama',
                'cost_per_1k': 0.0005,
                'speed': 2.3
            },
            ComplexityLevel.MEDIO: {
                'model': 'anthropic_haiku',
                'cost_per_1k': 0.0015,
                'speed': 4.1
            },
            ComplexityLevel.COMPLEXO: {
                'model': 'anthropic_sonnet',
                'cost_per_1k': 0.015,
                'speed': 6.8
            },
            ComplexityLevel.ESPECIALIZADO: {
                'model': 'anthropic_opus',
                'cost_per_1k': 0.075,
                'speed': 9.2
            }
        }
        
        selected = routing_map[complexity]
        
        # Estimar tokens (4 chars per token + output tokens)
        estimated_tokens = (text_length // 4) + 2000  # input + output
        
        # Calcular custos
        estimated_cost = (estimated_tokens / 1000) * selected['cost_per_1k']
        opus_cost = (estimated_tokens / 1000) * routing_map[ComplexityLevel.ESPECIALIZADO]['cost_per_1k']
        
        return {
            'selected_model': selected['model'],
            'estimated_cost': estimated_cost,
            'opus_cost': opus_cost,
            'estimated_time': selected['speed'],
            'estimated_tokens': estimated_tokens
        }
    
    def _simulate_analysis_result(self, complexity: ComplexityLevel, contract_info: Dict[str, Any]) -> Dict[str, Any]:
        """Simula resultado da análise"""
        
        analysis_map = {
            ComplexityLevel.SIMPLES: {
                'risk_level': 'BAIXO',
                'issues': ['Renovação automática', 'Cobrança recorrente'],
                'recommendations': ['Verificar política de cancelamento', 'Monitorar cobranças']
            },
            ComplexityLevel.MEDIO: {
                'risk_level': 'MÉDIO',
                'issues': ['Múltiplas garantias', 'Multa rescisória alta', 'Reajuste anual'],
                'recommendations': ['Negociar garantias', 'Revisar multa', 'Acompanhar reajustes']
            },
            ComplexityLevel.COMPLEXO: {
                'risk_level': 'ALTO',
                'issues': ['Cláusula penal elevada', 'Propriedade intelectual', 'Pagamento parcelado'],
                'recommendations': ['Revisar penalidades', 'Esclarecer PI', 'Garantir etapas']
            },
            ComplexityLevel.ESPECIALIZADO: {
                'risk_level': 'ALTO',
                'issues': ['Taxa administração alta', 'Alteração unilateral', 'Tributação complexa'],
                'recommendations': ['Negociar taxas', 'Limitar alterações', 'Planejar IR']
            }
        }
        
        return analysis_map[complexity]

async def main():
    """Executa demonstração completa"""
    demo = LLMRouterDemo()
    await demo.run_complete_demo()

if __name__ == "__main__":
    print("🚀 Iniciando demonstração do roteador inteligente de LLMs...")
    print()
    
    asyncio.run(main())