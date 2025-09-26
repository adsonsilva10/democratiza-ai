from app.agents.base_agent import BaseContractAgent

class TVSubscriptionAgent(BaseContractAgent):
    """Agente especializado em contratos de TV por assinatura"""
    
    def __init__(self):
        self.specialization = "TV por Assinatura"
        self.icon = "📺"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para TV por assinatura"""
        
        if not question:
            return """📺 **TV por Assinatura - Análise Especializada**

Olá! Sou especialista em contratos de TV por assinatura. Posso ajudar com:

**📋 Principais Análises:**
• Planos, canais e qualidade de imagem
• Período de fidelidade e multas
• Equipamentos e instalação
• Mudança de endereço e portabilidade
• Cancelamento e devolução de aparelhos

**⚠️ Pontos Críticos:**
• Fidelidade superior a 12 meses
• Cobrança de canais não solicitados
• Dificuldades no cancelamento
• Multa desproporcional por rescisão

**📞 Órgãos de Defesa:**
• ANATEL - Regulamentação de telecomunicações
• PROCON - Defesa do consumidor
• Anatel.gov.br - Portal de reclamações

Como posso ajudar com sua TV por assinatura?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['cancelar', 'cancelamento', 'rescindir', 'sair']):
            return """❌ **Cancelamento de TV por Assinatura**

**Seu Direito de Cancelar:**
• **Após fidelidade**: Cancelamento livre e gratuito
• **Durante fidelidade**: Pagamento de multa proporcional
• **Direito de arrependimento**: 7 dias para novos contratos
• **Prazo de cancelamento**: Até 30 dias de antecedência

**Como Cancelar:**
• **Central de atendimento**: 0800 ou chat online
• **Presencial**: Loja da operadora
• **Por escrito**: Email ou carta registrada
• **Protocolo**: Sempre anote número do protocolo

**Prazos Importantes:**
• **Solicitação**: Até dia 25 para vencer no mês seguinte
• **Suspensão do serviço**: Imediata ou conforme solicitado
• **Devolução de equipamentos**: Até 30 dias após cancelamento
• **Última cobrança**: Proporcional aos dias de uso

**⚠️ Cuidados no Cancelamento:**
• Confirme data de suspensão do serviço
• Solicite protocolo por escrito (email/SMS)
• Agende retirada dos equipamentos
• Guarde comprovante de devolução dos aparelhos

**Devolução de Equipamentos:**
• **Prazo**: Até 30 dias após cancelamento
• **Responsabilidade**: Sua (entregar em perfeito estado)
• **Multa**: Se não devolver ou danificar equipamentos
• **Agendamento**: Operadora deve facilitar a devolução

**🛡️ Seus Direitos:**
• Cancelamento gratuito após período de fidelidade
• Protocolo de cancelamento por escrito
• Prazo adequado para devolução de equipamentos
• Não cobrança após data do cancelamento

**📞 Se Houver Dificuldades:**
• **ANATEL**: anatel.gov.br ou 1331
• **PROCON**: Reclamação por cobrança indevida
• **Operadora**: Ouvidoria da empresa

**💡 Dica Importante:**
Sempre confirme cancelamento por escrito e guarde protocolo. Muitas operadoras "esquecem" cancelamentos feitos só por telefone.

**⚖️ Base Legal:**
Lei 9.472/97 (Lei Geral de Telecomunicações) e CDC.

Está enfrentando dificuldades para cancelar? Posso orientar sobre os próximos passos!"""
        
        if any(word in question_lower for word in ['fidelidade', 'multa', 'prazo', 'contrato']):
            return """⏰ **Fidelidade e Multas - TV por Assinatura**

**Período de Fidelidade:**
• **Duração máxima**: 12 meses por lei (ANATEL)
• **Início**: A partir da ativação do serviço
• **Renovação**: Só com concordância expressa do cliente
• **Benefício**: Desconto na mensalidade ou equipamento gratuito

**Multa por Rescisão:**
• **Base de cálculo**: Mensalidades restantes do período de fidelidade
• **Desconto**: Proporcional ao tempo já cumprido
• **Limite**: Valor das parcelas restantes do desconto obtido
• **Cobrança**: Na última fatura ou boleto separado

**Cálculo da Multa:**
```
Exemplo: Fidelidade 12 meses, cancelou no 8º mês
Multa = (12 - 8) × valor do desconto mensal
Multa = 4 × desconto recebido por mês
```

**⚠️ Situações Sem Multa:**
• **Mudança de endereço**: Se operadora não atende nova região
• **Falha na prestação**: Serviço inadequado comprovado
• **Direito de arrependimento**: Primeiros 7 dias
• **Vício do serviço**: Problemas técnicos não resolvidos

**Contestação de Multa:**
• **ANATEL**: Se multa for abusiva ou indevida
• **Documentação**: Protocolos de reclamação de problemas
• **Mediação**: PROCON pode ajudar na negociação
• **Acordo**: Operadora pode aceitar reduzir ou perdoar multa

**🛡️ Seus Direitos:**
• Fidelidade máxima de 12 meses
• Informação clara sobre valor da multa
• Não renovação automática da fidelidade
• Contestar multa se serviço foi inadequado

**📋 Renovação de Fidelidade:**
• **Automática**: PROIBIDA por lei
• **Expressa**: Só com sua concordância formal
• **Benefício**: Deve ter contrapartida clara
• **Liberdade**: Pode recusar renovação sem penalidade

**💡 Dicas Importantes:**
• Leia contrato antes de aceitar fidelidade
• Documente problemas técnicos (podem anular multa)
• Negocie com operadora antes de aceitar multa
• Compare benefício da fidelidade com liberdade de trocar

**🚨 Multa Abusiva?**
Se multa for superior ao benefício recebido ou sem contrapartida clara, conteste na ANATEL!

Precisa de ajuda para calcular ou contestar sua multa?"""
        
        if any(word in question_lower for word in ['canais', 'programação', 'qualidade', 'sinal']):
            return """📺 **Canais e Qualidade do Serviço**

**Obrigações da Operadora:**
• **Canais contratados**: Fornecer TODOS os canais do plano
• **Qualidade de imagem**: HD/4K conforme prometido
• **Estabilidade**: Sinal sem interrupções frequentes
• **Programação**: Conforme grade divulgada

**Qualidade Mínima Exigida:**
• **Disponibilidade**: 95% do tempo por mês
• **Qualidade de imagem**: Conforme tecnologia contratada (SD/HD/4K)
• **Áudio**: Sincronizado e sem ruídos
• **Legendas**: Funcionando corretamente quando disponíveis

**Problemas Comuns:**
• **Canais fora do ar**: Sem justificativa técnica
• **Imagem pixelizada**: Sinal fraco ou equipamento defeituoso
• **Áudio dessincronizado**: Problema técnico não resolvido
• **Canais removidos**: Sem aviso prévio adequado

**⚠️ Mudança na Programação:**
• **Remoção de canais**: Aviso prévio de 30 dias obrigatório
• **Substituição**: Deve ser por canal similar ou superior
• **Redução de valor**: Se remoção reduzir qualidade do plano
• **Rescisão sem multa**: Se alteração substancial prejudicar serviço

**Como Reclamar de Problemas:**
• **1º passo**: Contatar suporte técnico da operadora
• **Protocolo**: Anotar número e data de cada contato
• **Prazo**: Operadora tem até 48h para resolver problemas técnicos
• **Persistência**: Se não resolver, escalar para ouvidoria

**🛡️ Seus Direitos:**
• Receber todos os canais contratados
• Qualidade conforme especificada no contrato
• Aviso prévio de mudanças na programação
• Desconto proporcional por indisponibilidade

**📞 Canais de Reclamação:**
• **Suporte da operadora**: Primeiro contato
• **ANATEL**: 1331 ou anatel.gov.br
• **PROCON**: Para questões de consumo
• **Ouvidoria da operadora**: Segunda instância

**Compensação por Problemas:**
• **Desconto na fatura**: Por dias sem serviço adequado
• **Upgrade gratuito**: Compensação por transtornos
• **Rescisão sem multa**: Se problemas persistentes

**💡 Dica Prática:**
Documente SEMPRE os problemas: data, horário, canais afetados, protocolo de atendimento. Essa documentação é essencial para comprovar falha na prestação.

**📊 Medição de Qualidade:**
ANATEL possui sistema de medição de qualidade. Operadoras que não cumprem metas podem ser multadas e você pode usar isso como argumento.

Está enfrentando problemas com canais ou qualidade? Posso orientar sobre como documentar e reclamar!"""
        
        if any(word in question_lower for word in ['equipamento', 'aparelho', 'decoder', 'instalação']):
            return """📡 **Equipamentos e Instalação**

**Tipos de Equipamentos:**
• **Receptor/Decoder**: Principal (HD/4K/DVR)
• **Controle remoto**: Incluído no equipamento
• **Cabos e conectores**: Fornecidos pela operadora
• **Antena parabólica**: Para TV via satélite
• **Pontos adicionais**: Receptores extras para outros cômodos

**Instalação do Serviço:**
• **Prazo**: Até 7 dias após solicitação (ANATEL)
• **Agendamento**: Operadora deve ofertar horários
• **Custo**: Primeira instalação geralmente gratuita
• **Técnico**: Credenciado pela operadora
• **Teste**: Verificar funcionamento de todos os canais

**⚠️ Cuidados na Instalação:**
• Técnico deve mostrar funcionamento completo
• Teste todos os canais contratados
• Verifique qualidade de imagem e áudio
• Solicite orientação sobre uso do controle/funcionalidades

**Manutenção de Equipamentos:**
• **Garantia**: Mínimo 12 meses para defeitos
• **Manutenção**: Gratuita durante contrato vigente
• **Substituição**: Por equipamento similar ou superior
• **Prazo para reparo**: Até 48h para problemas técnicos

**Pontos Adicionais:**
• **Custo**: Varia por operadora (R$ 10-30/mês por ponto)
• **Instalação**: Pode ter custo adicional
• **Equipamento**: Receptor adicional necessário
• **Funcionalidades**: Podem ser limitadas vs ponto principal

**🛡️ Seus Direitos:**
• Instalação no prazo (7 dias)
• Equipamentos em perfeito funcionamento
• Manutenção gratuita durante vigência do contrato
• Substituição por defeito sem custo

**Problemas com Equipamentos:**
• **Defeito**: Substituição gratuita se em garantia
• **Obsolescência**: Atualização sem custo adicional
• **Perda/Roubo**: Sua responsabilidade de reposição
• **Dano**: Avaliar se foi por mau uso ou defeito

**Devolução na Rescisão:**
• **Prazo**: Até 30 dias após cancelamento
• **Estado**: Perfeitas condições de uso
• **Acessórios**: Incluir controles, cabos, fontes
• **Agendamento**: Operadora deve facilitar retirada

**💰 Custos Evitáveis:**
• **Taxa de instalação**: Questione se há promoção
• **Seguro de equipamento**: Geralmente opcional
• **Ponto adicional**: Negocie na contratação
• **Upgrade de equipamento**: Avalie necessidade real

**📞 Para Problemas Técnicos:**
1. **Suporte técnico**: 0800 da operadora
2. **Reagendamento**: Se técnico não compareceu
3. **ANATEL**: Se prazo não for cumprido
4. **Protocolo**: Sempre anote para acompanhamento

**💡 Dica Importante:**
Na instalação, teste TUDO antes de liberar o técnico. Problemas detectados depois podem gerar nova visita com possível custo.

Precisa de orientação sobre instalação ou problemas com equipamentos?"""
        
        if any(word in question_lower for word in ['mudança', 'endereço', 'mudar', 'transferir']):
            return """🏠 **Mudança de Endereço**

**Seu Direito à Portabilidade:**
• **Serviço disponível**: Transferência gratuita se operadora atende novo endereço
• **Serviço indisponível**: Rescisão sem multa se não atende
• **Mesmo plano**: Manter condições contratuais
• **Prazo**: Até 7 dias para ativação no novo endereço

**Processo de Mudança:**
• **Solicitação**: Contatar operadora com antecedência mínima de 15 dias
• **Verificação**: Operadora verifica disponibilidade técnica
• **Agendamento**: Instalação no novo endereço
• **Retirada**: Equipamentos do endereço antigo

**⚠️ Situações Especiais:**
• **Área sem cobertura**: Rescisão sem multa garantida por lei
• **Tecnologia inferior**: Direito a manter mesmo plano ou rescindir
• **Custo adicional**: Operadora não pode cobrar taxa de mudança
• **Fidelidade**: Continua valendo no novo endereço

**Custos na Mudança:**
• **Transferência**: GRATUITA por lei (ANATEL)
• **Nova instalação**: Sem custo adicional
• **Equipamentos**: Mesmos equipamentos ou similares
• **Plano**: Mesmas condições contratuais

**🛡️ Seus Direitos:**
• Mudança gratuita se há cobertura no novo endereço
• Rescisão sem multa se não há cobertura
• Manter mesmo plano e condições
• Instalação no prazo (até 7 dias)

**Problemas Comuns:**
• **Taxa de mudança**: ILEGAL - conteste
• **Plano inferior**: Direito a manter o mesmo ou similar
• **Demora na instalação**: Acima de 7 dias é irregular
• **Equipamentos diferentes**: Devem ter mesma funcionalidade

**Mudança para Área Sem Cobertura:**
• **Rescisão automática**: Sem multa ou penalidade
• **Devolução de equipamentos**: Prazo estendido (até 60 dias)
• **Valores pagos antecipadamente**: Devem ser restituídos
• **Comprovação**: Operadora deve comprovar indisponibilidade

**📞 Como Solicitar:**
1. **Contato**: Central de atendimento da operadora
2. **Documentação**: Comprovante do novo endereço
3. **Verificação**: Aguardar análise técnica de viabilidade
4. **Agendamento**: Definir data da instalação
5. **Protocolo**: Anotar número para acompanhamento

**💡 Dicas Importantes:**
• Solicite mudança com antecedência (mín. 15 dias)
• Confirme cobertura antes de se mudar definitivamente
• Documente toda comunicação com protocolos
• Se não houver cobertura, exija rescisão sem multa

**⚖️ Base Legal:**
Resolução ANATEL 632/14 sobre mudança de endereço.

**🚨 Operadora se recusa?**
Se operadora cobrar taxa ou se recusar a transferir serviço disponível, registre reclamação na ANATEL imediatamente!

Está planejando mudança ou enfrentando problemas? Posso orientar sobre seus direitos!"""
        
        if any(word in question_lower for word in ['cobrança', 'fatura', 'valor', 'desconto']):
            return """💰 **Cobrança e Faturamento**

**Composição da Fatura:**
• **Mensalidade do plano**: Valor fixo contratado
• **Pontos adicionais**: Receptores extras
• **Canais premium**: Se contratados separadamente  
• **Equipamentos**: Aluguel de decoders especiais
• **Serviços extras**: Pay-per-view, gravação, etc.

**Regras de Cobrança:**
• **Vencimento**: Data fixa mensal
• **Cobrança proporcional**: No primeiro mês de ativação
• **Antecipada**: Mensalidade é sempre antecipada
• **Reajuste**: Uma vez ao ano, máximo IGP-M + 3%

**⚠️ Cobranças Irregulares:**
• **Serviços não solicitados**: Canais premium automáticos
• **Equipamentos não pedidos**: Decoders extras
• **Multas indevidas**: Por problemas técnicos da operadora
• **Reajustes abusivos**: Acima do permitido por lei

**Contestação de Valores:**
• **Prazo**: Até 90 dias após recebimento da fatura
• **Documentação**: Protocolos e comprovantes necessários
• **Suspensão**: Operadora deve suspender cobrança contestada
• **Análise**: Operadora tem até 30 dias para responder

**🛡️ Seus Direitos:**
• Fatura detalhada com discriminação de serviços
• Contestar valores indevidos
• Não pagamento de serviços não solicitados
• Reajuste limitado por lei

**Desconto por Problemas:**
• **Indisponibilidade**: Desconto proporcional aos dias sem serviço
• **Qualidade inferior**: Redução por não cumprimento do contrato
• **Falha técnica**: Compensação por transtornos
• **Atraso na instalação**: Desconto pela demora

**Suspensão por Inadimplência:**
• **Prazo**: Após 30 dias do vencimento
• **Notificação**: Aviso prévio obrigatório
• **Religação**: Até 24h após pagamento
• **Taxa de religação**: Limitada pelo valor regulamentado

**📊 Auditoria de Conta:**
• **Análise mensal**: Verifique todos os itens da fatura
• **Histórico**: Compare com faturas anteriores
• **Serviços**: Confirme se todos foram solicitados
• **Valores**: Verifique se estão conforme contrato

**💡 Dicas para Economizar:**
• Analise se usa todos os canais do plano
• Questione necessidade de pontos adicionais
• Avalie canais premium vs streaming
• Negocie desconto na renovação do contrato

**📞 Para Contestar Cobrança:**
1. **Central de atendimento**: Primeira tentativa
2. **Protocolo**: Anote número da reclamação
3. **Por escrito**: Email ou carta se necessário
4. **PROCON/ANATEL**: Se operadora não resolver

**⚖️ Base Legal:**
CDC e Regulamento da ANATEL sobre cobrança de telecomunicações.

Está com problemas na sua fatura? Posso ajudar a identificar cobranças irregulares!"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""📺 **Análise do Contrato de TV por Assinatura**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Plano e Serviços:**
• Canais incluídos no pacote contratado
• Qualidade de imagem (SD/HD/4K)
• Serviços adicionais incluídos
• Número de pontos/receptores

**2. Fidelidade e Multas:**
• Período de fidelidade (máx. 12 meses)
• Valor e cálculo da multa rescisória
• Benefícios obtidos pela fidelidade
• Condições de renovação

**3. Equipamentos:**
• Tipos de equipamentos fornecidos
• Responsabilidades de manutenção
• Condições de devolução na rescisão
• Custos de pontos adicionais

**4. Condições Comerciais:**
• Valor da mensalidade e reajustes
• Condições de mudança de endereço
• Política de cancelamento
• Prazos de instalação e atendimento

**⚖️ Conformidade Legal:**
Este contrato deve seguir regulamentação da ANATEL e CDC.

Posso analisar algum ponto específico que está gerando dúvida?"""
        
        # Resposta geral
        return """📺 **TV por Assinatura - Orientação Geral**

Entendi sua pergunta sobre TV por assinatura. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de fidelidade e multas (conformidade ANATEL)
• Análise de canais e qualidade do serviço
• Orientação sobre cancelamento e mudança de endereço
• Contestação de cobranças irregulares

**⚠️ Problemas Mais Comuns:**
• Fidelidade superior a 12 meses
• Dificuldades no cancelamento
• Cobrança de serviços não solicitados
• Problemas na mudança de endereço

**🛡️ Seus Direitos Principais:**
• Fidelidade máxima de 12 meses
• Cancelamento livre após fidelidade
• Mudança gratuita de endereço (se há cobertura)
• Qualidade dos serviços conforme contratado

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça o texto do contrato."""