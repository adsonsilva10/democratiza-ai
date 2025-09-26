from app.agents.base_agent import BaseContractAgent

class GasAgent(BaseContractAgent):
    """Agente especializado em contratos de fornecimento de gás"""
    
    def __init__(self):
        self.specialization = "Gás"
        self.icon = "🔥"
        
    def generate_response(self, question: str, contract_text: str = "") -> str:
        """Gera resposta especializada para fornecimento de gás"""
        
        if not question:
            return """🔥 **Gás - Análise Especializada**

Olá! Sou especialista em contratos de fornecimento de gás. Posso ajudar com:

**📋 Principais Análises:**
• Gás natural canalizado (distribuidoras)
• GLP - Gás Liquefeito de Petróleo (botijão)
• Tarifas e modalidades de cobrança
• Ligação nova e transferência de titularidade
• Segurança e manutenção

**⚠️ Pontos Críticos:**
• Reajustes tarifários
• Cobrança de taxas irregulares
• Problemas de fornecimento
• Segurança das instalações

**🏭 Órgãos Reguladores:**
• ANP - Agência Nacional do Petróleo
• PROCON - Defesa do consumidor
• Agências estaduais reguladoras

Como posso ajudar com seu contrato de gás?"""
        
        # Análise baseada na pergunta
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['natural', 'canalizado', 'encanado', 'rede']):
            return """🏢 **Gás Natural Canalizado**

**O que é Gás Natural:**
• **Composição**: Principalmente metano (CH₄)
• **Origem**: Combustível fóssil extraído de reservas
• **Distribuição**: Rede de tubulações subterrâneas
• **Usos**: Cocção, aquecimento, indústria

**🏭 Sistema de Distribuição:**

**Cadeia do Gás Natural:**
• **Produção**: Petrobras e outras produtoras
• **Transporte**: Gasodutos de alta pressão
• **Distribuição**: Empresas estaduais (Comgás, CEG, etc.)
• **Consumo**: Residencial, comercial, industrial

**Distribuidoras Principais:**
• **São Paulo**: Comgás
• **Rio de Janeiro**: CEG, CEG Rio
• **Minas Gerais**: Gasmig
• **Bahia**: Bahiagás
• **Ceará**: Cegás

**📊 Modalidades Tarifárias:**

**Residencial:**
• **Tarifa única**: Valor por m³ consumido
• **Progressiva**: Preço aumenta conforme consumo
• **Tarifa mínima**: Valor básico mensal
• **Taxa de disponibilidade**: Manutenção da rede

**Comercial/Industrial:**
• **Interruptível**: Pode ser cortado (menor preço)
• **Firme**: Garantia de fornecimento
• **Take or pay**: Pagar mínimo mesmo sem consumir
• **Negociação**: Preços especiais conforme volume

**💰 Composição da Conta:**

**Valores Fixos:**
• **Tarifa disponibilidade**: Manutenção da rede
• **Taxa ligação**: Amortização do ramal
• **TUSD**: Tarifa Uso Sistema Distribuição
• **Impostos**: ICMS, PIS/COFINS

**Valores Variáveis:**
• **Consumo**: m³ x preço do gás
• **Margem distribuição**: Lucro da distribuidora
• **Transporte**: Custo dos gasodutos
• **Gás**: Preço da molécula

**🛡️ Seus Direitos:**
• Fornecimento contínuo e adequado
• Qualidade do gás conforme especificação
• Medição correta do consumo
• Atendimento de emergência 24h

**⚠️ Reajustes Tarifários:**

**Revisão Periódica:**
• **Prazo**: Geralmente 4-5 anos
• **Critérios**: Custos operacionais, investimentos
• **Audiência pública**: Participação da sociedade
• **Agência reguladora**: Aprovação necessária

**Reajuste Anual:**
• **Índices**: IGP-M, IPCA ou similar
• **Repasse**: Custos de transporte e gás
• **Transparência**: Metodologia deve ser clara
• **Contestação**: Possível junto ao regulador

**🔧 Ligação Nova:**

**Solicitação:**
• **Viabilidade técnica**: Disponibilidade da rede
• **Projeto**: Ramal predial e instalações
• **Orçamento**: Custos de ligação
• **Cronograma**: Prazos para execução

**Custos:**
• **Ramal predial**: Ligação até o imóvel
• **Kit instalação**: Medidor e regulador
• **Vistoria**: Aprovação das instalações
• **Taxa ligação**: Valor administrativo

**📋 Documentação:**
• **Propriedade**: Escritura ou contrato locação
• **Identidade**: RG, CPF do titular
• **Comprovante endereço**: Conta de luz recente
• **ART**: Responsável técnico pelas instalações

**🔍 Segurança do Gás Natural:**

**Características Seguras:**
• **Mais leve que ar**: Dispersa rapidamente
• **Não tóxico**: Não contamina ambiente
• **Sem odor**: Adicionado odorizante para detectar
• **Queima limpa**: Menor poluição

**Cuidados Obrigatórios:**
• **Ventilação**: Ambientes bem arejados
• **Detecção**: Sistemas de alarme recomendados
• **Manutenção**: Instalações revisadas periodicamente
• **Emergência**: 193 (Bombeiros) ou distribuidora

**⚖️ Regulamentação:**
• **ANP**: Regulação nacional do setor
• **Agências estaduais**: Distribuição local
• **ABNT**: Normas técnicas de segurança
• **Portarias**: Regulamentos específicos

**💡 Vantagens do Gás Natural:**
• **Economia**: Geralmente mais barato que GLP
• **Conveniência**: Não acaba, sem troca de botijão
• **Segurança**: Características físicas favoráveis
• **Ambiente**: Menor impacto ambiental

**📞 Atendimento de Emergência:**
• **Vazamento**: Ligue imediatamente para distribuidora
• **24 horas**: Serviço disponível sempre
• **Gratuito**: Atendimento sem custo
• **Evacuação**: Se necessário, abandone local

**Base Legal:**
Lei do Gás (11.909/09) e regulamentações da ANP.

Precisa de orientação sobre ligação nova, tarifas ou problemas com gás natural?"""
        
        if any(word in question_lower for word in ['glp', 'botijão', 'p13', 'liquefeito', 'engarrafado']):
            return """🔥 **GLP - Gás Liquefeito de Petróleo**

**O que é GLP:**
• **Composição**: Propano e Butano liquefeitos
• **Origem**: Refinarias de petróleo e processamento de gás natural
• **Armazenamento**: Botijões pressurizados
• **Usos**: Cocção doméstica, aquecimento, indústria

**⚖️ Regulamentação do GLP:**

**ANP - Agência Nacional:**
• **Preços**: Livres desde 2002 (exceto P13)
• **Qualidade**: Especificação técnica obrigatória
• **Segurança**: Normas de fabricação e distribuição
• **Fiscalização**: Postos de revenda autorizados

**Tipos de Botijões:**
• **P13 (13kg)**: Uso doméstico, preço subsidiado
• **P20 (20kg)**: Uso comercial
• **P45 (45kg)**: Uso industrial/comercial
• **P90 (90kg)**: Grandes consumidores

**💰 Formação de Preços:**

**P13 Subsidiado:**
• **Política pública**: Subsídio federal para famílias de baixa renda
• **Auxílio Gás**: Vale-gás para beneficiários do Auxílio Brasil
• **Preço controlado**: Limite máximo nacional
• **Distribuidoras**: Reembolso do subsídio pelo governo

**GLP Comercial (P20, P45):**
• **Preço livre**: Definido pelo mercado
• **Competição**: Entre distribuidoras e revendedores
• **Variação regional**: Conforme logística local
• **Negociação**: Possível para grandes volumes

**🏪 Comércio de GLP:**

**Distribuidoras Autorizadas:**
• **Ultragaz**: Líder nacional
• **Liquigás**: Petrobras Distribuidora
• **Supergasbras**: Rede nacional
• **Nacional Gás**: Distribuidora regional
• **Copagaz**: Atuação regional

**Pontos de Venda:**
• **Revendedores**: Lojas especializadas
• **Supermercados**: Venda no varejo
• **Postos combustível**: Alguns comercializam
• **Entrega domiciliar**: Serviço das distribuidoras

**🛡️ Direitos do Consumidor:**

**Qualidade do Produto:**
• **Especificação ANP**: Composição correta
• **Peso líquido**: 13kg para P13
• **Validade**: Sem prazo de validade (produto não perecível)
• **Teste qualidade**: Direito de verificação

**Segurança:**
• **Botijão íntegro**: Sem vazamentos ou danos
• **Lacre inviolado**: Selo de segurança
• **Válvula funcionando**: Abertura e fechamento adequados
• **Troca gratuita**: Botijões com defeito

**⚠️ Cuidados de Segurança:**

**Instalação Correta:**
• **Local arejado**: Nunca em locais fechados
• **Distância**: Longe de fontes de calor
• **Posição vertical**: Botijão sempre em pé
• **Mangueira**: Certificada e em bom estado

**Detecção de Vazamentos:**
• **Odor característico**: Cheiro forte adicionado
• **Teste água e sabão**: Nas conexões
• **Não usar fogo**: Para testar vazamento
• **Emergência**: Fechar registro e ventilar

**🔧 Manutenção e Troca:**

**Vida Útil Equipamentos:**
• **Botijão**: 15-20 anos (verificar data)
• **Regulador**: 5 anos ou conforme manual
• **Mangueira**: 2-5 anos dependendo do tipo
• **Válvula**: Verificar funcionamento regularmente

**Sinais de Troca:**
• **Ferrugem**: Botijão oxidado
• **Amassados**: Deformações significativas
• **Vazamentos**: Nas válvulas ou conexões
• **Data vencida**: Conforme estampagem

**💡 Dicas de Economia:**

**Uso Eficiente:**
• **Regulagem chama**: Azul e estável
• **Panelas adequadas**: Fundo largo e plano
• **Tampa nas panelas**: Acelera cozimento
• **Manutenção fogão**: Bicos limpos e regulados

**Compra Inteligente:**
• **Compare preços**: Entre diferentes pontos de venda
• **Promoções**: Descontos para pagamento à vista
• **Fidelidade**: Programas de pontuação
• **Entrega**: Custo-benefício vs. buscar

**📊 Consumo Médio:**
• **Família 4 pessoas**: 1 P13 por mês (uso só cocção)
• **Casal**: 1 P13 a cada 45-60 dias
• **Pessoa sozinha**: 1 P13 a cada 2-3 meses
• **Uso intenso**: Inclui aquecimento de água

**🏢 Uso Comercial:**

**P20/P45 para Negócios:**
• **Restaurantes**: Múltiplos botijões
• **Padarias**: Fornos industriais
• **Lavanderia**: Secadoras a gás
• **Preço**: Negociação direta com distribuidora

**Central de Gás:**
• **Múltiplos botijões**: Sistema centralizado
• **Troca automática**: Sem interrupção
• **Segurança**: Instalação externa
• **Manutenção**: Técnico especializado

**📞 Em Caso de Problemas:**
• **Vazamento**: Feche o registro, ventile, chame bombeiros
• **Defeito no botijão**: Troque no local da compra
• **Reclamações**: PROCON ou ANP
• **Emergência**: 193 (Bombeiros)

**Base Legal:**
Regulamentações ANP e normas ABNT de segurança.

Está com dúvidas sobre GLP, segurança ou problemas com fornecedor?"""
        
        if any(word in question_lower for word in ['tarifa', 'conta', 'cobrança', 'valor', 'reajuste']):
            return """💰 **Tarifas e Cobrança de Gás**

**Gás Natural - Estrutura Tarifária:**

**Componentes da Tarifa:**
• **Gás**: Custo da molécula (commodity)
• **Transporte**: Uso dos gasodutos
• **Distribuição**: Margem da distribuidora local
• **Impostos**: ICMS, PIS/COFINS

**💡 Modalidades Tarifárias:**

**Residencial:**
• **Tarifa volumétrica**: Preço por m³ consumido
• **Tarifa mínima**: Valor básico mensal
• **Faixas progressivas**: Preço aumenta com consumo
• **Taxa disponibilidade**: Custo da infraestrutura

**Comercial/Industrial:**
• **Firme**: Fornecimento garantido (mais caro)
• **Interruptível**: Pode ser cortado (mais barato)
• **Take or pay**: Pagamento de mínimo garantido
• **Sazonalidade**: Preços diferentes por período

**📊 Composição da Conta de Gás Natural:**

**Valores Fixos:**
• **Tarifa de disponibilidade**: R$ 15-50/mês (varia por região)
• **Taxa de ligação**: Amortização do ramal predial
• **Assinatura básica**: Custo operacional mínimo
• **Multa/juros**: Se houver atraso

**Valores Variáveis:**
• **Consumo medido**: m³ x tarifa unitária
• **TUSD**: Tarifa Uso Sistema Distribuição
• **Tributos**: Proporcionais ao consumo
• **Ajustes**: Revisões tarifárias anteriores

**⚖️ Reajustes Tarifários:**

**Tipos de Reajuste:**
• **Anual**: IGP-M ou IPCA + fator X
• **Revisão**: A cada 4-5 anos (mais ampla)
• **Extraordinário**: Mudanças significativas de custo
• **Repasse**: Variação preço do gás na origem

**Metodologia:**
• **Agência reguladora**: Define critérios
• **Audiência pública**: Participação sociedade
• **Base de custos**: Análise detalhada
• **Modicidade**: Tarifa justa para consumidor

**🔥 GLP - Formação de Preços:**

**P13 (Botijão 13kg):**
• **Preço subsidiado**: Para baixa renda
• **Auxílio Gás**: R$ 51 (valor 2024)
• **Preço máximo**: Controlado pelo governo
• **Variação regional**: Conforme distribuição

**GLP Comercial:**
• **Preço livre**: Definido pelo mercado
• **Competição**: Entre distribuidoras
• **Margem revenda**: Do ponto de venda
• **Logística**: Custo transporte incluso

**💳 Formas de Pagamento:**

**Gás Natural:**
• **Débito automático**: Desconto na tarifa
• **Boleto bancário**: Vencimento mensal
• **PIX**: Pagamento instantâneo
• **Casas lotéricas**: Rede de atendimento

**GLP:**
• **À vista**: Desconto comum
• **Cartão**: Débito ou crédito
• **Vale-gás**: Para beneficiários sociais
• **Fiado**: Em alguns estabelecimentos

**⚠️ Problemas Comuns na Cobrança:**

**Conta Alta:**
• **Vazamento**: Verificar instalações
• **Leitura errada**: Conferir medidor
• **Tarifa**: Mudança de modalidade
• **Consumo real**: Aparelhos novos/pessoas

**Cobranças Irregulares:**
• **Taxas indevidas**: Não previstas em contrato
• **Juros abusivos**: Acima do permitido
• **Religação**: Cobrança excessiva
• **Vistoria**: Não pode ser cobrada

**🛡️ Direitos na Cobrança:**

**Transparência:**
• **Conta detalhada**: Discriminação dos valores
• **Histórico consumo**: Comparação meses anteriores
• **Tarifa aplicada**: Modalidade e valor unitário
• **Impostos**: Discriminação por tipo

**Contestação:**
• **Prazo**: 30 dias da data de vencimento
• **Revisão**: Leitura e cálculos
• **Suspensão**: Cobrança contestada
• **Prova**: Ônus da distribuidora

**💡 Dicas para Economizar:**

**Gás Natural:**
• **Uso consciente**: Evitar desperdícios
• **Manutenção**: Equipamentos regulados
• **Horário**: Alguns contratos têm tarifa diferenciada
• **Modalidade**: Avaliar mudança se aplicável

**GLP:**
• **Comparar preços**: Entre pontos de venda
• **Compra antecipada**: Promoções sazonais
• **Uso eficiente**: Regulagem adequada da chama
• **Manutenção**: Fogão bem regulado

**📞 Para Reclamar:**
• **Distribuidora**: Central atendimento primeiro
• **Agência reguladora**: Se não resolver
• **PROCON**: Problemas contratuais
• **ANP**: Questões de qualidade/preço

**⚖️ Base Legal:**
Lei do Gás, regulamentações ANP e contratos de concessão.

Está com problemas na conta de gás ou dúvidas sobre tarifas?"""
        
        if any(word in question_lower for word in ['ligação', 'nova', 'instalação', 'ramal', 'medidor']):
            return """🔧 **Ligação Nova e Instalação de Gás**

**Gás Natural - Ligação Nova:**

**Verificação de Disponibilidade:**
• **Rede próxima**: Verificar se há rede na região
• **Viabilidade técnica**: Análise da distribuidora
• **Pressão adequada**: Capacidade de atendimento
• **Consulta online**: Site da distribuidora local

**📋 Documentação Necessária:**

**Pessoa Física:**
• **Identidade**: RG e CPF do solicitante
• **Comprovante renda**: Para análise de crédito
• **Comprovante residência**: Conta de luz recente
• **Propriedade**: Escritura, contrato locação ou autorização

**Pessoa Jurídica:**
• **CNPJ**: Cartão ou contrato social
• **Representante legal**: Documentos do responsável
• **Comprovante endereço**: Conta em nome da empresa
• **Licenças**: Alvará funcionamento se necessário

**🏗️ Projeto e Instalação:**

**Ramal Predial:**
• **Projeto**: Elaborado pela distribuidora
• **Escavação**: Da rede até o imóvel
• **Tubulação**: Conforme normas técnicas
• **Teste**: Pressão e estanqueidade

**Instalação Interna:**
• **Responsabilidade**: Do consumidor
• **Projeto ART**: Profissional habilitado
• **Materiais**: Certificados pelo INMETRO
• **Vistoria**: Aprovação pela distribuidora

**💰 Custos de Ligação:**

**Gás Natural:**
• **Ramal padrão**: R$ 1.500 a R$ 5.000 (varia por região)
• **Ramal especial**: Custos adicionais conforme distância
• **Kit instalação**: Medidor, regulador, válvulas (R$ 800-1.500)
• **Taxa ligação**: Valor administrativo (R$ 100-300)

**Parcelamento:**
• **Entrada**: Geralmente 30-50%
• **Prestações**: Até 24-36x na conta de gás
• **Juros**: Conforme política da distribuidora
• **Antecipação**: Desconto para pagamento à vista

**⏰ Prazos de Execução:**

**Cronograma Típico:**
• **Orçamento**: 5-10 dias úteis
• **Aprovação**: Projeto interno (5-15 dias)
• **Execução ramal**: 15-30 dias úteis
• **Vistoria final**: 5-10 dias úteis
• **Ligação**: Imediatamente após aprovação

**Fatores que Afetam Prazo:**
• **Complexidade**: Distância da rede
• **Licenças**: Prefeitura, concessionárias
• **Interferências**: Outras redes subterrâneas
• **Clima**: Chuvas podem atrasar obras

**🔍 Instalações Internas:**

**Projeto Obrigatório:**
• **Responsável técnico**: Engenheiro ou técnico habilitado
• **ART/TRT**: Registro no conselho profissional
• **Normas ABNT**: NBR 15526 e outras aplicáveis
• **Memorial descritivo**: Detalhamento técnico

**Componentes Básicos:**
• **Medidor**: Equipamento da distribuidora
• **Regulador primário**: Redução de pressão
• **Tubulação interna**: Cobre ou aço
• **Válvulas**: Bloqueio e segurança
• **Ventilação**: Adequada aos ambientes

**🛡️ Segurança na Instalação:**

**Normas Obrigatórias:**
• **NBR 15526**: Redes internas gás combustível
• **NBR 13103**: Adequação de ambientes
• **NBR 14570**: Instalações prediais gás natural
• **NR-13**: Caldeiras e vasos pressão (industrial)

**Itens de Segurança:**
• **Detector de gás**: Recomendado
• **Válvula corte**: Bloqueio emergência
• **Ventilação natural**: Permanente
• **Identificação**: Tubulação sinalizada

**🏠 GLP - Instalação Central:**

**Central de Gás:**
• **Múltiplos botijões**: P45 ou P90
• **Troca automática**: Sem interrupção
• **Local externo**: Ventilado e protegido
• **Rede interna**: Distribuição para pontos

**Vantagens:**
• **Autonomia**: Maior reserva de gás
• **Conveniência**: Sem troca frequente
• **Segurança**: Botijões fora de casa
• **Economia**: Menor preço P45/P90

**💡 Dicas Importantes:**

**Antes da Instalação:**
• Compare orçamentos entre empresas
• Verifique qualificação do profissional
• Confirme garantia dos serviços
• Planeje locais dos equipamentos

**Durante a Obra:**
• Acompanhe execução conforme projeto
• Exija uso de materiais certificados
• Documente etapas com fotos
• Teste todos os pontos de consumo

**📞 Suporte e Atendimento:**
• **Distribuidora**: Para questões técnicas
• **Instalador**: Garantia dos serviços
• **Fiscal Prefeitura**: Para aprovações
• **Bombeiros**: Em emergências

**⚖️ Base Legal:**
Normas ABNT, regulamentações ANP e código de obras municipal.

Precisa de orientação sobre ligação nova ou instalação de gás?"""
        
        if any(word in question_lower for word in ['emergência', 'vazamento', 'segurança', 'acidente']):
            return """🚨 **Segurança e Emergências com Gás**

**🔥 Características do Gás:**

**Gás Natural:**
• **Mais leve que ar**: Dispersa rapidamente para cima
• **Não tóxico**: Não contamina o ambiente
• **Limite inflamabilidade**: 5% a 15% no ar
• **Odorização**: Mercaptana adicionada para detectar

**GLP:**
• **Mais pesado que ar**: Acumula em locais baixos
• **Concentração**: Perigosa em ambientes fechados
• **Limite inflamabilidade**: 1,8% a 9,5% no ar
• **Odor característico**: Facilita detecção

**⚠️ Sinais de Vazamento:**

**Como Identificar:**
• **Odor forte**: Cheiro característico de gás
• **Som de escape**: Assobio ou sibilar
• **Vegetação**: Plantas murchas próximas à rede
• **Bolhas**: Em poças d'água sobre tubulação

**Teste de Vazamento:**
• **Água com sabão**: Nas conexões e juntas
• **NUNCA usar fogo**: Para testar vazamento
• **Detector eletrônico**: Equipamento específico
• **Profissional**: Para verificações complexas

**🚨 Emergência - Vazamento de Gás:**

**Ações Imediatas:**
• **1º**: Não acenda fósforos, isqueiros ou equipamentos elétricos
• **2º**: Abra portas e janelas para ventilar
• **3º**: Feche o registro de gás imediatamente
• **4º**: Retire todas as pessoas do local
• **5º**: Ligue para emergência de local seguro

**O QUE NÃO FAZER:**
• **Interruptores**: Não ligue/desligue luz
• **Telefone**: Não use dentro do ambiente
• **Cigarro**: Não fume próximo ao local
• **Veículos**: Não ligue motor perto do vazamento

**📞 Números de Emergência:**

**Gás Natural:**
• **Comgás (SP)**: 0800-773-3444
• **CEG (RJ)**: 0800-282-0197
• **Gasmig (MG)**: 0800-031-0197
• **Bahiagás (BA)**: 0800-284-0080

**Emergências Gerais:**
• **Bombeiros**: 193
• **Defesa Civil**: 199
• **SAMU**: 192
• **Polícia**: 190

**🔧 Prevenção de Acidentes:**

**Instalação Adequada:**
• **Profissional habilitado**: Para instalação e manutenção
• **Materiais certificados**: INMETRO/ABNT
• **Ventilação**: Ambientes sempre ventilados
• **Localização**: Equipamentos em locais adequados

**Manutenção Preventiva:**
• **Inspeção regular**: Conexões e mangueiras
• **Troca periódica**: Mangueiras e reguladores
• **Limpeza**: Bicos do fogão desobstruídos
• **Profissional**: Revisão anual recomendada

**🏠 Segurança Doméstica:**

**Cozinha:**
• **Ventilação**: Janela ou exaustor
• **Posicionamento**: Botijão longe do fogão
• **Mangueira**: Máximo 1,25m de comprimento
• **Abraçadeiras**: Bem fixadas

**Ambiente:**
• **Detector de gás**: Recomendado
• **Extintor**: CO₂ para fogos de gás
• **Rota de fuga**: Planejada e conhecida
• **Crianças**: Orientadas sobre riscos

**🏭 Segurança Comercial/Industrial:**

**Equipamentos Obrigatórios:**
• **Sistema detecção**: Alarmes automáticos
• **Válvulas bloqueio**: Corte emergencial
• **Ventilação forçada**: Exaustores automáticos
• **Sinalização**: Identificação de riscos

**Procedimentos:**
• **Treinamento**: Funcionários capacitados
• **Plano emergência**: Ações definidas
• **Manutenção**: Programada e registrada
• **Brigada**: Equipe para emergências

**💡 Dicas de Segurança:**

**Uso Diário:**
• Feche o registro após usar
• Verifique chama azul no fogão
• Não deixe panela vazia no fogo
• Mantenha área limpa e ventilada

**Sinais de Alerta:**
• **Chama amarela**: Queima incompleta
• **Fuligem**: Nas panelas ou parede
• **Dor de cabeça**: Possível intoxicação
• **Sonolência**: Em ambiente fechado

**🆘 Primeiros Socorros:**

**Inalação de Gás:**
• **Remover da área**: Para local ventilado
• **Respiração**: Se parou, fazer respiração artificial
• **Consciência**: Manter pessoa acordada
• **Médico**: Procurar ajuda imediatamente

**Queimaduras por Gás:**
• **Água corrente**: Resfriar queimadura
• **Não**: Aplicar pomadas ou gelo
• **Cobrir**: Com pano limpo e seco
• **Socorro médico**: Imediatamente

**⚖️ Responsabilidades:**

**Distribuidora:**
• **Rede externa**: Até medidor
• **Emergência**: Atendimento 24h
• **Manutenção**: Sistema de distribuição
• **Orientação**: Sobre uso seguro

**Consumidor:**
• **Instalação interna**: Após o medidor
• **Manutenção**: Equipamentos próprios
• **Uso adequado**: Conforme orientações
• **Comunicação**: Problemas à distribuidora

**Base Legal:**
Normas ABNT, regulamentos ANP e código de defesa civil.

Tem dúvidas sobre segurança ou está enfrentando emergência com gás?"""
        
        # Resposta geral com análise do contrato se disponível
        if contract_text:
            return f"""🔥 **Análise do Contrato de Fornecimento de Gás**

Com base na sua pergunta "{question}" e no contrato fornecido, posso fazer uma análise especializada.

**📋 Principais pontos a verificar:**

**1. Modalidade de Fornecimento:**
• Gás natural canalizado ou GLP
• Classe de consumo (residencial, comercial, industrial)
• Volume contratado e flexibilidades
• Condições de fornecimento

**2. Estrutura Tarifária:**
• Composição dos preços
• Critérios de reajuste
• Tarifas mínimas e disponibilidade
• Impostos e taxas aplicáveis

**3. Segurança e Responsabilidades:**
• Instalações da distribuidora vs consumidor
• Manutenção e inspeções
• Atendimento de emergência
• Seguros obrigatórios

**4. Direitos e Obrigações:**
• Qualidade do fornecimento
• Interrupções programadas
• Procedimentos de reclamação
• Rescisão contratual

**⚖️ Conformidade Legal:**
Este contrato deve seguir regulamentações ANP, normas ABNT e CDC.

Posso analisar algum aspecto específico que está causando dúvida?"""
        
        # Resposta geral
        return """🔥 **Gás - Orientação Geral**

Entendi sua pergunta sobre fornecimento de gás. Posso ajudar com:

**📋 Análises Especializadas:**
• Gás natural canalizado vs GLP
• Tarifas e reajustes de preços
• Ligação nova e instalações
• Segurança e emergências

**⚠️ Problemas Mais Comuns:**
• Cobrança de taxas irregulares
• Problemas na ligação nova
• Vazamentos e emergências
• Reajustes tarifários abusivos

**🛡️ Seus Direitos Principais:**
• Fornecimento contínuo e seguro
• Transparência nas tarifas
• Atendimento de emergência 24h
• Qualidade conforme normas técnicas

Para uma análise mais precisa, me conte sobre sua situação específica ou forneça detalhes do contrato."""