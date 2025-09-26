from app.agents.base_agent import BaseContractAgent

class MobileAgent(BaseContractAgent):
    """Agente especializado em contratos de telefonia móvel"""
    
    def __init__(self):
        self.specialization = "Telefonia Móvel"
        self.icon = "📱"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para telefonia móvel"""
        
        if not question:
            return """📱 **Telefonia Móvel - Análise Especializada**

Olá! Sou especialista em contratos de telefonia móvel. Posso ajudar com:

**📋 Principais Análises:**
• Planos pré e pós-pago
• Fidelidade e multas contratuais  
• Cobertura e qualidade do sinal
• Portabilidade numérica
• Cobrança de serviços adicionais

**⚠️ Pontos Críticos:**
• Fidelidade superior a 12 meses
• Serviços premium não solicitados
• Cobertura inadequada na região
• Dificuldades no cancelamento

**📞 Órgãos de Defesa:**
• ANATEL - Regulamentação de telecomunicações
• PROCON - Defesa do consumidor
• Portal da ANATEL (anatel.gov.br)

Como posso ajudar com seu plano móvel?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['plano', 'pré', 'pós', 'franquia', 'dados']):
            return """📱 **Planos de Telefonia Móvel**

**Tipos de Plano:**

**Pré-pago:**
• **Funcionamento**: Pagamento antecipado de créditos
• **Validade**: Créditos têm prazo de validade
• **Vantagem**: Controle total dos gastos
• **Desvantagem**: Pode ficar sem crédito em emergências
• **Regulamentação**: Mínimo 30 dias de validade

**Pós-pago:**
• **Funcionamento**: Fatura mensal com valor fixo + extras
• **Franquia**: Limites de minutos, SMS e dados
• **Vantagem**: Não precisa recarregar, mais serviços
• **Desvantagem**: Conta pode vir alta por extras
• **Fidelidade**: Pode ter contrato de permanência

**Planos Controle:**
• **Híbrido**: Características de pré + pós
• **Limite**: Valor máximo pré-definido na fatura
• **Franquia**: Pacote fixo de serviços
• **Bloqueio**: Sem riscos de extrapolação

**⚠️ Componentes da Franquia:**

**Minutos:**
• **Locais**: Para mesma área (DDD)
• **Nacionais**: Para qualquer DDD do Brasil
• **Fixo-móvel**: Diferenciação pode existir
• **Ilimitado**: Uso livre dentro da fair use policy

**SMS:**
• **Quantidade**: Limitada por mês
• **Cobrança extra**: Por SMS excedente
• **WhatsApp**: Não conta como SMS
• **Internacional**: Tarifas especiais

**Dados (Internet):**
• **Franquia mensal**: GB disponíveis por mês
• **Velocidade reduzida**: Após esgotar franquia
• **Rollover**: Franquia não utilizada acumula (alguns planos)
• **Zero rating**: Apps que não consomem franquia

**🛡️ Seus Direitos:**
• Informação clara sobre limites e tarifas
• Bloqueio de serviços pagos não solicitados
• Aviso quando atingir 80% e 100% da franquia
• Velocidade mínima mesmo após franquia (256 kbps)

**Fair Use Policy:**
• **"Ilimitado"**: Na verdade tem limites de fair use
• **Limite típico**: 100-300 GB/mês para dados
• **Consequência**: Velocidade reduzida após limite
• **Transparência**: Deve estar claro no contrato

**Serviços Extras Comuns:**
• **Roaming**: Uso fora da área de cobertura
• **Internacional**: Chamadas e dados no exterior
• **Premium**: Conteúdos pagos (música, vídeo)
• **Seguro**: Proteção do aparelho

**💡 Como Escolher o Plano Ideal:**
• Analise seu consumo real de minutos, SMS e dados
• Verifique cobertura na sua região e locais frequentes
• Compare preços entre operadoras
• Considere portabilidade se insatisfeito

**📊 Monitoramento do Consumo:**
• App da operadora para acompanhar gastos
• SMS automático com avisos de consumo
• *544# para consultar saldo e franquia
• Configurar alertas de limite

**⚖️ Base Legal:**
Regulamento da ANATEL sobre Serviços de Telecomunicações.

Precisa de orientação sobre qual tipo de plano escolher ou problemas com seu plano atual?"""
        
        if any(word in question_lower for word in ['portabilidade', 'trocar', 'mudar', 'operadora']):
            return """🔄 **Portabilidade Numérica**

**O que é Portabilidade:**
• **Direito garantido**: Manter seu número ao trocar de operadora
• **Gratuito**: Não pode haver cobrança pela portabilidade
• **Rápido**: Processo em até 3 dias úteis
• **Simples**: Apenas alguns documentos necessários

**Como Fazer Portabilidade:**

**Passo a Passo:**
• **1º**: Escolha nova operadora e plano
• **2º**: Solicite portabilidade (não cancelamento)
• **3º**: Forneça documentos necessários
• **4º**: Aguarde processo (até 3 dias úteis)
• **5º**: Receba confirmação da portabilidade

**Documentos Necessários:**
• **Pessoa física**: RG, CPF
• **Pessoa jurídica**: CNPJ, contrato social
• **Procuração**: Se representante for fazer
• **Conta atual**: Últimas faturas para confirmar titularidade

**⚠️ Requisitos para Portabilidade:**
• **Linha ativa**: Não pode estar cancelada
• **Titular**: Só titular pode solicitar
• **Débitos**: Operadora atual pode exigir quitação
• **Fidelidade**: Multa pode ser cobrada (se aplicável)

**Prazos do Processo:**
• **Solicitação**: Até 18h do dia útil
• **Processamento**: 1 a 3 dias úteis
• **Ativação**: Automática no horário agendado
• **Confirmação**: SMS de ambas operadoras

**🛡️ Seus Direitos:**
• Portabilidade gratuita
• Manter mesmo número
• Processo em até 3 dias úteis
• Não pode ser impedido por débitos contestados

**Problemas Comuns:**
• **Operadora atual nega**: Só pode negar se titular não for quem solicita
• **Demora excessiva**: Acima de 3 dias é irregular
• **Cobrança indevida**: Portabilidade é gratuita
• **Perda de serviços**: Alguns benefícios podem não transferir

**Portabilidade com Débito:**
• **Débito reconhecido**: Pode impedir portabilidade
• **Débito contestado**: Não pode impedir
• **Negociação**: Tente acordo antes da portabilidade
• **Direito**: Contestar na ANATEL se impedimento for indevido

**Cancelamento vs Portabilidade:**
• **Cancelamento**: Perde o número definitivamente
• **Portabilidade**: Mantém número na nova operadora
• **Multa**: Mesma regra para ambos (se houver fidelidade)
• **Processo**: Portabilidade é mais vantajosa

**💡 Dicas Importantes:**
• Nunca cancele a linha antes de fazer portabilidade
• Compare planos detalhadamente antes de decidir
• Verifique cobertura da nova operadora na sua região
• Guarde protocolos de toda comunicação

**Portabilidade Empresarial:**
• **Múltiplas linhas**: Pode portar várias simultaneamente
• **Documentação**: Mais complexa (CNPJ, procuração)
• **Negociação**: Operadoras oferecem condições especiais
• **Prazo**: Mesmo prazo (3 dias úteis)

**📞 Se Houver Problemas:**
• **ANATEL**: 1331 ou anatel.gov.br
• **Protocolo**: Anote todos os números para acompanhamento
• **Ouvidoria**: Das operadoras envolvidas
• **PROCON**: Se houver cobrança indevida

**⚖️ Regulamentação:**
Resolução ANATEL 85/98 sobre portabilidade numérica.

Está pensando em fazer portabilidade ou enfrentou problemas no processo?"""
        
        if any(word in question_lower for word in ['cobertura', 'sinal', 'qualidade', 'área']):
            return """📡 **Cobertura e Qualidade do Sinal**

**Tipos de Cobertura:**

**2G (GSM):**
• **Função**: Chamadas de voz e SMS
• **Velocidade**: Até 384 kbps (dados básicos)
• **Alcance**: Maior cobertura geográfica
• **Status**: Sendo desativado gradualmente

**3G (UMTS/HSPA):**
• **Função**: Voz, SMS e dados
• **Velocidade**: 384 kbps a 42 Mbps
• **Uso**: Internet básica, WhatsApp
• **Cobertura**: Ampla nas cidades

**4G (LTE):**
• **Função**: Dados em alta velocidade + VoLTE
• **Velocidade**: 1 Mbps a 1 Gbps
• **Uso**: Streaming, videochamadas
• **Cobertura**: Foco em áreas urbanas

**5G:**
• **Função**: Ultra alta velocidade e baixa latência
• **Velocidade**: Até 20 Gbps
• **Uso**: IoT, realidade virtual
• **Cobertura**: Ainda limitada (grandes centros)

**⚠️ Problemas de Cobertura:**

**Sem Sinal:**
• **Área não coberta**: Fora da área de cobertura da operadora
• **Obstáculos**: Prédios, montanhas bloqueiam sinal
• **Sobrecarga**: Muitos usuários na mesma célula
• **Manutenção**: Torres em manutenção temporária

**Sinal Fraco:**
• **Distância**: Longe da torre mais próxima
• **Interferência**: Outros equipamentos eletrônicos
• **Indoor**: Interior de prédios com estrutura metálica
• **Clima**: Chuva forte pode afetar sinal

**🛡️ Seus Direitos:**
• Cobertura conforme mapa divulgado pela operadora
• Qualidade adequada nas áreas cobertas
• Informação clara sobre limitações
• Rescisão sem multa se cobertura for inadequada

**Como Verificar Cobertura:**
• **Site da operadora**: Mapa de cobertura oficial
• **App da ANATEL**: "Sinal" para medição
• **Teste in loco**: Verificar no local antes da contratação
• **Consulta**: Informar CEP para operadora

**Medição de Qualidade:**
• **Velocidade**: Apps como Speedtest, nPerf
• **Chamadas**: Taxa de chamadas completadas
• **Cobertura indoor**: Sinal dentro de imóveis
• **Latência**: Tempo de resposta da rede

**Reclamação por Má Cobertura:**
• **1º passo**: Protocolar na operadora
• **Documentação**: Prints de testes, fotos do local
• **Prazo**: Operadora tem 30 dias para resposta
• **ANATEL**: Se operadora não resolver

**💡 Soluções para Melhorar Sinal:**

**Temporárias:**
• **Posicionamento**: Próximo a janelas, áreas altas
• **Horário**: Evitar horários de pico (18h-22h)
• **Wi-Fi**: Usar Wi-Fi calling quando disponível
• **Modo avião**: Resetar conexão com a rede

**Definitivas:**
• **Repetidor de sinal**: Para ambientes internos
• **Antena externa**: Para áreas rurais
• **Troca de operadora**: Se cobertura for inadequada
• **Plano**: Operadora com melhor cobertura na região

**Cobertura Rural:**
• **Programas governamentais**: Ampliação de cobertura
• **Tecnologia**: Antenas de longo alcance
• **Limitações**: Velocidades menores
• **Alternativas**: Internet via satélite

**📊 Metas de Qualidade ANATEL:**
• **Cobertura**: Mínimo por região
• **Velocidade**: Conforme tecnologia
• **Disponibilidade**: Percentual de tempo ativo
• **Multas**: Para operadoras que não cumprem

**📞 Canais para Reclamação:**
• **Operadora**: Central de atendimento primeiro
• **ANATEL**: 1331 ou anatel.gov.br
• **App Sinal**: Para reportar problemas de cobertura
• **PROCON**: Se houver prejuízo comercial

**⚖️ Regulamentação:**
Regulamento de Gestão da Qualidade da ANATEL.

Está enfrentando problemas de sinal ou cobertura na sua região?"""
        
        if any(word in question_lower for word in ['cancelar', 'cancelamento', 'fidelidade', 'multa']):
            return """❌ **Cancelamento e Fidelidade**

**Cancelamento de Linha Móvel:**

**Pós-pago:**
• **Como cancelar**: Central de atendimento ou loja
• **Protocolo**: Sempre solicitar número do protocolo
• **Prazo**: Efetivação em até 24-48h
• **Última fatura**: Proporcional aos dias de uso

**Pré-pago:**
• **Automático**: Para de funcionar quando acabam créditos
• **Manual**: Solicitar bloqueio definitivo
• **Portabilidade**: Melhor opção para manter número
• **Sem custos**: Não há fatura para quitar

**⚠️ Fidelidade Contratual:**

**Regras da Fidelidade:**
• **Prazo máximo**: 12 meses por lei
• **Benefício**: Desconto no aparelho ou na mensalidade
• **Multa**: Proporcional ao período restante
• **Renovação**: Só com concordância expressa

**Cálculo da Multa:**
```
Multa = (Meses restantes / 12) × Benefício recebido
Exemplo: 6 meses restantes, desconto R$ 240 no aparelho
Multa = (6/12) × R$ 240 = R$ 120
```

**Situações Sem Multa:**
• **Cobertura inadequada**: Se operadora não atende sua região
• **Mudança de endereço**: Para área sem cobertura
• **Falha na prestação**: Problemas não resolvidos
• **Direito de arrependimento**: 7 dias (CDC)

**🛡️ Seus Direitos:**
• Cancelamento gratuito após fidelidade
• Multa proporcional (não integral)
• Informação clara sobre valor da multa
• Contestar se serviço foi inadequado

**Problemas no Cancelamento:**

**Operadora Dificulta:**
• **Retenção agressiva**: Ofertas para não cancelar
• **Burocracia excessiva**: Exigir presença em loja
• **Demora**: Não processar cancelamento
• **Cobrança posterior**: Fatura após cancelamento

**Como Proceder:**
• **Seja firme**: Confirme que quer cancelar
• **Protocolo**: Anote e exija por escrito (email/SMS)
• **Prazo**: Dê prazo máximo para efetivação
• **ANATEL**: Reclame se houver resistência

**Cancelamento por Morte:**
• **Documentos**: Certidão de óbito + documentos do titular
• **Família**: Parentes podem solicitar
• **Multa**: Geralmente perdoada
• **Processo**: Simplificado pela operadora

**Transferência de Titularidade:**
• **Alternativa**: Em vez de cancelar, transferir
• **Cônjuge/filhos**: Para familiares
• **Venda**: Para terceiros (com anuência)
• **Manter fidelidade**: Benefícios continuam

**💡 Dicas Antes de Cancelar:**
• **Portabilidade**: Considere trocar de operadora
• **Negociação**: Tente melhor plano/preço
• **Backup**: Salve contatos e dados importantes
• **Confirme**: Se realmente quer perder o número

**Cobrança Após Cancelamento:**
• **Ilegítima**: Não deve haver cobrança
• **Contestação**: Protocole imediatamente
• **Prova**: Guarde protocolo do cancelamento
• **Negativação**: Indevida se cancelamento foi protocolado

**📞 Canais para Cancelamento:**
• **Central**: 1057 (geral) ou 0800 da operadora
• **Loja física**: Presencial com documentos
• **App/Site**: Algumas operadoras permitem
• **Chat online**: Opção em algumas operadoras

**⚖️ Base Legal:**
CDC e Regulamento da ANATEL sobre direito de cancelamento.

Está enfrentando dificuldades para cancelar ou tem dúvidas sobre multa de fidelidade?"""
        
        if any(word in question_lower for word in ['cobrança', 'fatura', 'conta', 'valor', 'serviço']):
            return """💰 **Cobrança e Faturamento Móvel**

**Composição da Fatura:**

**Valores Fixos:**
• **Mensalidade**: Valor base do plano contratado
• **Franquia**: Minutos, SMS e dados inclusos
• **Linha adicional**: Se família/empresarial
• **Seguro**: Proteção do aparelho (se contratado)

**Valores Variáveis:**
• **Excedentes**: Uso além da franquia
• **Roaming**: Uso fora da área de origem
• **Internacional**: Chamadas/dados no exterior
• **Serviços premium**: Conteúdos pagos

**⚠️ Cobranças Irregulares:**

**Serviços Não Solicitados:**
• **Premium SMS**: Assinatura de conteúdos
• **Torpedos promocionais**: Cobrança por receber
• **Jogos/ringtones**: Ativação automática
• **Horóscopo/notícias**: Serviços de valor adicionado

**Como Identificar:**
• **Códigos curtos**: 4 ou 5 dígitos (4141, 86886)
• **Valores pequenos**: R$ 0,30 a R$ 4,99 por SMS
• **Frequência**: Cobranças recorrentes
• **Descrição vaga**: "Serv. Valor Agregado"

**🛡️ Seus Direitos:**
• Bloqueio gratuito de serviços premium
• Estorno de cobranças não autorizadas
• Fatura clara e detalhada
• Aviso antes de atingir limites

**Bloqueio de Serviços Premium:**
• **Gratuito**: Por lei, não pode haver cobrança
• **Como solicitar**: Central de atendimento (*144)
• **Tipos**: Bloqueio parcial ou total
• **Efeito**: Impede novas contratações acidentais

**Contestação de Valores:**
• **Prazo**: Até 90 dias da data da fatura
• **Como**: Central, app ou por escrito
• **Suspensão**: Operadora deve suspender cobrança contestada
• **Análise**: Até 30 dias para resposta

**Cobrança de Roaming:**
• **Nacional**: Uso fora da área de registro
• **Internacional**: No exterior
• **Tarifas**: Mais caras que uso normal
• **Bloqueio preventivo**: Solicitar antes de viajar

**💡 Dicas para Controlar Gastos:**

**Monitoramento:**
• **App da operadora**: Consumo em tempo real
• **SMS automático**: Alertas de 50%, 80% e 100%
• **Código**: *544# para consultar saldo
• **Configurações**: Limite de dados no smartphone

**Bloqueios Preventivos:**
• **Dados no exterior**: Evitar cobrança internacional
• **Serviços premium**: Impedir assinaturas acidentais
• **Chamadas 0900**: Números de tarifa especial
• **Roaming**: Se não vai usar fora da cidade

**Parcelamento de Débitos:**
• **Direito**: Até 12 vezes para débitos
• **Condições**: Conforme política da operadora
• **Juros**: Podem ser aplicados
• **Negociação**: Desconto para pagamento à vista

**📊 Auditoria da Fatura:**
• **Confira mensalmente**: Todos os itens
• **Compare**: Com faturas anteriores
• **Questione**: Valores não reconhecidos
• **Documente**: Protocolos de reclamação

**Fatura Digital:**
• **Vantagens**: Chegada mais rápida, sem taxa postal
• **Ambiente**: Contribui com meio ambiente
• **Acesso**: App, email ou site da operadora
• **Histórico**: Consulta de faturas antigas

**⚖️ Tributação:**
• **ICMS**: Imposto estadual (varia por UF)
• **Fistel**: Taxa anual de fiscalização
• **ISS**: Sobre alguns serviços (municipal)

**📞 Para Contestar Cobranças:**
• **Central da operadora**: *144 ou 1057
• **App/Site**: Canais digitais
• **Loja**: Atendimento presencial
• **PROCON**: Se operadora não resolver

**⚖️ Base Legal:**
CDC sobre direito de contestação e transparência na cobrança.

Está com problemas na sua fatura ou cobranças não reconhecidas?"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""📱 **Análise do Contrato de Telefonia Móvel**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Tipo de Plano:**
• Modalidade (pré, pós-pago, controle)
• Franquia de minutos, SMS e dados
• Serviços inclusos e opcionais
• Condições de uso (fair use policy)

**2. Fidelidade e Multas:**
• Período de permanência (máx. 12 meses)
• Benefícios obtidos pela fidelidade
• Cálculo da multa rescisória
• Situações de isenção de multa

**3. Cobertura e Qualidade:**
• Área de cobertura garantida
• Tecnologias disponíveis (3G, 4G, 5G)
• Metas de qualidade
• Direitos em caso de má cobertura

**4. Cobrança e Faturamento:**
• Composição do valor mensal
• Tarifas de excedentes
• Serviços premium e bloqueios
• Condições de reajuste

**⚖️ Conformidade Legal:**
Este contrato deve seguir regulamentação da ANATEL e CDC.

Posso analisar algum aspecto específico que está causando dúvida?"""
        
        # Resposta geral
        return """📱 **Telefonia Móvel - Orientação Geral**

Entendi sua pergunta sobre telefonia móvel. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de planos e franquias
• Orientação sobre portabilidade numérica
• Análise de problemas de cobertura
• Contestação de cobranças irregulares

**⚠️ Problemas Mais Comuns:**
• Serviços premium não solicitados
• Dificuldades no cancelamento
• Multa de fidelidade abusiva
• Cobertura inadequada

**🛡️ Seus Direitos Principais:**
• Fidelidade máxima de 12 meses
• Portabilidade gratuita
• Bloqueio gratuito de serviços premium
• Cancelamento após fidelidade sem multa

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça detalhes do contrato."""