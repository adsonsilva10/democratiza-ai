from app.agents.base_agent import BaseContractAgent

class EnergyAgent(BaseContractAgent):
    """Agente especializado em contratos de fornecimento de energia elétrica"""
    
    def __init__(self):
        self.specialization = "Energia Elétrica"
        self.icon = "⚡"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para energia elétrica"""
        
        if not question:
            return """⚡ **Energia Elétrica - Análise Especializada**

Olá! Sou especialista em contratos de fornecimento de energia elétrica. Posso ajudar com:

**📋 Principais Análises:**
• Tarifa e modalidade de cobrança
• Qualidade do fornecimento e interrupções
• Leitura e faturamento do consumo
• Ligação nova e transferência de titularidade
• Direitos do consumidor de energia

**⚠️ Pontos Críticos:**
• Cobrança por estimativa excessiva
• Interrupções frequentes sem justificativa
• Problemas na qualidade da energia
• Dificuldades para religação

**📞 Órgãos de Defesa:**
• ANEEL - Agência Nacional de Energia Elétrica
• PROCON - Defesa do consumidor
• Ouvidoria da distribuidora local

Como posso ajudar com sua conta de energia?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['conta', 'fatura', 'cobrança', 'valor', 'tarifa']):
            return """💡 **Conta de Energia e Tarifas**

**Composição da Conta:**
• **Energia consumida**: kWh multiplicado pela tarifa
• **Taxa de iluminação pública**: Custeio da iluminação municipal  
• **Bandeiras tarifárias**: Adicional conforme condições do sistema
• **ICMS**: Imposto estadual sobre energia
• **PIS/COFINS**: Tributos federais

**Modalidades Tarifárias:**
• **Convencional**: Residencial, pequeno comércio
• **Branca**: 3 horários diferentes (ponta, intermediário, fora ponta)
• **Verde/Azul**: Para grandes consumidores (indústrias)

**Bandeiras Tarifárias:**
• **Verde**: Sem acréscimo
• **Amarela**: +R$ 2,989/100kWh  
• **Vermelha 1**: +R$ 6,50/100kWh
• **Vermelha 2**: +R$ 9,795/100kWh
• **Escassez hídrica**: Adicional emergencial (quando ativa)

**⚠️ Problemas Comuns na Cobrança:**
• **Estimativa excessiva**: Leitura não realizada por meses
• **Erro de leitura**: Digitação incorreta do medidor
• **Tarifa incorreta**: Classificação errada do consumidor
• **Cobrança retroativa**: Valores antigos sem justificativa

**🛡️ Seus Direitos:**
• Leitura mensal obrigatória do medidor
• Fatura clara e detalhada
• Revisão de cobrança com erro comprovado
• Parcelamento de débitos em até 12 vezes

**Como Contestar Cobrança:**
• **1º passo**: Solicitar revisão à distribuidora
• **Documentação**: Histórico de consumo e fotos do medidor
• **Prazo**: Distribuidora tem até 30 dias para responder
• **Recurso**: ANEEL se distribuidora não resolver

**💰 Dicas para Economizar:**
• Tarifa branca: Pode ser vantajosa para quem usa mais energia fora do horário de ponta
• Bandeiras: Monitore e reduza consumo em bandeiras vermelhas
• Equipamentos: Troque por modelos mais eficientes (selo PROCEL)

**📊 Histórico de Consumo:**
• Compare consumo mensal dos últimos 12 meses
• Variações acima de 50% merecem investigação
• Picos podem indicar problema no medidor ou instalação

**⚖️ Base Legal:**
Resolução ANEEL 414/10 sobre condições gerais de fornecimento.

Está com problemas na sua conta de energia? Posso ajudar a analisar!"""
        
        if any(word in question_lower for word in ['interrupção', 'falta', 'corte', 'religação']):
            return """🔌 **Interrupções e Religação de Energia**

**Tipos de Interrupção:**

**Programadas (Manutenção):**
• **Aviso prévio**: Mínimo 3 dias de antecedência
• **Duração máxima**: 8 horas em área urbana, 16h rural
• **Horário**: Preferencialmente fora do horário de ponta
• **Compensação**: Não há, pois é programada

**Não Programadas (Emergência):**
• **Causas**: Tempestades, acidentes, falha de equipamentos
• **Prazo de religação**: Varia conforme área e causa
• **Compensação**: Direito se demora exceder prazos regulamentares

**Prazos Máximos para Religação:**
• **Área urbana**: 3 horas para defeito simples
• **Área rural**: 6 horas para defeito simples
• **Defeito complexo**: 18-24 horas conforme complexidade
• **Eventos climáticos**: Prazos estendidos conforme gravidade

**⚠️ Interrupção por Inadimplência:**
• **Prazo**: Após 15 dias do vencimento
• **Aviso**: Notificação prévia de 15 dias
• **Valor mínimo**: R$ 50 para corte (consumidor residencial)
• **Religação**: Até 24h após pagamento

**Situações que Impedem Corte:**
• **Sexta após 12h**: Só religará na segunda-feira
• **Feriados e vésperas**: Corte não permitido
• **Consumidor essencial**: Hospitais, bombeiros (prioridade)
• **Idosos/doentes**: Com comprovação médica

**🛡️ Seus Direitos:**
• Aviso prévio para manutenção programada
• Religação rápida após pagamento
• Compensação por demora na religação
• Prioridade para consumidores essenciais

**Compensação por Demora:**
• **Cálculo**: Proporcional ao tempo de interrupção
• **Automática**: Deve aparecer na próxima fatura
• **Valores**: Conforme tabela ANEEL
• **Solicitação**: Se não apareceu, solicite à distribuidora

**📞 Em Caso de Falta de Energia:**
• **Central de emergência**: 0800 da distribuidora
• **Protocolo**: Anote número da ocorrência
• **Acompanhamento**: Site/app da distribuidora mostra previsão
• **Reclamação**: ANEEL se demora for excessiva

**Religação de Urgência:**
• **Situações**: Doença grave, equipamento de suporte à vida
• **Documentação**: Atestado médico obrigatório
• **Prazo**: 4 horas após solicitação
• **Gratuidade**: Sem custo adicional se comprovada necessidade

**💡 Dicas Importantes:**
• Mantenha conta atualizada para evitar cortes
• Cadastre-se como consumidor de baixa renda se aplicável
• Tenha sempre protocolo de solicitações
• Fotografe medidor em caso de problemas

**⚖️ Regulamentação:**
Resolução ANEEL 414/10 sobre prazos e procedimentos de religação.

Está enfrentando cortes ou demoras na religação? Posso orientar seus direitos!"""
        
        if any(word in question_lower for word in ['medidor', 'leitura', 'consumo', 'estimativa']):
            return """📊 **Medição e Leitura de Consumo**

**Como Funciona a Medição:**
• **Leitura mensal**: Obrigatória todos os meses
• **Período**: 27 a 33 dias entre leituras
• **Horário**: Entre 6h e 18h em dias úteis
• **Registro**: kWh consumidos desde última leitura

**Tipos de Medidor:**
• **Eletromecânico**: Analógico com disco giratório
• **Eletrônico**: Digital com display LCD
• **Smart meter**: Medição remota (sendo implantado)
• **Pré-pago**: Pagamento antecipado (piloto em algumas áreas)

**Problemas na Leitura:**
• **Medidor inacessível**: Cliente deve facilitar acesso
• **Leitura não realizada**: Gera cobrança por estimativa
• **Erro de digitação**: Consumo muito diferente do habitual
• **Medidor defeituoso**: Registra consumo incorreto

**⚠️ Cobrança por Estimativa:**
• **Máximo**: 3 meses consecutivos por estimativa
• **Base**: Média dos últimos 12 meses
• **Acerto**: Na próxima leitura real
• **Direito**: Contestar se estimativa for abusiva

**Como Verificar Leitura:**
• **Anote**: Registre leitura mensalmente
• **Compare**: Com valor informado na conta
• **Teste**: Desligue tudo e veja se medidor para
• **Histórico**: Compare com meses anteriores

**🛡️ Seus Direitos:**
• Leitura real mensal obrigatória
• Acesso ao medidor facilitado pela distribuidora
• Contestar leitura obviamente incorreta
• Substituição de medidor defeituoso gratuita

**Medidor Defeituoso:**
• **Sintomas**: Consumo muito alto sem explicação
• **Teste**: Desligue todos os equipamentos
• **Solicitação**: Peça verificação à distribuidora
• **Prazo**: Análise em até 10 dias úteis
• **Custos**: Gratuito se confirmado defeito

**Troca de Medidor:**
• **Iniciativa da distribuidora**: Sem custo
• **Solicitação do cliente**: Pode ter custo
• **Medidor quebrado**: Substituição gratuita
• **Upgrade tecnológico**: Programa da distribuidora

**📋 Consumo Consciente:**
• **Horário de ponta**: 17h30-20h30 (tarifa mais cara)
• **Bandeiras vermelhas**: Reduzir uso não essencial
• **Equipamentos**: Verificar eficiência energética
• **Hábitos**: Desligar aparelhos em standby

**Auto-leitura:**
• **Como fazer**: Anote números do medidor no dia da leitura
• **Informar**: App ou site da distribuidora
• **Vantagem**: Evita cobrança por estimativa
• **Conferência**: Distribuidora fará leitura de conferência

**💡 Dica para Monitoramento:**
Anote leitura do medidor todo dia 1º do mês. Isso ajuda a identificar problemas rapidamente.

**⚖️ Regulamentação:**
Resolução ANEEL 414/10 sobre procedimentos de medição.

Está com dúvidas sobre sua leitura ou consumo? Posso ajudar a analisar!"""
        
        if any(word in question_lower for word in ['ligação', 'instalação', 'nova', 'transferência']):
            return """🔌 **Ligação Nova e Transferência**

**Ligação Nova de Energia:**

**Documentação Necessária:**
• **Pessoa física**: RG, CPF, comprovante de endereço
• **Pessoa jurídica**: CNPJ, contrato social, procuração
• **Propriedade**: Escritura, IPTU ou contrato de locação
• **Projeto elétrico**: Para cargas acima de 75kW

**Tipos de Ligação:**
• **Residencial**: Até 25kW (bifásica ou trifásica)
• **Comercial**: Pequeno porte até 75kW
• **Industrial**: Acima de 75kW (requer projeto)
• **Rural**: Condições especiais conforme localização

**Prazos para Ligação:**
• **Urbana consolidada**: Até 5 dias úteis
• **Urbana não consolidada**: Até 10 dias úteis
• **Rural**: Até 15 dias úteis
• **Extensão de rede**: Conforme complexidade da obra

**Custos da Ligação:**
• **Taxa de ligação**: Valor regulamentado pela ANEEL
• **Padrão de entrada**: Por conta do consumidor
• **Extensão de rede**: Gratuita até 30 metros
• **Acima de 30m**: Cliente paga excedente

**⚠️ Transferência de Titularidade:**

**Processo de Transferência:**
• **Solicitação**: Novo titular na distribuidora
• **Documentação**: RG, CPF, comprovante de endereço
• **Quitação**: Débitos devem estar em dia
• **Prazo**: Até 5 dias úteis para efetivação

**Situações Especiais:**
• **Óbito**: Herdeiros podem transferir com certidão
• **Separação**: Cônjuge pode assumir com comprovação
• **Venda**: Comprador deve fazer transferência imediata
• **Locação**: Inquilino pode solicitar transferência

**🛡️ Seus Direitos:**
• Ligação no prazo regulamentado
• Informação clara sobre custos
• Transferência sem burocracia excessiva
• Padrão técnico adequado da instalação

**Recusa de Ligação:**
• **Motivos válidos**: Documentação incompleta, débito pendente, local sem rede
• **Prazo**: Distribuidora deve informar motivo em 5 dias
• **Recurso**: Pode contestar na ANEEL se recusa for indevida
• **Correção**: Após correção, nova análise em 5 dias

**Extensão de Rede Elétrica:**
• **Direito**: Todo cidadão tem direito ao fornecimento
• **Gratuidade**: Até 30 metros da rede existente
• **Compartilhamento**: Custos divididos se múltiplos interessados
• **Prazo**: Conforme complexidade da obra

**Padrão de Entrada:**
• **Responsabilidade**: Do consumidor
• **Normas técnicas**: Conforme padrão da distribuidora
• **Inspeção**: Distribuidora verifica antes da ligação
• **Adequação**: Deve seguir normas de segurança

**💰 Financiamento:**
• **Programa Luz para Todos**: Para áreas rurais de baixa renda
• **Parcelamento**: Custos podem ser parcelados
• **Subsídios**: Para consumidores de baixa renda
• **Cooperativas**: Alternativa em áreas rurais

**📋 Dicas Importantes:**
• Contrate eletricista qualificado para padrão de entrada
• Guarde todos os protocolos de solicitação
• Faça transferência imediatamente ao mudar/comprar imóvel
• Verifique se local tem rede elétrica antes de construir

**⚖️ Regulamentação:**
Resolução ANEEL 414/10 sobre condições de fornecimento.

Precisa fazer ligação nova ou transferência? Posso orientar sobre o processo!"""
        
        if any(word in question_lower for word in ['qualidade', 'problema', 'oscilação', 'tensão']):
            return """⚡ **Qualidade da Energia Elétrica**

**Parâmetros de Qualidade:**

**Tensão Elétrica:**
• **Residencial**: 220V (±5%) ou 127V (±5%)
• **Trifásica**: 380V ou 220V conforme região
• **Variação permitida**: ±5% em condições normais
• **Variação crítica**: ±10% (direito a reclamação)

**Frequência:**
• **Padrão**: 60 Hz
• **Variação permitida**: ±0,5 Hz
• **Monitoramento**: Contínuo pela distribuidora

**Problemas Comuns:**

**Oscilação de Tensão:**
• **Sintomas**: Lâmpadas piscando, equipamentos desligando
• **Causas**: Sobrecarga na rede, problemas no transformador
• **Riscos**: Danos em equipamentos eletrônicos
• **Medição**: Solicitar análise técnica à distribuidora

**Subtensão (Tensão Baixa):**
• **Sintomas**: Equipamentos com baixo desempenho
• **Causas**: Rede inadequada, excesso de consumo
• **Efeitos**: Motores queimam, lâmpadas fracas
• **Solução**: Adequação da rede pela distribuidora

**Sobretensão (Tensão Alta):**
• **Sintomas**: Equipamentos queimando, fusíveis estourando
• **Causas**: Desbalanceamento da rede, problemas no transformador
• **Riscos**: Danos graves em equipamentos
• **Urgência**: Solicitar verificação imediata

**🛡️ Seus Direitos:**
• Energia dentro dos padrões técnicos
• Análise gratuita da qualidade
• Compensação por danos causados por má qualidade
• Adequação da rede sem custo (se problema for da distribuidora)

**Como Solicitar Análise:**
• **Protocolo**: Registrar reclamação na distribuidora
• **Prazo**: Análise em até 10 dias úteis
• **Medição**: Equipamento instalado por 7 dias
• **Laudo**: Resultado técnico da qualidade

**Compensação por Danos:**
• **Direito**: Se comprovada má qualidade da energia
• **Documentação**: Nota fiscal dos equipamentos, laudo técnico
• **Prazo**: Até 120 dias para análise do pedido
• **Valor**: Conforme avaliação dos danos

**⚠️ Situações de Risco:**
• **Fios desencapados**: Perigo de choque elétrico
• **Transformador sobrecarregado**: Oscilações constantes
• **Rede antiga**: Inadequada para consumo atual
• **Conexões irregulares**: "Gatos" prejudicam qualidade

**Proteção de Equipamentos:**
• **Protetor de surto**: Para equipamentos sensíveis
• **Estabilizador**: Para variações pequenas de tensão
• **Nobreak**: Para equipamentos críticos
• **DPS**: Proteção contra descargas atmosféricas

**Medição da Qualidade:**
• **Multímetro**: Para verificações básicas
• **Analisador**: Equipamento profissional (distribuidora)
• **Monitoramento**: 7 dias contínuos para diagnóstico
• **Relatório**: Laudo técnico da qualidade medida

**💡 Sinais de Problema:**
• Equipamentos eletrônicos queimando frequentemente
• Lâmpadas com brilho irregular
• Chuveiro elétrico com baixo desempenho
• Computadores desligando sozinhos

**📞 Emergência Elétrica:**
• **Fios soltos**: Ligue imediatamente para distribuidora
• **Cheiro de queimado**: Desligue energia e chame técnico
• **Choque elétrico**: Verificar instalação interna
• **Faíscos**: Problema grave, solicitar vistoria urgente

**⚖️ Base Legal:**
Módulo 8 dos Procedimentos de Distribuição (PRODIST) da ANEEL.

Está com problemas na qualidade da energia? Posso orientar sobre medições e direitos!"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""⚡ **Análise do Contrato de Fornecimento de Energia**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Modalidade Tarifária:**
• Tipo de tarifa aplicável (convencional, branca, etc.)
• Horários de ponta e fora ponta
• Aplicação de bandeiras tarifárias
• Classificação do consumidor

**2. Condições de Fornecimento:**
• Padrões de qualidade da energia
• Prazos para ligação e religação
• Procedimentos para leitura
• Direitos em caso de interrupção

**3. Faturamento:**
• Composição da conta de energia
• Tributos e taxas aplicáveis
• Prazos de pagamento
• Condições para parcelamento

**4. Direitos e Deveres:**
• Responsabilidades do consumidor
• Obrigações da distribuidora
• Procedimentos para reclamações
• Condições para transferência

**⚖️ Conformidade Legal:**
Este contrato deve seguir regulamentação da ANEEL e CDC.

Posso analisar algum aspecto específico que está gerando dúvida?"""
        
        # Resposta geral
        return """⚡ **Energia Elétrica - Orientação Geral**

Entendi sua pergunta sobre energia elétrica. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de conta e tarifas aplicadas
• Análise de problemas de qualidade da energia
• Orientação sobre ligação nova e transferência
• Direitos em caso de interrupções

**⚠️ Problemas Mais Comuns:**
• Cobrança por estimativa excessiva
• Oscilações e problemas na qualidade
• Demoras na religação após pagamento
• Dificuldades em ligações novas

**🛡️ Seus Direitos Principais:**
• Energia com qualidade adequada
• Leitura mensal obrigatória
• Religação no prazo após pagamento
• Informação clara sobre tarifas

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça detalhes do contrato."""