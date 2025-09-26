from app.agents.base_agent import BaseContractAgent

class ConsortiumAgent(BaseContractAgent):
    """Agente especializado em contratos de consórcio"""
    
    def __init__(self):
        self.specialization = "Consórcio"
        self.icon = "🎯"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para consórcios"""
        
        if not question:
            return """🎯 **Consórcio - Análise Especializada**

Olá! Sou especialista em contratos de consórcio. Posso ajudar com:

**📋 Principais Análises:**
• Taxa de administração e adesão
• Prazo do grupo e modalidade de sorteio
• Condições de contemplação e lance
• Seguro prestamista e proteção
• Desistência e transferência de cotas

**⚠️ Pontos Críticos:**
• Taxa de administração acima da média (máx. 25%)
• Cláusulas abusivas de retenção de valores
• Falta de transparência nos critérios de sorteio
• Condições de seguro obrigatório

**📞 Órgãos de Defesa:**
• BACEN (Banco Central) - Regulamentação
• ABAC (Associação Brasileira de Administradoras de Consórcio)
• PROCON - Defesa do consumidor

Como posso ajudar com seu consórcio?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['taxa', 'administração', 'adesão', 'percentual']):
            return """💰 **Taxas no Consórcio**

**Taxa de Administração:**
• **Limite legal**: Máximo 25% do valor do bem
• **Média mercado**: 15% a 20% para imóveis, 20% a 25% para veículos
• **Cobrança**: Mensal, embutida na parcela
• **Regulamentação**: Circular BACEN 3.432/09

**Taxa de Adesão:**
• **Finalidade**: Custos de entrada no grupo
• **Valor típico**: R$ 50 a R$ 200
• **Cobrança**: Única, no ato da adesão
• **Legalidade**: Permitida se razoável

**Fundo de Reserva:**
• **Percentual**: Até 10% das parcelas pagas
• **Objetivo**: Cobrir inadimplência e custos
• **Devolução**: Ao final do grupo, corrigido monetariamente

**Seguro Prestamista:**
• **Obrigatoriedade**: Definida pela administradora
• **Cobertura**: Morte e invalidez total
• **Custo**: 0,1% a 0,5% do saldo devedor ao mês
• **Benefício**: Quitação do consórcio em caso coberto

**⚠️ Pontos de Atenção:**
• Taxa acima de 25% é abusiva
• Fundo de reserva deve ser devolvido ao final
• Seguros opcionais não podem ser impostos
• Taxa de adesão deve ter justificativa clara

**🛡️ Comparação Recomendada:**
• Compare taxa de administração entre administradoras
• Verifique se há taxa de adesão
• Confirme percentual do fundo de reserva
• Analise custos totais, não apenas parcela mensal

**💡 Dica Importante:**
Taxa menor nem sempre significa melhor negócio - analise todas as condições do grupo.

Precisa que eu analise as taxas do seu consórcio específico?"""
        
        if any(word in question_lower for word in ['sorteio', 'contemplação', 'lance', 'como funciona']):
            return """🎲 **Contemplação no Consórcio**

**Formas de Contemplação:**
• **Sorteio**: Aleatório, sem custo adicional
• **Lance**: Oferta de valor maior que parcela
• **Aniversário**: Em alguns grupos, contemplação automática

**Como Funciona o Sorteio:**
• **Frequência**: Mensal, conforme assembleia
• **Participação**: Automática para cotistas em dia
• **Transparência**: Deve ser público e auditado
• **Igualdade**: Mesma chance para todos em dia

**Sistema de Lances:**
• **Lance embutido**: Valor adicional na parcela mensal
• **Lance livre**: Oferta específica na assembleia
• **Critério**: Maior lance vence (% sobre saldo devedor)
• **Limite**: Não pode ultrapassar 100% do valor do bem

**⚠️ Importante sobre Lances:**
• Lance não é obrigatório - é estratégia
• Lance perdedor não gera custo extra
• Contemplado por lance paga valor integral do lance
• Lance pode ser parcelado em alguns grupos

**📊 Probabilidades:**
• **Sorteio**: Diminui conforme contemplações (1/N participantes)
• **Lance**: Depende da concorrência e valor ofertado
• **Estratégia**: Combinar sorteio + lance pequeno

**🎯 Quando Usar Cada Modalidade:**
• **Sorteio**: Se não tem pressa e quer economizar
• **Lance**: Se precisa da carta de crédito rapidamente
• **Lance baixo**: Para aumentar chances sem muito custo

**🛡️ Seus Direitos:**
• Participar de todos os sorteios estando em dia
• Dar lances livres nas assembleias
• Receber carta de crédito imediatamente se contemplado
• Informações transparentes sobre critérios

**💡 Dica Estratégica:**
Estude histórico do grupo: quantos lances típicos, valores médios, frequência de contemplação.

Precisa de orientação sobre estratégia de lances no seu grupo?"""
        
        if any(word in question_lower for word in ['desistir', 'desistência', 'cancelar', 'sair']):
            return """❌ **Desistência do Consórcio**

**Tipos de Saída:**
• **Desistência antes da contemplação**
• **Desistência após contemplação (só com quitação)**
• **Exclusão por inadimplência**
• **Transferência de cota para terceiro**

**Desistência Antes da Contemplação:**
• **Direito garantido**: Pode sair quando quiser
• **Valores a receber**: Valores pagos - taxa administrativa - multa
• **Prazo de devolução**: Até 60 dias após encerramento do grupo
• **Correção**: Valores corrigidos monetariamente

**Cálculo da Devolução:**
• **Base**: Soma de todas as parcelas pagas
• **Descontos**: Taxa de administração + multa por desistência
• **Fundo de reserva**: Devolvido ao final do grupo
• **Correção**: IGPM ou índice definido no contrato

**Multa por Desistência:**
• **Limite legal**: Máximo 10% das parcelas pagas
• **Finalidade**: Compensar custos administrativos
• **Base legal**: Lei 11.795/08 (Lei do Consórcio)

**⚠️ Pontos Importantes:**
• Contemplado NÃO pode desistir - deve quitar
• Devolução só ocorre após fim do grupo (60-120 meses)
• Taxa administrativa não é devolvida
• Multa incide sobre valor já descontado da taxa

**Transferência de Cota:**
• **Alternativa**: Vender cota para terceiro
• **Vantagem**: Recebe valores imediatamente
• **Processo**: Através da administradora
• **Documentação**: Transferência formal necessária

**🛡️ Seus Direitos na Desistência:**
• Sair do consórcio quando quiser (se não contemplado)
• Receber valores pagos (descontadas taxas legais)
• Correção monetária dos valores
• Devolução no prazo legal (60 dias após encerramento)

**📋 Processo de Desistência:**
1. Comunicar administradora por escrito
2. Quitar parcelas em atraso (se houver)
3. Aguardar cálculo da administradora
4. Conferir valores e prazos
5. Receber termo de desistência

**💡 Alternativas à Desistência:**
• Suspensão temporária (se permitida)
• Transferência para parente
• Venda da cota no mercado

**⚖️ Base Legal:**
Lei 11.795/08 e Circular BACEN 3.432/09.

**🚨 Importante:**
Antes de desistir, calcule: pode ser melhor manter até contemplação ou transferir a cota.

Precisa de ajuda para calcular os valores da sua desistência?"""
        
        if any(word in question_lower for word in ['bem', 'carta', 'crédito', 'usar', 'comprar']):
            return """🏆 **Uso da Carta de Crédito**

**O que é a Carta de Crédito:**
• **Documento**: Autorização para aquisição do bem
• **Valor**: Corresponde ao saldo devedor atualizado
• **Prazo**: Geralmente 30 dias para usar após contemplação
• **Finalidade**: Comprar o bem especificado no contrato

**Como Usar a Carta:**
• **Escolha do bem**: Dentro das especificações contratadas
• **Fornecedor**: Deve aceitar consórcio e estar credenciado
• **Documentação**: Apresentar carta + documentos do bem
• **Vistoria**: Administradora pode exigir vistoria do bem

**Tipos de Bem por Consórcio:**
• **Imóvel**: Casa, apartamento, terreno, comercial
• **Veículo**: Carro, moto, caminhão (novo ou usado)
• **Serviços**: Reforma, viagem, casamento (específicos)
• **Eletrodomésticos**: Linha branca, móveis, eletrônicos

**⚠️ Restrições Comuns:**
• Bem deve estar dentro do valor da carta
• Alguns consórcios só permitem bem novo
• Localização geográfica pode ter restrições
• Bem usado pode ter limite de idade

**Documentação Necessária:**
• **Carta de crédito** original
• **Documentos do bem** (nota fiscal, certidões)
• **Documentos pessoais** atualizados
• **Comprovante de renda** (se exigido)

**Prazos Importantes:**
• **Para usar**: Geralmente 30 dias após contemplação
• **Prorrogação**: Pode ser solicitada (justificada)
• **Perda do direito**: Se não usar no prazo

**🛡️ Seus Direitos:**
• Escolher livremente o bem dentro das especificações
• Solicitar prorrogação de prazo com justificativa
• Recusar bem com defeito ou preço abusivo
• Transferir carta para parente (conforme contrato)

**💡 Dicas Práticas:**
• Pesquise preços antes da contemplação
• Confirme se fornecedor trabalha com consórcio
• Negocie condições de pagamento do saldo (se houver)
• Guarde todos os comprovantes e documentos

**🏠 Para Imóveis:**
• Verifique certidões negativas
• Confirme regularização do imóvel
• Analise localização e valorização
• Considere custos adicionais (ITBI, cartório)

**🚗 Para Veículos:**
• Verifique procedência e documentação
• Faça vistoria técnica completa
• Confirme valor na tabela FIPE
• Considere seguro obrigatório

Precisa de orientação sobre como usar sua carta de crédito?"""
        
        if any(word in question_lower for word in ['inadimplência', 'atraso', 'exclusão', 'expulsão']):
            return """⚠️ **Inadimplência e Exclusão do Consórcio**

**Regras de Inadimplência:**
• **Atraso permitido**: Geralmente até 60 dias sem exclusão
• **Multa**: Máximo 2% sobre valor da parcela
• **Juros de mora**: 1% ao mês sobre valor em atraso
• **Exclusão**: Após 60 dias de atraso consecutivo

**Processo de Exclusão:**
• **Notificação**: Aviso formal sobre atraso
• **Prazo para regularização**: Geralmente 15-30 dias
• **Assembleia de exclusão**: Deliberação do grupo
• **Comunicação**: Notificação formal da exclusão

**Consequências da Exclusão:**
• **Perda da cota**: Não participa mais do grupo
• **Devolução de valores**: Só ao final do grupo
• **Negativação**: Nome pode ir para SPC/SERASA
• **Perda de contemplação**: Se já contemplado, deve quitar o bem

**Valores na Exclusão:**
• **A receber**: Parcelas pagas - taxa administrativa - multa
• **Prazo**: Até 60 dias após encerramento do grupo
• **Correção**: Conforme índice do contrato
• **Fundo de reserva**: Devolvido proporcionalmente

**🛡️ Como Evitar a Exclusão:**
• **Comunicação**: Avisar sobre dificuldades antes do atraso
• **Negociação**: Solicitar parcelamento do débito
• **Transferência**: Passar cota para parente ou terceiro
• **Suspensão**: Solicitar pausa temporária (se permitida)

**Renegociação de Débitos:**
• **Parcelamento**: Dividir débito em várias parcelas
• **Desconto**: Em juros e multas (negociável)
• **Novo prazo**: Adequar à capacidade de pagamento
• **Acordo**: Formalizar por escrito

**Exclusão de Contemplado:**
• **Situação especial**: Contemplado inadimplente
• **Consequência**: Deve devolver o bem ou quitar totalmente
• **Processo legal**: Administradora pode executar judicialmente
• **Negociação**: Ainda é possível acordo

**🛡️ Seus Direitos na Exclusão:**
• Receber notificação formal com prazo
• Participar da assembleia que decidirá exclusão
• Contestar exclusão se irregular
• Receber valores devidos conforme lei

**📞 O que Fazer em Dificuldades:**
• **Imediato**: Contatar administradora para negociar
• **PROCON**: Se administradora não negociar
• **ABAC**: Mediação entre consumidor e administradora
• **Advogado**: Se necessário processo judicial

**💡 Dica Importante:**
Nunca deixe chegar à exclusão - negocie sempre antes do prazo limite!

**⚖️ Base Legal:**
Lei 11.795/08 e Circular BACEN 3.432/09.

Está enfrentando dificuldades para pagar? Posso orientar sobre negociação!"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""🎯 **Análise do Contrato de Consórcio**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Taxas e Custos:**
• Taxa de administração (máx. 25%)
• Taxa de adesão e sua justificativa
• Percentual do fundo de reserva
• Seguros obrigatórios e custos

**2. Funcionamento do Grupo:**
• Prazo total do consórcio
• Modalidades de contemplação
• Critérios de sorteio e lances
• Frequência das assembleias

**3. Direitos e Deveres:**
• Condições de desistência
• Multas e penalidades
• Regras de inadimplência e exclusão
• Transferência de cotas

**4. Uso da Carta de Crédito:**
• Especificações do bem a adquirir
• Prazo para uso da carta
• Restrições geográficas ou de fornecedor
• Condições de vistoria

**⚖️ Conformidade Legal:**
Este contrato deve seguir a Lei 11.795/08 e normas do BACEN.

Posso analisar algum ponto específico que está causando dúvida?"""
        
        # Resposta geral
        return """🎯 **Consórcio - Orientação Geral**

Entendi sua pergunta sobre consórcio. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de taxas (conformidade BACEN)
• Análise de condições de contemplação
• Orientação sobre desistência e transferência
• Cálculos de devolução de valores

**⚠️ Problemas Mais Comuns:**
• Taxa de administração acima de 25%
• Falta de transparência nos sorteios
• Dificuldades na devolução de valores
• Cláusulas abusivas de exclusão

**🛡️ Seus Direitos Principais:**
• Taxa de administração limitada a 25%
• Participação em sorteios estando em dia
• Desistência com devolução de valores
• Transparência total no funcionamento do grupo

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça o texto do contrato."""