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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      {/* Header moderno com breadcrumb */}
      <div className="bg-white border-b border-gray-200 px-4 md:px-6 py-4 md:py-6">
        <div className="flex flex-col gap-2">
          <nav className="text-sm text-gray-500">
            <span>Plataforma</span> <span className="mx-2">›</span> <span className="text-gray-900">Ajuda e Suporte</span>
          </nav>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <span className="text-xl text-purple-600">🆘</span>
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-bold text-gray-900">Ajuda e Suporte</h1>
              <p className="text-sm text-gray-600">Encontre respostas rápidas ou entre em contato conosco</p>
            </div>
          </div>
        </div>
      </div>

      <div className="p-4 md:p-6">

        <div className="flex flex-col lg:flex-row gap-6 lg:gap-8 max-w-7xl mx-auto">
          {/* Navegação aprimorada */}
          <div className="lg:w-72">
            {/* Mobile: Cards horizontais com scroll */}
            <div className="lg:hidden mb-6">
              <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                <button
                  onClick={() => setActiveSection('faq')}
                  className={`flex-shrink-0 flex items-center gap-2 px-4 py-3 rounded-xl transition-all font-medium text-sm ${
                    activeSection === 'faq'
                      ? 'bg-purple-600 text-white shadow-lg shadow-purple-200'
                      : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-lg">❓</span>
                  <span>FAQ</span>
                </button>
                <button
                  onClick={() => setActiveSection('contato')}
                  className={`flex-shrink-0 flex items-center gap-2 px-4 py-3 rounded-xl transition-all font-medium text-sm ${
                    activeSection === 'contato'
                      ? 'bg-purple-600 text-white shadow-lg shadow-purple-200'
                      : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-lg">✉️</span>
                  <span>Contato</span>
                </button>
                <button
                  onClick={() => setActiveSection('recursos')}
                  className={`flex-shrink-0 flex items-center gap-2 px-4 py-3 rounded-xl transition-all font-medium text-sm ${
                    activeSection === 'recursos'
                      ? 'bg-purple-600 text-white shadow-lg shadow-purple-200'
                      : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-lg">📚</span>
                  <span>Recursos</span>
                </button>
              </div>
            </div>
            {/* Desktop: Navegação sidebar aprimorada */}
            <nav className="hidden lg:block">
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                <button
                  onClick={() => setActiveSection('faq')}
                  className={`w-full flex items-center gap-4 px-6 py-4 text-left transition-all border-b border-gray-50 ${
                    activeSection === 'faq'
                      ? 'bg-gradient-to-r from-purple-50 to-indigo-50 text-purple-700 border-l-4 border-l-purple-500'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <div className={`p-2 rounded-lg ${
                    activeSection === 'faq' 
                      ? 'bg-purple-100 text-purple-600' 
                      : 'bg-gray-100 text-gray-600'
                  }`}>
                    <span className="text-lg">❓</span>
                  </div>
                  <div className="flex-1">
                    <span className="font-medium">FAQ</span>
                    <div className={`text-xs mt-0.5 ${
                      activeSection === 'faq' ? 'text-purple-600' : 'text-gray-500'
                    }`}>
                      Perguntas frequentes
                    </div>
                  </div>
                </button>
                
                <button
                  onClick={() => setActiveSection('contato')}
                  className={`w-full flex items-center gap-4 px-6 py-4 text-left transition-all border-b border-gray-50 ${
                    activeSection === 'contato'
                      ? 'bg-gradient-to-r from-purple-50 to-indigo-50 text-purple-700 border-l-4 border-l-purple-500'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <div className={`p-2 rounded-lg ${
                    activeSection === 'contato' 
                      ? 'bg-purple-100 text-purple-600' 
                      : 'bg-gray-100 text-gray-600'
                  }`}>
                    <span className="text-lg">✉️</span>
                  </div>
                  <div className="flex-1">
                    <span className="font-medium">Fale Conosco</span>
                    <div className={`text-xs mt-0.5 ${
                      activeSection === 'contato' ? 'text-purple-600' : 'text-gray-500'
                    }`}>
                      Entre em contato
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => setActiveSection('recursos')}
                  className={`w-full flex items-center gap-4 px-6 py-4 text-left transition-all ${
                    activeSection === 'recursos'
                      ? 'bg-gradient-to-r from-purple-50 to-indigo-50 text-purple-700 border-l-4 border-l-purple-500'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <div className={`p-2 rounded-lg ${
                    activeSection === 'recursos' 
                      ? 'bg-purple-100 text-purple-600' 
                      : 'bg-gray-100 text-gray-600'
                  }`}>
                    <span className="text-lg">📚</span>
                  </div>
                  <div className="flex-1">
                    <span className="font-medium">Recursos e Guias</span>
                    <div className={`text-xs mt-0.5 ${
                      activeSection === 'recursos' ? 'text-purple-600' : 'text-gray-500'
                    }`}>
                      Materiais de apoio
                    </div>
                  </div>
                </button>
              </div>
            </nav>
        </div>

          {/* Conteúdo principal */}
          <div className="flex-1">
            
            {/* FAQ */}
            {activeSection === 'faq' && (
              <div className="space-y-6 lg:space-y-8">
                {faqs.map((categoria, index) => (
                  <div key={index} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                    <div className="bg-gradient-to-r from-purple-50 to-indigo-50 p-6 border-b border-gray-100">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-purple-100 rounded-lg">
                          <span className="text-xl text-purple-600">{
                            categoria.categoria === 'Geral' ? '🌟' :
                            categoria.categoria === 'Análise' ? '🔍' : '👤'
                          }</span>
                        </div>
                        <div>
                          <h2 className="text-xl font-semibold text-gray-900">{categoria.categoria}</h2>
                          <p className="text-sm text-gray-600">
                            {categoria.categoria === 'Geral' && 'Informações básicas sobre a plataforma'}
                            {categoria.categoria === 'Análise' && 'Como funciona nossa análise de contratos'}
                            {categoria.categoria === 'Conta' && 'Gerenciamento da sua conta'}
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="divide-y divide-gray-100">
                      {categoria.perguntas.map((faq, faqIndex) => (
                        <details key={faqIndex} className="p-6 hover:bg-gray-50 transition-colors">
                          <summary className="cursor-pointer font-semibold text-gray-900 hover:text-purple-600 transition-colors flex items-center gap-2">
                            <span className="text-purple-500">💬</span>
                            {faq.pergunta}
                          </summary>
                          <div className="mt-4 pl-7 text-gray-700 leading-relaxed bg-gradient-to-r from-gray-50 to-white p-4 rounded-xl border-l-4 border-purple-200">
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
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                <div className="bg-gradient-to-r from-blue-50 to-cyan-50 p-6 md:p-8 border-b border-gray-100">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <span className="text-xl text-blue-600">✉️</span>
                    </div>
                    <div>
                      <h2 className="text-xl font-semibold text-gray-900">Entre em Contato</h2>
                      <p className="text-sm text-gray-600">Nossa equipe responde em até 24 horas</p>
                    </div>
                  </div>
                  <p className="text-gray-700 bg-white/50 p-4 rounded-xl border border-blue-100">
                    💡 <strong>Dica:</strong> Antes de enviar, verifique se sua dúvida não está na seção FAQ. 
                    Isso pode economizar seu tempo!
                  </p>
                </div>
                
                <form onSubmit={handleContactSubmit} className="p-6 md:p-8 space-y-6">
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                        <span>👨‍💼</span> Nome Completo
                      </label>
                      <input
                        type="text"
                        required
                        value={contactForm.nome}
                        onChange={(e) => setContactForm(prev => ({...prev, nome: e.target.value}))}
                        className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white shadow-sm"
                        placeholder="Digite seu nome completo"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                        <span>📧</span> Email
                      </label>
                      <input
                        type="email"
                        required
                        value={contactForm.email}
                        onChange={(e) => setContactForm(prev => ({...prev, email: e.target.value}))}
                        className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white shadow-sm"
                        placeholder="seu@email.com"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                      <span>📂</span> Assunto
                    </label>
                    <select
                      required
                      value={contactForm.assunto}
                      onChange={(e) => setContactForm(prev => ({...prev, assunto: e.target.value}))}
                      className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white shadow-sm"
                    >
                      <option value="">Selecione um assunto</option>
                      <option value="duvida-tecnica">🛠️ Dúvida Técnica</option>
                      <option value="problema-analise">🔍 Problema na Análise</option>
                      <option value="sugestao">💡 Sugestão</option>
                      <option value="bug">🐛 Relatar Bug</option>
                      <option value="outro">❓ Outro</option>
                    </select>
                  </div>

                  <div className="space-y-2">
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                      <span>💬</span> Mensagem
                    </label>
                    <textarea
                      required
                      rows={6}
                      value={contactForm.mensagem}
                      onChange={(e) => setContactForm(prev => ({...prev, mensagem: e.target.value}))}
                      placeholder="Descreva sua dúvida ou problema em detalhes. Quanto mais informações você fornecer, melhor poderemos ajudar!"
                      className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-sm bg-white shadow-sm resize-none"
                    />
                    <p className="text-xs text-gray-500">Mínimo 20 caracteres</p>
                  </div>

                  <div className="flex flex-col sm:flex-row gap-4 justify-end pt-6 border-t border-gray-100">
                    <button
                      type="button"
                      onClick={() => setContactForm({ nome: '', email: '', assunto: '', mensagem: '' })}
                      className="px-6 py-3 text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-xl transition-all text-sm font-medium"
                    >
                      🗑️ Limpar Formulário
                    </button>
                    <button
                      type="submit"
                      className="px-8 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all shadow-lg hover:shadow-xl text-sm font-medium"
                    >
                      ✉️ Enviar Mensagem
                    </button>
                  </div>
              </form>
            </div>
          )}

            {/* Recursos e Guias */}
            {activeSection === 'recursos' && (
              <div className="space-y-6">
                <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-2xl border border-green-100">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-green-100 rounded-lg">
                      <span className="text-xl text-green-600">📚</span>
                    </div>
                    <div>
                      <h2 className="text-xl font-semibold text-gray-900">Recursos e Materiais</h2>
                      <p className="text-sm text-gray-600">Tudo que você precisa para se informar</p>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer group">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                        <span className="text-2xl text-blue-600">📖</span>
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                          Guia do Consumidor
                        </h3>
                        <p className="text-sm text-gray-600">
                          Aprenda sobre seus direitos e como identificar cláusulas abusivas
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium px-3 py-1 bg-blue-100 text-blue-700 rounded-full">
                        📚 Educativo
                      </span>
                      <span className="text-blue-600 hover:text-blue-700 font-medium text-sm group-hover:translate-x-1 transition-transform">
                        Acessar Guia →
                      </span>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer group">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                        <span className="text-2xl text-green-600">📋</span>
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-green-600 transition-colors">
                          Modelos de Contrato
                        </h3>
                        <p className="text-sm text-gray-600">
                          Baixe modelos seguros e bem estruturados
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium px-3 py-1 bg-green-100 text-green-700 rounded-full">
                        📄 Templates
                      </span>
                      <span className="text-blue-600 hover:text-blue-700 font-medium text-sm group-hover:translate-x-1 transition-transform">
                        Ver Modelos →
                      </span>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer group">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                        <span className="text-2xl text-purple-600">🎥</span>
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">
                          Vídeo Tutoriais
                        </h3>
                        <p className="text-sm text-gray-600">
                          Aprenda a usar a plataforma com nossos tutoriais
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium px-3 py-1 bg-purple-100 text-purple-700 rounded-full">
                        🎬 Vídeos
                      </span>
                      <span className="text-blue-600 hover:text-blue-700 font-medium text-sm group-hover:translate-x-1 transition-transform">
                        Assistir Vídeos →
                      </span>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer group">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                        <span className="text-2xl text-red-600">⚠️</span>
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-red-600 transition-colors">
                          Alertas Legais
                        </h3>
                        <p className="text-sm text-gray-600">
                          Fique por dentro das mudanças na legislação
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium px-3 py-1 bg-red-100 text-red-700 rounded-full">
                        🚨 Alertas
                      </span>
                      <span className="text-blue-600 hover:text-blue-700 font-medium text-sm group-hover:translate-x-1 transition-transform">
                        Ver Alertas →
                      </span>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all cursor-pointer group">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                        <span className="text-2xl text-orange-600">📞</span>
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-orange-600 transition-colors">
                          Suporte Direto
                        </h3>
                        <p className="text-sm text-gray-600">
                          Chat ou chamada para casos urgentes
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium px-3 py-1 bg-orange-100 text-orange-700 rounded-full">
                        ⚡ Urgente
                      </span>
                      <span className="text-blue-600 hover:text-blue-700 font-medium text-sm group-hover:translate-x-1 transition-transform">
                        Contatar →
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}