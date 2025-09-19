import re
from typing import Dict, Any
from app.agents.base_agent import BaseContractAgent
from app.core.config import settings

class ClassifierAgent(BaseContractAgent):
    """Agent responsible for classifying contract types"""
    
    CONTRACT_TYPES = {
        "locacao": ["aluguel", "locação", "locatário", "locador", "imóvel", "caução"],
        "telecom": ["telecomunicações", "internet", "telefone", "dados", "banda larga", "plano"],
        "financeiro": ["empréstimo", "financiamento", "crédito", "juros", "parcela", "banco"],
        "trabalho": ["emprego", "trabalhador", "empregador", "salário", "férias", "rescisão"],
        "servicos": ["prestação", "serviços", "fornecedor", "cliente", "entrega"],
        "compra_venda": ["compra", "venda", "vendedor", "comprador", "produto", "mercadoria"]
    }
    
    async def classify_contract(self, contract_text: str) -> Dict[str, Any]:
        """Classify contract type and confidence"""
        contract_lower = contract_text.lower()
        
        # Count keywords for each contract type
        scores = {}
        for contract_type, keywords in self.CONTRACT_TYPES.items():
            score = sum(1 for keyword in keywords if keyword in contract_lower)
            scores[contract_type] = score
        
        # Get the best match
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type] / len(self.CONTRACT_TYPES[best_type])
        
        # Use Claude for confirmation if confidence is low
        if confidence < 0.3:
            claude_classification = await self._claude_classify(contract_text)
            return claude_classification
        
        return {
            "contract_type": best_type,
            "confidence": min(confidence, 1.0),
            "method": "keyword_matching"
        }
    
    async def _claude_classify(self, contract_text: str) -> Dict[str, Any]:
        """Use Claude for contract classification when keyword matching is uncertain"""
        
        prompt = f"""
        Analise o seguinte contrato brasileiro e classifique-o em uma das categorias:
        
        Categorias disponíveis:
        - locacao: Contratos de aluguel ou locação de imóveis
        - telecom: Contratos de telecomunicações, internet, telefone
        - financeiro: Contratos de empréstimo, financiamento, cartão de crédito
        - trabalho: Contratos de trabalho ou prestação de serviços pessoa física
        - servicos: Contratos de prestação de serviços empresariais
        - compra_venda: Contratos de compra e venda de produtos/mercadorias
        
        Contrato:
        {contract_text[:2000]}...
        
        Responda APENAS com um JSON no formato:
        {{"contract_type": "categoria", "confidence": 0.95, "reasoning": "breve explicação"}}
        """
        
        try:
            response = await self.claude_client.completions.create(
                model="claude-3-sonnet-20240229",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.1
            )
            
            # Parse JSON response
            import json
            result = json.loads(response.content[0].text.strip())
            result["method"] = "claude_classification"
            return result
            
        except Exception as e:
            # Fallback to most common type
            return {
                "contract_type": "servicos",
                "confidence": 0.5,
                "method": "fallback",
                "error": str(e)
            }
    
    async def analyze_contract(self, contract_text: str, context: Dict[str, Any] = None) -> None:
        """Classifier doesn't perform full analysis, only classification"""
        raise NotImplementedError("Use classify_contract() method instead")
    
    def get_specialized_prompt(self, contract_text: str, rag_context: str = "") -> str:
        """Classifier doesn't use specialized prompts"""
        raise NotImplementedError("Use classify_contract() method instead")
