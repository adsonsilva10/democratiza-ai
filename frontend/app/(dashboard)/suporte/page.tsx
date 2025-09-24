'use client'

import { useState } from 'react'

const faqData = [
  {
    id: 1,
    categoria: 'Geral',
    pergunta: 'Como funciona a análise de contratos da Democratiza AI?',
    resposta: 'Nossa IA utiliza algoritmos avançados de processamento de linguagem natural para analisar seus contratos, identificando cláusulas abusivas, riscos potenciais e pontos de atenção. O processo leva poucos minutos e gera um relatório detalhado com recomendações jurídicas.'
  },
  {
    id: 2,
    categoria: 'Segurança',
    pergunta: 'Meus documentos estão seguros na plataforma?',
    resposta: 'Sim! Utilizamos criptografia de ponta a ponta, armazenamento seguro e seguimos as melhores práticas de segurança da informação. Seus documentos são processados de forma segura e podem ser excluídos a qualquer momento.'
  },
  {
    id: 3,
    categoria: 'Funcionalidades',
    pergunta: 'Que tipos de contratos posso analisar?',
    resposta: 'Suportamos diversos tipos: contratos de locação, empréstimos, seguros, planos de saúde, contratos de trabalho, termos de serviço, contratos comerciais e muito mais. Nossa IA é treinada para reconhecer padrões em documentos jurídicos brasileiros.'
  },
  {
    id: 4,
    categoria: 'Preços',
    pergunta: 'Como funciona o modelo de preços?',
    resposta: 'Oferecemos planos flexíveis: Básico (análises limitadas), Profissional (análises ilimitadas + chat IA) e Empresarial (múltiplos usuários + API). Teste gratuitamente por 7 dias.'
  },
  {
    id: 5,
    categoria: 'Técnico',
    pergunta: 'Posso usar a plataforma no celular?',
    resposta: 'Sim! Nossa plataforma é totalmente responsiva e funciona perfeitamente em dispositivos móveis. Você pode fazer upload de fotos de contratos e receber análises completas diretamente no seu smartphone.'
  },
  {
    id: 6,
    categoria: 'Jurídico',
    pergunta: 'A análise da IA substitui um advogado?',
    resposta: 'Não. Nossa IA é uma ferramenta de apoio que identifica pontos de atenção e riscos, mas não substitui a consulta jurídica profissional. Recomendamos sempre consultar um advogado para questões complexas.'
  }
]

const tutoriaisData = [
  {
    id: 1,
    titulo: 'Como fazer upload do seu primeiro contrato',
    descricao: 'Aprenda o passo a passo para enviar e analisar seu primeiro documento',
    duracao: '3 min',
    dificuldade: 'Iniciante',
    icone: '📤'
  },
  {
    id: 2,
    titulo: 'Entendendo os relatórios de análise',
    descricao: 'Como interpretar os resultados e níveis de risco identificados',
    duracao: '5 min',
    dificuldade: 'Iniciante',
    icone: '📊'
  },
  {
    id: 3,
    titulo: 'Usando o Chat IA de forma eficiente',
    descricao: 'Dicas para fazer perguntas e obter respostas mais precisas',
    duracao: '4 min',
    dificuldade: 'Intermediário',
    icone: '💬'
  },
  {
    id: 4,
    titulo: 'Configurando notificações personalizadas',
    descricao: 'Configure alertas para ser notificado sobre riscos importantes',
    duracao: '2 min',
    dificuldade: 'Iniciante',
    icone: '🔔'
  }
]

export default function SuportePage() {
  const [activeTab, setActiveTab] = useState('faq')
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null)
  const [chamadoForm, setChamadoForm] = useState({
    assunto: '',
    categoria: '',
    prioridade: '',
    descricao: '',
    anexo: null as File | null
  })

  const handleSubmitChamado = (e: React.FormEvent) => {
    e.preventDefault()
    // Aqui seria enviado o chamado
    alert('Chamado enviado com sucesso! Nossa equipe retornará em até 24h.')
    setChamadoForm({
      assunto: '',
      categoria: '',
      prioridade: '',
      descricao: '',
      anexo: null
    })
  }

  return (
    <div className="w-full max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          🆘 Ajuda e Suporte
        </h1>
        <p className="text-gray-600 text-base sm:text-lg">
          Encontre respostas, tutoriais e entre em contato com nossa equipe
        </p>
      </div>

      {/* Navegação por Tabs */}
      <div className="bg-white rounded-xl shadow-lg mb-8">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('faq')}
              className={`py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'faq'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              ❓ FAQ
            </button>
            <button
              onClick={() => setActiveTab('tutoriais')}
              className={`py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'tutoriais'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              🎓 Tutoriais
            </button>
            <button
              onClick={() => setActiveTab('chamado')}
              className={`py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'chamado'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              🎫 Abrir Chamado
            </button>
            <button
              onClick={() => setActiveTab('contato')}
              className={`py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'contato'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📞 Contato
            </button>
          </nav>
        </div>

        <div className="p-6">
          {/* FAQ Tab */}
          {activeTab === 'faq' && (
            <div>
              <div className="mb-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  Perguntas Frequentes
                </h2>
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Buscar nas perguntas frequentes..."
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                  <div className="absolute left-3 top-1/2 transform -translate-y-1/2">
                    <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                {faqData.map((faq) => (
                  <div key={faq.id} className="border border-gray-200 rounded-lg">
                    <button
                      onClick={() => setExpandedFaq(expandedFaq === faq.id ? null : faq.id)}
                      className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-start space-x-3">
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full font-medium">
                          {faq.categoria}
                        </span>
                        <span className="font-medium text-gray-900 flex-1">
                          {faq.pergunta}
                        </span>
                      </div>
                      <svg
                        className={`w-5 h-5 text-gray-500 transform transition-transform ${
                          expandedFaq === faq.id ? 'rotate-180' : ''
                        }`}
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </button>
                    
                    {expandedFaq === faq.id && (
                      <div className="px-6 pb-4">
                        <p className="text-gray-700 leading-relaxed">
                          {faq.resposta}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tutoriais Tab */}
          {activeTab === 'tutoriais' && (
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-6">
                Tutoriais e Guias
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {tutoriaisData.map((tutorial) => (
                  <div key={tutorial.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                    <div className="flex items-start space-x-4">
                      <div className="text-3xl">{tutorial.icone}</div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 mb-2">
                          {tutorial.titulo}
                        </h3>
                        <p className="text-gray-600 text-sm mb-4">
                          {tutorial.descricao}
                        </p>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4 text-sm text-gray-500">
                            <span>⏱️ {tutorial.duracao}</span>
                            <span>📊 {tutorial.dificuldade}</span>
                          </div>
                          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
                            Assistir
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-8 bg-blue-50 p-6 rounded-lg border border-blue-200">
                <h3 className="font-semibold text-blue-900 mb-2">
                  💡 Dica: Central de Ajuda Completa
                </h3>
                <p className="text-blue-800 mb-4">
                  Acesse nossa central de ajuda online com mais de 50 tutoriais, vídeos explicativos e documentação completa da plataforma.
                </p>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  Acessar Central de Ajuda
                </button>
              </div>
            </div>
          )}

          {/* Chamado Tab */}
          {activeTab === 'chamado' && (
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-6">
                Abrir Chamado de Suporte
              </h2>
              
              <form onSubmit={handleSubmitChamado} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Assunto
                    </label>
                    <input
                      type="text"
                      required
                      value={chamadoForm.assunto}
                      onChange={(e) => setChamadoForm({...chamadoForm, assunto: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Descreva brevemente o problema"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Categoria
                    </label>
                    <select
                      required
                      value={chamadoForm.categoria}
                      onChange={(e) => setChamadoForm({...chamadoForm, categoria: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Selecione a categoria</option>
                      <option value="tecnico">Problema Técnico</option>
                      <option value="analise">Análise de Contrato</option>
                      <option value="conta">Conta e Cobrança</option>
                      <option value="funcionalidade">Nova Funcionalidade</option>
                      <option value="outro">Outro</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Prioridade
                    </label>
                    <select
                      required
                      value={chamadoForm.prioridade}
                      onChange={(e) => setChamadoForm({...chamadoForm, prioridade: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Selecione a prioridade</option>
                      <option value="baixa">Baixa</option>
                      <option value="media">Média</option>
                      <option value="alta">Alta</option>
                      <option value="urgente">Urgente</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Descrição Detalhada
                  </label>
                  <textarea
                    required
                    rows={6}
                    value={chamadoForm.descricao}
                    onChange={(e) => setChamadoForm({...chamadoForm, descricao: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Descreva o problema em detalhes, incluindo os passos que levaram ao erro e o comportamento esperado..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Anexar Arquivo (opcional)
                  </label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
                    <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                      <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    <p className="mt-2 text-sm text-gray-600">
                      <span className="font-medium">Clique para enviar</span> ou arraste e solte
                    </p>
                    <p className="text-xs text-gray-500">PNG, JPG, PDF até 10MB</p>
                  </div>
                </div>

                <div className="flex justify-end space-x-4">
                  <button
                    type="button"
                    className="px-6 py-3 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Enviar Chamado
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Contato Tab */}
          {activeTab === 'contato' && (
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-6">
                Entre em Contato
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div className="flex items-start space-x-4">
                    <div className="text-2xl">📧</div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">E-mail</h3>
                      <p className="text-gray-600 mb-2">suporte@democratizaai.com.br</p>
                      <p className="text-sm text-gray-500">Resposta em até 24 horas</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="text-2xl">💬</div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">Chat ao Vivo</h3>
                      <p className="text-gray-600 mb-2">Segunda a Sexta, 9h às 18h</p>
                      <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                        Iniciar chat →
                      </button>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="text-2xl">📱</div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">WhatsApp</h3>
                      <p className="text-gray-600 mb-2">(11) 99999-9999</p>
                      <p className="text-sm text-gray-500">Disponível 24/7</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="text-2xl">📍</div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">Escritório</h3>
                      <p className="text-gray-600 text-sm leading-relaxed">
                        Av. Paulista, 1000 - Sala 100<br />
                        Bela Vista, São Paulo - SP<br />
                        CEP: 01310-100
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-4">
                    Horários de Atendimento
                  </h3>
                  <div className="space-y-3 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Segunda a Sexta</span>
                      <span className="font-medium">9h às 18h</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Sábados</span>
                      <span className="font-medium">9h às 14h</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Domingos e Feriados</span>
                      <span className="text-red-600">Fechado</span>
                    </div>
                  </div>

                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <h4 className="font-semibold text-gray-900 mb-3">
                      Redes Sociais
                    </h4>
                    <div className="flex space-x-4">
                      <a href="#" className="text-blue-600 hover:text-blue-700">
                        LinkedIn
                      </a>
                      <a href="#" className="text-blue-600 hover:text-blue-700">
                        Twitter
                      </a>
                      <a href="#" className="text-blue-600 hover:text-blue-700">
                        Instagram
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}