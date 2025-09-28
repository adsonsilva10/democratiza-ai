'use client'

import { useState } from 'react'

export default function SuportePage() {
  const [activeSection, setActiveSection] = useState('faq')
  const [contactForm, setContactForm] = useState({
    nome: '',
    email: '',
    assunto: '',
    mensagem: ''
  })

  const faqs = [
    {
      categoria: 'Geral',
      perguntas: [
        {
          pergunta: 'Como funciona a análise de contratos?',
          resposta: 'Nossa IA analisa seu contrato usando algoritmos avançados e base de conhecimento jurídica para identificar cláusulas abusivas, riscos e pontos de atenção, fornecendo uma análise detalhada em linguagem clara.'
        },
        {
          pergunta: 'Quais tipos de contrato posso analisar?',
          resposta: 'Analisamos diversos tipos: contratos de locação, telecomunicações, financiamentos, cartão de crédito, seguros, planos de saúde, contratos de trabalho e muito mais.'
        },
        {
          pergunta: 'Meus documentos ficam seguros?',
          resposta: 'Sim! Todos os documentos são criptografados e armazenados com segurança máxima. Seguimos as normas da LGPD e nunca compartilhamos seus dados.'
        }
      ]
    },
    {
      categoria: 'Análise',
      perguntas: [
        {
          pergunta: 'Quanto tempo leva para analisar um contrato?',
          resposta: 'A análise básica leva de 30 segundos a 2 minutos. Análises mais profundas podem levar até 5 minutos, dependendo da complexidade do documento.'
        },
        {
          pergunta: 'O que significa cada nível de risco?',
          resposta: 'Alto Risco: cláusulas potencialmente abusivas que podem prejudicar significativamente o consumidor. Médio Risco: pontos que merecem atenção. Baixo Risco: cláusulas padrão dentro da normalidade.'
        }
      ]
    },
    {
      categoria: 'Conta',
      perguntas: [
        {
          pergunta: 'Como altero minha senha?',
          resposta: 'Acesse Configurações > Segurança e clique em "Alterar Senha". Você precisará informar sua senha atual e definir uma nova.'
        },
        {
          pergunta: 'Posso excluir minha conta?',
          resposta: 'Sim, você pode solicitar a exclusão da conta entrando em contato conosco. Todos os seus dados serão permanentemente removidos.'
        }
      ]
    }
  ]

  const handleContactSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Aqui implementaria o envio do formulário
    alert('Mensagem enviada com sucesso! Responderemos em breve.')
    setContactForm({ nome: '', email: '', assunto: '', mensagem: '' })
  }

  return (
    <div className="p-4 lg:p-6">
      <h1 className="text-xl lg:text-2xl font-bold text-gray-900 mb-4 lg:mb-6">Ajuda e Suporte</h1>

      <div className="flex flex-col lg:flex-row gap-4 lg:gap-8">
        {/* Navegação lateral - Mobile como dropdown */}
        <div className="lg:w-64">
          <div className="lg:hidden mb-4">
            <select 
              value={activeSection}
              onChange={(e) => setActiveSection(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="faq">❓ FAQ - Perguntas Frequentes</option>
              <option value="contato">✉️ Fale Conosco</option>
              <option value="recursos">📚 Recursos e Guias</option>
            </select>
          </div>
          <nav className="hidden lg:block space-y-2">
            <button
              onClick={() => setActiveSection('faq')}
              className={`w-full flex items-center gap-3 px-3 lg:px-4 py-2 lg:py-3 text-left rounded-lg transition-colors text-sm lg:text-base ${
                activeSection === 'faq'
                  ? 'bg-blue-100 text-blue-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span className="text-base lg:text-lg">❓</span>
              FAQ - Perguntas Frequentes
            </button>
            
            <button
              onClick={() => setActiveSection('contato')}
              className={`w-full flex items-center gap-3 px-3 lg:px-4 py-2 lg:py-3 text-left rounded-lg transition-colors text-sm lg:text-base ${
                activeSection === 'contato'
                  ? 'bg-blue-100 text-blue-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span className="text-base lg:text-lg">✉️</span>
              Fale Conosco
            </button>

            <button
              onClick={() => setActiveSection('recursos')}
              className={`w-full flex items-center gap-3 px-3 lg:px-4 py-2 lg:py-3 text-left rounded-lg transition-colors text-sm lg:text-base ${
                activeSection === 'recursos'
                  ? 'bg-blue-100 text-blue-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span className="text-base lg:text-lg">📚</span>
              Recursos e Guias
            </button>
          </nav>
        </div>

        {/* Conteúdo principal */}
        <div className="flex-1">
          
          {/* FAQ */}
          {activeSection === 'faq' && (
            <div className="space-y-4 lg:space-y-8">
              {faqs.map((categoria, index) => (
                <div key={index} className="bg-white rounded-lg shadow">
                  <div className="p-4 lg:p-6 border-b">
                    <h2 className="text-lg lg:text-xl font-semibold text-gray-900">{categoria.categoria}</h2>
                  </div>
                  <div className="divide-y divide-gray-200">
                    {categoria.perguntas.map((faq, faqIndex) => (
                      <details key={faqIndex} className="p-4 lg:p-6">
                        <summary className="cursor-pointer font-medium text-gray-900 hover:text-blue-600 text-sm lg:text-base">
                          {faq.pergunta}
                        </summary>
                        <div className="mt-2 lg:mt-3 text-gray-600 leading-relaxed text-sm lg:text-base">
                          {faq.resposta}
                        </div>
                      </details>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Formulário de Contato */}
          {activeSection === 'contato' && (
            <div className="bg-white rounded-lg shadow">
              <div className="p-4 lg:p-6 border-b">
                <h2 className="text-lg lg:text-xl font-semibold text-gray-900">Entre em Contato</h2>
                <p className="text-gray-600 mt-2 text-sm lg:text-base">
                  Não encontrou a resposta que procurava? Envie-nos uma mensagem e nossa equipe responderá em breve.
                </p>
              </div>
              
              <form onSubmit={handleContactSubmit} className="p-4 lg:p-6 space-y-4 lg:space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6">
                  <div>
                    <label className="block text-xs lg:text-sm font-medium text-gray-700 mb-2">
                      Nome Completo
                    </label>
                    <input
                      type="text"
                      required
                      value={contactForm.nome}
                      onChange={(e) => setContactForm(prev => ({...prev, nome: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm lg:text-base"
                    />
                  </div>

                  <div>
                    <label className="block text-xs lg:text-sm font-medium text-gray-700 mb-2">
                      Email
                    </label>
                    <input
                      type="email"
                      required
                      value={contactForm.email}
                      onChange={(e) => setContactForm(prev => ({...prev, email: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm lg:text-base"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs lg:text-sm font-medium text-gray-700 mb-2">
                    Assunto
                  </label>
                  <select
                    required
                    value={contactForm.assunto}
                    onChange={(e) => setContactForm(prev => ({...prev, assunto: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm lg:text-base"
                  >
                    <option value="">Selecione um assunto</option>
                    <option value="duvida-tecnica">Dúvida Técnica</option>
                    <option value="problema-analise">Problema na Análise</option>
                    <option value="sugestao">Sugestão</option>
                    <option value="bug">Relatar Bug</option>
                    <option value="outro">Outro</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs lg:text-sm font-medium text-gray-700 mb-2">
                    Mensagem
                  </label>
                  <textarea
                    required
                    rows={5}
                    value={contactForm.mensagem}
                    onChange={(e) => setContactForm(prev => ({...prev, mensagem: e.target.value}))}
                    placeholder="Descreva sua dúvida ou problema em detalhes..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm lg:text-base"
                  />
                </div>

                <div className="flex justify-end">
                  <button
                    type="submit"
                    className="px-4 py-2 lg:px-6 lg:py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm lg:text-base"
                  >
                    Enviar Mensagem
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Recursos e Guias */}
          {activeSection === 'recursos' && (
            <div className="space-y-4 lg:space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 lg:gap-6">
                <div className="bg-white p-4 lg:p-6 rounded-lg shadow">
                  <div className="text-blue-600 mb-4">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  <h3 className="text-base lg:text-lg font-semibold text-gray-900 mb-2">
                    Guia do Consumidor
                  </h3>
                  <p className="text-gray-600 mb-3 lg:mb-4 text-sm lg:text-base">
                    Aprenda sobre seus direitos e como identificar cláusulas abusivas
                  </p>
                  <button className="text-blue-600 hover:text-blue-700 font-medium text-sm lg:text-base">
                    Acessar Guia →
                  </button>
                </div>

                <div className="bg-white p-4 lg:p-6 rounded-lg shadow">
                  <div className="text-green-600 mb-4 text-4xl lg:text-5xl">
                    📋
                  </div>
                  <h3 className="text-base lg:text-lg font-semibold text-gray-900 mb-2">
                    Modelos de Contrato
                  </h3>
                  <p className="text-gray-600 mb-3 lg:mb-4 text-sm lg:text-base">
                    Baixe modelos seguros e bem estruturados
                  </p>
                  <button className="text-blue-600 hover:text-blue-700 font-medium text-sm lg:text-base">
                    Ver Modelos →
                  </button>
                </div>

                <div className="bg-white p-4 lg:p-6 rounded-lg shadow">
                  <div className="text-purple-600 mb-4 text-4xl lg:text-5xl">
                    🎥
                  </div>
                  <h3 className="text-base lg:text-lg font-semibold text-gray-900 mb-2">
                    Vídeo Tutoriais
                  </h3>
                  <p className="text-gray-600 mb-3 lg:mb-4 text-sm lg:text-base">
                    Aprenda a usar a plataforma com nossos tutoriais
                  </p>
                  <button className="text-blue-600 hover:text-blue-700 font-medium text-sm lg:text-base">
                    Assistir Vídeos →
                  </button>
                </div>

                <div className="bg-white p-4 lg:p-6 rounded-lg shadow">
                  <div className="text-red-600 mb-4 text-4xl lg:text-5xl">
                    ⚠️
                  </div>
                  <h3 className="text-base lg:text-lg font-semibold text-gray-900 mb-2">
                    Alertas Legais
                  </h3>
                  <p className="text-gray-600 mb-3 lg:mb-4 text-sm lg:text-base">
                    Fique por dentro das mudanças na legislação
                  </p>
                  <button className="text-blue-600 hover:text-blue-700 font-medium text-sm lg:text-base">
                    Ver Alertas →
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}