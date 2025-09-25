from app.agents.base_agent import BaseContractAgent

class EmploymentCLTAgent(BaseContractAgent):
    """Agente especializado em contratos de trabalho CLT"""
    
    def __init__(self):
        self.specialization = "Contrato CLT"
        self.icon = "👷"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para contratos CLT"""
        
        if not question:
            return """👷 **Contrato de Trabalho CLT - Análise Especializada**

Olá! Sou especialista em contratos de trabalho CLT. Posso ajudar com:

**📋 Principais Análises:**
• Salário, benefícios e adicionais
• Jornada de trabalho e horas extras
• Férias, 13º salário e FGTS
• Cláusulas abusivas e ilegalidades
• Direitos trabalhistas garantidos

**⚠️ Pontos Críticos:**
• Jornada máxima (44h semanais/8h diárias)
• Banco de horas e compensação
• Cláusulas que violem direitos mínimos
• Períodos de experiência (máx. 90 dias)

**📞 Órgãos de Proteção:**
• Ministério do Trabalho e Emprego
• Superintendência Regional do Trabalho
• Justiça do Trabalho
• Sindicatos da categoria

Como posso ajudar com seu contrato de trabalho?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['salário', 'remuneração', 'vencimento', 'pagamento']):
            return """💰 **Salário e Remuneração CLT**

**Componentes da Remuneração:**
• **Salário base**: Valor fixo mensal
• **Adicionais**: Horas extras, noturno, insalubridade, periculosidade
• **Comissões**: Se previsto no contrato
• **Gratificações**: Bonificações variáveis

**Regras Salariais:**
• Não pode ser inferior ao salário mínimo nacional
• Respeitar piso salarial da categoria (se houver)
• Pagamento até o 5º dia útil do mês seguinte
• Desconto máximo de 70% para pensão alimentícia

**Adicionais Obrigatórios:**
• **Hora extra**: Mín. 50% sobre valor normal (até 2h/dia)
• **Adicional noturno**: Mín. 20% (22h às 5h)
• **Insalubridade**: 10%, 20% ou 40% do salário mínimo
• **Periculosidade**: 30% do salário base

**⚠️ Cláusulas Proibidas:**
• Redução salarial (exceto acordo/convenção)
• Pagamento em utilidades acima de 70%
• Desconto sem autorização legal/expressa
• Salário abaixo do mínimo legal

**🛡️ Base Legal:**
Arts. 457 a 467 da CLT e CF/88, Art. 7º.

Tem dúvidas sobre algum componente salarial específico?"""
        
        if any(word in question_lower for word in ['jornada', 'horário', 'horas', 'extra', 'banco']):
            return """⏰ **Jornada de Trabalho e Horas Extras**

**Limites de Jornada:**
• **Diária**: Máximo 8 horas normais + 2 horas extras
• **Semanal**: Máximo 44 horas normais + extras
• **Intervalo**: Mínimo 15min (até 4h) ou 1h (acima de 6h)
• **Descanso semanal**: 24h consecutivas (preferencialmente domingo)

**Tipos de Jornada:**
• **Padrão**: 8h/dia, 44h/semana
• **12x36**: 12h trabalhadas, 36h descanso
• **Turno de revezamento**: 6h contínuas
• **Horário flexível**: Com acordo/convenção

**Horas Extras:**
• Remuneração mínima: 50% sobre hora normal
• Limite: 2 horas por dia
• Base de cálculo: salário + adicionais fixos
• Reflexos: férias, 13º, FGTS, INSS

**Banco de Horas:**
• Acordo individual ou coletivo obrigatório
• Compensação no prazo máximo de 1 ano
• Proporção 1:1 (1 hora extra = 1 hora folga)
• Se não compensar, pagar como extra

**⚠️ Violações Comuns:**
• Jornada superior a 10h/dia sem autorização
• Não pagamento de horas extras
• Supressão irregular do intervalo
• Banco de horas sem acordo formal

**🛡️ Base Legal:**
Arts. 58 a 75 da CLT e Lei nº 13.467/2017.

Precisa esclarecer algo sobre sua jornada de trabalho?"""
        
        if any(word in question_lower for word in ['férias', 'descanso', '13', 'décimo', 'fgts']):
            return """🏖️ **Férias, 13º Salário e FGTS**

**Férias Anuais:**
• **Período**: 30 dias corridos por ano
• **Aquisição**: Após 12 meses de trabalho
• **Pagamento**: Até 2 dias antes do início
• **1/3 constitucional**: Adicional obrigatório
• **Venda**: Máximo 1/3 das férias (10 dias)

**Fracionamento de Férias:**
• Acordo entre empregado e empregador
• Máximo 3 períodos
• Um período mínimo de 14 dias
• Demais não inferiores a 5 dias

**13º Salário:**
• **Valor**: 1/12 da remuneração por mês trabalhado
• **1ª parcela**: Entre fev. e nov. (até 50%)
• **2ª parcela**: Até 20 de dezembro
• **Base**: Salário de dezembro ou rescisão

**FGTS (Fundo de Garantia):**
• **Percentual**: 8% sobre remuneração mensal
• **Depósito**: Até dia 7 do mês seguinte
• **Multa rescisória**: 40% em demissão sem justa causa
• **Saque**: Demissão, aposentadoria, doenças graves, etc.

**⚠️ Direitos Irrenunciáveis:**
• Todos são direitos constitucionais
• Não podem ser negociados para menor
• Cláusula contrária é nula

**🛡️ Base Legal:**
Arts. 129-153 da CLT (férias), Lei nº 4.090/62 (13º) e Lei nº 8.036/90 (FGTS).

Tem dúvidas sobre cálculo ou pagamento desses direitos?"""
        
        if any(word in question_lower for word in ['demissão', 'rescisão', 'demitir', 'justa causa', 'aviso']):
            return """📋 **Demissão e Rescisão de Contrato**

**Tipos de Rescisão:**

**1. Por Iniciativa do Empregador:**
• **Sem justa causa**: Aviso prévio + multa FGTS 40%
• **Com justa causa**: Sem aviso prévio nem multa

**2. Por Iniciativa do Empregado:**
• **Pedido de demissão**: Dar aviso prévio
• **Rescisão indireta**: Por falta grave do empregador

**3. Outras Formas:**
• **Acordo mútuo**: Metade do aviso + 20% FGTS
• **Término do contrato**: Se por prazo determinado

**Verbas Rescisórias:**

**Demissão sem justa causa:**
• Saldo de salário + férias + 1/3 + 13º proporcional
• Aviso prévio (30 dias + 3 dias por ano)
• FGTS + multa de 40%
• Seguro-desemprego (se aplicável)

**Pedido de demissão:**
• Saldo + férias + 1/3 + 13º proporcional
• FGTS (sem multa)
• Dar aviso prévio de 30 dias

**⚠️ Causas de Justa Causa (Art. 482 CLT):**
• Ato de improbidade
• Incontinência ou mau procedimento
• Negociação habitual (concorrência)
• Condenação criminal com trânsito em julgado
• Desídia (negligência) no trabalho
• Embriaguez habitual ou em serviço

**🕒 Prazos Importantes:**
• Pagamento das verbas: Até 10 dias da rescisão
• Entrega da CTPS: Até 48h
• Chaves de FGTS: Imediato

**🛡️ Base Legal:**
Arts. 477-486 da CLT e Lei nº 13.467/2017.

Está enfrentando alguma situação de demissão específica?"""
        
        if any(word in question_lower for word in ['experiência', 'período', 'teste', 'probatório']):
            return """🧪 **Período de Experiência**

**Características do Contrato de Experiência:**
• **Finalidade**: Testar aptidão e adaptação mútua
• **Duração máxima**: 90 dias (não renovável)
• **Forma**: Deve ser por escrito
• **Prorrogação**: Uma única vez, dentro dos 90 dias

**Estrutura do Prazo:**
• **Exemplo**: 45 dias + 45 dias
• **Ou**: 30 dias + 60 dias  
• **Limite**: Soma não pode exceder 90 dias
• **Renovação**: Só uma vez durante o período

**Direitos Durante a Experiência:**
• Todos os direitos trabalhistas normais
• Salário igual ou superior ao mínimo
• Registro em CTPS
• FGTS, INSS, férias e 13º proporcionais
• Adicional noturno, horas extras (se aplicáveis)

**Rescisão no Período de Experiência:**

**Por iniciativa do empregador:**
• Sem aviso prévio (se antes do fim)
• Verbas proporcionais
• Sem multa de 40% do FGTS

**Por iniciativa do empregado:**
• Sem aviso prévio
• Verbas proporcionais
• Sem direito ao seguro-desemprego

**⚠️ Cuidados Importantes:**
• Após 90 dias, vira contrato indeterminado
• Sucessivos contratos de experiência são proibidos
• Não pode ser usado para funções temporárias
• Deve haver real período de teste/aprendizado

**🛡️ Base Legal:**
Art. 443, §2º da CLT e Súmula 188 do TST.

Tem dúvidas sobre seu período de experiência?"""
        
        if any(word in question_lower for word in ['benefício', 'vale', 'auxílio', 'plano', 'convênio']):
            return """🎁 **Benefícios e Auxílios Trabalhistas**

**Benefícios Obrigatórios:**
• **Vale-transporte**: Desconto máx. 6% do salário
• **Auxílio-alimentação**: Se previsto em acordo/convenção
• **Salário-família**: Para baixa renda (automático)
• **Equipamentos de segurança**: EPI gratuito

**Benefícios Facultativos Comuns:**
• **Vale-refeição/alimentação**: Integra salário se habitual
• **Plano de saúde**: Empresarial ou familiar
• **Seguro de vida**: Individual ou em grupo
• **Participação nos lucros**: Se houver programa

**Regras dos Vales:**
• **Transporte**: Obrigatório se distância casa-trabalho
• **Refeição**: Não integra salário se em PAT
• **Alimentação**: Pode integrar salário se habitual
• **Combustível**: Geralmente integra remuneração

**Programa de Alimentação do Trabalhador (PAT):**
• Incentivo fiscal para empresas
• Vale não integra salário (se dentro do programa)
• Desconto máximo de 20% sobre vale fornecido
• Regulamentação específica do Ministério do Trabalho

**⚠️ Pontos de Atenção:**
• Benefício habitual integra salário para todos os fins
• Supressão pode gerar direito adquirido
• Deve estar claro se integra ou não a remuneração
• Convenção coletiva pode tornar obrigatório

**Plano de Saúde Empresarial:**
• Pode ser obrigatório por convenção
• Empregado pode contribuir parcialmente
• Direito de manter após rescisão (lei 9.656/98)
• Dependentes podem ser incluídos

**🛡️ Integração Salarial:**
Súmula 241 do TST - benefício habitual integra salário.

**💡 Dica:**
Verifique na convenção coletiva quais benefícios são obrigatórios na sua categoria.

Tem dúvidas sobre algum benefício específico?"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""👷 **Análise do Contrato de Trabalho CLT**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar em contratos CLT:**

**1. Dados Básicos:**
• Qualificação completa das partes
• Função/cargo específico
• Local de trabalho
• Data de início

**2. Remuneração:**
• Salário base (não inferior ao mínimo)
• Adicionais (horas extras, noturno, etc.)
• Benefícios e suas integrações
• Forma e data de pagamento

**3. Jornada de Trabalho:**
• Horário de trabalho
• Intervalos obrigatórios
• Banco de horas (se aplicável)
• Trabalho aos domingos/feriados

**4. Período de Experiência:**
• Duração (máx. 90 dias)
• Possibilidade de prorrogação
• Condições específicas

**5. Cláusulas Especiais:**
• Cláusula de não concorrência
• Confidencialidade
• Participação nos lucros
• Plano de carreira

**6. Direitos e Deveres:**
• Férias e 13º salário
• FGTS e benefícios
• Obrigações do empregado
• Equipamentos de trabalho

**⚖️ Conformidade Legal:**
Este contrato deve seguir a CLT, CF/88 e convenção coletiva da categoria.

Posso analisar algum ponto específico que está causando dúvida?"""
        
        # Resposta geral
        return """👷 **Contrato de Trabalho CLT - Orientação Geral**

Entendi sua pergunta sobre contrato de trabalho. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de salário e benefícios
• Análise de jornada e horas extras
• Orientação sobre direitos trabalhistas
• Identificação de cláusulas irregulares

**⚠️ Problemas Mais Comuns:**
• Salário abaixo do mínimo legal
• Jornada excessiva sem pagamento de extras
• Supressão de intervalos obrigatórios
• Cláusulas que violem direitos mínimos

**🛡️ Direitos Fundamentais CLT:**
• Salário mínimo e 13º salário
• Férias remuneradas + 1/3 constitucional
• FGTS e seguro-desemprego
• Limitação da jornada de trabalho
• Equipamentos de segurança gratuitos

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça o texto do contrato."""