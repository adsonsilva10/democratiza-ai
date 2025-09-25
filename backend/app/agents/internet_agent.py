from app.agents.base_agent import BaseContractAgent

class InternetAgent(BaseContractAgent):
    """Agente especializado em contratos de internet banda larga"""
    
    def __init__(self):
        super().__init__()
        self.specialization = "Internet Banda Larga"
        self.icon = "🌐"
        
    def generate_response(self, question: str, context: str = None) -> str:
        """Gera resposta especializada para contratos de internet"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["velocidade", "mega", "fibra", "lenta"]):
            return """🌐 **VELOCIDADE DA INTERNET**:
            
📊 **GARANTIAS ANATEL**: 
🔸 **Fibra Óptica** → Mínimo 40% da velocidade contratada
🔸 **Cabo/Radio** → Mínimo 20% da velocidade contratada  
🔸 **Média mensal** → Mínimo 80% da velocidade

🔍 **TESTE OFICIAL**: anatel.gov.br/brasilbandalarga - **Único aceito** para comprovação oficial de problemas.

⚖️ **DIREITOS**: 🔸 **Desconto proporcional** na fatura, 🔸 **Rescisão sem multa** por descumprimento, 🔸 **Upgrade gratuito** se disponível.

📞 **RECLAMAÇÃO**: Primeiro com operadora (protocolo), depois ANATEL 1331 ou anatel.gov.br."""

        elif any(word in question_lower for word in ["instabilidade", "oscilação", "cai", "falha"]):
            return """🌐 **INSTABILIDADE/OSCILAÇÃO**:
            
📋 **REGISTRO**: Anote data/hora das falhas, faça testes no site da ANATEL, guarde protocolos de atendimento.

🔧 **CAUSAS COMUNS**: Equipamentos desatualizados, cabeamento interno, interferências, problemas na rede externa.

⚖️ **DIREITOS**: 🔸 **Desconto** proporcional ao tempo sem serviço, 🔸 **Visita técnica gratuita**, 🔸 **Troca de equipamentos** defeituosos.

📱 **TESTE**: Use app "Brasil Banda Larga" da ANATEL para medições oficiais. **Mínimo 6 testes** em dias/horários diferentes."""

        elif any(word in question_lower for word in ["fidelidade", "cancelar", "multa", "rescisão"]):
            return """🌐 **FIDELIDADE INTERNET**:
            
⏰ **PRAZOS**: Máximo **24 meses** de fidelidade (Decreto 10.771/21). **Após período** → Cancelamento livre.

💰 **MULTA**: Proporcional ao tempo restante. **Cálculo**: (Meses restantes ÷ Total) × Valor do desconto recebido.

🚫 **RESCISÃO SEM MULTA**:
🔸 **Mudança de endereço** sem cobertura
🔸 **Descumprimento da velocidade** 
🔸 **Alteração unilateral** prejudicial
🔸 **Desemprego** (comprovado)

📞 **PROCEDIMENTO**: Comunicar por escrito, exigir protocolo, confirmar data de corte e quitação final."""

        elif any(word in question_lower for word in ["equipamento", "modem", "roteador", "wifi"]):
            return """🌐 **EQUIPAMENTOS**:
            
📡 **FORNECIMENTO**: Operadora deve fornecer **modem básico gratuito** para acesso ao serviço contratado.

🔧 **INSTALAÇÃO**: **Primeira instalação gratuita**. Cobranças extras só para serviços adicionais (pontos extras, cabeamento especial).

📶 **WI-FI**: Roteador Wi-Fi pode ter custo adicional, mas muitas operadoras incluem no combo. **Verifique contrato**.

⚖️ **TROCA/DEFEITO**: Equipamento defeituoso deve ser trocado **gratuitamente**. Operadora não pode cobrar por problemas técnicos dela."""

        elif any(word in question_lower for word in ["franquia", "limite", "dados", "ilimitado"]):
            return """🌐 **FRANQUIA DE DADOS**:
            
📊 **BANDA LARGA FIXA**: Não pode ter franquia ou limite de dados (Resolução ANATEL 614/13). **Ilimitado real**.

🚨 **REDUÇÃO DE VELOCIDADE**: Após determinado uso pode haver redução, mas **deve estar clara no contrato**.

📱 **DIFERENÇA**: Internet móvel (celular) pode ter franquia, mas fixa domiciliar não.

⚖️ **DENÚNCIA**: Cobrança por excesso em internet fixa é **irregular**. Procure ANATEL 1331 para denunciar."""

        elif any(word in question_lower for word in ["mudança", "endereço", "transferir"]):
            return """🌐 **MUDANÇA DE ENDEREÇO**:
            
📍 **COBERTURA EXISTE**: Transferência gratuita ou taxa máxima de instalação. Manter mesmo plano e condições.

🚫 **SEM COBERTURA**: **Rescisão sem multa**, mesmo durante fidelidade. Operadora deve informar prazo para expansão.

📋 **PROCEDIMENTO**: 🔸 Consultar cobertura no novo endereço, 🔸 Protocolar solicitação, 🔸 Agendar transferência/desinstalação.

⏰ **PRAZO**: Até **7 dias** para instalar no novo endereço com cobertura existente."""

        else:
            return f"""🌐 **INTERNET BANDA LARGA**: Analisando sua questão sobre "{question}".

**Especialidades**: 📊 **Velocidade** (testes, garantias), 🔧 **Problemas Técnicos** (instabilidade, equipamentos), ⏰ **Fidelidade**, 📋 **Mudança de Endereço**, ⚖️ **Direitos ANATEL**.

🔍 **Seja mais específico**: Informe sobre velocidade, problemas técnicos, cancelamento, ou outros aspectos para orientação detalhada conforme regulamentações ANATEL!"""