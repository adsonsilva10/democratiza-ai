from app.agents.base_agent import BaseContractAgent

class RealEstateAgent(BaseContractAgent):
    """Agente especializado em contratos de compra e venda de imóveis"""
    
    def __init__(self):
        super().__init__()
        self.specialization = "Compra e Venda de Imóveis"
        self.icon = "🏠"
        
    def generate_response(self, question: str, context: str = None) -> str:
        """Gera resposta especializada para contratos de compra e venda"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["vício", "defeito", "oculto", "problema"]):
            return """🏠 **VÍCIOS OCULTOS**:
            
⚖️ **DEFINIÇÃO**: Defeitos não aparentes na vistoria que diminuem valor/utilidade do imóvel. **Prazo**: 1 ano para vícios aparentes, 3 anos para estruturais (Art. 618 CC).

🔍 **EXEMPLOS**: Infiltração, problemas elétricos/hidráulicos, rachaduras estruturais, documentação irregular.

💰 **DIREITOS**: 🔸 **Abatimento proporcional** do preço, 🔸 **Rescisão** + devolução + perdas e danos, 🔸 **Reparação** por conta do vendedor.

📋 **PROVA**: Laudo técnico, fotos, orçamentos. **Ação**: Dentro dos prazos legais no judiciário."""

        elif any(word in question_lower for word in ["escritura", "cartório", "registro"]):
            return """🏠 **ESCRITURA E REGISTRO**:
            
📄 **ESCRITURA**: Formaliza a compra no cartório de notas. **Documentos**: CPF, RG, certidões, matrícula atualizada, ITBI quitado.

🏛️ **REGISTRO**: Transfere propriedade no cartório de registro de imóveis. **SÓ APÓS REGISTRO** você é proprietário oficial!

💰 **CUSTOS**: 🔸 **ITBI** (2-3% valor venal), 🔸 **Cartório** (varia por estado), 🔸 **Registro** (conforme tabela).

⚠️ **ATENÇÃO**: Verificar débitos anteriores, ônus, hipotecas na matrícula. Exigir **certidões negativas** atualizadas."""

        elif any(word in question_lower for word in ["sinal", "arras", "entrada", "como funcionam"]):
            return """🏠 **SINAL/ARRAS**:
            
💰 **FUNÇÃO**: Confirma negócio e demonstra seriedade das partes. **Valor**: Geralmente 10-30% do valor total.

⚖️ **TIPOS**: 🔸 **Confirmatórias** → Integram preço final, 🔸 **Penitenciais** → Garantem direito de arrependimento.

📋 **ARREPENDIMENTO**: **Comprador** → Perde sinal, **Vendedor** → Devolve em dobro (se penitenciais).

🚨 **CUIDADO**: Definir claramente no contrato tipo de arras, condições e consequências do descumprimento."""

        elif any(word in question_lower for word in ["financiamento", "banco", "aprovação"]):
            return """🏠 **FINANCIAMENTO IMOBILIÁRIO**:
            
🏦 **APROVAÇÃO**: Contrato geralmente condicionado à aprovação do crédito. **Prazo**: 30-60 dias para análise.

📋 **DOCUMENTOS**: Comprovante renda, IR, extratos, certidões, avaliação do imóvel pelo banco.

⚠️ **SE NEGADO**: 🔸 **Cláusula resolutiva** → Contrato cancelado sem penalidades, 🔸 **Sem cláusula** → Comprador deve honrar ou pagar multa.

💡 **DICA**: Sempre incluir cláusula de resolução por negativa de financiamento para proteção do comprador."""

        elif any(word in question_lower for word in ["itbi", "imposto", "transmissão"]):
            return """🏠 **ITBI - Imposto de Transmissão**:
            
💰 **CÁLCULO**: 2-3% sobre valor venal ou declarado (o maior). **Responsabilidade**: Geralmente do comprador, mas negociável.

📅 **PRAZO**: Até 30 dias após escritura para evitar multa e juros. **Pagamento**: Antes da escritura na maioria dos municípios.

🔍 **ISENÇÕES**: Primeira casa (alguns municípios), SFH até valor limite, permuta por imóvel menor valor.

⚖️ **VERIFICAÇÃO**: Confirmar quitação antes do registro, pois débito pode gerar problemas futuros."""

        else:
            return f"""🏠 **COMPRA E VENDA**: Analisando sua questão sobre "{question}".

**Especialidades**: 📄 **Documentação** (escritura, registro, matrícula), 💰 **Aspectos Financeiros** (financiamento, ITBI, custos), ⚖️ **Vícios e Problemas**, 🔒 **Garantias e Direitos**.

🔍 **Seja mais específico**: Informe sobre documentação, financiamento, vícios, impostos ou outras questões para orientação detalhada!"""