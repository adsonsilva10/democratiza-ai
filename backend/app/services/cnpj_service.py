"""
CNPJ Service for Company Validation and Risk Assessment
"""
import httpx
import re
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from app.core.config import settings

class CNPJService:
    """Service for CNPJ consultation and company analysis"""
    
    def __init__(self):
        self.base_url = "https://www.receitaws.com.br/v1/cnpj/"  # API pública
        # Ou usar: "https://brasilapi.com.br/api/cnpj/v1/"
    
    def extract_cnpj_from_text(self, contract_text: str) -> Optional[str]:
        """Extract CNPJ from contract text"""
        # Regex para CNPJ (com ou sem formatação)
        cnpj_pattern = r'\b\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}\b'
        matches = re.findall(cnpj_pattern, contract_text)
        
        if matches:
            # Limpar formatação
            cnpj = re.sub(r'[^\d]', '', matches[0])
            if len(cnpj) == 14:
                return cnpj
        return None
    
    async def get_company_data(self, cnpj: str) -> Optional[Dict[str, Any]]:
        """Fetch company data from CNPJ API"""
        try:
            # Limpar CNPJ
            clean_cnpj = re.sub(r'[^\d]', '', cnpj)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{clean_cnpj}",
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return None
                    
        except Exception as e:
            print(f"Erro ao consultar CNPJ {cnpj}: {e}")
            return None
    
    def analyze_company_risk(self, company_data: Dict[str, Any], contract_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze company risk factors based on CNPJ data"""
        if not company_data:
            return {
                "risk_level": "high",
                "risk_factors": ["CNPJ não encontrado ou inválido"],
                "recommendations": ["Verificar se a empresa está regularizada"]
            }
        
        risk_factors = []
        risk_level = "low"
        
        # 1. Verificar situação cadastral
        situacao = company_data.get("situacao", "").upper()
        if situacao in ["SUSPENSA", "INAPTA", "BAIXADA"]:
            risk_factors.append(f"Empresa com situação irregular: {situacao}")
            risk_level = "high"
        
        # 2. Verificar data de abertura (empresa muito nova)
        try:
            data_abertura = datetime.strptime(company_data.get("abertura", ""), "%d/%m/%Y")
            if datetime.now() - data_abertura < timedelta(days=180):  # 6 meses
                risk_factors.append("Empresa com menos de 6 meses de funcionamento")
                if risk_level == "low":
                    risk_level = "medium"
        except:
            pass
        
        # 3. Verificar capital social
        try:
            capital = float(company_data.get("capital_social", "0").replace(",", "."))
            if capital < 1000:  # Capital muito baixo
                risk_factors.append(f"Capital social baixo: R$ {capital:.2f}")
                if risk_level == "low":
                    risk_level = "medium"
        except:
            pass
        
        # 4. Verificar porte vs. contexto do contrato
        porte = company_data.get("porte", "")
        if contract_context and contract_context.get("contract_type") == "telecom":
            if porte == "MEI":
                risk_factors.append("MEI oferecendo serviços de telecomunicações (verificar capacidade)")
                if risk_level == "low":
                    risk_level = "medium"
        
        # 5. Verificar telefone
        telefone = company_data.get("telefone", "")
        if not telefone or telefone == "(00) 0000-0000":
            risk_factors.append("Empresa sem telefone de contato cadastrado")
            if risk_level == "low":
                risk_level = "medium"
        
        # Gerar recomendações
        recommendations = []
        if risk_level == "high":
            recommendations.append("⚠️ ATENÇÃO: Empresa com situação irregular - NÃO RECOMENDADO assinar contrato")
            recommendations.append("Consulte a situação da empresa na Receita Federal antes de prosseguir")
        elif risk_level == "medium":
            recommendations.append("Solicite documentos adicionais da empresa (certidões negativas)")
            recommendations.append("Verifique referências de outros clientes")
        else:
            recommendations.append("Empresa em situação regular, mas sempre verifique cláusulas contratuais")
        
        return {
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "company_info": {
                "razao_social": company_data.get("nome", ""),
                "situacao": situacao,
                "porte": porte,
                "atividade_principal": company_data.get("atividade_principal", [{}])[0].get("text", "") if company_data.get("atividade_principal") else "",
                "data_abertura": company_data.get("abertura", ""),
                "capital_social": company_data.get("capital_social", "0"),
                "endereco": f"{company_data.get('logradouro', '')}, {company_data.get('municipio', '')} - {company_data.get('uf', '')}",
                "telefone": telefone
            }
        }