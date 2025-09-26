from app.agents.base_agent import BaseContractAgent

class VehicleFinancingAgent(BaseContractAgent):
    """Agente especializado em financiamento de veículos"""
    
    def __init__(self):
        self.specialization = "Financiamento Veicular"
        self.icon = "🚗"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para financiamento de veículos"""
        
        if not question:
            return """🚗 **Financiamento Veicular - Análise Especializada**

Olá! Sou especialista em financiamento de veículos. Posso ajudar com:

**📋 Principais Análises:**
• Taxas de juros e CET
• Valor do bem e valor financiado
• Prazo e forma de pagamento
• Seguros obrigatórios e opcionais
• Transferência de propriedade

**⚠️ Pontos Críticos:**
• Taxa de juros acima da média (consulte BACEN)
• Seguros com sobrepreço
• Cláusulas de alienação fiduciária
• IOF e tarifas bancárias

**📞 Órgãos de Defesa:**
• BACEN (Banco Central) - SCR/Registrato
• PROCON - Defesa do consumidor
• DETRAN - Documentação veicular

Como posso ajudar com seu financiamento?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['juros', 'taxa', 'cet', 'percentual']):
            return """📊 **Juros e Taxas - Financiamento Veicular**

**Taxa de Juros:**
• **Pessoa Física**: Média 1,5% a 3,5% ao mês
• **Pessoa Jurídica**: Média 1,2% a 2,8% ao mês
• **Veículo Novo**: Taxas menores (1,5% a 2,5%)
• **Veículo Usado**: Taxas maiores (2,5% a 4,0%)

**CET (Custo Efetivo Total):**
• Deve incluir TODAS as taxas (juros + IOF + tarifas)
• Obrigatório informar ANTES da assinatura
• Compare sempre o CET, não apenas os juros
• CET pode ser 1-2% maior que taxa nominal

**Taxas Adicionais Comuns:**
• **IOF**: 0,0082% ao dia + 0,38% adicional
• **Taxa de cadastro**: Máx. R$ 50 (Resolução CMN 3.518)
• **Tarifa de avaliação**: R$ 50-200 (negociável)
• **Registro de contrato**: R$ 30-80

**🛡️ Proteções Legais:**
• Taxa deve estar no contrato ANTES da assinatura
• CET obrigatório (Circular BACEN 3.371)
• Proibição de cobrança de taxa abusiva
• Direito de quitação antecipada com desconto

**💡 Dica Importante:**
Use o calculadora do BACEN para comparar taxas: bcb.gov.br/calculadora

Precisa que eu analise suas taxas específicas?"""
        
        if any(word in question_lower for word in ['seguro', 'proteção', 'cobertura', 'obrigatório']):
            return """🛡️ **Seguros no Financiamento Veicular**

**Seguros Obrigatórios:**
• **Seguro Auto** (proteção do bem financiado)
• **Seguro Prestamista** (cobertura do saldo devedor)
• Cobertura contra morte, invalidez, desemprego

**Seguros Opcionais:**
• **Seguro estendido** (garantia mecânica)
• **Proteção de parcelas** (múltiplas coberturas)
• **Assistência 24h**

**⚠️ Pontos de Atenção:**
• Seguros podem representar 20-40% do valor da parcela
• Compare preços com outras seguradoras
• Leia cobertura e exclusões detalhadamente
• Alguns seguros podem ser contratados separadamente

**Como Funciona:**
• **Seguro Auto**: Protege o banco em caso de sinistro total
• **Prestamista**: Quite o financiamento em casos cobertos
• **Renovação**: Anual, pode renegociar a cada ano

**🛡️ Seus Direitos:**
• Escolher seguradora (não pode ser imposto)
• Cancelar seguros opcionais
• Receber proposta detalhada antes da contratação
• Período de reflexão para seguros (7 dias)

**📋 Regulamentação:**
• Circular SUSEP sobre seguros vinculados a financiamentos
• CDC - proteção contra venda casada

**💡 Dica Legal:**
Seguro auto pode ser contratado em qualquer seguradora, não necessariamente do banco.

Tem dúvidas sobre algum seguro específico no seu contrato?"""
        
        if any(word in question_lower for word in ['alienação', 'propriedade', 'documento', 'transferência']):
            return """📋 **Alienação Fiduciária e Documentação**

**O que é Alienação Fiduciária:**
• O banco fica como proprietário fiduciário até quitação
• Você é proprietário e possuidor direto do veículo
• Consta no CRLV como "alienação fiduciária"
• Só transfere totalmente após pagamento final

**Documentação Durante Financiamento:**
• **CRLV**: Em seu nome com restrição "alienação fiduciária"
• **IPVA**: Sua responsabilidade (mesmo com financiamento)
• **Multas**: Sua responsabilidade direta
• **Seguro**: Obrigatório e em seu nome

**Transferência de Propriedade:**
• Ocorre automaticamente após quitação
• Banco deve liberar gravame em até 10 dias
• DETRAN atualiza documentação
• Novo CRLV sem restrição

**⚠️ Cuidados Importantes:**
• Não pode vender sem quitar (crime)
• Não pode dar garantia/penhor do veículo
• Atraso pode resultar em busca e apreensão
• Veículo pode ser rastreado pelo banco

**🛡️ Seus Direitos:**
• Usar veículo normalmente (trabalho, lazer)
• Fazer modificações (com limite)
• Vender quitando o financiamento antecipadamente
• Receber documento liberado após quitação

**📞 Em Caso de Problemas:**
• DETRAN: Para questões de documentação
• BACEN: Para demora na liberação do gravame
• Cartório: Para segunda via de documentos

**💡 Quitação Antecipada:**
Sempre há desconto dos juros futuros - calcule se vale a pena!

Precisa de orientação sobre algum aspecto da documentação?"""
        
        if any(word in question_lower for word in ['prazo', 'parcela', 'entrada', 'valor']):
            return """💰 **Prazo, Parcelas e Condições**

**Prazos Comuns:**
• **Veículo Novo**: 12 a 60 meses (até 5 anos)
• **Veículo Usado**: 12 a 48 meses (até 4 anos)
• **Veículo Seminovo**: 12 a 54 meses (até 4,5 anos)
• **Prazo máximo**: Varia por ano do veículo

**Composição do Valor:**
• **Valor do veículo**: Conforme tabela FIPE/avaliação
• **Valor financiado**: Até 100% (zero de entrada)
• **Entrada típica**: 20% a 50% do valor
• **IOF**: Sobre valor financiado

**Cálculo da Parcela:**
• **Principal**: Valor financiado ÷ número de parcelas
• **Juros**: Taxa sobre saldo devedor
• **Seguros**: Valor mensal dos seguros
• **IOF**: Diluído nas parcelas

**Modalidades de Pagamento:**
• **Tabela Price**: Parcelas fixas
• **SAC**: Parcelas decrescentes
• **Bullet**: Pagamento no vencimento (raro)

**⚠️ Pontos de Atenção:**
• Quanto maior prazo, maior juros totais
• Entrada maior = parcela menor + menos juros
• Primeira parcela pode vencer em 30-45 dias
• Antecipação de parcelas gera desconto

**🛡️ Direitos na Renegociação:**
• Quitação antecipada com desconto dos juros
• Renegociação em caso de dificuldades
• Portabilidade para outro banco
• Amortização extraordinária

**💡 Simulação Recomendada:**
Sempre simule cenários: entrada maior vs. prazo maior vs. investimento da entrada.

**📊 Dica Prática:**
Use planilhas de simulação ou calculadora do BACEN para comparar opções.

Precisa de ajuda para calcular a melhor opção para seu caso?"""
        
        if any(word in question_lower for word in ['quitar', 'quitação', 'antecipada', 'saldo']):
            return """💵 **Quitação Antecipada do Financiamento**

**Como Funciona:**
• Direito garantido por lei (pode quitar quando quiser)
• Desconto obrigatório dos juros futuros
• Cálculo por juros compostos (não lineares)
• IOF proporcional ao prazo restante

**Cálculo do Saldo Devedor:**
• **Saldo atual**: Principal + juros até a data
• **Desconto**: Juros futuros não pagos
• **IOF restante**: Proporcional aos dias restantes
• **Valor final**: Menor que soma das parcelas restantes

**Formas de Quitação:**
• **Total**: Pagamento integral do saldo com desconto
• **Amortização**: Pagamento parcial reduz prazo/parcela
• **Portabilidade**: Transferência para outro banco
• **Refinanciamento**: Novo contrato com condições melhores

**⚠️ Pontos Importantes:**
• Solicite extrato atualizado do saldo devedor
• Desconto de juros é obrigatório por lei
• IOF não é devolvido (apenas proporcional)
• Liberação do gravame em até 10 dias úteis

**🛡️ Seus Direitos:**
• Quitação antecipada sem multa ou penalidade
• Desconto dos juros não transcorridos (CDC Art. 52, §2º)
• Receber documentação liberada rapidamente
• Extrato detalhado do cálculo

**📋 Documentos Necessários:**
• RG, CPF e comprovante de endereço
• CRLV do veículo
• Comprovante de renda (se exigido)
• Conta bancária para débito

**💡 Dica Estratégica:**
Compare: quitação antecipada vs. investimento do dinheiro. Às vezes compensar manter parcelas e investir.

**📞 Processo:**
1. Solicite saldo devedor atualizado
2. Confirme cálculo e desconto
3. Efetue pagamento
4. Acompanhe liberação do gravame

Quer que eu ajude a avaliar se vale a pena quitar antecipadamente?"""
        
        if any(word in question_lower for word in ['atraso', 'inadimplência', 'busca', 'apreensão']):
            return """⚠️ **Atraso e Inadimplência no Financiamento**

**Consequências do Atraso:**
• **Multa**: Máximo 2% sobre valor da parcela
• **Juros de mora**: Máximo 1% ao mês
• **Negativação**: SPC/SERASA após 15 dias
• **Busca e Apreensão**: Após 30 dias de atraso

**Estágios da Inadimplência:**
• **1-15 dias**: Multa e juros, cobrança telefônica
• **15-30 dias**: Negativação nos órgãos de proteção
• **30-60 dias**: Possibilidade de busca e apreensão
• **Acima de 60 dias**: Processo judicial provável

**Busca e Apreensão:**
• **Legal após**: 30 dias de atraso (Decreto-Lei 911/69)
• **Processo**: Liminar judicial, oficial de justiça
• **Sua defesa**: 15 dias para contestar ou pagar
• **Leilão**: Se não regularizar, veículo é vendido

**O que Fazer em Caso de Dificuldades:**
• **Negociar ANTES** do atraso
• **Renegociação**: Novo prazo/valor de parcelas
• **Portabilidade**: Transferir para banco com menor taxa
• **Venda do veículo**: Quitar financiamento e ficar livre

**🛡️ Seus Direitos na Renegociação:**
• Propor novo plano de pagamento
• Contestar valores cobrados indevidamente
• Solicitar revisão de juros abusivos
• Buscar acordo antes do leilão

**📞 Canais de Negociação:**
• **Banco**: Central de relacionamento/renegociação
• **PROCON**: Mediação de conflitos
• **BACEN**: Registrator para reclamações
• **Defensoria Pública**: Orientação jurídica gratuita

**💡 Dicas Importantes:**
• Nunca ignore as cobranças - negocie sempre
• Documente todas as negociações por escrito
• Em caso de desemprego, informe e negocie carência
• Venda do veículo pode ser melhor opção que busca e apreensão

**⚖️ Base Legal:**
• Decreto-Lei 911/69 (Busca e Apreensão)
• CDC (Limitação de multas e juros)
• Lei 10.931/04 (Alienação Fiduciária)

**🚨 Urgente:**
Se já está atrasado, contate o banco HOJE para negociar!

Precisa de orientação para negociar com o banco?"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""🚗 **Análise do Contrato de Financiamento Veicular**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Condições Financeiras:**
• Taxa de juros nominal e CET
• Valor do bem e valor financiado
• Prazo e valor das parcelas
• IOF e demais taxas

**2. Seguros:**
• Tipos de seguro (auto, prestamista)
• Valores e coberturas
• Possibilidade de escolha da seguradora
• Clausulas de renovação

**3. Alienação Fiduciária:**
• Condições de propriedade durante financiamento
• Restrições de uso e modificação
• Processo de liberação após quitação

**4. Direitos e Obrigações:**
• Direito à quitação antecipada
• Responsabilidades com documentação
• Consequências do inadimplemento
• Condições de renegociação

**⚖️ Conformidade Legal:**
Este contrato deve seguir o CDC, normas do BACEN, SUSEP e legislação de trânsito.

Posso analisar algum ponto específico que está gerando dúvida?"""
        
        # Resposta geral
        return """🚗 **Financiamento Veicular - Orientação Geral**

Entendi sua pergunta sobre financiamento de veículos. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de taxas e CET (conformidade BACEN)
• Análise de seguros obrigatórios e opcionais
• Orientação sobre alienação fiduciária
• Cálculos de quitação antecipada

**⚠️ Problemas Mais Comuns:**
• Taxas de juros acima da média do mercado
• Seguros com preços abusivos
• Dificuldades na liberação do gravame
• Cobrança de tarifas irregulares

**🛡️ Seus Direitos Principais:**
• CET claramente informado antes da assinatura
• Quitação antecipada com desconto dos juros futuros
• Escolha da seguradora (não pode ser imposta)
• Renegociação em caso de dificuldades

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça o texto do contrato."""