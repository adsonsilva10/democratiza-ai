from app.agents.base_agent import BaseContractAgent

class HealthInsuranceAgent(BaseContractAgent):
    """Agente especializado em contratos de plano de saúde"""
    
    def __init__(self):
        super().__init__()
        self.specialization = "Planos de Saúde"
        self.icon = "🏥"
        
    def generate_response(self, question: str, context: str = None) -> str:
        """Gera resposta especializada para planos de saúde"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["carência", "prazo", "espera"]):
            return """🏥 **CARÊNCIAS DOS PLANOS**:
            
⏰ **PRAZOS MÁXIMOS** (Lei 9.656/98):
🔸 **Urgência/Emergência** → 24h
🔸 **Consultas/Exames simples** → 30 dias  
🔸 **Exames especiais** → 180 dias
🔸 **Internações** → 180 dias
🔸 **Cirurgias** → 180 dias
🔸 **Parto** → 300 dias

✅ **SEM CARÊNCIA**: Urgência/emergência nas primeiras 12h, doenças preexistentes declaradas após 24 meses (CPO).

⚖️ **REDUÇÃO**: Portabilidade entre planos pode reduzir ou zerar carências conforme tempo de cobertura anterior."""

        elif any(word in question_lower for word in ["cobertura", "negativa", "autorização", "não cobre"]):
            return """🏥 **COBERTURA OBRIGATÓRIA**:
            
✅ **DEVE COBRIR** (Rol ANS 2023):
🔸 **Consultas** médicas ilimitadas
🔸 **Exames** diagnósticos e laboratoriais  
🔸 **Cirurgias** no rol ANS
🔸 **Internações** clínicas e cirúrgicas
🔸 **UTI** quando necessária
🔸 **Psicoterapia** (até 40 sessões/ano)
🔸 **Fisioterapia** (conforme prescrição)

🚨 **NEGATIVA INDEVIDA**: Plano não pode negar tratamento no rol. **Direito**: Liminar judicial, multa, ressarcimento.

📞 **CANAIS**: ANS (0800 701 9656), Procon, Ministério Público, Judiciário."""

        elif any(word in question_lower for word in ["coparticipação", "copagamento", "franquia"]):
            return """🏥 **COPARTICIPAÇÃO**:
            
💰 **DEFINIÇÃO**: Valor pago pelo beneficiário por procedimento utilizado. **Objetivo**: Uso racional dos serviços.

📋 **REGRAS**: 🔸 **Consultas** → Máximo 40% valor total, 🔸 **Exames/Terapias** → Máximo 40%, 🔸 **Internação** → Máximo 40% da diária.

🚫 **PROIBIDO COBRAR**: Urgência/emergência nas primeiras 12h, prevenção (vacinas, check-up), alguns exames específicos.

⚖️ **ABUSO**: Valores excessivos ou cobrança indevida podem ser contestados na ANS ou judicialmente."""

        elif any(word in question_lower for word in ["reembolso", "livre escolha", "médico particular"]):
            return """🏥 **REEMBOLSO**:
            
💵 **FUNCIONAMENTO**: Paciente paga médico particular e solicita reembolso conforme tabela do plano.

📊 **VALORES**: Geralmente baseados na CBHPM (Classificação Brasileira Hierarquizada de Procedimentos Médicos) com percentuais variáveis.

📋 **DOCUMENTOS**: Recibo médico, relatório, prescrições, comprovante pagamento, guia de reembolso preenchida.

⏰ **PRAZO**: Plano tem até **30 dias** para analisar e pagar após entrega completa da documentação.

💡 **DICA**: Confirme percentual de reembolso antes do atendimento para evitar surpresas."""

        elif any(word in question_lower for word in ["ans", "reclamação", "denúncia", "problema"]):
            return """🏥 **RECLAMAÇÕES ANS**:
            
📞 **CANAIS ANS**:
🔸 **Telefone** → 0800 701 9656
🔸 **Site** → ans.gov.br
🔸 **App** → ANS Digital
🔸 **Presencial** → Núcleos ANS

📋 **DOCUMENTOS**: Número do plano, protocolo de negativas, relatórios médicos, comprovantes.

⚖️ **DIREITOS**: Resposta em até 10 dias úteis, instauração de processo administrativo, aplicação de multas à operadora.

🏛️ **OUTROS CANAIS**: Procon estadual, Ministério Público, Defensoria Pública, Poder Judiciário."""

        elif any(word in question_lower for word in ["cancelamento", "rescisão", "sair do plano"]):
            return """🏥 **CANCELAMENTO DO PLANO**:
            
📝 **PELO BENEFICIÁRIO**: Comunicação por escrito com 30 dias de antecedência. **Direito**: Cancelar a qualquer momento.

🚨 **PELA OPERADORA**: Somente por fraude ou inadimplência >60 dias com notificação prévia. **Proibido**: Cancelar por doença ou idade.

💰 **DEVOLUÇÃO**: Valores pagos antecipadamente devem ser devolvidos proporcionalmente.

⚖️ **PROTEÇÃO**: Lei proíbe cancelamento discriminatório. Cancelamento abusivo gera direito a indenização e reintegração."""

        else:
            return f"""🏥 **PLANOS DE SAÚDE**: Analisando sua questão sobre "{question}".

**Especialidades**: ⏰ **Carências**, ✅ **Coberturas Obrigatórias**, 💰 **Coparticipação**, 💵 **Reembolso**, 📞 **Reclamações ANS**, ⚖️ **Direitos do Beneficiário**.

🔍 **Seja mais específico**: Informe sobre carências, negativas, valores, ou outros aspectos para orientação detalhada conforme Lei 9.656/98 e regulamentações ANS!"""