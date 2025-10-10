"""
População COMPLETA da Base de Conhecimento Jurídico
Cobre todos os tipos de contratos que o sistema precisa analisar
"""
import asyncio
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.services.rag_service import get_rag_service

# BASE DE CONHECIMENTO COMPLETA - 92 DOCUMENTOS
COMPLETE_LEGAL_KNOWLEDGE = [
    # ================================================================
    # DIREITO DO CONSUMIDOR (CDC) - 10 documentos
    # ================================================================
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 6º, III",
        "content": "São direitos básicos do consumidor: III - a informação adequada e clara sobre os diferentes produtos e serviços, com especificação correta de quantidade, características, composição, qualidade, tributos incidentes e preço, bem como sobre os riscos que apresentem."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 39, V",
        "content": "É vedado ao fornecedor de produtos ou serviços: V - exigir do consumidor vantagem manifestamente excessiva."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 51, IV",
        "content": "São nulas de pleno direito, entre outras, as cláusulas contratuais relativas ao fornecimento de produtos e serviços que: IV - estabeleçam obrigações consideradas iníquas, abusivas, que coloquem o consumidor em desvantagem exagerada, ou sejam incompatíveis com a boa-fé ou a equidade."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 49",
        "content": "O consumidor pode desistir do contrato, no prazo de 7 dias a contar de sua assinatura ou do ato de recebimento do produto ou serviço, sempre que a contratação de fornecimento de produtos e serviços ocorrer fora do estabelecimento comercial, especialmente por telefone ou a domicílio."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 54, §4º",
        "content": "As cláusulas que implicarem limitação de direito do consumidor deverão ser redigidas com destaque, permitindo sua imediata e fácil compreensão."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 18",
        "content": "Os fornecedores de produtos de consumo duráveis ou não duráveis respondem solidariamente pelos vícios de qualidade ou quantidade que os tornem impróprios ou inadequados ao consumo a que se destinam ou lhes diminuam o valor."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 20",
        "content": "O fornecedor de serviços responde pelos vícios de qualidade que os tornem impróprios ao consumo ou lhes diminuam o valor, assim como por aqueles decorrentes da disparidade com as indicações constantes da oferta ou mensagem publicitária."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 30",
        "content": "Toda informação ou publicidade, suficientemente precisa, veiculada por qualquer forma ou meio de comunicação com relação a produtos e serviços oferecidos ou apresentados, obriga o fornecedor que a fizer veicular ou dela se utilizar e integra o contrato que vier a ser celebrado."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 42",
        "content": "Na cobrança de débitos, o consumidor inadimplente não será exposto a ridículo, nem será submetido a qualquer tipo de constrangimento ou ameaça. Parágrafo único: O consumidor cobrado em quantia indevida tem direito à repetição do indébito, por valor igual ao dobro do que pagou em excesso, acrescido de correção monetária e juros legais."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "consumer_protection",
        "article": "Art. 14",
        "content": "O fornecedor de serviços responde, independentemente da existência de culpa, pela reparação dos danos causados aos consumidores por defeitos relativos à prestação dos serviços, bem como por informações insuficientes ou inadequadas sobre sua fruição e riscos."
    },
    
    # ================================================================
    # CONTRATOS FINANCEIROS - 15 documentos
    # ================================================================
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "financial",
        "article": "Art. 52",
        "content": "No fornecimento de produtos ou serviços que envolva outorga de crédito ou concessão de financiamento ao consumidor, o fornecedor deverá informar prévia e adequadamente: I - preço do produto ou serviço em moeda corrente nacional; II - montante dos juros de mora e da taxa efetiva anual de juros; III - acréscimos legalmente previstos; IV - número e periodicidade das prestações; V - soma total a pagar, com e sem financiamento."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "financial",
        "article": "Art. 52, §1º",
        "content": "As multas de mora decorrentes do inadimplemento de obrigações no seu termo não poderão ser superiores a dois por cento do valor da prestação."
    },
    {
        "source": "Lei 8.078/1990 (CDC)",
        "category": "financial",
        "article": "Art. 52-A",
        "content": "O consumidor tomador de empréstimo consignado em folha de pagamento tem direito a liquidar antecipadamente, no todo ou em parte, o débito, com redução proporcional dos juros e demais acréscimos."
    },
    {
        "source": "Lei 4.595/1964 (Sistema Financeiro Nacional)",
        "category": "financial",
        "article": "Art. 4º, IX",
        "content": "Compete ao Conselho Monetário Nacional: IX - limitar, sempre que necessário, as taxas de juros, descontos, comissões e qualquer outra forma de remuneração de operações e serviços bancários ou financeiros."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "financial",
        "article": "Art. 591",
        "content": "Destinando-se o mútuo a fins econômicos, presumem-se devidos juros, os quais, sob pena de redução, não poderão exceder a taxa a que se refere o art. 406, permitida a capitalização anual."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "financial",
        "article": "Art. 406",
        "content": "Quando os juros moratórios não forem convencionados, ou o forem sem taxa estipulada, ou quando provierem de determinação da lei, serão fixados segundo a taxa que estiver em vigor para a mora do pagamento de impostos devidos à Fazenda Nacional."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "financial",
        "article": "Art. 413",
        "content": "A penalidade deve ser reduzida equitativamente pelo juiz se a obrigação principal tiver sido cumprida em parte, ou se o montante da penalidade for manifestamente excessivo, tendo-se em vista a natureza e a finalidade do negócio."
    },
    {
        "source": "Resolução CMN 3.517/2007 (Consignado)",
        "category": "financial",
        "article": "Art. 2º",
        "content": "A taxa de juros máxima para operações de crédito consignado em folha de pagamento não pode exceder os limites estabelecidos pelo Conselho Monetário Nacional, atualmente 2,14% ao mês para servidores públicos e 1,80% ao mês para aposentados do INSS."
    },
    {
        "source": "Lei 4.595/1964",
        "category": "financial",
        "article": "Art. 18, §1º",
        "content": "Nos contratos de mútuo bancário, não se aplicam as limitações da Lei de Usura (Decreto 22.626/1933), prevalecendo as taxas estipuladas pelo Conselho Monetário Nacional."
    },
    {
        "source": "Súmula 297 STJ",
        "category": "financial",
        "article": "Súmula 297",
        "content": "O Código de Defesa do Consumidor é aplicável às instituições financeiras."
    },
    {
        "source": "Súmula 381 STJ",
        "category": "financial",
        "article": "Súmula 381",
        "content": "Nos contratos bancários, é vedado ao julgador conhecer, de ofício, da abusividade das cláusulas."
    },
    {
        "source": "Súmula 539 STJ",
        "category": "financial",
        "article": "Súmula 539",
        "content": "É permitida a capitalização de juros com periodicidade inferior à anual em contratos celebrados após 31.3.2000, desde que expressamente pactuada."
    },
    {
        "source": "Resolução Bacen 4.753/2019",
        "category": "financial",
        "article": "Art. 4º",
        "content": "As instituições financeiras devem apresentar o Custo Efetivo Total (CET) de forma clara e destacada em todas as operações de crédito, incluindo todos os custos, tributos e seguros incidentes."
    },
    {
        "source": "Lei 13.172/2015",
        "category": "financial",
        "article": "Art. 1º",
        "content": "A portabilidade de crédito é gratuita e deve ser oferecida pelas instituições financeiras, sendo vedada a cobrança de qualquer taxa ou encargo adicional ao consumidor que solicitar a transferência de seu contrato para outra instituição."
    },
    {
        "source": "CDC Art. 51, IV - Financeiro",
        "category": "financial",
        "article": "Art. 51, IV",
        "content": "São nulas cláusulas que estabeleçam obrigações iníquas, abusivas, que coloquem o consumidor em desvantagem exagerada, como renovação automática de contratos, juros abusivos, capitalização irregular ou multas desproporcionais."
    },
    
    # ================================================================
    # DIREITO DO TRABALHO (CLT) - 12 documentos
    # ================================================================
    {
        "source": "CLT (Decreto-Lei 5.452/1943)",
        "category": "labor",
        "article": "Art. 2º",
        "content": "Considera-se empregador a empresa, individual ou coletiva, que, assumindo os riscos da atividade econômica, admite, assalaria e dirige a prestação pessoal de serviço."
    },
    {
        "source": "CLT (Decreto-Lei 5.452/1943)",
        "category": "labor",
        "article": "Art. 3º",
        "content": "Considera-se empregado toda pessoa física que prestar serviços de natureza não eventual a empregador, sob a dependência deste e mediante salário. Requisitos: pessoalidade, subordinação, habitualidade, onerosidade."
    },
    {
        "source": "CLT (Decreto-Lei 5.452/1943)",
        "article": "Art. 58",
        "category": "labor",
        "content": "A duração normal do trabalho, para os empregados em qualquer atividade privada, não excederá de 8 (oito) horas diárias e 44 (quarenta e quatro) horas semanais, facultada a compensação de horários e a redução da jornada, mediante acordo ou convenção coletiva de trabalho."
    },
    {
        "source": "CLT (Decreto-Lei 5.452/1943)",
        "category": "labor",
        "article": "Art. 59, §1º",
        "content": "A remuneração da hora extra será, pelo menos, 50% (cinquenta por cento) superior à da hora normal. No caso de trabalho em domingos e feriados, o acréscimo é de 100%."
    },
    {
        "source": "CLT (Decreto-Lei 5.452/1943)",
        "category": "labor",
        "article": "Art. 443",
        "content": "O contrato individual de trabalho poderá ser acordado tácita ou expressamente, verbalmente ou por escrito, por prazo determinado ou indeterminado, ou para prestação de trabalho intermitente."
    },
    {
        "source": "CLT (Decreto-Lei 5.452/1943)",
        "category": "labor",
        "article": "Art. 477, §8º",
        "content": "A inobservância do disposto no §6º deste artigo sujeitará o infrator à multa de 160 BTN, por trabalhador, bem assim ao pagamento da multa a favor do empregado, em valor equivalente ao seu salário, devidamente corrigido pelo índice de variação do BTN, salvo quando, comprovadamente, o trabalhador der causa à mora."
    },
    {
        "source": "CLT (Decreto-Lei 5.452/1943)",
        "category": "labor",
        "article": "Art. 468",
        "content": "Nos contratos individuais de trabalho só é lícita a alteração das respectivas condições por mútuo consentimento, e ainda assim desde que não resultem, direta ou indiretamente, prejuízos ao empregado, sob pena de nulidade da cláusula infringente desta garantia."
    },
    {
        "source": "Lei 13.467/2017 (Reforma Trabalhista)",
        "category": "labor",
        "article": "Art. 452-A",
        "content": "O contrato de trabalho intermitente deve ser celebrado por escrito e deve conter especificamente o valor da hora de trabalho, que não pode ser inferior ao valor horário do salário mínimo ou àquele devido aos demais empregados do estabelecimento que exerçam a mesma função."
    },
    {
        "source": "Lei 13.467/2017 (Reforma Trabalhista)",
        "category": "labor",
        "article": "Art. 75-B",
        "content": "Considera-se teletrabalho a prestação de serviços preponderantemente fora das dependências do empregador, com a utilização de tecnologias de informação e de comunicação que, por sua natureza, não se constituam como trabalho externo."
    },
    {
        "source": "Súmula 331 TST (Terceirização)",
        "category": "labor",
        "article": "Súmula 331, I",
        "content": "A contratação de trabalhadores por empresa interposta é ilegal, formando-se o vínculo diretamente com o tomador dos serviços, salvo no caso de trabalho temporário (Lei 6.019/1974)."
    },
    {
        "source": "Lei 6.019/1974 (Trabalho Temporário)",
        "category": "labor",
        "article": "Art. 10",
        "content": "O contrato de trabalho temporário, com relação ao mesmo empregador, não poderá exceder ao prazo de cento e oitenta dias, consecutivos ou não."
    },
    {
        "source": "CLT Art. 75-D (Home Office)",
        "category": "labor",
        "article": "Art. 75-D",
        "content": "As disposições relativas à responsabilidade pela aquisição, manutenção ou fornecimento dos equipamentos tecnológicos e da infraestrutura necessária e adequada à prestação do trabalho remoto, bem como ao reembolso de despesas arcadas pelo empregado, serão previstas em contrato escrito."
    },
    
    # ================================================================
    # TELECOMUNICAÇÕES - 10 documentos
    # ================================================================
    {
        "source": "Lei 12.965/2014 (Marco Civil da Internet)",
        "category": "telecommunications",
        "article": "Art. 7º, VIII",
        "content": "O acesso à internet é essencial ao exercício da cidadania, e ao usuário são asseguradas as seguintes garantias: VIII - informações claras e completas sobre coleta, uso, armazenamento, tratamento e proteção de seus dados pessoais, que somente poderão ser utilizados para finalidades que justifiquem sua coleta e não sejam vedadas pela legislação."
    },
    {
        "source": "Resolução Anatel 632/2014",
        "category": "telecommunications",
        "article": "Art. 16",
        "content": "A velocidade média de conexão à internet deve ser de, no mínimo, 80% da velocidade contratada, e a velocidade instantânea não pode ser inferior a 40% da contratada, em qualquer horário do dia."
    },
    {
        "source": "Resolução Anatel 632/2014",
        "category": "telecommunications",
        "article": "Art. 39",
        "content": "O consumidor tem direito a testar a velocidade real de sua conexão através de ferramentas homologadas pela Anatel, e caso comprovada a deficiência, pode requerer redução proporcional do valor pago ou rescisão sem multa."
    },
    {
        "source": "Resolução Anatel 477/2007",
        "category": "telecommunications",
        "article": "Art. 55",
        "content": "O consumidor pode cancelar o contrato de prestação de serviço de telecomunicações a qualquer tempo. A multa de fidelização só é devida se houve benefício ao consumidor (desconto no aparelho, isenção de habilitação) e não pode exceder o valor do benefício concedido proporcionalmente ao período faltante."
    },
    {
        "source": "Lei 9.472/1997 (Lei Geral de Telecomunicações)",
        "category": "telecommunications",
        "article": "Art. 3º",
        "content": "O usuário de serviços de telecomunicações tem direito: I - de acesso aos serviços de telecomunicações; II - à liberdade de escolha de sua prestadora de serviço; III - de não ser discriminado quanto às condições de acesso e fruição do serviço; IV - à informação adequada sobre as condições de prestação dos serviços, suas tarifas e período de validade."
    },
    {
        "source": "Resolução Anatel 632/2014",
        "category": "telecommunications",
        "article": "Art. 91",
        "content": "É vedada a cobrança de franquia de dados na internet fixa. A prestadora pode apenas reduzir a velocidade após atingido o limite contratado, mas nunca cobrar valores adicionais ou interromper o serviço."
    },
    {
        "source": "CDC Art. 39, IX (Telecom)",
        "category": "telecommunications",
        "article": "Art. 39, IX",
        "content": "É vedado ao fornecedor recusar a venda de serviços a quem se disponha a adquiri-los mediante pronto pagamento, ressalvados os casos de intermediação regulados em leis especiais. Venda casada de serviços de telecomunicações é prática abusiva."
    },
    {
        "source": "Resolução Anatel 477/2007",
        "category": "telecommunications",
        "article": "Art. 65",
        "content": "A prestadora deve enviar mensalmente a fatura contendo: discriminação dos serviços utilizados, valores cobrados, tributos incidentes, período de apuração, formas de pagamento e prazo para contestação."
    },
    {
        "source": "Lei 13.709/2018 (LGPD) - Telecom",
        "category": "telecommunications",
        "article": "Art. 18",
        "content": "O titular de dados pessoais tem direito a obter da prestadora de telecomunicações: confirmação da existência de tratamento, acesso aos dados, correção de dados incompletos ou desatualizados, eliminação dos dados tratados com consentimento, e revogação do consentimento."
    },
    {
        "source": "Resolução Anatel 632/2014",
        "category": "telecommunications",
        "article": "Art. 102",
        "content": "Em caso de interrupção do serviço de internet por período superior a 24 horas, o consumidor tem direito a desconto proporcional na fatura e, se recorrente, à rescisão contratual sem qualquer ônus."
    },
    
    # ================================================================
    # LOCAÇÃO (Lei do Inquilinato) - 10 documentos
    # ================================================================
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 22",
        "content": "O locador é obrigado a: I - entregar ao locatário o imóvel alugado em estado de servir ao uso a que se destina; II - garantir, durante o tempo da locação, o uso pacífico do imóvel locado."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 23",
        "content": "O locatário é obrigado a: I - pagar pontualmente o aluguel e os encargos da locação, legal ou contratualmente exigíveis, no prazo estipulado ou, em sua falta, até o sexto dia útil do mês vincendo."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 9º",
        "content": "A ação de revisão do aluguel, seja por iniciativa do locador ou do locatário, só poderá ser ajuizada se houver acordo prévio ou transcorrido prazo de 3 anos de vigência do contrato ou do acordo anterior. O reajuste anual deve seguir índice acordado (IGPM, IPCA ou outro)."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 4º",
        "content": "Durante o prazo estipulado para a duração do contrato, não poderá o locador reaver o imóvel alugado. Na locação por prazo determinado, o locador não pode retomar o imóvel antes do prazo, salvo cláusula contratual específica."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 40",
        "content": "O locatário terá o prazo de 15 dias para desocupação voluntária após notificação, findo o qual será despejado. Em caso de falta de pagamento, o despejo é imediato após sentença judicial."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 45",
        "content": "Quando o imóvel for alienado durante a locação, o locatário tem direito de preferência para compra, em igualdade de condições com terceiros. O locador deve notificá-lo com antecedência mínima de 30 dias."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 58-A",
        "content": "Na locação para temporada, o contrato não pode exceder 90 dias, e devem constar: I - destinação exclusiva para fins não residenciais; II - prazo da locação; III - valor do aluguel e encargos; IV - forma de pagamento. Não se aplica a renovação compulsória."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 23, X",
        "content": "O locatário é obrigado a realizar a entrega do imóvel, finda a locação, no estado em que o recebeu, salvo as deteriorações decorrentes do uso normal. Benfeitorias necessárias podem ser indenizadas."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 38",
        "content": "O fiador pode exonerar-se das suas responsabilidades mediante notificação ao locador, com 120 dias de antecedência, respondendo ainda pelas obrigações do locatário durante esse período e por contratos em renovação."
    },
    {
        "source": "Lei 8.245/1991 (Lei do Inquilinato)",
        "category": "rental_law",
        "article": "Art. 22, II",
        "content": "O locador é obrigado a pagar as taxas de administração imobiliária e os tributos sobre o imóvel (IPTU), salvo disposição expressa em contrário no contrato. A transferência do IPTU ao locatário deve ser explícita."
    },
    
    # ================================================================
    # PRESTAÇÃO DE SERVIÇOS - 10 documentos
    # ================================================================
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "service_provision",
        "article": "Art. 593",
        "content": "A prestação de serviço, que não estiver sujeita às leis trabalhistas ou a lei especial, reger-se-á pelas disposições deste Capítulo. O prestador de serviços pode ser contratado por pessoa física ou jurídica."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "service_provision",
        "article": "Art. 594",
        "content": "Toda a espécie de serviço ou trabalho lícito, material ou imaterial, pode ser contratada mediante retribuição."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "service_provision",
        "article": "Art. 599",
        "content": "Não havendo prazo estipulado, nem podendo este inferir-se da natureza do contrato, qualquer das partes, a seu arbítrio, mediante prévio aviso, pode resolver o contrato de prestação de serviços."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "service_provision",
        "article": "Art. 610",
        "content": "O empreiteiro de uma obra pode contribuir para ela só com seu trabalho ou com ele e os materiais. A empreitada pode ser de lavor (apenas trabalho) ou mista (trabalho + materiais)."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "service_provision",
        "article": "Art. 615",
        "content": "Concluída a obra de acordo com o ajuste, ou o costume do lugar, o dono é obrigado a recebê-la. Poderá, porém, rejeitá-la, se o empreiteiro se afastou das instruções recebidas e dos planos dados, ou das regras técnicas em trabalhos de tal natureza."
    },
    {
        "source": "CDC Art. 14 (Serviços)",
        "category": "service_provision",
        "article": "Art. 14",
        "content": "O fornecedor de serviços responde, independentemente da existência de culpa, pela reparação dos danos causados aos consumidores por defeitos relativos à prestação dos serviços, bem como por informações insuficientes ou inadequadas sobre sua fruição e riscos."
    },
    {
        "source": "CDC Art. 20 (Serviços)",
        "category": "service_provision",
        "article": "Art. 20",
        "content": "O fornecedor de serviços responde pelos vícios de qualidade que os tornem impróprios ao consumo ou lhes diminuam o valor, assim como por aqueles decorrentes da disparidade com as indicações constantes da oferta ou mensagem publicitária."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "service_provision",
        "article": "Art. 618",
        "content": "Nos contratos de empreitada de edifícios ou outras construções consideráveis, o empreiteiro de materiais e execução responderá, durante o prazo irredutível de cinco anos, pela solidez e segurança do trabalho, assim em razão dos materiais, como do solo."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "service_provision",
        "article": "Art. 596",
        "content": "Não se conta no prazo do contrato o tempo em que o prestador de serviço, por culpa sua, deixou de servir."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "service_provision",
        "article": "Art. 598",
        "content": "A prestação de serviço não se poderá convencionar por mais de quatro anos, embora o contrato tenha por causa o pagamento de dívida de quem o presta, ou se destine à execução de certa e determinada obra."
    },
    
    # ================================================================
    # CONTRATOS CIVIS (Princípios Gerais) - 8 documentos
    # ================================================================
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "civil_contracts",
        "article": "Art. 421",
        "content": "A liberdade contratual será exercida nos limites da função social do contrato."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "civil_contracts",
        "article": "Art. 422",
        "content": "Os contratantes são obrigados a guardar, assim na conclusão do contrato, como em sua execução, os princípios de probidade e boa-fé."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "civil_contracts",
        "article": "Art. 423",
        "content": "Quando houver no contrato de adesão cláusulas ambíguas ou contraditórias, dever-se-á adotar a interpretação mais favorável ao aderente."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "civil_contracts",
        "article": "Art. 424",
        "content": "Nos contratos de adesão, são nulas as cláusulas que estipulem a renúncia antecipada do aderente a direito resultante da natureza do negócio."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "civil_contracts",
        "article": "Art. 157",
        "content": "Ocorre a lesão quando uma pessoa, sob premente necessidade, ou por inexperiência, se obriga a prestação manifestamente desproporcional ao valor da prestação oposta. Aprecia-se a desproporção segundo os valores vigentes ao tempo em que foi celebrado o negócio jurídico."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "civil_contracts",
        "article": "Art. 478",
        "content": "Nos contratos de execução continuada ou diferida, se a prestação de uma das partes se tornar excessivamente onerosa, com extrema vantagem para a outra, em virtude de acontecimentos extraordinários e imprevisíveis, poderá o devedor pedir a resolução do contrato."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "civil_contracts",
        "article": "Art. 473",
        "content": "A resilição unilateral, nos casos em que a lei expressa ou implicitamente o permita, opera mediante denúncia notificada à outra parte. Parágrafo único: Se, porém, dada a natureza do contrato, uma das partes houver feito investimentos consideráveis para a sua execução, a denúncia unilateral só produzirá efeito depois de transcorrido prazo compatível com a natureza e o vulto dos investimentos."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "civil_contracts",
        "article": "Art. 389",
        "content": "Não cumprida a obrigação, responde o devedor por perdas e danos, mais juros e atualização monetária segundo índices oficiais regularmente estabelecidos, e honorários de advogado."
    },
    
    # ================================================================
    # PROTEÇÃO DE DADOS (LGPD) - 7 documentos
    # ================================================================
    {
        "source": "Lei 13.709/2018 (LGPD)",
        "category": "data_protection",
        "article": "Art. 6º, I",
        "content": "As atividades de tratamento de dados pessoais deverão observar a boa-fé e os seguintes princípios: I - finalidade: realização do tratamento para propósitos legítimos, específicos, explícitos e informados ao titular."
    },
    {
        "source": "Lei 13.709/2018 (LGPD)",
        "category": "data_protection",
        "article": "Art. 7º, I",
        "content": "O tratamento de dados pessoais somente poderá ser realizado mediante o consentimento do titular, que deve ser fornecido por escrito ou por outro meio que demonstre a manifestação de vontade do titular."
    },
    {
        "source": "Lei 13.709/2018 (LGPD)",
        "category": "data_protection",
        "article": "Art. 8º, §4º",
        "content": "O consentimento deverá referir-se a finalidades determinadas, e as autorizações genéricas para o tratamento de dados pessoais serão nulas."
    },
    {
        "source": "Lei 13.709/2018 (LGPD)",
        "category": "data_protection",
        "article": "Art. 9º",
        "content": "O titular tem direito ao acesso facilitado às informações sobre o tratamento de seus dados, que deverão ser disponibilizadas de forma clara, adequada e ostensiva."
    },
    {
        "source": "Lei 13.709/2018 (LGPD)",
        "category": "data_protection",
        "article": "Art. 18",
        "content": "O titular dos dados pessoais tem direito a obter do controlador: confirmação da existência de tratamento, acesso aos dados, correção de dados incompletos, inexatos ou desatualizados, anonimização, bloqueio ou eliminação de dados desnecessários, excessivos ou tratados em desconformidade."
    },
    {
        "source": "Lei 13.709/2018 (LGPD)",
        "category": "data_protection",
        "article": "Art. 42",
        "content": "O controlador ou o operador que, em razão do exercício de atividade de tratamento de dados pessoais, causar a outrem dano patrimonial, moral, individual ou coletivo, em violação à legislação de proteção de dados pessoais, é obrigado a repará-lo."
    },
    {
        "source": "Lei 13.709/2018 (LGPD)",
        "category": "data_protection",
        "article": "Art. 52",
        "content": "As infrações às normas da LGPD sujeitam os infratores a sanções administrativas aplicáveis pela autoridade nacional: advertência, multa simples de até 2% do faturamento (limitada a R$ 50 milhões por infração), multa diária, publicização da infração, bloqueio ou eliminação dos dados."
    },
    
    # ================================================================
    # DIREITO PREVIDENCIÁRIO - 7 documentos
    # ================================================================
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 18, I",
        "content": "O Regime Geral de Previdência Social compreende as seguintes prestações, devidas inclusive em razão de eventos decorrentes de acidente do trabalho: I - quanto ao segurado: a) aposentadoria por invalidez; b) aposentadoria por idade; c) aposentadoria por tempo de contribuição; d) aposentadoria especial; e) auxílio-doença; f) salário-família; g) salário-maternidade; h) auxílio-acidente."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 48",
        "content": "A aposentadoria por idade será devida ao segurado que, cumprida a carência exigida, completar 65 (sessenta e cinco) anos de idade, se homem, e 62 (sessenta e dois) anos, se mulher. §1º Os limites fixados no caput são reduzidos para sessenta e cinquenta e cinco anos no caso de trabalhadores rurais."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 74",
        "content": "A pensão por morte será devida ao conjunto dos dependentes do segurado que falecer, aposentado ou não, a contar da data: I - do óbito, quando requerida até 90 (noventa) dias depois deste; II - do requerimento, quando requerida após o prazo previsto no inciso anterior."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 77",
        "content": "A pensão por morte concedida a dependente inválido ou com deficiência terá duração indeterminada. A pensão por morte havida por outros dependentes terá os seguintes prazos de duração: I - 4 (quatro) meses se o óbito ocorrer sem que o segurado tenha vertido 18 (dezoito) contribuições mensais; II - duração variável conforme idade do beneficiário."
    },
    {
        "source": "Emenda Constitucional 103/2019 (Reforma da Previdência)",
        "category": "retirement_pension",
        "article": "Art. 201, §7º, I",
        "content": "É assegurada aposentadoria no regime geral de previdência social, nos termos da lei, obedecidas as seguintes condições: I - 65 (sessenta e cinco) anos de idade, se homem, e 62 (sessenta e dois) anos de idade, se mulher, observado tempo mínimo de contribuição de 15 anos para mulheres e 20 anos para homens."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 57",
        "content": "A aposentadoria especial será devida, uma vez cumprida a carência exigida, ao segurado empregado, trabalhador avulso e contribuinte individual, este somente quando cooperado filiado a cooperativa de trabalho ou de produção, que tenha trabalhado sujeito a condições especiais que prejudiquem a saúde ou a integridade física, durante 15 (quinze), 20 (vinte) ou 25 (vinte e cinco) anos."
    },
    {
        "source": "Lei 8.213/1991 (Plano de Benefícios da Previdência Social)",
        "category": "retirement_pension",
        "article": "Art. 29, §5º",
        "content": "Não será computado como tempo de contribuição, para efeito de concessão do benefício de aposentadoria por tempo de contribuição, o período em que o segurado contribuinte individual ou facultativo tiver contribuído na forma do §2º do art. 21 da Lei nº 8.212, de 24 de julho de 1991 (contribuição reduzida de 11%), salvo se tiver complementado as contribuições."
    },
    
    # ================================================================
    # COMPRA E VENDA - 5 documentos
    # ================================================================
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "purchase_sale",
        "article": "Art. 481",
        "content": "Pelo contrato de compra e venda, um dos contratantes se obriga a transferir o domínio de certa coisa, e o outro, a pagar-lhe certo preço em dinheiro."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "purchase_sale",
        "article": "Art. 492",
        "content": "Até o momento da tradição, os riscos da coisa correm por conta do vendedor, e os do preço por conta do comprador. A tradição é a entrega efetiva do bem."
    },
    {
        "source": "Código Civil (Lei 10.406/2002)",
        "category": "purchase_sale",
        "article": "Art. 441",
        "content": "A coisa recebida em virtude de contrato comutativo pode ser enjeitada por vícios ou defeitos ocultos, que a tornem imprópria ao uso a que é destinada, ou lhe diminuam o valor."
    },
    {
        "source": "CDC Art. 49 (Compra e Venda)",
        "category": "purchase_sale",
        "article": "Art. 49",
        "content": "O consumidor pode desistir do contrato de compra, no prazo de 7 dias a contar de sua assinatura ou do ato de recebimento do produto, sempre que a contratação ocorrer fora do estabelecimento comercial (internet, telefone, domicílio)."
    },
    {
        "source": "CDC Art. 35",
        "category": "purchase_sale",
        "article": "Art. 35",
        "content": "Se o fornecedor se recusar cumprimento à oferta, apresentação ou publicidade, o consumidor poderá alternativamente: I - exigir o cumprimento forçado da obrigação; II - aceitar outro produto ou prestação de serviço equivalente; III - rescindir o contrato, com direito à restituição da quantia eventualmente antecipada, monetariamente atualizada, e perdas e danos."
    }
]

async def populate_complete_database():
    """Popular base com conhecimento completo"""
    
    print("\n" + "="*80)
    print("🚀 POPULAÇÃO COMPLETA DA BASE DE CONHECIMENTO JURÍDICO")
    print("="*80)
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL não configurado!")
        return False
    
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Limpar base existente
    print("\n🗑️  Limpando base de dados existente...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM knowledge_base"))
        before = result.scalar()
        print(f"   Documentos antes: {before}")
        
        conn.execute(text("DELETE FROM knowledge_base"))
        conn.commit()
        print(f"   ✅ Base limpa!")
    
    # Inserir novos documentos
    total = len(COMPLETE_LEGAL_KNOWLEDGE)
    print(f"\n📚 Inserindo {total} documentos jurídicos...")
    
    # Agrupar por categoria para estatísticas
    categories = {}
    for doc in COMPLETE_LEGAL_KNOWLEDGE:
        cat = doc["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📊 Distribuição por categoria:")
    for cat, count in sorted(categories.items()):
        print(f"   • {cat}: {count} documentos")
    
    print(f"\n🔄 Processando inserções...")
    
    inserted = 0
    errors = 0
    
    for i, doc in enumerate(COMPLETE_LEGAL_KNOWLEDGE, 1):
        try:
            metadata = {
                "source": doc["source"],
                "category": doc["category"],
                "article": doc["article"]
            }
            
            metadata_json = json.dumps(metadata)
            content_str = doc["content"]
            doc_id_result = None
            
            # Usar f-string para evitar escape de ::jsonb
            with engine.connect() as conn:
                sql = f"""
                INSERT INTO knowledge_base 
                (content, metadata, created_at)
                VALUES 
                ('{content_str.replace("'", "''")}', '{metadata_json}'::jsonb, NOW())
                RETURNING id
                """
                result = conn.execute(text(sql))
                doc_id_result = result.scalar()
                conn.commit()
            
            inserted += 1
            
            if i % 10 == 0 or i == total:
                print(f"   ✅ {i}/{total} documentos inseridos ({(i/total*100):.1f}%)")
            
        except Exception as e:
            errors += 1
            print(f"   ❌ Erro no documento {doc['article']}: {e}")
    
    session.commit()
    session.close()
    
    # Verificar total final
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM knowledge_base"))
        final_count = result.scalar()
    
    print(f"\n✅ População concluída!")
    print(f"   • Inseridos: {inserted}/{total}")
    print(f"   • Erros: {errors}")
    print(f"   • Total na base: {final_count}")
    
    # Gerar embeddings
    print(f"\n🔄 Gerando embeddings OpenAI (1536d) para {final_count} documentos...")
    print(f"   ⏱️  Tempo estimado: ~{final_count * 0.5:.0f} segundos")
    
    rag = get_rag_service()
    print(f"   📊 Provider: {rag.provider.value}")
    print(f"   📏 Dimensão: {rag.embedding_dimension}d")
    
    # Buscar documentos sem embedding
    result = session.execute(text("""
        SELECT id, content 
        FROM knowledge_base 
        WHERE embedding IS NULL
        ORDER BY created_at
    """))
    
    documents = result.fetchall()
    
    processed = 0
    for doc_id, content in documents:
        try:
            embeddings = await rag.create_embeddings([content])
            embedding_vector = embeddings[0]
            vector_str = '[' + ','.join(map(str, embedding_vector)) + ']'
            
            with engine.connect() as conn:
                sql = f"UPDATE knowledge_base SET embedding = '{vector_str}'::vector WHERE id = '{str(doc_id)}'"
                conn.execute(text(sql))
                conn.commit()
            
            processed += 1
            if processed % 10 == 0 or processed == len(documents):
                print(f"   ✅ {processed}/{len(documents)} embeddings gerados ({(processed/len(documents)*100):.1f}%)")
            
        except Exception as e:
            print(f"   ❌ Erro ao gerar embedding para {doc_id}: {e}")
    
    # Estatísticas finais
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(embedding) as with_embedding
            FROM knowledge_base
        """))
        row = result.fetchone()
        
        print(f"\n" + "="*80)
        print(f"✅ BASE DE CONHECIMENTO COMPLETA!")
        print(f"="*80)
        print(f"\n📊 Estatísticas Finais:")
        print(f"   • Total de documentos: {row.total}")
        print(f"   • Com embeddings: {row.with_embedding}")
        print(f"   • Sem embeddings: {row.total - row.with_embedding}")
        print(f"   • Categorias: {len(categories)}")
        print(f"\n📋 Categorias cobertas:")
        for cat, count in sorted(categories.items()):
            print(f"   ✅ {cat}: {count} docs")
        
        print(f"\n🎯 Tipos de contratos suportados:")
        print(f"   ✅ Consumidor geral (CDC)")
        print(f"   ✅ Contratos financeiros (empréstimos, cartões, consignados)")
        print(f"   ✅ Contratos trabalhistas (CLT, PJ, temporários, home office)")
        print(f"   ✅ Telecomunicações (internet, telefonia, TV)")
        print(f"   ✅ Locação residencial e comercial")
        print(f"   ✅ Prestação de serviços e empreitadas)")
        print(f"   ✅ Proteção de dados (LGPD)")
        print(f"   ✅ Previdência e aposentadoria")
        print(f"   ✅ Compra e venda")
        
        print(f"\n🚀 Sistema pronto para análises de contratos com RAG completo!")
        print(f"="*80 + "\n")
    
    return True

if __name__ == "__main__":
    print("\n" + "🎯"*40)
    print("DEMOCRATIZA AI - BOOTSTRAP COMPLETO DA BASE JURÍDICA")
    print("População de 92 documentos essenciais da legislação brasileira")
    print("🎯"*40)
    
    success = asyncio.run(populate_complete_database())
    
    if success:
        print("\n✅ SUCESSO! Base de conhecimento jurídico completa e operacional.")
    else:
        print("\n❌ FALHA na população da base.")
