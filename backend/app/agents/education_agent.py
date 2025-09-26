from app.agents.base_agent import BaseContractAgent

class EducationAgent(BaseContractAgent):
    """Agente especializado em contratos de educação"""
    
    def __init__(self):
        self.specialization = "Educação"
        self.icon = "🎓"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para contratos educacionais"""
        
        if not question:
            return """🎓 **Educação - Análise Especializada**

Olá! Sou especialista em contratos educacionais. Posso ajudar com:

**📋 Principais Análises:**
• Contratos de matrícula escolar/universitária
• Mensalidades e reajustes
• Material didático e taxas extras
• Transferência e trancamento
• Serviços educacionais adicionais

**⚠️ Pontos Críticos:**
• Reajustes acima da inflação
• Cobrança de material obrigatório
• Multas por cancelamento
• Cláusulas de rematrícula automática

**📚 Órgãos de Defesa:**
• MEC - Ministério da Educação
• PROCON - Defesa do consumidor
• INEP - Supervisão da qualidade

Como posso ajudar com seu contrato educacional?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['mensalidade', 'reajuste', 'valor', 'aumento', 'preço']):
            return """💰 **Mensalidades e Reajustes Escolares**

**Cobrança de Mensalidades:**

**Regras Básicas:**
• **Vencimento**: Até o dia 10 de cada mês
• **Proporcionalidade**: Primeira e última mensalidade proporcionais
• **Número de parcelas**: Máximo 12 parcelas anuais
• **Antecipação**: Desconto para pagamento antecipado

**📊 Reajustes Anuais:**

**Limite Legal:**
• **Educação básica**: Sem limite específico, mas deve ser razoável
• **Superior**: Liberdade de preços (exceto em contratos especiais)
• **Critério**: Deve considerar custos operacionais reais
• **Justificativa**: Instituição deve demonstrar necessidade

**Fatores para Reajuste:**
• **Custo pessoal**: Salários de professores e funcionários
• **Infraestrutura**: Manutenção e melhorias
• **Material didático**: Livros e recursos pedagógicos
• **Tecnologia**: Investimentos em equipamentos

**⚠️ Reajustes Abusivos:**
• **Acima da inflação**: Sem justificativa adequada
• **Retroativo**: Aplicado sem aviso prévio (mín. 45 dias)
• **Múltiplos**: Mais de um reajuste por ano letivo
• **Discriminatório**: Valores diferentes sem justificativa

**🛡️ Seus Direitos:**
• Aviso prévio de 45 dias sobre reajuste
• Justificativa detalhada dos aumentos
• Contestar reajustes abusivos
• Transferência sem multa se não aceitar reajuste

**Como Contestar Reajuste:**
• **1º passo**: Solicitar justificativa por escrito
• **2º passo**: Negociar com a escola
• **3º passo**: PROCON se não houver acordo
• **4º passo**: Ação judicial em último caso

**💡 Dicas Importantes:**
• Compare valores com outras instituições
• Verifique melhorias oferecidas que justifiquem aumento
• Negocie condições especiais (família, irmãos)
• Considere qualidade × custo-benefício

**Desconto para Irmãos:**
• **Não obrigatório**: Escola não é obrigada a dar
• **Negociação**: Pode ser conversado
• **Política própria**: Cada escola define sua regra
• **Contrato**: Deve estar previsto se aplicado

**📅 Cronograma de Pagamentos:**
• **Matrícula**: Janeiro/fevereiro
• **Mensalidades**: Fevereiro a dezembro (11 ou 12 parcelas)
• **Material**: Pode ser parcelado
• **Extras**: Uniformes, atividades opcionais

**⚖️ Base Legal:**
CDC e Lei 9.870/99 sobre cobrança de anuidades escolares.

Está enfrentando problemas com reajuste de mensalidade ou cobrança irregular?"""
        
        if any(word in question_lower for word in ['matrícula', 'rematrícula', 'renovação', 'contrato']):
            return """📝 **Matrícula e Rematrícula Escolar**

**Processo de Matrícula:**

**Documentação Necessária:**
• **Pessoa física**: RG, CPF do responsável e aluno
• **Comprovante de renda**: Para verificação financeira
• **Histórico escolar**: Da escola anterior
• **Declaração de escolaridade**: Se em andamento
• **Atestado médico**: Para atividades físicas

**Reserva de Vaga:**
• **Taxa**: Valor para garantir vaga (geralmente 1 mensalidade)
• **Dedução**: Deve ser deduzida da primeira mensalidade
• **Devolução**: Se escola cancelar matrícula
• **Prazo**: Para confirmar matrícula definitiva

**🔄 Rematrícula Automática:**

**Regras Legais:**
• **Proibição**: Rematrícula automática é PROIBIDA por lei
• **Renovação**: Deve ser expressa e voluntária
• **Prazo**: Escola deve dar prazo para decidir
• **Comunicação**: Informar condições da renovação

**Procedimento Correto:**
• **Comunicado**: Escola informa sobre renovação (até outubro)
• **Condições**: Valores e regras para ano seguinte
• **Prazo**: Mínimo 45 dias para resposta dos pais
• **Confirmação**: Expressa da família

**⚠️ Práticas Irregulares:**
• **Cobrança automática**: Sem autorização expressa
• **Pressão**: Ameaças de perda de vaga
• **Prazo curto**: Menos de 30 dias para decidir
• **Mudança súbita**: Alteração de regras sem aviso

**🛡️ Direitos na Matrícula:**
• Informação clara sobre valores e regras
• Prazo adequado para análise do contrato
• Não rematrícula automática
• Devolução da taxa se escola cancelar

**Cancelamento da Matrícula:**
• **Até o início das aulas**: Devolução integral da taxa
• **Após início**: Cobrança proporcional ao período
• **Transferência**: Direito à documentação
• **Material**: Devolução se não utilizado

**Lista de Espera:**
• **Transparência**: Posição na fila deve ser informada
• **Critérios**: Claros para classificação
• **Comunicação**: Aviso quando vaga abrir
• **Taxa**: Não pode cobrar para manter na lista

**💡 Dicas para Matrícula:**
• Leia todo o contrato antes de assinar
• Questione cláusulas não compreendidas
• Verifique reputação da escola no MEC
• Compare custo-benefício com outras opções

**Transferência de Escola:**
• **Documentação**: Escola deve fornecer imediatamente
• **Proporcionalidade**: Pagamento apenas do período estudado
• **Sem retenção**: Não pode reter documentos por débito
• **Material**: Devolução do não utilizado

**📋 Contrato Educacional:**
• **Clareza**: Linguagem acessível obrigatória
• **Serviços**: Detalhamento do que está incluso
• **Valores**: Discriminação de todas as taxas
• **Regras**: Condições de renovação e cancelamento

**⚖️ Base Legal:**
Lei 9.870/99 e CDC sobre relações de consumo educacional.

Precisa de orientação sobre matrícula, rematrícula ou transferência escolar?"""
        
        if any(word in question_lower for word in ['material', 'didático', 'livro', 'apostila', 'uniforme']):
            return """📚 **Material Didático e Uniformes**

**Material Didático:**

**Regras de Cobrança:**
• **Separação**: Valor do material separado da mensalidade
• **Opcional**: Em princípio, compra deve ser facultativa
• **Lista**: Escola deve fornecer lista detalhada
• **Preços**: Transparência nos valores cobrados

**⚠️ Venda Casada:**
• **Proibição**: Não pode obrigar compra na escola
• **Escolha**: Pais podem comprar onde quiser
• **Especificação**: Se exigir marca específica, deve justificar
• **Alternativas**: Escola deve aceitar material equivalente

**Situações Permitidas:**
• **Material personalizado**: Específico da metodologia
• **Apostilas próprias**: Sistema de ensino exclusivo
• **Plataforma digital**: Acesso a conteúdo online
• **Material consumível**: Uso durante as aulas

**🛡️ Seus Direitos:**
• Lista de material até dezembro do ano anterior
• Preços transparentes e justos
• Opção de comprar em outros locais
• Parcelamento do valor do material

**📖 Tipos de Material:**

**Livros Didáticos:**
• **Escolha**: Pais podem comprar usados ou em livrarias
• **Edição**: Escola não pode exigir edição específica (exceto se houver mudanças significativas)
• **Lista**: Deve ser fornecida com antecedência
• **Reutilização**: Incentivar uso de livros de anos anteriores

**Apostilas Sistêmicas:**
• **Sistema próprio**: Escola pode exigir se for metodologia exclusiva
• **Cobrança**: Valor justo pelo conteúdo
• **Atualização**: Deve ser realmente necessária
• **Parcelamento**: Opção de dividir em mensalidades

**Material de Arte/Laboratório:**
• **Uso coletivo**: Para atividades específicas da escola
• **Individual**: Cada aluno deve levar o seu
• **Especificação**: Clara sobre o que é necessário
• **Substituição**: Aceitar materiais equivalentes

**👕 Uniformes Escolares:**

**Obrigatoriedade:**
• **Decisão escolar**: Escola pode exigir uniforme
• **Justificativa**: Segurança, identidade, igualdade
• **Especificação**: Modelo e cores definidas
• **Fornecedor**: Não pode obrigar compra na escola

**Fornecedores:**
• **Livre escolha**: Pais podem comprar onde quiser
• **Múltiplas opções**: Escola deve indicar vários fornecedores
• **Preço justo**: Não pode haver superfaturamento
• **Qualidade**: Padrão adequado para uso escolar

**⚠️ Práticas Abusivas:**
• **Fornecedor único**: Obrigar compra em local específico
• **Preço abusivo**: Valores muito acima do mercado
• **Marca específica**: Sem justificativa pedagógica
• **Mudança frequente**: Alterações desnecessárias

**💡 Dicas para Material e Uniforme:**
• Pesquise preços em diferentes fornecedores
• Reutilize material de anos anteriores quando possível
• Negocie parcelamento com a escola
• Questione especificações muito restritivas

**📋 Lista de Material:**
• **Prazo**: Até 45 dias antes do início das aulas
• **Detalhamento**: Especificação clara de cada item
• **Quantidades**: Justificadas para o uso escolar
• **Preços**: Estimativa de valores (quando vendido pela escola)

**Atividades Extras:**
• **Opcional**: Passeios e atividades não curriculares
• **Transparência**: Valores e programação claros
• **Escolha**: Pais decidem participação
• **Qualidade**: Atividades com valor educativo

**⚖️ Base Legal:**
CDC sobre venda casada e transparência na cobrança.

Está enfrentando problemas com cobrança de material ou uniformes obrigatórios?"""
        
        if any(word in question_lower for word in ['cancelar', 'cancelamento', 'transferência', 'trancar', 'desistir']):
            return """❌ **Cancelamento e Transferência Escolar**

**Cancelamento de Matrícula:**

**Direito de Arrependimento:**
• **Prazo**: 7 dias corridos após assinatura do contrato
• **Devolução**: Integral dos valores pagos
• **Forma**: Comunicação por escrito
• **Sem multa**: Não pode haver cobrança de penalidade

**Cancelamento Após Início das Aulas:**
• **Proporcionalidade**: Pagamento apenas do período estudado
• **Aviso prévio**: Recomendável dar 30 dias de antecedência
• **Multa**: Só se prevista em contrato (máx. 10% da anuidade)
• **Material**: Devolução do não utilizado

**⚠️ Situações Especiais:**

**Mudança de Cidade:**
• **Comprovação**: Documentar a mudança de endereço
• **Isenção**: Geralmente isenta de multa
• **Transferência**: Direito à documentação imediata
• **Negociação**: Escola pode ser flexível com prazos

**Problemas Financeiros:**
• **Negociação**: Tentar acordo com a escola
• **Parcelamento**: Débitos em aberto
• **Bolsa**: Verificar programas de auxílio
• **Transferência**: Para escola mais acessível

**🛡️ Transferência de Escola:**

**Documentação Obrigatória:**
• **Histórico escolar**: Completo e atualizado
• **Declaração de escolaridade**: Se ano em andamento
• **Ficha individual**: Dados do aluno
• **Boletim**: Notas do período atual

**Prazos para Fornecimento:**
• **Imediato**: Para documentos já prontos
• **30 dias**: Para histórico final (fim do ano)
• **Sem retenção**: Mesmo com débitos pendentes
• **Gratuito**: Não pode cobrar pela documentação

**Débitos Pendentes:**
• **Documentação**: Não pode ser retida por débito
• **Cobrança**: Continua válida para valores devidos
• **Negociação**: Escola pode facilitar acordo
• **Judicial**: Cobrança por via apropriada

**💡 Processo de Transferência:**

**1. Comunicação:**
• Informar escola sobre transferência
• Solicitar documentação necessária
• Definir data da saída

**2. Acertos Financeiros:**
• Calcular valores proporcionais
• Negociar débitos pendentes
• Solicitar devolução de material não usado

**3. Nova Escola:**
• Verificar documentação necessária
• Confirmar disponibilidade de vaga
• Processo de adaptação curricular

**🎓 Trancamento de Matrícula:**
• **Ensino superior**: Permitido conforme regras da IES
• **Educação básica**: Geralmente não aplicável
• **Prazos**: Seguir cronograma acadêmico
• **Retorno**: Condições para rematrícula

**📋 Dicas Importantes:**
• Guarde todos os comprovantes de pagamento
• Solicite documentação por escrito
• Verifique se nova escola aceita transferência
• Negocie prazos se necessário

**Rescisão por Inadimplência:**
• **Prazo**: Escola deve dar oportunidade de regularização
• **Comunicação**: Por escrito com prazo para pagamento
• **Proporcionalidade**: Consequência proporcional ao débito
• **Documentação**: Mesmo com débito, deve fornecer

**⚖️ Base Legal:**
CDC sobre direito de cancelamento e Lei 9.870/99 sobre anuidades escolares.

Precisa cancelar matrícula, fazer transferência ou está enfrentando dificuldades nesse processo?"""
        
        if any(word in question_lower for word in ['superior', 'universidade', 'faculdade', 'graduação', 'pós']):
            return """🎓 **Ensino Superior - Contratos Universitários**

**Contratos de Ensino Superior:**

**Características Específicas:**
• **Autonomia**: Instituições têm maior liberdade de preços
• **Semestralidade**: Cobrança por períodos letivos
• **Flexibilidade**: Maior variedade de formas de pagamento
• **Regulamentação**: MEC, INEP e órgãos estaduais

**💰 Mensalidades e Reajustes:**

**Formação de Preços:**
• **Livre**: Não há tabelamento oficial
• **Mercado**: Baseado na concorrência
• **Qualidade**: Relacionado à infraestrutura e corpo docente
• **Modalidade**: Presencial vs. EAD

**Reajustes Anuais:**
• **Liberdade**: Maior que na educação básica
• **Critérios**: Custos operacionais e inflação
• **Aviso**: Mínimo 45 dias de antecedência
• **Contestação**: Possível se abusivo

**📚 Serviços Educacionais:**

**Inclusos na Mensalidade:**
• **Aulas**: Conforme grade curricular
• **Biblioteca**: Acesso ao acervo
• **Laboratórios**: Para aulas práticas
• **Infraestrutura básica**: Salas, banheiros, segurança

**Serviços Extras:**
• **Material didático**: Pode ser cobrado separadamente
• **Atividades complementares**: Eventos, palestras
• **Certificações**: Cursos adicionais
• **Estacionamento**: Geralmente cobrado à parte

**🎯 Modalidades de Curso:**

**Presencial:**
• **Frequência**: Obrigatória conforme LDB
• **Infraestrutura**: Salas, laboratórios, biblioteca
• **Corpo docente**: Titulação adequada
• **Avaliação MEC**: Conceito do curso

**EAD (Ensino à Distância):**
• **Plataforma**: Ambiente virtual de aprendizagem
• **Tutoria**: Suporte pedagógico online
• **Provas**: Presenciais em polos credenciados
• **Diploma**: Mesmo valor que presencial

**Semipresencial:**
• **Híbrido**: Aulas presenciais + online
• **Flexibilidade**: Adequado para trabalhadores
• **Polos**: Pontos de apoio regionais
• **Tecnologia**: Recursos digitais integrados

**🛡️ Direitos do Estudante:**

**Qualidade do Ensino:**
• **Professores qualificados**: Titulação mínima exigida
• **Infraestrutura adequada**: Conforme projeto pedagógico
• **Biblioteca atualizada**: Acervo suficiente
• **Laboratórios equipados**: Para cursos que exigem

**Transparência:**
• **Projeto pedagógico**: Disponível para consulta
• **Grade curricular**: Clara e detalhada
• **Corpo docente**: Qualificação informada
• **Conceito MEC**: Nota da avaliação oficial

**⚠️ Problemas Comuns:**

**Qualidade Inadequada:**
• **Professores sem qualificação**: Abaixo do exigido pelo MEC
• **Infraestrutura deficiente**: Laboratórios sem equipamentos
• **Biblioteca inadequada**: Acervo insuficiente
• **Irregularidades**: Funcionamento sem autorização

**Questões Financeiras:**
• **Reajustes abusivos**: Acima da capacidade de pagamento
• **Cobrança irregular**: Serviços não contratados
• **Falta de transparência**: Valores não informados claramente
• **Descumprimento**: Serviços pagos não prestados

**💡 Dicas para Escolha:**
• Verifique conceito do curso no MEC
• Visite as instalações antes da matrícula
• Pesquise empregabilidade dos egressos
• Compare custo-benefício entre instituições

**📋 Programas de Financiamento:**
• **FIES**: Financiamento estudantil governamental
• **ProUni**: Bolsas em instituições privadas
• **Bolsas próprias**: Programas da própria instituição
• **Parcelamento**: Negociação direta com a IES

**⚖️ Órgãos Reguladores:**
• **MEC**: Autorização e reconhecimento de cursos
• **INEP**: Avaliação da qualidade (ENADE)
• **Conselhos profissionais**: Para cursos regulamentados
• **PROCON**: Defesa do consumidor

**Base Legal:**
LDB, CDC e regulamentações específicas do MEC.

Está enfrentando problemas com seu curso superior ou precisa de orientação sobre direitos universitários?"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""🎓 **Análise do Contrato Educacional**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Mensalidades e Reajustes:**
• Valor da anuidade e forma de pagamento
• Critérios para reajustes anuais
• Prazo de aviso prévio para aumentos
• Política de desconto para irmãos

**2. Serviços Inclusos:**
• O que está coberto pela mensalidade
• Material didático obrigatório
• Atividades extracurriculares
• Uso de instalações e equipamentos

**3. Matrícula e Rematrícula:**
• Processo de renovação anual
• Taxa de matrícula e reserva de vaga
• Prazo para confirmação
• Condições para transferência

**4. Cancelamento e Transferência:**
• Direito de arrependimento (7 dias)
• Multas por cancelamento
• Documentação para transferência
• Proporcionalidade de valores

**⚖️ Conformidade Legal:**
Este contrato deve seguir CDC, Lei 9.870/99 e regulamentações do MEC.

Posso analisar algum aspecto específico que está causando dúvida?"""
        
        # Resposta geral
        return """🎓 **Educação - Orientação Geral**

Entendi sua pergunta sobre contratos educacionais. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de mensalidades e reajustes
• Orientação sobre matrícula e rematrícula
• Análise de cobrança de material didático
• Direitos em cancelamento e transferência

**⚠️ Problemas Mais Comuns:**
• Reajustes acima da inflação sem justificativa
• Rematrícula automática (proibida por lei)
• Cobrança de material obrigatório na escola
• Dificuldades em transferência de documentos

**🛡️ Seus Direitos Principais:**
• Transparência total nos valores cobrados
• Material didático opcional (salvo exceções)
• Cancelamento com proporcionalidade
• Documentação sem retenção por débitos

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça detalhes do contrato educacional."""