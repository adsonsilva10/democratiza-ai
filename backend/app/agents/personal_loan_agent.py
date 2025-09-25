from app.agents.base_agent import BaseContractAgent

class PersonalLoanAgent(BaseContractAgent):
    """Agente especializado em empréstimos pessoais"""
    
    def __init__(self):
        super().__init__()
        self.specialization = "Empréstimos Pessoais"
        self.icon = "💰"
        
    def generate_response(self, question: str, context: str = None) -> str:
        """Gera resposta especializada para empréstimos pessoais"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["juros", "taxa", "cet", "abusivo"]):
            return """💰 **JUROS EM EMPRÉSTIMOS**:
            
📊 **LIMITES LEGAIS**: **Pessoa Física** → Até 2% ao mês + multa 2% (CDC). **Consignado** → Taxa regulamentada pelo BACEN (aprox. 2,14% ao mês).

🏦 **CET (Custo Efetivo Total)**: Deve incluir **TODAS** as taxas: juros, IOF, seguros, tarifas. **Obrigatório** informar no contrato.

🚨 **JUROS ABUSIVOS**: Superiores a **4x** a taxa SELIC ou que tornem prestação >30% da renda. **Direito**: Revisão judicial.

⚖️ **AÇÃO**: Busque advogado se suspeitar de abuso. Guarde contratos e comprovantes de pagamento."""

        elif any(word in question_lower for word in ["consignado", "desconto", "folha", "aposentado"]):
            return """💰 **CRÉDITO CONSIGNADO**:
            
✅ **VANTAGENS**: Menores juros (garantia no salário), aprovação mais fácil, sem consulta SPC/Serasa severa.

📋 **LIMITE**: Até **35%** da renda líquida (30% empréstimo + 5% cartão consignado). **Desconto direto** na folha/benefício.

👥 **QUEM PODE**: CLT, servidor público, aposentado/pensionista INSS, Forças Armadas.

⚠️ **CUIDADO**: Portabilidade gratuita entre bancos. **Não aceite**: Pressão para contratar seguros desnecessários ou produtos casados."""

        elif any(word in question_lower for word in ["avalista", "fiador", "garantia"]):
            return """💰 **GARANTIAS EM EMPRÉSTIMOS**:
            
🛡️ **AVALISTA**: Garante o pagamento sem benefício de ordem (cobrança direta). **Risco**: Bens próprios podem ser executados.

🏠 **FIADOR**: Similar ao avalista, mas com benefício de ordem (cobrar primeiro devedor principal).

⚖️ **DIREITOS**: 🔸 **Exoneração** após 2 anos (Súmula 214 STJ), 🔸 **Sub-rogação** nos direitos contra devedor principal.

🚨 **ATENÇÃO**: Avalista/fiador respondem mesmo após morte do devedor. **Analise bem** antes de assinar qualquer garantia!"""

        elif any(word in question_lower for word in ["antecipação", "quitação", "desconto"]):
            return """💰 **QUITAÇÃO ANTECIPADA**:
            
⚖️ **DIREITO CDC**: Redução proporcional dos juros e acréscimos (Art. 52, §2º). **Não podem**: Cobrar multa por antecipação.

💵 **CÁLCULO**: 🔸 **Juros simples** → Desconto proporcional aos dias, 🔸 **Juros compostos** → Usar tabela Price invertida.

📞 **NEGOCIAÇÃO**: Ligue para banco e solicite **simulação oficial**. Compare com cálculo próprio. **Exija desconto** de IOF proporcional.

💡 **DICA**: Guarde protocolos e confirme desconto por escrito. Em caso de recusa, procure Procon ou Bacen."""

        elif any(word in question_lower for word in ["renegociação", "acordo", "dívida", "parcelamento"]):
            return """💰 **RENEGOCIAÇÃO DE DÍVIDAS**:
            
📞 **CANAIS**: Serasa Limpa Nome, SPC Quero Quitar, Registrato (Bacen), WhatsApp do banco, app oficial.

💡 **ESTRATÉGIAS**: 🔸 **Pagamento à vista** → Maior desconto (até 90%), 🔸 **Parcelamento** → Menor desconto, mais prazo.

📋 **DOCUMENTOS**: CPF, comprovante renda atualizado, proposta por escrito, protocolo de atendimento.

⚠️ **CUIDADO**: Não assine sem ler. **Confirme**: Retirada do nome dos órgãos, ausência de juros abusivos no acordo."""

        elif any(word in question_lower for word in ["spc", "serasa", "score", "nome sujo"]):
            return """💰 **NOME NEGATIVADO**:
            
📱 **CONSULTA GRATUITA**: SPC/Serasa apps oficiais, Registrato (Bacen), ou presencial com documento.

⏰ **EXCLUSÃO**: Automática após **5 anos** do vencimento. **Pagamento** → Até 5 dias úteis para sair.

📊 **SCORE**: Pontuação de 0-1000. **Melhora com**: Pagamentos em dia, relacionamento bancário, atualização de dados.

🔍 **DIREITOS**: Contestar informações incorretas gratuitamente. **Prazo**: 5 dias úteis para correção após solicitação."""

        else:
            return f"""💰 **EMPRÉSTIMOS PESSOAIS**: Analisando sua questão sobre "{question}".

**Especialidades**: 📊 **Juros e Taxas** (CET, limites legais), 🛡️ **Garantias** (avalista, fiador), 💵 **Quitação Antecipada**, 🔄 **Renegociação**, 📋 **Direitos CDC**.

🔍 **Seja mais específico**: Informe sobre taxas, garantias, renegociação, ou direitos para orientação detalhada conforme CDC e regulamentações BACEN!"""