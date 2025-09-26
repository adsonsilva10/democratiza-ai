from app.agents.base_agent import BaseContractAgent

class EcommerceAgent(BaseContractAgent):
    """Agente especializado em contratos de e-commerce e compras online"""
    
    def __init__(self):
        self.specialization = "E-commerce"
        self.icon = "🛒"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para e-commerce"""
        
        if not question:
            return """🛒 **E-commerce - Análise Especializada**

Olá! Sou especialista em contratos de e-commerce e compras online. Posso ajudar com:

**📋 Principais Análises:**
• Termos de uso e políticas de privacidade
• Direito de arrependimento (7 dias)
• Políticas de troca e devolução
• Garantias de produtos online
• Marketplaces e vendedores terceiros

**⚠️ Pontos Críticos:**
• Cláusulas abusivas nos termos de uso
• Dificuldades no direito de arrependimento
• Problemas com entregas e prazos
• Segurança de dados pessoais

**🏪 Órgãos de Defesa:**
• PROCON - Defesa do consumidor
• SENACON - Secretaria Nacional do Consumidor
• Marco Civil da Internet

Como posso ajudar com sua compra ou contrato online?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['arrependimento', 'cancelar', 'devolver', '7 dias', 'desistir']):
            return """↩️ **Direito de Arrependimento no E-commerce**

**Marco Legal - CDC Art. 49:**
*"O consumidor pode desistir do contrato, no prazo de 7 dias corridos, a contar de sua assinatura ou do ato de recebimento do produto ou serviço, sempre que a contratação de fornecimento de produtos e serviços ocorrer fora do estabelecimento comercial, especialmente por telefone ou a domicílio."*

**📅 Prazo de 7 Dias:**

**Início da Contagem:**
• **Produtos**: Recebimento pelo consumidor ou terceiro indicado
• **Serviços**: Contratação ou início da prestação
• **Dias corridos**: Inclui sábados, domingos e feriados
• **Marco**: 24h do último dia (meia-noite)

**Como Exercer o Direito:**
• **Comunicação**: Por qualquer meio (email, chat, telefone)
• **Por escrito**: Recomendado para prova
• **Motivo**: Não precisa justificar
• **Produto**: Deve estar em condições originais

**🛡️ Seus Direitos:**
• Devolução integral do valor pago
• Estorno em até 10 dias corridos
• Frete de devolução por conta do vendedor
• Produto danificado na entrega: prazo não conta

**⚠️ Exceções ao Direito de Arrependimento:**

**Produtos Não Elegíveis:**
• **Personalizados**: Feitos sob encomenda
• **Perecíveis**: Alimentos, medicamentos
• **Íntimos**: Produtos de higiene íntima
• **Digitais**: Software, e-books (após download)
• **Lacrados**: CDs, DVDs abertos

**Serviços Não Elegíveis:**
• **Já executados**: Com concordância expressa do consumidor
• **Emergenciais**: Reparos urgentes
• **Eventos**: Ingressos com data específica

**💰 Devolução de Valores:**

**Estorno Integral:**
• **Produto**: Valor total pago
• **Frete**: De ida e volta
• **Taxas**: Todas as cobranças
• **Prazo**: Até 10 dias corridos

**Forma de Devolução:**
• **Mesmo meio**: Do pagamento original
• **Cartão de crédito**: Estorno na fatura
• **Boleto/PIX**: Depósito em conta
• **Dinheiro**: Se pago em espécie

**📦 Estado do Produto:**

**Condições para Devolução:**
• **Embalagem original**: Se possível, manter
• **Acessórios**: Todos os itens inclusos
• **Funcionamento**: Produto deve funcionar normalmente
• **Uso mínimo**: Para testar apenas

**Produto Danificado:**
• **Culpa do transporte**: Direito mantido
• **Uso excessivo**: Pode perder direito
• **Teste normal**: Não prejudica direito
• **Desgaste natural**: Do manuseio para teste

**🚚 Logística da Devolução:**

**Responsabilidades:**
• **Vendedor**: Autorizar devolução
• **Frete**: Custo da empresa (ida e volta)
• **Retirada**: Agendar coleta
• **Prazo**: Para processar devolução

**Processo Recomendado:**
• **1º**: Comunicar desistência por escrito
• **2º**: Solicitar autorização de devolução
• **3º**: Aguardar orientações sobre envio
• **4º**: Acompanhar estorno

**💡 Dicas Importantes:**
• Fotografe produto ao receber
• Guarde email de confirmação da desistência
• Use transportadora com rastreamento
• Mantenha produto em condições originais

**🛒 Marketplaces:**
• **Responsabilidade**: Solidária com vendedor
• **Processo**: Mesmo direito de arrependimento
• **Suporte**: Plataforma deve mediar
• **Proteção**: Programas de proteção ao comprador

**⚖️ Problemas Comuns:**
• **Recusa**: Vendedor não aceita devolução
• **Demora**: Estorno além de 10 dias
• **Frete**: Tentativa de cobrar do consumidor
• **Condições**: Exigências abusivas

**📞 Se Houver Problemas:**
• **Plataforma**: Acionar suporte primeiro
• **PROCON**: Se não resolver amigavelmente
• **Protocolo**: Documentar todas as tentativas
• **Judiciário**: Juizado Especial Cível

**Base Legal:**
CDC Art. 49 e Decreto 7.962/13 sobre comércio eletrônico.

Está enfrentando dificuldades para exercer seu direito de arrependimento?"""
        
        if any(word in question_lower for word in ['entrega', 'prazo', 'frete', 'correio', 'transportadora']):
            return """🚚 **Entrega e Prazos no E-commerce**

**Prazos de Entrega:**

**Informação Obrigatória:**
• **Antes da compra**: Prazo deve estar claro
• **Região**: Pode variar por localização
• **Tipo de produto**: Prazos diferentes conforme item
• **Frete**: Valor e prazo informados

**⏰ Contagem de Prazos:**
• **Dias úteis**: Segunda a sexta, exceto feriados
• **Início**: Confirmação do pagamento
• **Postagem**: Não é entrega
• **Tentativas**: Múltiplas tentativas contam

**📦 Modalidades de Frete:**

**Frete Grátis:**
• **Marketing**: Estratégia comercial
• **Valor**: Embutido no preço do produto
• **Prazo**: Pode ser maior que frete pago
• **Condições**: Valor mínimo ou região

**Frete Expresso:**
• **Velocidade**: Entrega mais rápida
• **Custo**: Valor adicional
• **Garantia**: Prazo mais confiável
• **Rastreamento**: Acompanhamento em tempo real

**PAC/SEDEX:**
• **Correios**: Principal transportadora
• **Prazos**: Conforme tabela oficial
• **Rastreamento**: Código fornecido
• **Seguro**: Opcional para valores altos

**⚠️ Atraso na Entrega:**

**Seus Direitos:**
• **Cancelamento**: Após prazo sem justificativa
• **Desconto**: Abatimento proporcional
• **Indenização**: Por danos morais (casos graves)
• **Nova tentativa**: Prazo razoável adicional

**Prazos para Reclamar:**
• **Imediatamente**: Após vencimento do prazo
• **30 dias**: Para produtos não duráveis
• **90 dias**: Para produtos duráveis
• **5 anos**: Para danos morais

**🏠 Problemas na Entrega:**

**Endereço Incorreto:**
• **Responsabilidade**: Do consumidor se erro for seu
• **Correção**: Possível durante trajeto
• **Nova entrega**: Pode gerar custo adicional
• **Devolução**: Se não for possível entregar

**Ausência no Recebimento:**
• **Tentativas**: Transportadora deve fazer múltiplas
• **Vizinho**: Só com autorização expressa
• **Agência**: Retirada em ponto de coleta
• **Prazo**: Para retirada antes da devolução

**Produto Danificado:**
• **Recusa**: Direito de não receber
• **Foto**: Documentar danos na presença do entregador
• **Troca**: Imediata sem custo
• **Responsabilidade**: Da loja/transportadora

**📱 Rastreamento:**

**Código de Rastreio:**
• **Fornecimento**: Obrigatório após postagem
• **Acompanhamento**: Em tempo real
• **Status**: Atualizações do trajeto
• **Problemas**: Identificação de falhas

**Informações no Rastreamento:**
• **Postado**: Produto saiu da loja
• **Em trânsito**: No caminho
• **Saiu para entrega**: Dia da entrega
• **Entregue**: Confirmação final

**💡 Dicas para Entrega:**

**Prevenção de Problemas:**
• Confira endereço cuidadosamente
• Mantenha telefone atualizado
• Acompanhe rastreamento regularmente
• Esteja disponível no prazo informado

**Recebimento Seguro:**
• Confira produto antes de assinar
• Verifique se é realmente seu pedido
• Documente problemas imediatamente
• Guarde comprovante de entrega

**🏢 Entrega Corporativa:**
• **Portaria**: Pode receber por você
• **Autorização**: Por escrito se necessário
• **Horário comercial**: Mais facilidade
• **Responsabilidade**: Da empresa receptora

**📞 Problemas com Entrega:**
• **Transportadora**: Contato direto primeiro
• **Loja**: Se transportadora não resolver
• **Correios**: 0800-725-7282 para seus serviços
• **PROCON**: Para problemas não resolvidos

**⚖️ Base Legal:**
CDC sobre prazo de entrega e Decreto 7.962/13 sobre e-commerce.

Está com problemas de entrega ou atraso no seu pedido?"""
        
        if any(word in question_lower for word in ['marketplace', 'mercadolivre', 'amazon', 'magazineluiza', 'terceiro']):
            return """🏪 **Marketplaces e Vendedores Terceiros**

**O que são Marketplaces:**
• **Plataforma**: Espaço virtual para múltiplos vendedores
• **Intermediação**: Facilita vendas entre terceiros e consumidores
• **Exemplos**: Mercado Livre, Amazon, Magazine Luiza, Americanas
• **Vendedores**: Pessoas físicas ou jurídicas independentes

**📋 Responsabilidades:**

**Do Marketplace:**
• **Informações**: Dados claros sobre vendedores
• **Segurança**: Proteção da transação
• **Suporte**: Mediação em conflitos
• **Responsabilidade solidária**: Por problemas na venda

**Do Vendedor Terceiro:**
• **Produto**: Qualidade e conformidade
• **Entrega**: Prazo e condições
• **Garantia**: Cumprimento da lei
• **Atendimento**: Suporte pós-venda

**🛡️ Proteção ao Consumidor:**

**Responsabilidade Solidária:**
• **Marketplace responde**: Junto com vendedor
• **Facilitação**: Para resolução de problemas
• **Garantias**: Mesmas da loja física
• **Cobrança**: De qualquer um dos dois

**Programas de Proteção:**
• **Mercado Livre**: Mercado Pago + Proteção
• **Amazon**: A-Z Guarantee
• **Magazine Luiza**: Proteção Magalu
• **Americanas**: Proteção Ame

**⚠️ Cuidados na Compra:**

**Avaliação do Vendedor:**
• **Reputação**: Histórico de vendas
• **Comentários**: Experiências de outros compradores
• **Tempo**: Há quanto tempo vende na plataforma
• **Produtos**: Variedade e especialização

**Informações Obrigatórias:**
• **CNPJ/CPF**: Identificação do vendedor
• **Endereço**: Localização física
• **Contato**: Telefone e email
• **Política**: Troca, devolução e garantia

**🔍 Red Flags - Sinais de Alerta:**
• **Preços muito baixos**: Desconfie de ofertas irreais
• **Sem avaliações**: Vendedor muito novo
• **Avaliações negativas**: Muitas reclamações
• **Informações vagas**: Produto mal descrito

**💳 Segurança no Pagamento:**

**Sistemas Seguros:**
• **Mercado Pago**: Proteção nas transações
• **PagSeguro**: Segurança UOL
• **Paypal**: Proteção internacional
• **Cartão na plataforma**: Dados protegidos

**⚠️ Evitar:**
• **Transferência direta**: TED, DOC fora da plataforma
• **Boleto de terceiros**: Não emitido pela plataforma
• **PIX direto**: Sem proteção da plataforma
• **Dinheiro**: Pagamento em espécie

**📦 Entrega e Logística:**

**Fulfillment:**
• **Amazon**: Produtos vendidos por terceiros, entregues pela Amazon
• **Mercado Envios**: Logística do Mercado Livre
• **Vantagens**: Prazo e confiabilidade
• **Rastreamento**: Sistema integrado

**Entrega Própria:**
• **Vendedor**: Responsável pela logística
• **Maior risco**: Menos garantias
• **Verificação**: Dados da transportadora
• **Prazo**: Pode ser menos confiável

**🛠️ Resolução de Problemas:**

**Ordem de Contato:**
• **1º**: Vendedor diretamente
• **2º**: Suporte da plataforma
• **3º**: Órgãos de defesa (PROCON)
• **4º**: Via judicial

**Mediação da Plataforma:**
• **Sistema interno**: Abertura de disputa
• **Prazos**: Para resolução
• **Evidências**: Fotos, conversas, comprovantes
• **Decisão**: Estorno ou outras soluções

**💡 Dicas para Compra Segura:**

**Antes de Comprar:**
• Leia descrição completa do produto
• Verifique reputação do vendedor
• Compare preços com outras lojas
• Confirme política de troca

**Durante a Compra:**
• Use sistema de pagamento da plataforma
• Salve todas as informações da transação
• Confirme endereço de entrega
• Guarde número do pedido

**Após a Compra:**
• Acompanhe rastreamento
• Confira produto ao receber
• Avalie vendedor honestamente
• Guarde comprovantes

**⚖️ Direitos Específicos:**
• **Mesmo CDC**: Todos os direitos mantidos
• **Arrependimento**: 7 dias normalmente
• **Garantia**: Conforme tipo de produto
• **Resolução**: Plataforma deve facilitar

**Base Legal:**
CDC, Lei 12.965/14 (Marco Civil) e regulamentações específicas.

Está com problemas em marketplace ou dúvidas sobre vendedor terceirizado?"""
        
        if any(word in question_lower for word in ['dados', 'privacidade', 'lgpd', 'informações', 'cadastro']):
            return """🔐 **Proteção de Dados e Privacidade no E-commerce**

**Marco Legal - LGPD:**
*Lei Geral de Proteção de Dados Pessoais (Lei 13.709/18) regulamenta tratamento de dados pessoais no Brasil, incluindo e-commerce.*

**📊 Tipos de Dados Coletados:**

**Dados Pessoais Básicos:**
• **Identificação**: Nome, CPF, RG
• **Contato**: Email, telefone, endereço
• **Financeiros**: Cartão de crédito, conta bancária
• **Comportamentais**: Histórico de compras, navegação

**Dados Sensíveis:**
• **Biométricos**: Impressão digital, reconhecimento facial
• **Saúde**: Para produtos farmacêuticos/médicos
• **Localização**: GPS, endereço IP
• **Preferências**: Orientação sexual, política, religião

**🛡️ Seus Direitos (LGPD):**

**Acesso e Transparência:**
• **Saber quais dados**: São coletados sobre você
• **Finalidade**: Para que são utilizados
• **Compartilhamento**: Com quem são divididos
• **Tempo**: Por quanto tempo ficam armazenados

**Controle dos Dados:**
• **Correção**: Atualizar dados incorretos
• **Exclusão**: Deletar dados desnecessários
• **Portabilidade**: Transferir para outro fornecedor
• **Oposição**: Recusar tratamento em certas situações

**⚠️ Consentimento:**

**Deve ser:**
• **Livre**: Sem coação
• **Informado**: Com explicação clara
• **Específico**: Para finalidade determinada
• **Inequívoco**: Sem dubiedade

**Pode ser Revogado:**
• **A qualquer momento**: Direito de mudar de ideia
• **Facilmente**: Processo simples
• **Sem penalização**: Não pode haver prejuízo
• **Gratuito**: Sem cobrança

**🍪 Cookies e Rastreamento:**

**Tipos de Cookies:**
• **Necessários**: Funcionamento básico do site
• **Funcionais**: Melhorar experiência do usuário
• **Analíticos**: Entender comportamento
• **Marketing**: Publicidade direcionada

**Seus Direitos:**
• **Aceitar ou recusar**: Cookies não essenciais
• **Configurar**: Quais tipos permitir
• **Excluir**: Remover cookies existentes
• **Informação clara**: Sobre cada tipo

**📧 Marketing e Comunicação:**

**Email Marketing:**
• **Opt-in**: Autorização expressa obrigatória
• **Opt-out**: Descadastro fácil e gratuito
• **Frequência**: Não pode ser excessiva
• **Conteúdo**: Relevante para o consumidor

**Spam e Comunicações Indesejadas:**
• **Proibição**: Sem autorização prévia
• **Multa**: Para empresas que enviam spam
• **Descadastro**: Imediato quando solicitado
• **Bloqueio**: Direito do consumidor

**🔒 Segurança dos Dados:**

**Medidas Obrigatórias:**
• **Criptografia**: Proteção durante transmissão
• **Armazenamento seguro**: Servidores protegidos
• **Acesso restrito**: Apenas pessoal autorizado
• **Backup**: Cópias de segurança

**Vazamento de Dados:**
• **Notificação**: ANPD em até 72h
• **Comunicação**: Ao titular se houver risco
• **Medidas**: Para conter o vazamento
• **Responsabilização**: Da empresa

**💡 Dicas de Proteção:**

**Para o Consumidor:**
• Leia política de privacidade
• Configure cookies conforme preferência
• Use senhas fortes e únicas
• Monitore movimentação financeira

**Verificações Importantes:**
• **HTTPS**: Site com certificado de segurança
• **Política clara**: Privacidade acessível
• **Contato DPO**: Data Protection Officer
• **Reputação**: Da empresa no mercado

**📞 Violação de Direitos:**

**ANPD (Autoridade Nacional):**
• **Canal oficial**: Para denúncias LGPD
• **Investigação**: Apura violações
• **Multas**: Até 2% do faturamento
• **Orientação**: Sobre direitos

**PROCON:**
• **Relação consumo**: Práticas abusivas
• **Mediação**: Conflitos com empresas
• **Multas**: Por descumprimento CDC
• **Orientação**: Direitos do consumidor

**⚖️ Política de Privacidade:**

**Deve Conter:**
• **Dados coletados**: Tipos e finalidades
• **Base legal**: Justificativa para tratamento
• **Compartilhamento**: Com terceiros
• **Direitos**: Como exercer seus direitos
• **Contato**: DPO ou responsável

**Linguagem:**
• **Clara**: Sem juridiquês excessivo
• **Acessível**: Fácil de encontrar
• **Atualizada**: Conforme práticas atuais
• **Específica**: Para aquela empresa

**Base Legal:**
LGPD (Lei 13.709/18), CDC e Marco Civil da Internet.

Tem dúvidas sobre como seus dados estão sendo tratados ou quer exercer algum direito LGPD?"""
        
        if any(word in question_lower for word in ['garantia', 'defeito', 'vício', 'troca', 'assistência']):
            return """🛠️ **Garantia e Vícios em Produtos de E-commerce**

**Tipos de Garantia:**

**Garantia Legal:**
• **30 dias**: Produtos não duráveis (alimentos, cosméticos)
• **90 dias**: Produtos duráveis (eletrônicos, eletrodomésticos)
• **Automática**: Independe de termo de garantia
• **Gratuita**: Sem custo para o consumidor

**Garantia Contratual:**
• **Adicional**: Complementa a legal
• **Prazo variável**: Conforme fabricante
• **Documento**: Termo de garantia específico
• **Condições**: Pode ter restrições

**⚠️ Vícios do Produto:**

**Vício Aparente:**
• **Visível**: Detectável no recebimento
• **Prazo**: 30 ou 90 dias para reclamar
• **Contagem**: Da entrega do produto
• **Direito**: Troca, conserto ou devolução

**Vício Oculto:**
• **Não visível**: Só aparece com uso
• **Prazo**: 30 ou 90 dias do surgimento
• **Contagem**: Quando vício se manifesta
• **Prova**: Pode exigir laudo técnico

**🔧 Direitos do Consumidor:**

**Opções Legais (Art. 18 CDC):**
• **1ª opção**: Substituição por produto novo
• **2ª opção**: Restituição do valor pago
• **3ª opção**: Abatimento proporcional do preço

**Prazo para Solução:**
• **30 dias**: Fornecedor tem prazo para resolver
• **Prorrogação**: Até 180 dias se consumidor concordar
• **Vencido prazo**: Consumidor escolhe uma das 3 opções

**🛒 Garantia no E-commerce:**

**Responsabilidades:**
• **Vendedor**: Principal responsável
• **Fabricante**: Solidariamente responsável
• **Marketplace**: Pode ser responsabilizado
• **Importador**: Se produto importado

**Assistência Técnica:**
• **Rede autorizada**: Deve ser informada
• **Prazo**: Máximo 30 dias para reparo
• **Gratuidade**: Durante período de garantia
• **Produto substituto**: Se demora exceder prazo

**📱 Produtos Eletrônicos:**

**Garantia Estendida:**
• **Opcional**: Não obrigatória
• **Adicional**: Além da garantia legal
• **Paga**: Valor extra
• **Condições**: Ler termos cuidadosamente

**Problemas Comuns:**
• **Tela quebrada**: Por queda (não coberto)
• **Defeito de fábrica**: Coberto pela garantia
• **Desgaste natural**: Não é vício
• **Mau uso**: Pode perder garantia

**🏠 Eletrodomésticos:**

**Instalação:**
• **Incluída**: Quando informado na compra
• **Técnico autorizado**: Recomendado
• **Prazo**: Para agendar instalação
• **Problemas**: Na instalação são cobertos

**Peças de Reposição:**
• **Disponibilidade**: Mínimo durante garantia
• **Preço justo**: Não pode ser abusivo
• **Originais**: Preferencialmente
• **Compatíveis**: Alternativa aceita

**💡 Dicas Importantes:**

**Conservar Garantia:**
• Guarde nota fiscal
• Mantenha termo de garantia
• Use conforme instruções
• Não tente reparo próprio

**Documentação:**
• **Fotos**: Do defeito/problema
• **Vídeos**: Funcionamento irregular
• **Laudos**: Técnicos quando necessário
• **Protocolos**: De atendimento

**🔍 Análise Técnica:**

**Quando Necessária:**
• **Disputas**: Sobre causa do problema
• **Produtos complexos**: Eletrônicos, eletrodomésticos
• **Valor alto**: Investimento significativo
• **Recusa**: Do fornecedor em aceitar vício

**Quem Paga:**
• **Vício confirmado**: Fornecedor
• **Mau uso**: Consumidor
• **Duvidoso**: Pode ser dividido
• **Perícia judicial**: Conforme decisão

**📞 Resolução de Problemas:**

**Passo a Passo:**
• **1º**: Contatar vendedor
• **2º**: Rede de assistência técnica
• **3º**: Fabricante/importador
• **4º**: PROCON/Justiça

**Documentação Necessária:**
• **Nota fiscal**: Comprovante da compra
• **Termo garantia**: Se houver
• **Protocolo**: Tentativas de solução
• **Fotos/vídeos**: Evidências do problema

**⚖️ Base Legal:**
CDC Art. 18 a 25 sobre vícios e garantia de produtos.

Está enfrentando problemas com garantia ou defeito em produto comprado online?"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""🛒 **Análise do Contrato de E-commerce**

Com base na sua pergunta "{question}" e nos termos fornecidos, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Direitos do Consumidor:**
• Direito de arrependimento (7 dias)
• Política de trocas e devoluções
• Prazos de entrega
• Garantias oferecidas

**2. Proteção de Dados:**
• Coleta de informações pessoais
• Uso dos dados para marketing
• Compartilhamento com terceiros
• Direitos LGPD do titular

**3. Termos de Uso:**
• Responsabilidades do marketplace
• Regras para vendedores terceiros
• Política de segurança
• Resolução de disputas

**4. Pagamento e Segurança:**
• Métodos de pagamento aceitos
• Proteção contra fraudes
• Política de estorno
• Taxas e encargos

**⚖️ Conformidade Legal:**
Este contrato deve seguir CDC, LGPD e regulamentações de e-commerce.

Posso analisar algum aspecto específico que está causando dúvida?"""
        
        # Resposta geral
        return """🛒 **E-commerce - Orientação Geral**

Entendi sua pergunta sobre e-commerce. Posso ajudar com:

**📋 Análises Especializadas:**
• Direito de arrependimento e devoluções
• Problemas com entrega e prazos
• Questões com marketplaces
• Proteção de dados pessoais (LGPD)

**⚠️ Problemas Mais Comuns:**
• Dificuldade para exercer direito de arrependimento
• Atraso na entrega sem comunicação
• Cobrança de frete na devolução
• Problemas com vendedores terceiros

**🛡️ Seus Direitos Principais:**
• 7 dias para desistir da compra
• Entrega no prazo informado
• Produtos conforme descrição
• Proteção dos seus dados pessoais

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça detalhes do problema."""