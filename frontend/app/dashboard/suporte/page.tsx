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
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Ajuda e Suporte</h1>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Navegação lateral */}
        <div className="lg:w-64">
          <nav className="space-y-2">
            <button
              onClick={() => setActiveSection('faq')}
              className={`w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg transition-colors ${
                activeSection === 'faq'
                  ? 'bg-blue-100 text-blue-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span className="text-lg">❓</span>
              FAQ - Perguntas Frequentes
            </button>
            
            <button
              onClick={() => setActiveSection('contato')}
              className={`w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg transition-colors ${
                activeSection === 'contato'
                  ? 'bg-blue-100 text-blue-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span className="text-lg">✉️</span>
              Fale Conosco
            </button>

            <button
              onClick={() => setActiveSection('recursos')}
              className={`w-full flex items-center gap-3 px-4 py-3 text-left rounded-lg transition-colors ${
                activeSection === 'recursos'
                  ? 'bg-blue-100 text-blue-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span className="text-lg">📚</span>
              Recursos e Guias
            </button>
          </nav>
        </div>

        {/* Conteúdo principal */}
        <div className="flex-1">
          
          {/* FAQ */}
          {activeSection === 'faq' && (
            <div className="space-y-8">
              {faqs.map((categoria, index) => (
                <div key={index} className="bg-white rounded-lg shadow">
                  <div className="p-6 border-b">
                    <h2 className="text-xl font-semibold text-gray-900">{categoria.categoria}</h2>
                  </div>
                  <div className="divide-y divide-gray-200">
                    {categoria.perguntas.map((faq, faqIndex) => (
                      <details key={faqIndex} className="p-6">
                        <summary className="cursor-pointer font-medium text-gray-900 hover:text-blue-600">
                          {faq.pergunta}
                        </summary>
                        <div className="mt-3 text-gray-600 leading-relaxed">
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
              <div className="p-6 border-b">
                <h2 className="text-xl font-semibold text-gray-900">Entre em Contato</h2>
                <p className="text-gray-600 mt-2">
                  Não encontrou a resposta que procurava? Envie-nos uma mensagem e nossa equipe responderá em breve.
                </p>
              </div>
              
              <form onSubmit={handleContactSubmit} className="p-6 space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nome Completo
                    </label>
                    <input
                      type="text"
                      required
                      value={contactForm.nome}
                      onChange={(e) => setContactForm(prev => ({...prev, nome: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email
                    </label>
                    <input
                      type="email"
                      required
                      value={contactForm.email}
                      onChange={(e) => setContactForm(prev => ({...prev, email: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Assunto
                  </label>
                  <select
                    required
                    value={contactForm.assunto}
                    onChange={(e) => setContactForm(prev => ({...prev, assunto: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Mensagem
                  </label>
                  <textarea
                    required
                    rows={6}
                    value={contactForm.mensagem}
                    onChange={(e) => setContactForm(prev => ({...prev, mensagem: e.target.value}))}
                    placeholder="Descreva sua dúvida ou problema em detalhes..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div className="flex justify-end">
                  <button
                    type="submit"
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Enviar Mensagem
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Recursos e Guias */}
          {activeSection === 'recursos' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="text-blue-600 mb-4">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Guia do Consumidor
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Aprenda sobre seus direitos e como identificar cláusulas abusivas
                  </p>
                  <button className="text-blue-600 hover:text-blue-700 font-medium">
                    Acessar Guia →
                  </button>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="text-green-600 mb-4">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 0v12a2 2 0 002 2h6a2 2 0 002-2V4M7 4h10M9 8h6m-6 4h6m-6 4h6" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Modelos de Contrato
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Baixe modelos seguros e bem estruturados
                  </p>
                  <button className="text-blue-600 hover:text-blue-700 font-medium">
                    Ver Modelos →
                  </button>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="text-purple-600 mb-4">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Vídeo Tutoriais
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Aprenda a usar a plataforma com nossos tutoriais
                  </p>
                  <button className="text-blue-600 hover:text-blue-700 font-medium">
                    Assistir Vídeos →
                  </button>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="text-red-600 mb-4">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.664-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Alertas Legais
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Fique por dentro das mudanças na legislação
                  </p>
                  <button className="text-blue-600 hover:text-blue-700 font-medium">
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