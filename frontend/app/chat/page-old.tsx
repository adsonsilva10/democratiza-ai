'use client'

import { useState } from 'react'
import ChatWithAgent from '@/components/features/ChatWithAgent'
import SimpleChat from '@/components/features/SimpleChat'
import Link from 'next/link'

interface ChatSession {
  id: string
  contract_id?: string
  messages: any[]
  created_at: string
  updated_at: string
}

export default function ChatPage() {
  const [activeTab, setActiveTab] = useState<'advanced' | 'simple'>('advanced')
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null)
  const [savedSessions, setSavedSessions] = useState<any[]>([])

  // Carregar sessões salvas do localStorage
  const loadSavedSessions = () => {
    try {
      const sessions = JSON.parse(localStorage.getItem('user_chat_sessions') || '[]')
      setSavedSessions(sessions)
    } catch (error) {
      console.error('Erro ao carregar sessões:', error)
    }
  }

  const startNewChat = () => {
    setCurrentSession(null)
  }

  const loadSession = (sessionId: string) => {
    try {
      const session = localStorage.getItem(`chat_session_${sessionId}`)
      if (session) {
        setCurrentSession(JSON.parse(session))
      }
    } catch (error) {
      console.error('Erro ao carregar sessão:', error)
    }
  }

  const handleSessionCreated = (session: ChatSession) => {
    setCurrentSession(session)
    loadSavedSessions()
  }

  // Carregar sessões quando componente monta
  useState(() => {
    loadSavedSessions()
  })
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 w-full overflow-x-hidden">
      {/* Header */}
      <header className="container mx-auto px-4 py-6 w-full">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 w-full">
          <Link href="/" className="text-lg sm:text-xl font-bold text-gray-900 truncate">
            ← Contrato Seguro
          </Link>
          <div className="flex gap-4 justify-start sm:justify-end">
            <Link 
              href="/login"
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Entrar
            </Link>
            <Link 
              href="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors whitespace-nowrap"
            >
              Criar conta
            </Link>
          </div>
        </div>
      </header>

      {/* Chat Section */}
      <div className="container mx-auto px-4 py-8 w-full">
        <div className="max-w-4xl mx-auto w-full">
          <div className="text-center mb-8">
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4">
              💬 Chat com Assistente Jurídico
            </h1>
            <p className="text-gray-600 mb-6 text-sm sm:text-base px-2">
              Converse com nosso assistente especializado em contratos e direito
            </p>
            
            {/* Tabs para alternar entre modos */}
            <div className="flex justify-center mb-6">
              <div className="bg-gray-100 p-1 rounded-lg">
                <button
                  onClick={() => setActiveTab('advanced')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'advanced'
                      ? 'bg-white text-gray-900 shadow'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Chat Avançado
                </button>
                <button
                  onClick={() => setActiveTab('simple')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'simple'
                      ? 'bg-white text-gray-900 shadow'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Agentes Especializados
                </button>
              </div>
            </div>
          </div>

          {/* Chat Avançado */}
          {activeTab === 'advanced' && (
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              {/* Sidebar com histórico */}
              <div className="lg:col-span-1">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-gray-900">Conversas</h3>
                    <button
                      onClick={startNewChat}
                      className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600 transition-colors"
                    >
                      + Nova
                    </button>
                  </div>

                  <div className="space-y-2">
                    {savedSessions.length === 0 ? (
                      <p className="text-sm text-gray-500 text-center py-4">
                        Nenhuma conversa ainda
                      </p>
                    ) : (
                      savedSessions.map((session) => (
                        <div
                          key={session.id}
                          onClick={() => loadSession(session.id)}
                          className={`p-3 rounded-lg cursor-pointer transition-colors ${
                            currentSession?.id === session.id
                              ? 'bg-blue-50 border border-blue-200'
                              : 'hover:bg-gray-50 border border-transparent'
                          }`}
                        >
                          <div className="text-sm font-medium text-gray-900">
                            {session.contract_id ? `Contrato ${session.contract_id.slice(0, 8)}...` : 'Chat Geral'}
                          </div>
                          <div className="text-xs text-gray-500">
                            {new Date(session.created_at).toLocaleDateString('pt-BR')}
                          </div>
                        </div>
                      ))
                    )}
                  </div>

                  <div className="mt-6 pt-4 border-t border-gray-200">
                    <button
                      onClick={loadSavedSessions}
                      className="text-sm text-blue-600 hover:text-blue-700 transition-colors"
                    >
                      🔄 Atualizar lista
                    </button>
                  </div>
                </div>
              </div>

              {/* Área do chat */}
              <div className="lg:col-span-3">
                <div className="h-[600px]">
                  <ChatWithAgent
                    sessionId={currentSession?.id}
                    contractId={currentSession?.contract_id}
                    onSessionCreated={handleSessionCreated}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Agentes Especializados (modo original) */}
          {activeTab === 'simple' && (
            <>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 w-full">
                {/* Chat de Locação */}
                <div className="w-full">
                  <h3 className="text-lg font-semibold mb-4 truncate">🏠 Agente de Locação</h3>
                  <SimpleChat agentType="rental" className="w-full" />
                </div>

                {/* Chat de Telecomunicações */}
                <div className="w-full">
                  <h3 className="text-lg font-semibold mb-4 truncate">📱 Agente de Telecomunicações</h3>
                  <SimpleChat agentType="telecom" className="w-full" />
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 mt-6 sm:mt-8 w-full">
                {/* Chat Financeiro */}
                <div className="w-full">
                  <h3 className="text-lg font-semibold mb-4 truncate">💰 Agente Financeiro</h3>
                  <SimpleChat agentType="financial" className="w-full" />
                </div>

                {/* Chat Classificador */}
                <div className="w-full">
                  <h3 className="text-lg font-semibold mb-4 truncate">🤖 Agente Classificador</h3>
                  <SimpleChat agentType="classifier" className="w-full" />
                </div>
              </div>
            </>
          )}

          {/* Informações sobre o chat */}
          <div className="mt-8 sm:mt-12 bg-white rounded-lg shadow-lg p-4 sm:p-8 w-full">
            {activeTab === 'advanced' ? (
              <>
                <h2 className="text-xl sm:text-2xl font-bold text-center mb-6">
                  💡 Como usar o Chat Avançado
                </h2>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
                  <div className="text-center">
                    <div className="text-3xl mb-3">💬</div>
                    <h3 className="font-semibold mb-2">Conversação Natural</h3>
                    <p className="text-sm text-gray-600">Fale naturalmente com o assistente jurídico especializado</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-3xl mb-3">🧠</div>
                    <h3 className="font-semibold mb-2">Contexto Inteligente</h3>
                    <p className="text-sm text-gray-600">O assistente lembra do contexto da conversa</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-3xl mb-3">💾</div>
                    <h3 className="font-semibold mb-2">Histórico Salvo</h3>
                    <p className="text-sm text-gray-600">Suas conversas ficam salvas para consulta posterior</p>
                  </div>
                </div>

                <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <h4 className="font-medium text-blue-900 mb-2">
                    Exemplos de perguntas que você pode fazer:
                  </h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• "O que significa esta cláusula no meu contrato?"</li>
                    <li>• "Quais são os riscos desta cláusula de rescisão?"</li>
                    <li>• "Como posso me proteger dessa obrigação?"</li>
                    <li>• "Este prazo de pagamento está adequado?"</li>
                  </ul>
                </div>
              </>
            ) : (
              <>
                <h2 className="text-xl sm:text-2xl font-bold text-center mb-6">
                  Como Funciona
                </h2>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full">
                  <div className="text-center">
                    <div className="text-3xl mb-3">📄</div>
                    <h3 className="font-semibold mb-2">1. Upload</h3>
                    <p className="text-sm text-gray-600">Envie seu contrato em PDF, DOC ou DOCX</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-3xl mb-3">🤖</div>
                    <h3 className="font-semibold mb-2">2. Análise IA</h3>
                    <p className="text-sm text-gray-600">Nossa IA analisa e classifica o contrato</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-3xl mb-3">💬</div>
                    <h3 className="font-semibold mb-2">3. Chat</h3>
                    <p className="text-sm text-gray-600">Converse com o agente especializado</p>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-3xl mb-3">📊</div>
                    <h3 className="font-semibold mb-2">4. Relatório</h3>
                    <p className="text-sm text-gray-600">Receba um relatório detalhado</p>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}