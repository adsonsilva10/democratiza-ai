"""
Mock LLM Service para desenvolvimento sem custos de API
Simula análise de contratos usando regras pré-definidas
"""
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class MockLLMService:
    """
    Serviço LLM simulado para análise de contratos
    Usa regras e templates pré-definidos
    """
    
    def __init__(self):
        self.risk_patterns = self._initialize_risk_patterns()
        self.contract_templates = self._initialize_contract_templates()
    
    def _initialize_risk_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Inicializa padrões de risco para análise automatizada"""
        return {
            "high_risk": [
                {
                    "patterns": ["multa", "penalidade", "rescisão unilateral", "sem direito a reembolso"],
                    "description": "Cláusulas com penalidades excessivas ou unilaterais",
                    "recommendation": "Negocie condições mais equilibradas ou busque assessoria jurídica"
                },
                {
                    "patterns": ["isenta", "exime", "não se responsabiliza", "por conta do contratante"],
                    "description": "Cláusulas que isentam responsabilidades do fornecedor",
                    "recommendation": "Estas cláusulas podem ser abusivas segundo o CDC"
                },
                {
                    "patterns": ["irrevogável", "irretratável", "não pode ser cancelado"],
                    "description": "Cláusulas que impedem cancelamento ou desistência",
                    "recommendation": "Verifique se respeitam o prazo de arrependimento do CDC"
                }
            ],
            "medium_risk": [
                {
                    "patterns": ["reajuste", "correção monetária", "índice", "percentual"],
                    "description": "Cláusulas de reajuste de valores",
                    "recommendation": "Verifique se os índices são oficiais e apropriados"
                },
                {
                    "patterns": ["prazo", "vencimento", "30 dias", "60 dias"],
                    "description": "Definições de prazos importantes",
                    "recommendation": "Certifique-se de que os prazos são razoáveis e cumprìveis"
                },
                {
                    "patterns": ["garantia", "fiança", "caução", "seguro"],
                    "description": "Exigências de garantias",
                    "recommendation": "Avalie se as garantias solicitadas são proporcionais ao risco"
                }
            ],
            "low_risk": [
                {
                    "patterns": ["direito do consumidor", "código de defesa", "legislação vigente"],
                    "description": "Referências à proteção do consumidor",
                    "recommendation": "Cláusulas que respeitam direitos básicos"
                },
                {
                    "patterns": ["foro", "comarca", "juízo competente"],
                    "description": "Definição de jurisdição",
                    "recommendation": "Cláusulas padrão de definição legal"
                }
            ]
        }
    
    def _initialize_contract_templates(self) -> Dict[str, Dict[str, Any]]:
        """Templates de análise por tipo de contrato"""
        return {
            "locacao": {
                "pontos_importantes": [
                    "Valor do aluguel e reajustes",
                    "Prazo de locação",
                    "Garantias exigidas",
                    "Responsabilidades do locatário",
                    "Condições de rescisão"
                ],
                "riscos_comuns": [
                    "Cláusulas de reajuste abusivas",
                    "Exigência de múltiplas garantias",
                    "Responsabilização por danos preexistentes",
                    "Multas rescisórias excessivas"
                ]
            },
            "telecom": {
                "pontos_importantes": [
                    "Velocidade contratada vs entregue",
                    "Permanência mínima",
                    "Multa por cancelamento",
                    "Suporte técnico",
                    "Garantias de qualidade"
                ],
                "riscos_comuns": [
                    "Velocidade não garantida",
                    "Multa rescisória abusiva",
                    "Renovação automática",
                    "Cobrança de serviços não contratados"
                ]
            },
            "financeiro": {
                "pontos_importantes": [
                    "Taxa de juros",
                    "IOF e demais encargos",
                    "Forma de pagamento",
                    "Consequências da inadimplência",
                    "Garantias exigidas"
                ],
                "riscos_comuns": [
                    "Juros abusivos",
                    "Capitalização irregular",
                    "Cláusulas leoninas",
                    "Cobrança de encargos não previstos"
                ]
            }
        }
    
    async def analyze_contract(self, 
                             contract_text: str, 
                             contract_type: Optional[str] = None) -> Dict[str, Any]:
        """Analisa contrato usando regras pré-definidas"""
        
        # Identifica tipo de contrato se não informado
        if not contract_type:
            contract_type = self._identify_contract_type(contract_text)
        
        # Executa análise
        risk_analysis = self._analyze_risks(contract_text)
        key_points = self._extract_key_points(contract_text, contract_type)
        recommendations = self._generate_recommendations(risk_analysis, contract_type)
        
        return {
            "contract_type": contract_type,
            "analysis_date": datetime.now().isoformat(),
            "risk_level": self._calculate_overall_risk(risk_analysis),
            "risk_analysis": risk_analysis,
            "key_points": key_points,
            "recommendations": recommendations,
            "summary": self._generate_summary(risk_analysis, contract_type),
            "legal_references": self._get_relevant_legal_refs(contract_type),
            "mock_analysis": True  # Indica que é análise simulada
        }
    
    def _identify_contract_type(self, text: str) -> str:
        """Identifica tipo de contrato baseado em palavras-chave"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["locação", "aluguel", "locador", "locatário"]):
            return "locacao"
        elif any(word in text_lower for word in ["internet", "telefone", "dados", "banda larga", "telecom"]):
            return "telecom"
        elif any(word in text_lower for word in ["empréstimo", "financiamento", "juros", "parcela", "crédito"]):
            return "financeiro"
        else:
            return "geral"
    
    def _analyze_risks(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Analisa riscos baseado em padrões"""
        results = {"high": [], "medium": [], "low": []}
        
        text_lower = text.lower()
        
        for risk_level, patterns_list in self.risk_patterns.items():
            for pattern_info in patterns_list:
                for pattern in pattern_info["patterns"]:
                    if pattern in text_lower:
                        # Encontra o contexto da cláusula
                        context = self._extract_context(text, pattern)
                        
                        risk_item = {
                            "clause": pattern,
                            "context": context,
                            "description": pattern_info["description"],
                            "recommendation": pattern_info["recommendation"],
                            "severity": risk_level.replace("_risk", "")
                        }
                        
                        results[risk_item["severity"]].append(risk_item)
        
        return results
    
    def _extract_context(self, text: str, pattern: str, context_length: int = 200) -> str:
        """Extrai contexto ao redor de um padrão encontrado"""
        pattern_index = text.lower().find(pattern.lower())
        if pattern_index == -1:
            return ""
        
        start = max(0, pattern_index - context_length // 2)
        end = min(len(text), pattern_index + len(pattern) + context_length // 2)
        
        context = text[start:end].strip()
        
        # Adiciona reticências se necessário
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."
            
        return context
    
    def _extract_key_points(self, text: str, contract_type: str) -> List[Dict[str, Any]]:
        """Extrai pontos-chave baseado no tipo de contrato"""
        key_points = []
        
        # Busca por valores monetários
        money_patterns = re.findall(r'R\$\s*[\d.,]+', text)
        if money_patterns:
            key_points.append({
                "category": "Valores",
                "content": f"Valores encontrados: {', '.join(money_patterns[:3])}",
                "importance": "high"
            })
        
        # Busca por datas e prazos
        date_patterns = re.findall(r'\d{1,2}/\d{1,2}/\d{4}|\d{1,2}\s+(?:dias?|meses?|anos?)', text)
        if date_patterns:
            key_points.append({
                "category": "Prazos",
                "content": f"Prazos identificados: {', '.join(date_patterns[:3])}",
                "importance": "medium"
            })
        
        # Adiciona pontos específicos por tipo
        template = self.contract_templates.get(contract_type, {})
        if template and "pontos_importantes" in template:
            for ponto in template["pontos_importantes"][:3]:
                if any(word.lower() in text.lower() for word in ponto.split()):
                    key_points.append({
                        "category": "Específico",
                        "content": f"Atenção para: {ponto}",
                        "importance": "medium"
                    })
        
        return key_points
    
    def _generate_recommendations(self, risk_analysis: Dict, contract_type: str) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recommendations = []
        
        high_risks = len(risk_analysis.get("high", []))
        medium_risks = len(risk_analysis.get("medium", []))
        
        if high_risks > 0:
            recommendations.append(
                f"⚠️ Atenção: {high_risks} cláusula(s) de alto risco identificada(s). "
                "Recomenda-se revisão jurídica antes da assinatura."
            )
        
        if medium_risks > 2:
            recommendations.append(
                f"📋 {medium_risks} pontos de atenção identificados. "
                "Revise cuidadosamente estas cláusulas."
            )
        
        # Recomendações específicas por tipo
        template = self.contract_templates.get(contract_type, {})
        if template and "riscos_comuns" in template:
            recommendations.append(
                f"💡 Para contratos de {contract_type}, fique atento a: "
                f"{', '.join(template['riscos_comuns'][:2])}"
            )
        
        if not recommendations:
            recommendations.append("✅ Análise preliminar não identificou riscos críticos.")
        
        return recommendations
    
    def _calculate_overall_risk(self, risk_analysis: Dict) -> str:
        """Calcula nível de risco geral"""
        high_count = len(risk_analysis.get("high", []))
        medium_count = len(risk_analysis.get("medium", []))
        
        if high_count >= 2:
            return "alto"
        elif high_count == 1 or medium_count >= 3:
            return "medio"
        else:
            return "baixo"
    
    def _generate_summary(self, risk_analysis: Dict, contract_type: str) -> str:
        """Gera resumo da análise"""
        high_count = len(risk_analysis.get("high", []))
        medium_count = len(risk_analysis.get("medium", []))
        low_count = len(risk_analysis.get("low", []))
        
        summary = f"Análise de contrato de {contract_type}:\n"
        summary += f"• {high_count} riscos altos, {medium_count} riscos médios, {low_count} pontos positivos\n"
        
        if high_count > 0:
            summary += "• Atenção especial necessária para cláusulas de alto risco\n"
        
        summary += "• Esta é uma análise preliminar automatizada"
        
        return summary
    
    def _get_relevant_legal_refs(self, contract_type: str) -> List[str]:
        """Retorna referências legais relevantes"""
        refs = ["Lei 8.078/90 - Código de Defesa do Consumidor"]
        
        if contract_type == "locacao":
            refs.append("Lei 8.245/91 - Lei do Inquilinato")
        elif contract_type == "telecom":
            refs.append("Lei 9.472/97 - Lei Geral de Telecomunicações")
        elif contract_type == "financeiro":
            refs.append("Lei 4.595/64 - Sistema Financeiro Nacional")
        
        refs.append("Lei 10.406/02 - Código Civil")
        return refs

    async def chat_with_contract(self, 
                               contract_analysis: Dict[str, Any], 
                               user_question: str) -> str:
        """Simula chat sobre análise de contrato"""
        question_lower = user_question.lower()
        
        # Respostas baseadas em padrões de perguntas
        if any(word in question_lower for word in ["risco", "perigoso", "problema"]):
            high_risks = contract_analysis.get("risk_analysis", {}).get("high", [])
            if high_risks:
                return f"Os principais riscos identificados são: {', '.join([r['description'] for r in high_risks[:2]])}. {high_risks[0]['recommendation']}"
            else:
                return "A análise não identificou riscos críticos neste contrato."
        
        elif any(word in question_lower for word in ["posso", "devo", "assinar"]):
            risk_level = contract_analysis.get("risk_level", "medio")
            if risk_level == "alto":
                return "Recomendo cautela. Este contrato apresenta cláusulas de alto risco. Considere buscar orientação jurídica antes de assinar."
            elif risk_level == "medio":
                return "O contrato apresenta alguns pontos de atenção. Revise cuidadosamente as cláusulas destacadas antes de assinar."
            else:
                return "A análise preliminar não identificou problemas críticos, mas sempre revise todo o documento antes de assinar."
        
        elif any(word in question_lower for word in ["multa", "penalidade", "cancelar"]):
            return "Verifique as cláusulas sobre cancelamento e penalidades. Segundo o CDC, multas excessivas podem ser consideradas abusivas."
        
        elif any(word in question_lower for word in ["legal", "lei", "direito"]):
            refs = contract_analysis.get("legal_references", [])
            return f"Este tipo de contrato é regulamentado por: {', '.join(refs[:2])}. Sempre consulte a legislação atual."
        
        else:
            return "Esta é uma análise automatizada. Para questões específicas, recomendo consultar um advogado especializado."

# Instância global
mock_llm_service = MockLLMService()