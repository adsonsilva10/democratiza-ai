from app.agents.base_agent import BaseContractAgent

class RentalCommercialAgent(BaseContractAgent):
    """Agente especializado em contratos de locação comercial"""
    
    def __init__(self):
        super().__init__()
        self.specialization = "Locação Comercial"
        self.icon = "🏢"
        
    def generate_response(self, question: str, context: str = None) -> str:
        """Gera resposta especializada para contratos de locação comercial"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["luva", "ponto comercial", "fundo"]):
            return """🏢 **LOCAÇÃO COMERCIAL - Luva/Ponto**: 
            
**Luva (Taxa de Cessão)**: Valor pago pela cessão de direitos sobre o ponto comercial. ⚖️ **Legal quando**: Há benfeitorias, clientela consolidada ou autorização expressa do proprietário.

🚨 **CUIDADO**: Luva sem justificativa pode ser considerada abusiva. **Verifique**: Escritura registrada, benfeitorias comprovadas, clientela estabelecida.

📋 **NEGOCIAÇÃO**: Valor da luva, forma de pagamento, garantias, direito de renovação compulsória (Lei 8.245/91, Art. 51)."""

        elif any(word in question_lower for word in ["renovação", "compulsória", "cinco anos"]):
            return """🏢 **RENOVAÇÃO COMPULSÓRIA**: 
            
**Requisitos Lei 8.245/91**: ✅ Contrato por escrito, prazo determinado ≥ 5 anos, ✅ Ramo de atividade por ≥ 3 anos, ✅ Contrato registrado no cartório.

⚖️ **DIREITOS**: Locatário pode exigir renovação nas mesmas condições, salvo: 📈 **Reajuste do aluguel** ao valor de mercado, 🔄 **Atualização de cláusulas** legais.

🚨 **EXCEÇÕES**: Proprietário pode negar se: Usar imóvel próprio/família, obras que impeçam uso, ofertar 20% mais que avaliação judicial."""

        elif any(word in question_lower for word in ["rescisão", "cancelar", "sair"]):
            return """🏢 **RESCISÃO COMERCIAL**:
            
**Locatário**: 🔸 **Prazo determinado** → Multa conforme contrato (geralmente 3 aluguéis), 🔸 **Prazo indeterminado** → Aviso prévio 30 dias.

**Locador**: 🔸 **Prazo determinado** → Só em casos específicos (falta pagamento, infração), 🔸 **Prazo indeterminado** → Aviso prévio 90 dias.

💰 **MULTA**: Verificar se proporcional ao tempo restante. 📋 **ENTREGA**: Vistoria, benfeitorias, estado do imóvel."""

        elif any(word in question_lower for word in ["alvará", "funcionamento", "licença"]):
            return """🏢 **ALVARÁ E LICENÇAS**:
            
📄 **RESPONSABILIDADE**: Geralmente do locatário obter alvarás necessários para atividade. **Verifique contrato**: Quem arca com taxas e documentação.

🏛️ **DOCUMENTOS**: Alvará de funcionamento, licença sanitária, corpo de bombeiros, IPTU, certidões. 

⚠️ **ATENÇÃO**: Atividade deve ser **compatível com zoneamento**. Proprietário não pode impedir uso permitido por lei."""

        elif any(word in question_lower for word in ["iptu", "condomínio", "taxas"]):
            return """🏢 **ENCARGOS COMERCIAIS**:
            
💰 **IPTU**: Normalmente **responsabilidade do locatário** em locação comercial, salvo disposição contrária.

🏢 **CONDOMÍNIO**: 🔸 **Ordinário** → Locatário, 🔸 **Extraordinário** → Negociável (verificar contrato).

⚖️ **TAXAS**: Iluminação pública, limpeza → Geralmente locatário. 📋 **Transparência**: Exigir demonstrativos e comprovantes de todas as taxas."""

        else:
            return f"""🏢 **LOCAÇÃO COMERCIAL**: Analisando sua questão sobre "{question}".

**Especialidades**: 📋 **Ponto Comercial** (luva, cessão), ⚖️ **Renovação Compulsória**, 💼 **Atividade Comercial**, 🏛️ **Alvarás e Licenças**, 💰 **Encargos e Impostos**.

🔍 **Seja mais específico**: Informe detalhes sobre renovação, rescisão, luva, alvarás ou encargos para orientação precisa conforme Lei 8.245/91!"""