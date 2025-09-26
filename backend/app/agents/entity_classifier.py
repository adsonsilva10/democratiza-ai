import re
from typing import Dict, Any, Literal, List, Optional
from dataclasses import dataclass

@dataclass
class EntityInfo:
    """Information about contract parties and legal framework"""
    type: Literal["cpf", "cnpj", "mixed", "unknown"]
    consumer_protection: bool  # Se CDC se aplica
    legal_framework: str  # Código Civil, CDC, etc.
    party_relationship: Literal["b2c", "b2b", "p2p", "mixed", "unknown"]
    identified_entities: List[Dict[str, Any]]
    confidence_score: float

class EntityClassifier:
    """Classifier for identifying contract parties (CPF/CNPJ) and determining legal framework"""
    
    def __init__(self):
        # Padrões para identificação de CPF
        self.cpf_patterns = [
            r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b',  # CPF format variations
            r'\bCPF\s*n?º?\s*\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b',
            r'\bpessoa\s+física\b',
            r'\bcidadão\b',
            r'\bconsumidor\b',
            r'\bcontratante\s+pessoa\s+física\b',
            r'\bparticular\b',
        ]
        
        # Padrões para identificação de CNPJ  
        self.cnpj_patterns = [
            r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b',  # CNPJ format variations
            r'\bCNPJ\s*n?º?\s*\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b',
            r'\bpessoa\s+jurídica\b',
            r'\bempresa\b',
            r'\bsociedade\b',
            r'\borganização\b',
            r'\bcorporação\b',
            r'\bfornecedor\b',
            r'\bprestador\b',
            r'\boperadora\b',
            r'\bdistribuidora\b',
            r'\bcompanhia\b',
            r'\bltda\.?\b',
            r'\bs\.?a\.?\b',
            r'\bmicroempresa\b',
            r'\bme\b',
            r'\bepp\b',
        ]
        
        # Indicadores específicos de relação B2C (empresa → pessoa física)
        self.b2c_indicators = [
            r'\bconsumidor\b',
            r'\bclientela\b', 
            r'\bserviços\s+ao\s+consumidor\b',
            r'\bprodutos\s+ou\s+serviços\b',
            r'\brelação\s+de\s+consumo\b',
            r'\bdireitos\s+do\s+consumidor\b',
            r'\bcontrato\s+de\s+adesão\b',
            r'\bfornecimento\s+de\s+produtos\b',
            r'\bprestação\s+de\s+serviços\b',
            r'\busuário\s+final\b',
            r'\bdestinário\s+final\b',
            r'\bproteção\s+do\s+consumidor\b',
        ]
        
        # Indicadores específicos de relação B2B (empresa → empresa)
        self.b2b_indicators = [
            r'\bcontratante\s+e\s+contratada\b',
            r'\bpartes\s+contraentes\b',
            r'\brelação\s+comercial\b',
            r'\bnegociação\s+empresarial\b',
            r'\bfornecimento\s+empresarial\b',
            r'\bparceria\s+comercial\b',
            r'\batividade\s+empresarial\b',
            r'\binsumos\b',
            r'\bmatérias-primas\b',
            r'\brevenda\b',
            r'\bdistribuição\b',
            r'\brepresentação\s+comercial\b',
        ]
        
        # Indicadores de relação P2P (pessoa → pessoa)
        self.p2p_indicators = [
            r'\bentre\s+as\s+partes\b',
            r'\brelação\s+civil\b',
            r'\bcontrato\s+particular\b',
            r'\bentre\s+particulares\b',
            r'\bboa-fé\s+objetiva\b',
            r'\bfunção\s+social\s+do\s+contrato\b',
        ]
        
    def identify_entities(self, contract_text: str) -> EntityInfo:
        """
        Identify the types of entities in the contract and determine legal framework
        
        Args:
            contract_text: The contract text to analyze
            
        Returns:
            EntityInfo with classification results
        """
        if not contract_text:
            return self._create_unknown_entity_info()
            
        text_lower = contract_text.lower()
        
        # Find and count entity matches
        cpf_matches = self._find_entity_matches(contract_text, self.cpf_patterns, "CPF")
        cnpj_matches = self._find_entity_matches(contract_text, self.cnpj_patterns, "CNPJ")
        
        # Count relationship indicators
        b2c_score = self._count_pattern_matches(text_lower, self.b2c_indicators)
        b2b_score = self._count_pattern_matches(text_lower, self.b2b_indicators) 
        p2p_score = self._count_pattern_matches(text_lower, self.p2p_indicators)
        
        # Classify relationship and entity type
        entity_type, party_relationship, confidence = self._classify_relationship(
            len(cpf_matches), len(cnpj_matches), b2c_score, b2b_score, p2p_score
        )
        
        # Determine legal framework and consumer protection
        consumer_protection, legal_framework = self._determine_legal_framework(
            entity_type, party_relationship
        )
        
        return EntityInfo(
            type=entity_type,
            consumer_protection=consumer_protection,
            legal_framework=legal_framework,
            party_relationship=party_relationship,
            identified_entities=cpf_matches + cnpj_matches,
            confidence_score=confidence
        )
    
    def _find_entity_matches(self, text: str, patterns: List[str], entity_type: str) -> List[Dict[str, Any]]:
        """Find and extract entity matches from text"""
        matches = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matches.append({
                    "text": match.group().strip(),
                    "start": match.start(),
                    "end": match.end(),
                    "pattern": pattern,
                    "entity_type": entity_type,
                    "is_document_number": self._is_document_pattern(pattern)
                })
        return matches
    
    def _is_document_pattern(self, pattern: str) -> bool:
        """Check if pattern matches actual document numbers (CPF/CNPJ)"""
        return any(char in pattern for char in [r'\d', '\\d'])
    
    def _count_pattern_matches(self, text: str, patterns: List[str]) -> int:
        """Count total pattern matches in text"""
        count = 0
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            count += len(matches)
        return count
    
    def _classify_relationship(self, cpf_count: int, cnpj_count: int, 
                             b2c_score: int, b2b_score: int, p2p_score: int) -> tuple:
        """Classify entity relationship based on detected patterns"""
        
        confidence = 0.0
        
        # Determine entity type first
        if cpf_count > 0 and cnpj_count > 0:
            entity_type = "mixed"
            confidence += 0.4
        elif cnpj_count > 0:
            entity_type = "cnpj" 
            confidence += 0.3
        elif cpf_count > 0:
            entity_type = "cpf"
            confidence += 0.3
        else:
            entity_type = "unknown"
        
        # Determine party relationship based on entity mix and indicators
        if entity_type == "mixed":
            if b2c_score >= b2b_score and b2c_score > 0:
                party_relationship = "b2c"  # Empresa fornecendo para pessoa física
                confidence += 0.4 if b2c_score > 2 else 0.2
            elif b2b_score > b2c_score:
                party_relationship = "b2b"  # Pode ser empresa terceirizada
                confidence += 0.3
            else:
                party_relationship = "mixed"
                confidence += 0.1
                
        elif entity_type == "cpf":
            if p2p_score > 0:
                party_relationship = "p2p"  # Pessoa para pessoa
                confidence += 0.3
            elif b2c_score > 0:
                party_relationship = "b2c"  # Pode ser consumidor sem CNPJ visível
                confidence += 0.2
            else:
                party_relationship = "p2p"  # Default for CPF only
                confidence += 0.2
                
        elif entity_type == "cnpj":
            if b2b_score > 0:
                party_relationship = "b2b"  # Empresa para empresa
                confidence += 0.4
            else:
                party_relationship = "b2b"  # Default for CNPJ
                confidence += 0.2
        else:
            # Unknown entity type - use indicators only
            if b2c_score > max(b2b_score, p2p_score):
                party_relationship = "b2c"
                confidence += 0.1
            elif b2b_score > max(b2c_score, p2p_score):
                party_relationship = "b2b"
                confidence += 0.1
            elif p2p_score > 0:
                party_relationship = "p2p"
                confidence += 0.1
            else:
                party_relationship = "unknown"
        
        # Cap confidence at 1.0
        confidence = min(confidence, 1.0)
        
        return entity_type, party_relationship, confidence
    
    def _determine_legal_framework(self, entity_type: str, 
                                  party_relationship: str) -> tuple:
        """Determine applicable legal framework and consumer protection"""
        
        if party_relationship == "b2c":
            return True, "CDC (Código de Defesa do Consumidor) + Código Civil"
        elif party_relationship == "b2b":
            return False, "Código Civil + Legislação Comercial"
        elif party_relationship == "p2p":
            return False, "Código Civil"
        else:
            return False, "Código Civil (framework genérico)"
    
    def _create_unknown_entity_info(self) -> EntityInfo:
        """Create EntityInfo for unknown/unclear cases"""
        return EntityInfo(
            type="unknown",
            consumer_protection=False,
            legal_framework="Código Civil (genérico)",
            party_relationship="unknown", 
            identified_entities=[],
            confidence_score=0.0
        )
    
    def get_applicable_rights(self, entity_info: EntityInfo) -> List[str]:
        """Get list of applicable rights based on entity classification"""
        
        rights = []
        
        if entity_info.consumer_protection:
            # Direitos específicos do CDC
            rights.extend([
                "Direito à informação adequada e clara sobre produtos/serviços",
                "Proteção contra práticas comerciais abusivas", 
                "Direito de arrependimento (7 dias em compras à distância)",
                "Inversão do ônus da prova em favor do consumidor",
                "Foro do domicílio do consumidor para ações judiciais",
                "Nulidade automática de cláusulas abusivas",
                "Direito à reparação integral de danos",
                "Proteção contra propaganda enganosa",
                "Direito à assistência técnica adequada"
            ])
        
        if entity_info.party_relationship == "b2b":
            # Direitos específicos para relações empresariais
            rights.extend([
                "Liberdade contratual ampla entre empresas",
                "Princípio da autonomia da vontade",
                "Validade de cláusula de eleição de foro",
                "Possibilidade de limitação consensual de responsabilidade",
                "Negociação paritária de condições contratuais",
                "Aplicação do princípio da boa-fé objetiva",
                "Revisão contratual por onerosidade excessiva"
            ])
        
        if entity_info.party_relationship == "p2p":
            # Direitos para relações entre pessoas físicas
            rights.extend([
                "Princípio da boa-fé objetiva nas relações contratuais",
                "Função social do contrato",
                "Equilíbrio e proporcionalidade contratual", 
                "Revisão por onerosidade excessiva superveniente",
                "Aplicação da teoria da imprevisão",
                "Proteção da parte mais vulnerável na relação"
            ])
        
        # Direitos gerais aplicáveis a todas as relações
        rights.extend([
            "Cumprimento das obrigações conforme pactuado",
            "Resolução por inadimplemento",
            "Indenização por perdas e danos",
            "Direito ao cumprimento específico da obrigação"
        ])
        
        return rights
    
    def get_risk_factors_by_entity_type(self, entity_info: EntityInfo) -> List[str]:
        """Get specific risk factors to analyze based on entity relationship"""
        
        risk_factors = []
        
        if entity_info.consumer_protection:
            # Riscos específicos em relações B2C
            risk_factors.extend([
                "Cláusulas que limitam direitos básicos do consumidor",
                "Foro de eleição que prejudique o consumidor", 
                "Informações inadequadas ou incompletas sobre o produto/serviço",
                "Cláusulas que invertam o ônus da prova em desfavor do consumidor",
                "Limitações abusivas de responsabilidade do fornecedor",
                "Renovação automática sem clara concordância",
                "Multas desproporcionais para o consumidor"
            ])
        
        if entity_info.party_relationship == "b2b":
            # Riscos específicos em relações B2B
            risk_factors.extend([
                "Desequilíbrio excessivo entre obrigações das partes",
                "Cláusulas penais desproporcionais ao valor do contrato",
                "Limitações de responsabilidade que tornem a obrigação sem sentido",
                "Condições leoninas que prejudiquem uma das partes",
                "Prazos excessivamente longos para uma das partes",
                "Garantias excessivas ou desproporcionais"
            ])
        
        if entity_info.party_relationship == "p2p":
            # Riscos específicos em relações P2P
            risk_factors.extend([
                "Desequilíbrio entre direitos e deveres das partes",
                "Ausência de garantias adequadas para cumprimento",
                "Condições que possam gerar onerosidade excessiva",
                "Falta de clareza sobre responsabilidades de cada parte",
                "Multas ou penalidades desproporcionais"
            ])
        
        return risk_factors