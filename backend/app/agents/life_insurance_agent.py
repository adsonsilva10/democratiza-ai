from app.agents.base_agent import BaseContractAgent

class LifeInsuranceAgent(BaseContractAgent):
    """Agente especializado em seguros de vida"""
    
    def __init__(self):
        self.specialization = "Seguro de Vida"
        self.icon = "🛡️"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para seguros de vida"""
        
        if not question:
            return """🛡️ **Seguro de Vida - Análise Especializada**

Olá! Sou especialista em seguros de vida. Posso ajudar com:

**📋 Principais Análises:**
• Coberturas básicas e adicionais
• Capital segurado e beneficiários
• Carência e exclusões de cobertura
• Prêmio e forma de pagamento
• Resgate e portabilidade

**⚠️ Pontos Críticos:**
• Declarações de saúde incorretas
• Carência excessiva para algumas coberturas
• Exclusões não informadas claramente
• Cláusulas abusivas de cancelamento

**📞 Órgãos de Defesa:**
• SUSEP - Superintendência de Seguros Privados
• PROCON - Defesa do consumidor
• CNseg - Confederação Nacional das Seguradoras

Como posso ajudar com seu seguro de vida?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['cobertura', 'cobrir', 'proteção', 'benefício']):
            return """🛡️ **Coberturas do Seguro de Vida**

**Cobertura Básica (Morte):**
• **Morte natural**: Por doença ou causas naturais
• **Morte acidental**: Por acidentes pessoais
• **Capital segurado**: Valor pago aos beneficiários
• **Vigência**: 24 horas por dia, mundial

**Coberturas Adicionais Comuns:**
• **IPA (Invalidez Permanente por Acidente)**: 25% a 100% do capital
• **IPD (Invalidez Permanente por Doença)**: Para doenças graves
• **Diárias de Incapacidade**: Renda durante afastamento
• **Auxílio Funeral**: Cobertura para despesas funerárias
• **Doenças Graves**: Antecipação do capital para tratamento

**Coberturas Especiais:**
• **Morte por doença**: Algumas apólices excluem nos primeiros anos
• **Suicídio**: Coberto após 2 anos de vigência (CDC)
• **Acidentes de trabalho**: Geralmente incluído
• **Atos de terceiros**: Homicídio, latrocínio, etc.

**⚠️ Principais Exclusões:**
• **Atos dolosos**: Suicídio nos primeiros 2 anos
• **Guerra**: Conflitos armados declarados
• **Atos ilícitos**: Crimes cometidos pelo segurado
• **Esportes radicais**: Podem ser excluídos ou ter adicional
• **Uso de drogas/álcool**: Em situações de risco

**Invalidez Permanente:**
• **Total**: 100% do capital segurado
• **Parcial**: Tabela de percentuais por membro/função
• **Critérios**: Deve ser comprovada por junta médica
• **Prazo**: Geralmente até 2 anos após acidente

**🛡️ Seus Direitos:**
• Cobertura conforme especificada na apólice
• Pagamento do sinistro em até 30 dias após documentação
• Informação clara sobre exclusões
• Contestar negativas indevidas de cobertura

**📋 Documentação para Sinistro:**
• **Morte**: Certidão de óbito, laudo médico
• **Invalidez**: Laudos médicos, exames complementares
• **Doença grave**: Relatórios médicos detalhados
• **Acidente**: Boletim de ocorrência, laudos

**💡 Dica Importante:**
Leia SEMPRE as condições gerais da apólice - é lá que estão detalhadas todas as coberturas e exclusões.

**🚨 Contestação de Negativa:**
Se seguradora negar sinistro indevidamente, você pode contestar via SUSEP ou buscar orientação jurídica.

Precisa de esclarecimento sobre alguma cobertura específica?"""
        
        if any(word in question_lower for word in ['beneficiário', 'herança', 'família', 'dependente']):
            return """👨‍👩‍👧‍👦 **Beneficiários do Seguro de Vida**

**Quem Pode Ser Beneficiário:**
• **Pessoas físicas**: Familiares, amigos, qualquer pessoa
• **Pessoas jurídicas**: Empresas, instituições, ONGs
• **Herdeiros legais**: Se não houver indicação específica
• **Múltiplos beneficiários**: Com percentual definido para cada um

**Tipos de Indicação:**
• **Nominalmente**: Nome completo, CPF, parentesco
• **Por classe**: "Cônjuge e filhos em partes iguais"
• **Subsidiária**: Beneficiário reserva se principal falecer antes
• **Sucessiva**: Ordem de preferência entre beneficiários

**Direitos dos Beneficiários:**
• **Recebimento integral**: Valor não entra em inventário
• **Impenhorabilidade**: Não pode ser penhorado por dívidas
• **Isenção de IR**: Valores recebidos são livres de imposto
• **Rapidez**: Pagamento independe de inventário/partilha

**⚠️ Alteração de Beneficiários:**
• **Direito do segurado**: Pode alterar a qualquer momento
• **Processo**: Comunicar seguradora por escrito
• **Cônjuge**: Tem direito a 50% se casado no regime de comunhão
• **Companheiro(a)**: União estável também garante direitos

**Beneficiário Menor de Idade:**
• **Representante legal**: Pais ou tutores recebem
• **Curatela**: Pode ser necessária para valores altos
• **Prestação de contas**: Uso do dinheiro deve ser comprovado
• **Aplicação**: Valores geralmente devem ser investidos

**🛡️ Proteção Patrimonial:**
• **Não integra herança**: Não precisa partilhar com outros herdeiros
• **Credores**: Não podem executar o seguro por dívidas do segurado
• **Separação**: Ex-cônjuge perde direito se não for beneficiário
• **Sucessão**: Planejamento sucessório facilitado

**Casos Especiais:**
• **Sem beneficiário indicado**: Segue ordem legal (cônjuge, filhos, pais)
• **Beneficiário falecido**: Direito passa aos herdeiros dele ou subsidiários
• **Divórcio**: Ex-cônjuge perde direito automático, mas pode continuar se indicado
• **Separação de fato**: Não altera automaticamente beneficiários

**📋 Documentação Necessária:**
• **Para alteração**: Solicitação por escrito + documentos do segurado
• **Para sinistro**: Documentos do beneficiário + certidão de óbito
• **Menor de idade**: Documentos do representante legal
• **Procuração**: Se beneficiário não puder comparecer

**💡 Planejamento Familiar:**
Seguro de vida é excelente ferramenta de planejamento sucessório - não entra em inventário e tem baixo custo.

**⚖️ Aspecto Legal:**
Código Civil garante livre escolha de beneficiários, exceto legítima do cônjuge em alguns casos.

**🚨 Dica Importante:**
Mantenha sempre atualizada a indicação de beneficiários, especialmente após mudanças familiares (casamento, nascimento, divórcio).

Precisa de orientação sobre como indicar ou alterar beneficiários?"""
        
        if any(word in question_lower for word in ['prêmio', 'pagamento', 'valor', 'custo']):
            return """💰 **Prêmio e Pagamento do Seguro**

**Como é Calculado o Prêmio:**
• **Idade**: Fator principal - quanto maior, mais caro
• **Sexo**: Mulheres geralmente pagam menos (maior expectativa de vida)
• **Profissão**: Atividades de risco aumentam valor
• **Capital segurado**: Quanto maior proteção, maior prêmio
• **Coberturas adicionais**: Cada cobertura tem custo extra

**Modalidades de Pagamento:**
• **Mensal**: Mais comum, pode ter IOF
• **Anual**: Geralmente com desconto (5-10%)
• **Semestral**: Opção intermediária
• **Prêmio único**: Pagamento único na contratação

**Formas de Pagamento:**
• **Débito automático**: Mais prático, evita esquecimento
• **Boleto bancário**: Tradicional, vence todo mês
• **Cartão de crédito**: Facilita controle, pode parcelar
• **Desconto em folha**: Para seguros empresariais

**⚠️ Reajustes do Prêmio:**
• **Anual**: Conforme idade ou índice contratual
• **Mudança de faixa etária**: Aumento automático por idade
• **Inflação**: Reajuste por índices econômicos (IGP-M, IPCA)
• **Sinistralidade**: Aumento geral se muitos sinistros no grupo

**Inadimplência e Consequências:**
• **Prazo de tolerância**: 30 dias após vencimento
• **Suspensão da cobertura**: Após período de tolerância
• **Reativação**: Possível mediante pagamento e reanálise
• **Carência**: Pode ser aplicada novamente na reativação

**🛡️ Seus Direitos:**
• Informação clara sobre cálculo do prêmio
• Aviso prévio sobre reajustes (30 dias)
• Período de tolerância para pagamento
• Possibilidade de reativação da apólice

**Desconto no Prêmio:**
• **Não fumante**: 10% a 30% de desconto
• **Boa saúde**: Exames médicos podem gerar desconto
• **Grupo familiar**: Seguro para família toda
• **Profissão**: Atividades de baixo risco pagam menos
• **Pagamento anual**: Desconto por pagamento à vista

**Seguro Empresarial:**
• **Desconto em folha**: Facilitação para pagamento
• **Grupo**: Preços menores por diluição de risco
• **Adesão**: Processo simplificado
• **Cobertura**: Pode ser básica ou personalizável

**💡 Dicas para Economizar:**
• Compare preços entre seguradoras
• Avalie necessidade real do capital segurado
• Considere pagamento anual para ter desconto
• Mantenha hábitos saudáveis (não fumar)
• Revise periodicamente se valor ainda adequado

**📊 Planejamento do Orçamento:**
• **Regra geral**: Prêmio não deve superar 5-10% da renda
• **Prioridade**: Primeiro segure chefe de família
• **Capital**: 5 a 10 vezes a renda anual é boa referência
• **Revisão**: Anual, conforme mudanças de vida

**⚖️ Regulamentação:**
SUSEP regula reajustes e condições de pagamento do seguro de vida.

**🚨 Atraso no Pagamento:**
Não deixe o seguro vencer! Reativação pode exigir nova análise de saúde e carência.

Precisa de ajuda para calcular o valor ideal do seu seguro?"""
        
        if any(word in question_lower for word in ['carência', 'prazo', 'cobertura', 'quando']):
            return """⏰ **Carência do Seguro de Vida**

**O que é Carência:**
• **Período de espera**: Tempo entre contratação e cobertura efetiva
• **Objetivo**: Evitar contratação com conhecimento de risco iminente
• **Variação**: Diferente para cada tipo de cobertura
• **Obrigatoriedade**: Definida pela seguradora conforme SUSEP

**Carências Típicas por Cobertura:**

**Morte Natural:**
• **Padrão**: 24 meses para morte por doença
• **Acidente**: Sem carência (cobertura imediata)
• **Suicídio**: 24 meses obrigatórios por lei
• **Reduzida**: Algumas seguradoras oferecem carência menor

**Invalidez:**
• **Por acidente**: Sem carência (imediata)
• **Por doença**: 24 meses é comum
• **Doenças preexistentes**: Podem ter carência maior ou exclusão
• **Degenerativas**: Alzheimer, Parkinson - carência especial

**Doenças Graves:**
• **Câncer**: 90 a 180 dias
• **Infarto**: 90 a 180 dias  
• **AVC**: 90 a 180 dias
• **Outras**: Conforme especificação da apólice

**⚠️ Situações Sem Carência:**
• **Morte por acidente**: Cobertura imediata 24h após contratação
• **Acidentes de trânsito**: Sem período de espera
• **Morte por terceiros**: Homicídio, latrocínio
• **Acidentes de trabalho**: Cobertura imediata

**Carência Reduzida:**
• **Exames médicos**: Podem reduzir ou eliminar carência
• **Declaração de saúde completa**: Carência menor
• **Seguros empresariais**: Frequentemente sem carência
• **Portabilidade**: Carência pode ser aproveitada do seguro anterior

**🛡️ Seus Direitos:**
• Informação clara sobre todas as carências
• Cobertura imediata para morte por acidente
• Carência limitada conforme regulamentação
• Aproveitamento de carências em portabilidade

**Redução da Carência:**
• **Exame médico**: Check-up completo pode eliminar carência
• **Idade**: Pessoas mais novas podem ter carência reduzida
• **Histórico**: Clientes antigos da seguradora
• **Negociação**: Algumas seguradoras são flexíveis

**⚖️ Aspectos Legais:**
• **Suicídio**: 2 anos obrigatórios por lei (CDC)
• **Doenças preexistentes**: Não podem ser cobertas se não declaradas
• **Má-fé**: Omissão de doença pode anular seguro
• **Boa-fé**: Declaração correta garante cobertura

**💡 Dicas Importantes:**
• Leia atentamente todas as carências na apólice
• Declare SEMPRE problemas de saúde corretamente
• Considere fazer exames médicos para reduzir carência
• Mantenha documentação médica atualizada

**📋 Documentação da Saúde:**
• **Declaração**: Seja sempre verdadeiro
• **Exames**: Guarde resultados atualizados
• **Tratamentos**: Informe medicamentos contínuos
• **Histórico familiar**: Pode influenciar na avaliação

**🚨 Cuidado com Omissões:**
Omitir doença preexistente pode anular completamente o seguro, mesmo após anos de pagamento!

Tem dúvidas sobre carências no seu seguro específico?"""
        
        if any(word in question_lower for word in ['resgate', 'cancelar', 'sair', 'devolver']):
            return """💵 **Resgate e Cancelamento do Seguro**

**Tipos de Seguro e Resgate:**

**Seguro de Vida Tradicional (Risco):**
• **Sem valor de resgate**: Puro seguro, não acumula reserva
• **Cancelamento**: Não há devolução de prêmios pagos
• **Funcionamento**: Como seguro de carro - paga só se acontecer sinistro
• **Vantagem**: Prêmios mais baixos, proteção máxima

**Seguro de Vida com Resgate (VGBL/PGBL):**
• **Acumulação**: Parte do prêmio vai para reserva matemática
• **Resgate**: Possível retirar valor acumulado
• **Rentabilidade**: Conforme aplicação escolhida
• **Tributação**: Diferentes regimes (progressivo/regressivo)

**⚠️ Cancelamento do Seguro Tradicional:**
• **Direito garantido**: Pode cancelar quando quiser
• **Sem reembolso**: Prêmios pagos não são devolvidos
• **Aviso prévio**: Não obrigatório, mas recomendado
• **Efeitos**: Cobertura cessa imediatamente

**Processo de Cancelamento:**
• **Comunicação**: Por escrito à seguradora
• **Protocolo**: Solicitar comprovante do cancelamento
• **Última parcela**: Proporcional ao período de cobertura
• **Beneficiários**: Avisar sobre cancelamento

**Resgate em Seguros com Acumulação:**
• **Parcial**: Retirar parte da reserva, manter seguro ativo
• **Total**: Encerrar seguro e resgatar todo valor acumulado
• **Prazo**: Até 30 dias para crédito após solicitação
• **Tributação**: Conforme tabela regressiva ou progressiva

**🛡️ Seus Direitos:**
• Cancelar seguro quando desejar
• Informação clara sobre valores de resgate
• Resgate em até 30 dias (seguros com acumulação)
• Portabilidade para outra seguradora

**Portabilidade de Seguro:**
• **Para outra seguradora**: Manter condições e carências
• **Sem custos**: Transferência gratuita
• **Requisitos**: Estar em dia com pagamentos
• **Prazo**: Processo em até 15 dias

**Quando Vale a Pena Cancelar:**
• **Mudança de situação financeira**: Não consegue mais pagar
• **Cobertura inadequada**: Não atende mais necessidades
• **Seguro melhor**: Encontrou opção com melhor custo-benefício
• **Sem mais dependentes**: Não há quem proteger

**💡 Alternativas ao Cancelamento:**
• **Redução do capital**: Diminuir cobertura e prêmio
• **Suspensão temporária**: Algumas seguradoras permitem
• **Portabilidade**: Migrar para seguradora com condições melhores
• **Renegociação**: Discutir novas condições de pagamento

**Impactos do Cancelamento:**
• **Proteção familiar**: Família fica desprotegida
• **Idade**: Novo seguro será mais caro por estar mais velho
• **Saúde**: Problemas desenvolvidos impedem novo seguro
• **Carência**: Novo seguro terá carências novamente

**📊 Análise Antes de Cancelar:**
• Compare custo vs. benefício atual
• Considere dificuldade de fazer novo seguro
• Avalie se há alternativas mais baratas
• Pense no impacto para a família

**⚖️ Base Legal:**
CDC garante direito de cancelamento e resgate conforme condições contratuais.

**🚨 Importante:**
Antes de cancelar, certifique-se de que conseguirá fazer novo seguro se necessário - idade e saúde podem ser impeditivos!

Está considerando cancelar seu seguro? Posso ajudar a avaliar alternativas!"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""🛡️ **Análise da Apólice de Seguro de Vida**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Coberturas:**
• Morte natural e por acidente
• Invalidez permanente (parcial/total)
• Doenças graves cobertas
• Auxílio funeral e outras coberturas

**2. Capital Segurado:**
• Valor da cobertura principal
• Valores das coberturas adicionais
• Adequação às necessidades familiares
• Atualização monetária

**3. Carências e Exclusões:**
• Prazos de carência por tipo de cobertura
• Exclusões específicas da apólice
• Condições para doenças preexistentes
• Situações não cobertas

**4. Beneficiários:**
• Indicação de beneficiários
• Percentuais de participação
• Direitos sucessórios
• Procedimentos para alteração

**5. Condições Financeiras:**
• Valor do prêmio e reajustes
• Formas e prazos de pagamento
• Condições de resgate (se aplicável)
• Consequências da inadimplência

**⚖️ Conformidade Legal:**
Esta apólice deve seguir regulamentação da SUSEP e CDC.

Posso analisar algum aspecto específico que está causando dúvida?"""
        
        # Resposta geral
        return """🛡️ **Seguro de Vida - Orientação Geral**

Entendi sua pergunta sobre seguro de vida. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de coberturas e exclusões
• Análise de carências e condições
• Orientação sobre beneficiários e sucessão
• Avaliação de custos e valor do prêmio

**⚠️ Problemas Mais Comuns:**
• Carências excessivas não informadas
• Exclusões não explicadas claramente
• Dificuldades no pagamento de sinistros
• Problemas com declaração de saúde

**🛡️ Seus Direitos Principais:**
• Cobertura conforme especificada na apólice
• Informação clara sobre carências e exclusões
• Pagamento de sinistros no prazo legal
• Livre escolha de beneficiários

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça o texto da apólice."""