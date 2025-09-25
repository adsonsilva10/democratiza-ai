from app.agents.base_agent import BaseContractAgent

class CreditCardAgent(BaseContractAgent):
    """Agente especializado em contratos de cartão de crédito"""
    
    def __init__(self):
        self.specialization = "Cartão de Crédito"
        self.icon = "💳"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para cartões de crédito"""
        
        if not question:
            return """💳 **Cartão de Crédito - Análise Especializada**

Olá! Sou especialista em contratos de cartão de crédito. Posso ajudar com:

**📋 Principais Análises:**
• Taxas e juros (rotativo, parcelado, saque)
• Anuidades e isenções
• Limite de crédito e alterações
• Seguros e produtos opcionais
• Programa de pontos e benefícios

**⚠️ Pontos Críticos:**
• Juros do rotativo (máximo de 8% ao mês)
• Cobrança de seguros não solicitados
• Alteração unilateral de condições
• Taxas abusivas ou não informadas

**📞 Órgãos de Defesa:**
• BACEN (Banco Central) - Registrator
• PROCON - Defesa do consumidor
• SPC/SERASA - Negativação indevida

Como posso ajudar com seu cartão de crédito?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['juros', 'taxa', 'rotativo', 'parcelamento', 'cet']):
            return """📊 **Juros e Taxas do Cartão de Crédito**

**Juros do Rotativo:**
• Máximo de 8% ao mês (Resolução CMN 4.549/2017)
• Cobrança apenas sobre valor em atraso
• Prazo mínimo de 30 dias para parcelamento

**Juros do Parcelamento:**
• Taxa livre negociação (mas deve ser informada)
• CET (Custo Efetivo Total) deve estar no contrato
• Simulações devem ser fornecidas antes da contratação

**Outras Taxas Comuns:**
• Saque: até 12% ao mês + tarifa fixa
• Pagamento mínimo: juros + principal
• Atraso na fatura: multa + juros + IOF

**🛡️ Proteções Legais:**
• Taxa deve ser informada ANTES da operação
• Direito ao CET antes da contratação
• Proibição de capitalização diária de juros

**💡 Dica Importante:**
Resolução CMN 4.549/2017 criou modalidade rotativo não remunerado (sem juros por 30 dias).

Precisa calcular alguma taxa específica?"""
        
        if any(word in question_lower for word in ['anuidade', 'anivers', 'isenção', 'isento', 'grátis']):
            return """💰 **Anuidade do Cartão de Crédito**

**Regras da Anuidade:**
• Pode ser cobrada anualmente ou em parcelas
• Valor deve estar claro no contrato
• Isenção pode ter condições específicas
• Cobrança proporcional ao uso (se aplicável)

**Tipos de Isenção:**
• **Permanente**: Sem condições adicionais
• **Por renda**: Comprovação de renda mínima
• **Por movimentação**: Gastos mínimos mensais/anuais
• **Promocional**: Por período determinado

**⚠️ Pontos de Atenção:**
• Leia condições de isenção detalhadamente
• Isenção promocional pode acabar
• Mudança de categoria pode alterar anuidade
• Cartões adicionais podem ter taxa própria

**🛡️ Seus Direitos:**
• Informação clara sobre anuidade
• Aviso prévio sobre cobrança
• Cancelamento sem custos se não aceitar
• Restituição se cobrança indevida

**📋 Regulamentação:**
Circular BACEN 3.598/2013 sobre transparência em cartões.

Tem dúvidas sobre isenção ou cobrança de anuidade?"""
        
        if any(word in question_lower for word in ['seguro', 'proteção', 'cobertura', 'opcional']):
            return """🛡️ **Seguros e Produtos Opcionais**

**Seguros Comuns:**
• Seguro proteção financeira
• Seguro de vida
• Seguro perda/roubo do cartão
• Seguro compra protegida
• Seguro viagem

**⚠️ Regras Importantes:**
• TODOS os seguros são OPCIONAIS
• Cobrança só pode ocorrer com autorização expressa
• Você pode cancelar a qualquer momento
• Cancelamento não pode ter custos

**Como identificar cobrança irregular:**
• Desconto na fatura sem autorização
• Seguros "automáticos" ou "gratuitos"
• Informação apenas em letra pequena
• Vendas por telefone sem confirmação por escrito

**🛡️ Seus Direitos (CDC):**
• Art. 39, III - Proibição de venda casada
• Cancelamento imediato sem custos
• Restituição de valores pagos indevidamente
• Informação clara sobre todos os custos

**📞 Como Cancelar:**
1. Ligue para o banco/administradora
2. Peça protocolo de cancelamento
3. Confirme por escrito (email/carta)
4. Guarde comprovantes

**💡 Dica Legal:**
Circular BACEN 3.598/2013 proíbe venda casada e exige autorização expressa.

Está enfrentando cobrança de seguro não autorizado?"""
        
        if any(word in question_lower for word in ['limite', 'aumentar', 'reduzir', 'crédito', 'disponível']):
            return """📈 **Limite de Crédito do Cartão**

**Como funciona o limite:**
• Valor máximo disponível para gastos
• Pode ser parcelado (limite rotativo)
• Inclui saques e compras
• Recompõe conforme pagamento

**Alteração de Limite:**
• **Aumento**: Depende de análise de crédito
• **Redução**: Você pode solicitar a qualquer momento
• **Bloqueio**: Por segurança ou inadimplência
• Aviso prévio obrigatório para reduções pelo banco

**Tipos de Limite:**
• **Compras**: Para aquisições normais
• **Saque**: Geralmente menor, com taxas maiores
• **Parcelamento**: Para dividir faturas
• **Internacional**: Para uso no exterior

**⚠️ Pontos Importantes:**
• Limite não é obrigação de usar
• Banco pode reduzir com aviso prévio
• Ultrapassar limite gera taxas extras
• Consulta ao CPF pode afetar limite

**🛡️ Regulamentação:**
• Resolução CMN 3.694/2009 sobre gestão de risco
• Circular BACEN 3.598/2013 sobre transparência

**💡 Dica:**
Mantenha dados atualizados para facilitar aumento de limite.

Precisa de ajuda com alguma questão específica sobre limite?"""
        
        if any(word in question_lower for word in ['cancelar', 'cancelamento', 'encerrar', 'rescindir']):
            return """❌ **Cancelamento do Cartão de Crédito**

**Como Cancelar:**
1. Quite todas as pendências (fatura, parcelamentos)
2. Entre em contato com o banco/administradora
3. Peça protocolo de cancelamento por escrito
4. Confirme por email ou carta registrada
5. Guarde todos os comprovantes

**Prazos Importantes:**
• Efeito imediato após quitação
• SPC/SERASA: baixa em até 5 dias úteis
• Última fatura: pode chegar após cancelamento
• Estorno de anuidade: proporcional se aplicável

**⚠️ Cuidados Especiais:**
• Cancele débitos automáticos vinculados
• Verifique se não há seguros ativos
• Confirme cancelamento de cartões adicionais
• Não desfaça-se do cartão antes da confirmação

**Situações Especiais:**
• **Cartão bloqueado**: Ainda precisa cancelar formalmente
• **Débitos pendentes**: Quitação obrigatória antes
• **Anuidade recente**: Direito ao estorno proporcional
• **Produto com pontos**: Verifique regras de resgate

**🛡️ Seus Direitos:**
• Cancelamento gratuito
• Baixa nos órgãos de proteção
• Estorno proporcional de anuidade
• Não cobrança após confirmação

**📞 Base Legal:**
Art. 6º, III do CDC - Direito à informação adequada sobre cancelamento.

Está enfrentando dificuldades para cancelar?"""
        
        if any(word in question_lower for word in ['pontos', 'milhas', 'programa', 'benefício', 'cashback']):
            return """⭐ **Programas de Pontos e Benefícios**

**Tipos de Programas:**
• **Pontos**: Acúmulo por compras para troca
• **Cashback**: Dinheiro de volta (%)
• **Milhas**: Para passagens aéreas
• **Descontos**: Em estabelecimentos parceiros

**Regras Importantes:**
• Validade dos pontos (geralmente 12-24 meses)
• Taxa de conversão deve ser clara
• Condições de resgate informadas
• Alterações com aviso prévio

**⚠️ Pontos de Atenção:**
• Leia regulamento completo do programa
• Pontos podem vencer se não usados
• Mudança de categoria pode afetar acúmulo
• Cancelamento do cartão pode fazer perder pontos

**Como Proteger seus Pontos:**
• Use periodicamente para não vencer
• Mantenha dados atualizados
• Acompanhe extratos regularmente
• Guarde comprovantes de resgates

**🛡️ Regulamentação:**
• Regulamento deve estar disponível
• Alterações com aviso de 30 dias
• Informação clara sobre validade

**💡 Estratégias:**
• Compare programas entre cartões
• Avalie custo x benefício da anuidade
• Use cartão específico para categoria com mais pontos

Tem dúvidas sobre algum programa de pontos específico?"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""💳 **Análise do Contrato de Cartão de Crédito**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Taxas e Juros:**
• Taxa do rotativo (máx. 8% a.m.)
• CET (Custo Efetivo Total) informado
• Taxa de saque e parcelamento
• Multa por atraso (máx. 2%)

**2. Anuidade e Isenções:**
• Valor da anuidade e forma de cobrança
• Condições para isenção (se houver)
• Prazo de validade da isenção promocional

**3. Seguros e Produtos Opcionais:**
• Quais seguros estão incluídos
• Se a contratação foi expressa
• Valores e formas de cancelamento

**4. Limites e Condições:**
• Limite inicial de crédito
• Condições para alteração
• Tipos de limite (compra, saque, internacional)

**5. Programa de Benefícios:**
• Pontos, milhas ou cashback
• Validade e regras de resgate
• Condições de alteração do programa

**⚖️ Conformidade Legal:**
Este contrato deve seguir o CDC, as Resoluções do BACEN e as normas do CMN.

Posso analisar algum ponto específico que está gerando dúvida?"""
        
        # Resposta geral
        return """💳 **Cartão de Crédito - Orientação Geral**

Entendi sua pergunta sobre cartão de crédito. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de taxas e juros (conformidade BACEN)
• Análise de seguros opcionais e vendas casadas
• Orientação sobre anuidades e isenções
• Programas de pontos e benefícios

**⚠️ Problemas Mais Comuns:**
• Cobrança de seguros não autorizados
• Juros acima do limite legal (8% a.m. rotativo)
• Informações não claras sobre taxas
• Dificuldades no cancelamento

**🛡️ Seus Direitos Principais:**
• Informação clara sobre TODAS as taxas
• Cancelamento gratuito de seguros opcionais
• Limite máximo de juros do rotativo
• 30 dias sem juros no rotativo (nova modalidade)

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça o texto do contrato."""