import re
from typing import Dict, Any, List, Tuple
from app.agents.entity_classifier import EntityClassifier, EntityInfo

class IntelligentClassifier:
    """Sistema inteligente de classificação automática de contratos"""
    
    def __init__(self):
        # Initialize entity classifier for CPF/CNPJ detection
        self.entity_classifier = EntityClassifier()
        
        # Mapeamento completo: categoria -> (agente, palavras-chave, peso)
        self.classification_rules = {
            # HABITAÇÃO E IMOBILIÁRIO
            'rental_residential': {
                'keywords': [
                    'aluguel', 'locação', 'inquilino', 'locador', 'imóvel residencial', 'apartamento',
                    'casa para alugar', 'contrato de locação', 'caução', 'fiador', 'iptu residencial',
                    'condomínio residencial', 'reforma apartamento', 'rescisão locação', 'vistoria imóvel'
                ],
                'agent': 'rental_residential',
                'priority': 10
            },
            'rental_commercial': {
                'keywords': [
                    'locação comercial', 'ponto comercial', 'loja', 'escritório', 'estabelecimento comercial',
                    'luva', 'renovação compulsória', 'fundo de comércio', 'alvará de funcionamento',
                    'iptu comercial', 'condomínio comercial', 'cessão de direitos comerciais', 'exploração comercial'
                ],
                'agent': 'rental_commercial',
                'priority': 10
            },
            'real_estate': {
                'keywords': [
                    'compra e venda', 'imóvel à venda', 'escritura', 'registro de imóveis', 'cartório',
                    'venda de imóvel', 'compromisso de compra e venda', 'sinal', 'itbi', 'habite-se',
                    'vício oculto', 'evicção', 'benfeitorias', 'matrícula do imóvel', 'financiamento imóvel'
                ],
                'agent': 'real_estate',
                'priority': 9
            },
            'housing_financing': {
                'keywords': [
                    'financiamento habitacional', 'casa própria', 'caixa econômica', 'banco do brasil',
                    'sistema financeiro habitação', 'sfh', 'alienação fiduciária', 'amortização',
                    'prestação casa', 'fgts', 'entrada imóvel', 'minha casa minha vida', 'sbpe'
                ],
                'agent': 'housing_financing',
                'priority': 9
            },
            
            # SERVIÇOS FINANCEIROS
            'personal_loan': {
                'keywords': [
                    'empréstimo pessoal', 'crediário', 'crédito consignado', 'crédito pré-aprovado',
                    'empréstimo com garantia', 'avalista', 'cdc empréstimo', 'juros empréstimo',
                    'refinanciamento', 'renegociação dívida', 'parcelamento', 'quitação antecipada',
                    'nome sujo', 'spc', 'serasa'
                ],
                'agent': 'personal_loan',
                'priority': 8
            },
            'credit_card': {
                'keywords': [
                    'cartão de crédito', 'anuidade cartão', 'limite cartão', 'rotativo cartão',
                    'fatura cartão', 'juros cartão', 'parcelamento cartão', 'bloqueio cartão',
                    'cancelamento cartão', 'bandeira cartão', 'mastercard', 'visa', 'elo',
                    'conta corrente', 'débito automático'
                ],
                'agent': 'credit_card',
                'priority': 8
            },
            'vehicle_financing': {
                'keywords': [
                    'financiamento veículo', 'financiamento carro', 'financiamento moto', 'carro financiado',
                    'alienação fiduciária veículo', 'vrg', 'valor residual garantido', 'leasing veículo',
                    'consórcio veículo', 'seguro financiamento', 'transferência financiamento', 'cdc veículo'
                ],
                'agent': 'vehicle_financing',
                'priority': 8
            },
            'consortium': {
                'keywords': [
                    'consórcio', 'carta de crédito', 'contemplação', 'lance consórcio', 'desistência consórcio',
                    'taxa administração consórcio', 'assembleia consórcio', 'fundo reserva consórcio',
                    'consórcio imóvel', 'consórcio veículo', 'consórcio eletrodomésticos', 'grupo consórcio'
                ],
                'agent': 'consortium',
                'priority': 7
            },
            
            # TELECOMUNICAÇÕES
            'internet': {
                'keywords': [
                    'internet banda larga', 'fibra óptica', 'velocidade internet', 'wifi', 'roteador',
                    'provedor internet', 'anatel internet', 'teste velocidade', 'instabilidade internet',
                    'cancelamento internet', 'mudança endereço internet', 'fidelidade internet', 'mega', 'adsl'
                ],
                'agent': 'internet',
                'priority': 7
            },
            'mobile': {
                'keywords': [
                    'telefone celular', 'plano celular', 'linha móvel', 'portabilidade', 'chip celular',
                    'recarga celular', 'dados móveis', '4g', '5g', 'roaming', 'tim', 'vivo', 'claro', 'oi',
                    'plano pós-pago', 'plano pré-pago', 'franquia dados'
                ],
                'agent': 'mobile',
                'priority': 7
            },
            'tv_subscription': {
                'keywords': [
                    'tv por assinatura', 'tv a cabo', 'sky', 'claro tv', 'vivo tv', 'oi tv',
                    'canais tv', 'programação tv', 'decoder', 'antena parabólica', 'permanência mínima tv',
                    'netflix', 'streaming', 'pacote tv', 'pay per view'
                ],
                'agent': 'tv_subscription',
                'priority': 6
            },
            
            # ENERGIA E UTILIDADES
            'electricity': {
                'keywords': [
                    'energia elétrica', 'conta luz', 'cpfl', 'enel', 'cemig', 'coelba', 'celpe',
                    'bandeira tarifária', 'tarifa energia', 'medidor luz', 'corte energia', 'religação',
                    'taxa iluminação pública', 'geração distribuída', 'energia solar', 'kwh'
                ],
                'agent': 'electricity',
                'priority': 6
            },
            'gas_supply': {
                'keywords': [
                    'gás natural', 'gás encanado', 'comgás', 'cea', 'gasbrasiliano', 'instalação gás',
                    'medidor gás', 'vazamento gás', 'segurança gás', 'conversão gás', 'tarifa gás',
                    'botijão gás', 'glp'
                ],
                'agent': 'gas_supply',
                'priority': 5
            },
            
            # TRANSPORTE E MOBILIDADE
            'vehicle_insurance': {
                'keywords': [
                    'seguro auto', 'seguro veículo', 'seguro carro', 'seguro moto', 'cobertura seguro',
                    'franquia', 'sinistro', 'guincho', 'carro reserva', 'vidros seguro', 'roubo veículo',
                    'colisão', 'terceiros seguro', 'dpvat', 'bonus seguro', 'apólice seguro', 'dpem'
                ],
                'agent': 'vehicle_insurance',
                'priority': 7
            },
            'vehicle_rental': {
                'keywords': [
                    'aluguel carro', 'locadora veículos', 'rental car', 'hertz', 'localiza', 'movida',
                    'unidas', 'combustível aluguel', 'seguro aluguel', 'franquia aluguel', 'devolução carro',
                    'quilometragem livre', 'condutor adicional', 'cartão crédito aluguel'
                ],
                'agent': 'vehicle_rental',
                'priority': 6
            },
            
            # SAÚDE
            'health_insurance': {
                'keywords': [
                    'plano saúde', 'convênio médico', 'unimed', 'bradesco saúde', 'sul américa saúde',
                    'amil', 'golden cross', 'carência plano', 'coparticipação', 'reembolso médico',
                    'rede credenciada', 'autorização exame', 'internação', 'urgência emergência',
                    'ans', 'agência nacional saúde suplementar', 'portabilidade carências'
                ],
                'agent': 'health_insurance',
                'priority': 9
            },
            'life_insurance': {
                'keywords': [
                    'seguro vida', 'apólice vida', 'beneficiário seguro', 'indenização morte',
                    'invalidez permanente', 'doenças graves', 'prêmio seguro vida', 'vigência seguro',
                    'exclusões seguro vida', 'suicídio seguro', 'declaração saúde', 'exame médico'
                ],
                'agent': 'life_insurance',
                'priority': 6
            },
            
            # EDUCAÇÃO
            'higher_education': {
                'keywords': [
                    'faculdade', 'universidade', 'ensino superior', 'graduação', 'pós-graduação',
                    'mensalidade faculdade', 'matrícula universidade', 'transferência faculdade',
                    'trancamento matrícula', 'diploma', 'histórico escolar', 'prouni', 'fies',
                    'bolsa estudos', 'vestibular', 'enade', 'mec'
                ],
                'agent': 'higher_education',
                'priority': 6
            },
            'professional_course': {
                'keywords': [
                    'curso profissionalizante', 'curso técnico', 'curso livre', 'certificado curso',
                    'senai', 'senac', 'sebrae', 'capacitação profissional', 'qualificação',
                    'desistência curso', 'devolução curso', 'ead', 'ensino distância'
                ],
                'agent': 'professional_course',
                'priority': 5
            },
            
            # TRABALHO
            'employment_clt': {
                'keywords': [
                    'contrato trabalho', 'clt', 'carteira assinada', 'registro trabalho',
                    'salário', 'vale transporte', 'vale refeição', 'plr', 'décimo terceiro',
                    'férias', 'rescisão contrato', 'aviso prévio', 'fgts', 'seguro desemprego',
                    'jornada trabalho', 'horas extras', 'adicional noturno', 'insalubridade'
                ],
                'agent': 'employment_clt',
                'priority': 8
            },
            'service_contract': {
                'keywords': [
                    'prestação serviços', 'contrato pj', 'pessoa jurídica', 'mei',
                    'microempreendedor individual', 'autônomo', 'freelancer', 'consultoria',
                    'exclusividade serviços', 'prazo contrato', 'rescisão prestação', 'nota fiscal'
                ],
                'agent': 'service_contract',
                'priority': 7
            },
            
            # CONSUMO E VAREJO
            'ecommerce': {
                'keywords': [
                    'compra online', 'e-commerce', 'loja virtual', 'mercado livre', 'amazon',
                    'shopee', 'magazine luiza', 'americanas', 'entrega produto', 'devolução produto',
                    'direito arrependimento', 'produto defeituoso', 'garantia produto', 'frete grátis',
                    'pagamento online', 'cartão virtual', 'boleto online'
                ],
                'agent': 'ecommerce',
                'priority': 6
            },
            'subscription_service': {
                'keywords': [
                    'assinatura mensal', 'streaming', 'netflix', 'spotify', 'amazon prime',
                    'disney plus', 'cancelamento assinatura', 'renovação automática', 'degustação grátis',
                    'período experimental', 'cobrança recorrente', 'débito automático assinatura'
                ],
                'agent': 'subscription_service',
                'priority': 5
            }
        }
    
    def classify_contract(self, text: str) -> Dict[str, Any]:
        """
        Classifica o contrato automaticamente baseado no conteúdo
        Retorna informações completas sobre a classificação
        """
        if not text or not text.strip():
            return self._create_general_classification("Texto vazio")
        
        text_lower = text.lower()
        scores = {}
        
        # Calcular pontuação para cada categoria
        for category, config in self.classification_rules.items():
            score = 0
            matched_keywords = []
            
            for keyword in config['keywords']:
                if keyword in text_lower:
                    # Peso baseado no tamanho da palavra-chave (frases valem mais)
                    word_weight = len(keyword.split()) * 2
                    # Prioridade da categoria
                    priority_weight = config['priority'] * 0.1
                    score += word_weight + priority_weight
                    matched_keywords.append(keyword)
            
            if score > 0:
                scores[category] = {
                    'score': score,
                    'matched_keywords': matched_keywords,
                    'agent': config['agent'],
                    'priority': config['priority']
                }
        
        # Se não encontrou correspondências, usar agente geral
        if not scores:
            return self._create_general_classification("Nenhuma palavra-chave encontrada")
        
        # Encontrar a melhor classificação
        best_category = max(scores.items(), key=lambda x: x[1]['score'])
        category_name = best_category[0]
        category_data = best_category[1]
        
        # Verificar confiança mínima
        if category_data['score'] < 4:  # Threshold mínimo
            return self._create_general_classification(f"Confiança baixa: {category_data['score']}")
        
        return {
            'classification': category_name,
            'agent_type': category_data['agent'],
            'confidence': min(category_data['score'] / 10, 1.0),  # Normalizar para 0-1
            'matched_keywords': category_data['matched_keywords'],
            'priority': category_data['priority'],
            'is_automatic': True,
            'method': 'keyword_analysis',
            'total_categories_evaluated': len(self.classification_rules),
            'categories_with_matches': len(scores)
        }
    
    def classify_contract_with_entities(self, text: str, question: str = "") -> Dict[str, Any]:
        """
        Enhanced classification that includes entity analysis (CPF/CNPJ)
        
        Returns both contract type AND entity relationship classification
        """
        # Base contract classification
        base_classification = self.classify_contract(text)
        
        # Entity classification (NEW)
        entity_info = self.entity_classifier.identify_entities(text)
        
        # Enhanced classification combining both analyses
        enhanced_classification = {
            **base_classification,
            "entity_analysis": {
                "entity_type": entity_info.type,
                "party_relationship": entity_info.party_relationship,
                "consumer_protection_applies": entity_info.consumer_protection,
                "legal_framework": entity_info.legal_framework,
                "identified_entities": entity_info.identified_entities,
                "applicable_rights": self.entity_classifier.get_applicable_rights(entity_info),
                "specific_risk_factors": self.entity_classifier.get_risk_factors_by_entity_type(entity_info),
                "confidence_score": entity_info.confidence_score
            }
        }
        
        # Adjust agent selection and confidence based on entity type
        if entity_info.consumer_protection:
            enhanced_classification["agent_specialization"] = "consumer_focused"
            enhanced_classification["legal_context"] = "B2C - Proteção CDC"
        elif entity_info.party_relationship == "b2b":
            enhanced_classification["agent_specialization"] = "commercial_focused"
            enhanced_classification["legal_context"] = "B2B - Código Civil + Comercial"
        elif entity_info.party_relationship == "p2p":
            enhanced_classification["agent_specialization"] = "civil_focused"
            enhanced_classification["legal_context"] = "P2P - Código Civil"
        else:
            enhanced_classification["agent_specialization"] = "general"
            enhanced_classification["legal_context"] = "Genérico - Código Civil"
        
        # Boost confidence if entity detection is strong
        if entity_info.confidence_score > 0.5:
            base_confidence = enhanced_classification.get("confidence", 0.0)
            enhanced_classification["confidence"] = min(base_confidence + (entity_info.confidence_score * 0.2), 1.0)
        
        # Include question analysis if provided
        if question and question.strip():
            enhanced_classification["question_context"] = question.strip()
            enhanced_classification["has_question"] = True
        else:
            enhanced_classification["has_question"] = False
        
        return enhanced_classification
    
    def _create_general_classification(self, reason: str) -> Dict[str, Any]:
        """Cria classificação para agente geral"""
        return {
            'classification': 'general',
            'agent_type': 'general',
            'confidence': 1.0,
            'matched_keywords': [],
            'priority': 1,
            'is_automatic': False,
            'method': 'fallback_to_general',
            'reason': reason,
            'total_categories_evaluated': len(self.classification_rules),
            'categories_with_matches': 0
        }
    
    def get_all_categories(self) -> List[str]:
        """Retorna todas as categorias disponíveis"""
        return list(self.classification_rules.keys())
    
    def get_category_info(self, category: str) -> Dict[str, Any]:
        """Retorna informações sobre uma categoria específica"""
        if category not in self.classification_rules:
            return None
        
        config = self.classification_rules[category]
        return {
            'category': category,
            'agent': config['agent'],
            'priority': config['priority'],
            'keywords_count': len(config['keywords']),
            'sample_keywords': config['keywords'][:5]  # Primeiras 5 palavras-chave
        }