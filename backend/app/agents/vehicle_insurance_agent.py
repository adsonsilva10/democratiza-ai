from app.agents.base_agent import BaseContractAgent

class VehicleInsuranceAgent(BaseContractAgent):
    """Agente especializado em contratos de seguro de veículos"""
    
    def __init__(self):
        self.specialization = "Seguro Veicular"
        self.icon = "🚗"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para seguros de veículos"""
        
        if not question:
            return """🚗 **Seguro Veicular - Análise Especializada**

Olá! Sou especialista em contratos de seguro de veículos. Posso ajudar com:

**📋 Principais Análises:**
• Coberturas obrigatórias vs. opcionais
• Franquia e valor da indenização
• Cláusulas de exclusão de cobertura
• Perfil do condutor e agravamento de risco
• Procedimentos em caso de sinistro

**⚠️ Pontos Críticos:**
• Declarações incorretas podem anular o seguro
• Prazo para comunicar sinistros (geralmente 24h)
• Limitações para condutores não habilitados
• Uso comercial vs. particular do veículo

**📞 Órgão Regulador:**
• SUSEP (Superintendência de Seguros Privados)
• Resolução CNSP nº 416/2021 (seguro auto)

Como posso ajudar com seu seguro veicular?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['cobertura', 'cobrir', 'indenizar', 'indenização']):
            return """🔍 **Coberturas do Seguro Veicular**

**Coberturas Básicas (obrigatórias):**
• Danos materiais a terceiros
• Danos corporais a terceiros
• Danos morais a terceiros (opcional mas recomendada)

**Coberturas Adicionais Comuns:**
• Colisão, incêndio e roubo (mais comum)
• Vidros, faróis e retrovisores
• Carro reserva
• Assistência 24h
• Cobertura para acessórios

**⚠️ Atenção:**
• Verifique o valor da franquia
• Confirme se há carência para algumas coberturas
• Cheque limitações geográficas
• Veja se há restrições por idade do condutor

Precisa de análise específica sobre alguma cobertura?"""
        
        if any(word in question_lower for word in ['franquia', 'participação', 'valor', 'pagar']):
            return """💰 **Franquia no Seguro Veicular**

**O que é a franquia:**
• Valor que você paga em caso de sinistro com culpa
• Não se aplica a terceiros (danos que você causa)
• Reduz o valor da indenização nos casos com cobertura

**Tipos de franquia:**
• **Fixa**: Valor determinado em R$
• **Percentual**: % do valor do veículo
• **Mista**: Combinação dos dois tipos

**⚠️ Pontos Importantes:**
• Franquia reduzida = prêmio maior
• Em caso de perda total, franquia pode não se aplicar
• Verifique se há franquia diferenciada por cobertura
• Cuidado com franquias muito baixas (prêmio alto)

**💡 Dica Legal:**
Pela Circular SUSEP nº 555/2017, a franquia deve ser clara e destacada no contrato.

Tem dúvidas sobre o valor da franquia no seu contrato?"""
        
        if any(word in question_lower for word in ['sinistro', 'acidente', 'batida', 'roubo', 'furto']):
            return """🚨 **Procedimentos em Caso de Sinistro**

**Primeiros passos (primeiras 24h):**
1. Preserve o local se possível
2. Acione a seguradora imediatamente
3. Registre BO se necessário (roubo/furto obrigatório)
4. Não assine nada sem ler
5. Documente com fotos

**Documentos necessários:**
• Carteira de habilitação válida
• CRLV (documento do veículo)
• Apólice de seguro
• Boletim de ocorrência (se aplicável)
• Laudo do IML (em casos graves)

**⚠️ Cuidados Importantes:**
• Não admita culpa no local
• Comunique em até 24h (prazo legal)
• Condutor deve estar habilitado
• Veículo deve estar regularizado

**🛡️ Proteção Legal:**
• Art. 771 do Código Civil sobre boa-fé
• Lei nº 8.078/90 (CDC) se pessoa física

Precisa de orientação sobre algum sinistro específico?"""
        
        if any(word in question_lower for word in ['cancelar', 'cancelamento', 'rescindir', 'rescisão']):
            return """❌ **Cancelamento do Seguro Veicular**

**Cancelamento pela seguradora:**
• Inadimplência do prêmio
• Agravamento do risco não comunicado
• Declarações incorretas comprovadas
• Deve comunicar com 30 dias de antecedência

**Cancelamento pelo segurado:**
• Pode cancelar a qualquer momento
• Direito à devolução proporcional do prêmio
• Deve comunicar por escrito
• Seguradora tem até 30 dias para devolver

**📋 Cálculo da Devolução:**
• Prêmio pago - período utilizado - custos administrativos
• IOF não é devolvido
• Deve ser proporcional ao tempo restante

**⚠️ Atenção:**
• Se houve sinistro, cálculo pode ser diferente
• Leia cláusulas específicas sobre cancelamento
• Guarde comprovantes de comunicação

**🛡️ Base Legal:**
Art. 760 do Código Civil e Circular SUSEP nº 541/2016.

Tem dúvidas sobre cancelamento do seu seguro?"""
        
        if any(word in question_lower for word in ['renovação', 'renovar', 'vencimento', 'prazo']):
            return """🔄 **Renovação do Seguro Veicular**

**Processo de Renovação:**
• Seguradora deve oferecer renovação com 30 dias de antecedência
• Você pode aceitar, negociar ou recusar
• Condições podem ser alteradas na renovação
• Prêmio pode aumentar baseado em sinistralidade

**Fatores que influenciam o novo prêmio:**
• Sinistros no período anterior
• Mudança de perfil (idade, estado civil, etc.)
• Alterações no veículo ou uso
• Mudança de CEP ou garagem

**⚠️ Direitos na Renovação:**
• Receber proposta por escrito
• Prazo mínimo de 15 dias para análise
• Negociar coberturas e franquias
• Buscar outras seguradoras

**💡 Dicas Importantes:**
• Compare com outras seguradoras
• Revise suas necessidades de cobertura
• Verifique histórico de sinistros
• Analise custo x benefício

**🛡️ Base Legal:**
Resolução CNSP nº 416/2021 sobre seguro auto.

Precisa de ajuda com renovação do seguro?"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""🚗 **Análise do Seguro Veicular**

Com base na sua pergunta "{question}" e no contrato fornecido, posso ajudar com análise especializada.

**📋 Principais pontos a verificar em seguros veiculares:**

**1. Coberturas Contratadas:**
• Danos materiais e corporais a terceiros
• Cobertura para o próprio veículo (colisão, incêndio, roubo)
• Vidros, lanternas e retrovisores
• Assistência 24 horas

**2. Valores e Franquias:**
• Valor da indenização (tabela FIPE?)
• Valor da franquia por tipo de sinistro
• Limite máximo por cobertura

**3. Exclusões Importantes:**
• Condutores não habilitados
• Uso comercial (se seguro é particular)
• Participação em competições
• Danos por guerra, atos terroristas

**4. Perfil e Declarações:**
• Dados do segurado e condutores
• Local de pernoite do veículo
• Uso do veículo (particular/comercial)
• Dispositivos de segurança

**⚖️ Conformidade Legal:**
Este contrato deve seguir a Resolução CNSP nº 416/2021 e as normas da SUSEP.

Posso fazer uma análise mais específica se você tiver alguma cláusula ou situação particular que gostaria de entender melhor."""
        
        # Resposta geral
        return """🚗 **Seguro Veicular - Orientação Geral**

Entendi sua pergunta sobre seguro veicular. Posso ajudar com:

**📋 Análises Especializadas:**
• Verificação de coberturas obrigatórias e opcionais
• Análise de cláusulas de exclusão
• Orientação sobre franquias e indenizações
• Procedimentos em caso de sinistro

**⚠️ Pontos Críticos Comuns:**
• Declarações incorretas (perfil, CEP, uso do veículo)
• Cláusulas abusivas de exclusão
• Prazos para comunicação de sinistros
• Limitações não informadas claramente

**🛡️ Seus Direitos:**
• Receber cópia da apólice
• Informações claras sobre coberturas
• Atendimento em caso de sinistro
• Recurso à SUSEP em caso de problemas

Para uma análise mais precisa, me forneça mais detalhes sobre sua situação específica ou o texto do contrato."""