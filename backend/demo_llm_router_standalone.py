"""
Democratiza AI - Demonstração Standalone do Roteador de LLMs
Simulação completa sem dependências externas
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
from enum import Enum

class ComplexityLevel(Enum):
    """Níveis de complexidade de contratos"""
    SIMPLES = "simples"
    MEDIO = "medio" 
    COMPLEXO = "complexo"
    ESPECIALIZADO = "especializado"

class LLMRouterDemo:
    """Demonstração completa do sistema de roteamento inteligente"""
    
    def __init__(self):
        print("🤖 DEMOCRATIZA AI - SISTEMA DE ROTEAMENTO INTELIGENTE DE LLMs")
        print("=" * 70)
        print()
        
        # Configuração dos modelos (custos reais)
        self.llm_costs = {
            'groq_llama': {
                'cost_per_1k_tokens': 0.0005,  # Muito econômico
                'speed_avg_seconds': 2.3,
                'quality': 'Boa para análises simples'
            },
            'anthropic_haiku': {
                'cost_per_1k_tokens': 0.0015,  # Econômico
                'speed_avg_seconds': 4.1,
                'quality': 'Boa para análises médias'
            },
            'anthropic_sonnet': {
                'cost_per_1k_tokens': 0.015,   # Médio
                'speed_avg_seconds': 6.8,
                'quality': 'Excelente para análises complexas'
            },
            'anthropic_opus': {
                'cost_per_1k_tokens': 0.075,   # Premium
                'speed_avg_seconds': 9.2,
                'quality': 'Máxima qualidade para casos especializados'
            }
        }
        
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
        analysis_results = []
        
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
            print(f"   🎯 Risk Level: {analysis_preview['risk_level']}")
            print(f"   ⚠️  Key Issues: {len(analysis_preview['issues'])} identificados")
            print(f"   💡 Recommendations: {len(analysis_preview['recommendations'])} sugestões")
            
            # Armazenar para estatísticas
            analysis_results.append({
                'complexity': complexity_level,
                'contract': contract_info['title'],
                'model': routing_decision['selected_model'],
                'cost': routing_decision['estimated_cost'],
                'opus_cost': opus_cost,
                'savings': savings
            })
        
        # Resumo final
        print(f"\n🎉 RESUMO FINAL DA DEMONSTRAÇÃO")
        print("=" * 50)
        print(f"💰 Custo total com roteamento: ${total_cost_with_routing:.4f}")
        print(f"💸 Custo sem roteamento (só Opus): ${total_cost_without_routing:.4f}")
        
        total_savings = total_cost_without_routing - total_cost_with_routing
        savings_percentage = (total_savings / total_cost_without_routing) * 100 if total_cost_without_routing > 0 else 0
        
        print(f"🏆 Economia Total: ${total_savings:.4f} ({savings_percentage:.1f}%)")
        print(f"📊 Eficiência do Sistema: {savings_percentage:.1f}% de redução de custos")
        
        # Demonstrar distribuição de uso
        print(f"\n📈 DISTRIBUIÇÃO DE MODELOS UTILIZADOS")
        print("-" * 45)
        
        model_usage = {}
        for result in analysis_results:
            model = result['model']
            if model not in model_usage:
                model_usage[model] = {'count': 0, 'total_cost': 0.0}
            model_usage[model]['count'] += 1
            model_usage[model]['total_cost'] += result['cost']
        
        for model, stats in model_usage.items():
            percentage = (stats['count'] / len(analysis_results)) * 100
            print(f"🤖 {model:<20}: {stats['count']:>1} uso ({percentage:>5.1f}%) | ${stats['total_cost']:>7.4f}")
        
        # Projeção de economia em escala
        print(f"\n📊 PROJEÇÃO DE ECONOMIA EM ESCALA")
        print("-" * 40)
        
        monthly_analyses = [100, 500, 1000, 5000]
        for monthly in monthly_analyses:
            monthly_cost_smart = total_cost_with_routing * monthly / len(self.sample_contracts)
            monthly_cost_opus = total_cost_without_routing * monthly / len(self.sample_contracts)
            monthly_savings = monthly_cost_opus - monthly_cost_smart
            annual_savings = monthly_savings * 12
            
            print(f"📅 {monthly:>4} análises/mês: ${monthly_savings:>7.2f}/mês | ${annual_savings:>8.2f}/ano economia")
        
        print(f"\n✨ BENEFÍCIOS DO SISTEMA:")
        print(f"   🎯 Roteamento inteligente baseado em complexidade real")
        print(f"   💰 Redução de {savings_percentage:.1f}% nos custos operacionais")
        print(f"   ⚡ Otimização automática de tempo vs qualidade")
        print(f"   🧠 Qualidade adequada para cada tipo de análise")
        print(f"   📊 Métricas detalhadas de performance e ROI")
        print(f"   🔄 Aprendizado contínuo para melhores decisões")
        
        # Casos de uso específicos
        print(f"\n🎯 CASOS DE USO RECOMENDADOS:")
        print("-" * 35)
        
        use_cases = {
            'groq_llama': 'Triagem inicial, contratos padronizados, análises rápidas',
            'anthropic_haiku': 'Contratos comerciais médios, relatórios detalhados',
            'anthropic_sonnet': 'Contratos complexos, due diligence, análises críticas',
            'anthropic_opus': 'Casos especializados, previdência, M&A, compliance'
        }
        
        for model, use_case in use_cases.items():
            print(f"🤖 {model:<18}: {use_case}")
        
        print(f"\n🔧 CONFIGURAÇÕES RECOMENDADAS:")
        print("-" * 35)
        print(f"   📊 Monitoramento contínuo de custos por categoria")
        print(f"   🎛️  Ajuste de thresholds baseado no volume de uso")
        print(f"   📈 A/B testing para validação de qualidade")
        print(f"   🔄 Feedback loop para refinamento do roteamento")
        print(f"   📋 Relatórios executivos de ROI mensal")
    
    def _analyze_complexity_mock(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Simula análise de complexidade"""
        
        text_length = len(text)
        word_count = len(text.split())
        text_lower = text.lower()
        
        # Score baseado em tamanho
        size_score = min(word_count // 150, 8)
        
        # Score baseado em termos especializados
        specialized_terms = {
            'previdência': 4, 'aposentadoria': 4, 'susep': 3, 'pgbl': 4, 'vgbl': 4,
            'cláusula penal': 3, 'força maior': 2, 'arbitragem': 3,
            'propriedade intelectual': 3, 'confidencialidade': 2,
            'lei complementar': 2, 'cnpj': 1, 'rescisão': 2
        }
        
        specialized_score = sum(
            score for term, score in specialized_terms.items() 
            if term in text_lower
        )
        
        # Score baseado em valores monetários
        import re
        money_matches = re.findall(r'R\$\s*[\d,.]+', text)
        money_score = min(len(money_matches), 5)
        
        # Score baseado em referências legais  
        legal_refs = re.findall(r'Lei\s+\d+|Art\.|Cláusula|§', text)
        legal_score = min(len(legal_refs) // 2, 6)
        
        # Score baseado em metadados
        metadata_score = 0
        if metadata.get('valor', 0) > 50000:
            metadata_score += 4
        elif metadata.get('valor', 0) > 10000:
            metadata_score += 2
            
        if metadata.get('duracao_meses', 0) > 60:
            metadata_score += 3
        elif metadata.get('duracao_meses', 0) > 12:
            metadata_score += 1
        
        total_score = size_score + specialized_score + money_score + legal_score + metadata_score
        
        reasoning_parts = []
        if specialized_score > 5:
            reasoning_parts.append(f"Termos altamente especializados ({specialized_score}pts)")
        elif specialized_score > 0:
            reasoning_parts.append(f"Termos especializados ({specialized_score}pts)")
            
        if legal_score > 3:
            reasoning_parts.append(f"Muitas referências legais ({legal_score}pts)")
        elif legal_score > 0:
            reasoning_parts.append(f"Referências legais ({legal_score}pts)")
            
        if metadata_score > 3:
            reasoning_parts.append("Alto valor/longo prazo")
        elif metadata_score > 0:
            reasoning_parts.append("Valor/prazo significativo")
            
        if size_score > 5:
            reasoning_parts.append("Documento extenso")
        
        reasoning = '; '.join(reasoning_parts) if reasoning_parts else f"Análise básica (score: {total_score})"
        
        return {
            'total_score': total_score,
            'breakdown': {
                'size_score': size_score,
                'specialized_score': specialized_score,
                'money_score': money_score,
                'legal_score': legal_score,
                'metadata_score': metadata_score
            },
            'reasoning': reasoning
        }
    
    def _simulate_routing(self, complexity: ComplexityLevel, text_length: int) -> Dict[str, Any]:
        """Simula decisão de roteamento"""
        
        # Mapear complexidade para modelo
        routing_map = {
            ComplexityLevel.SIMPLES: 'groq_llama',
            ComplexityLevel.MEDIO: 'anthropic_haiku',
            ComplexityLevel.COMPLEXO: 'anthropic_sonnet',
            ComplexityLevel.ESPECIALIZADO: 'anthropic_opus'
        }
        
        selected_model = routing_map[complexity]
        model_config = self.llm_costs[selected_model]
        
        # Estimar tokens (aproximação: 4 chars per token + tokens de output)
        input_tokens = text_length // 4
        output_tokens = {
            ComplexityLevel.SIMPLES: 800,
            ComplexityLevel.MEDIO: 1500,
            ComplexityLevel.COMPLEXO: 2500,
            ComplexityLevel.ESPECIALIZADO: 4000
        }[complexity]
        
        total_tokens = input_tokens + output_tokens
        
        # Calcular custos
        estimated_cost = (total_tokens / 1000) * model_config['cost_per_1k_tokens']
        opus_cost = (total_tokens / 1000) * self.llm_costs['anthropic_opus']['cost_per_1k_tokens']
        
        return {
            'selected_model': selected_model,
            'estimated_cost': estimated_cost,
            'opus_cost': opus_cost,
            'estimated_time': model_config['speed_avg_seconds'],
            'estimated_tokens': total_tokens,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens
        }
    
    def _simulate_analysis_result(self, complexity: ComplexityLevel, contract_info: Dict[str, Any]) -> Dict[str, Any]:
        """Simula resultado da análise baseado na complexidade"""
        
        analysis_map = {
            ComplexityLevel.SIMPLES: {
                'risk_level': 'BAIXO',
                'issues': [
                    'Renovação automática sem notificação prévia',
                    'Cobrança recorrente no cartão de crédito'
                ],
                'recommendations': [
                    'Verificar política de cancelamento',
                    'Monitorar extratos de cobrança',
                    'Definir alerta de renovação'
                ]
            },
            ComplexityLevel.MEDIO: {
                'risk_level': 'MÉDIO',
                'issues': [
                    'Múltiplas garantias exigidas (caução + fiador)',
                    'Multa rescisória de 3 aluguéis (alta)',
                    'Reajuste anual sem teto definido',
                    'Manutenção por conta do locatário'
                ],
                'recommendations': [
                    'Negociar redução para uma única garantia',
                    'Propor multa proporcional ao tempo restante',
                    'Estabelecer limite para reajustes',
                    'Esclarecer responsabilidades de manutenção'
                ]
            },
            ComplexityLevel.COMPLEXO: {
                'risk_level': 'ALTO',
                'issues': [
                    'Cláusula penal de 20% muito elevada',
                    'Propriedade intelectual mal definida',
                    'Pagamento concentrado nas fases iniciais',
                    'Confidencialidade muito ampla',
                    'Foro de eleição restritivo'
                ],
                'recommendations': [
                    'Renegociar cláusula penal para máximo 10%',
                    'Detalhar direitos de propriedade intelectual',
                    'Equilibrar cronograma de pagamentos',
                    'Limitar escopo da confidencialidade',
                    'Avaliar alternativa de arbitragem'
                ]
            },
            ComplexityLevel.ESPECIALIZADO: {
                'risk_level': 'ALTO',
                'issues': [
                    'Taxa de administração 2,5% acima do mercado',
                    'Cláusula de alteração unilateral muito ampla',
                    'Tributação regressiva pode ser desvantajosa',
                    'Taxa de performance de 20% muito alta',
                    'Composição de carteira sem transparência'
                ],
                'recommendations': [
                    'Negociar taxa de administração máxima de 2%',
                    'Limitar alterações unilaterais a casos específicos',
                    'Simular cenários tributários progressivo vs regressivo',
                    'Revisar taxa de performance para máximo 15%',
                    'Exigir transparência total da carteira',
                    'Considerar portabilidade para planos mais vantajosos'
                ]
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