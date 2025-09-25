'use client'

import { useState } from 'react'
import ChatWithAgent from '@/components/features/ChatWithAgent'
import SimpleChat from '@/components/features/SimpleChat'
import ChatHistory from '@/components/features/ChatHistory'
import Link from 'next/link'

interface ChatSession {
  id: string
  contract_id?: string
  messages: Array<{
    id: string
    content: string
    role: 'user' | 'assistant'
    timestamp: string
    agent_type?: string
  }>
  created_at: string
  updated_at: string
  title?: string
  agent_type?: string
}

export default function ChatPage() {
  const [activeTab, setActiveTab] = useState<'advanced' | 'simple'>('advanced')
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null)
  const [sessionKey, setSessionKey] = useState(0) // Força re-render do ChatWithAgent

  const handleSessionLoad = (session: ChatSession) => {
    setCurrentSession(session)
    setSessionKey(prev => prev + 1)
  }

  const handleNewSession = () => {
    setCurrentSession(null)
    setSessionKey(prev => prev + 1)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-xl font-bold text-gray-900">
            ← Contrato Seguro
          </Link>
          <div className="flex gap-4">
            <Link 
              href="/login"
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Entrar
            </Link>
            <Link 
              href="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
            >
              Criar conta
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto">
          
          {/* Title */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Chat Jurídico IA
            </h1>
            <p className="text-gray-600">
              Converse com nossos assistentes especializados sobre seus contratos
            </p>
          </div>

          {/* Tabs */}
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
                💬 Chat Avançado
              </button>
              <button
                onClick={() => setActiveTab('simple')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'simple'
                    ? 'bg-white text-gray-900 shadow'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                🎯 Agentes Especializados
              </button>
            </div>
          </div>

          {/* Chat Interface */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden" style={{height: '600px'}}>
            <div className="flex h-full">
              
              {/* Sidebar - Histórico */}
              <div className="w-80 bg-gray-50 border-r border-gray-200">
                <ChatHistory
                  onSessionLoad={handleSessionLoad}
                  currentSessionId={currentSession?.id}
                  onNewSession={handleNewSession}
                  className="h-full"
                />
              </div>

              {/* Chat Area */}
              <div className="flex-1">
                {activeTab === 'advanced' ? (
                  <ChatWithAgent 
                    key={sessionKey}
                    sessionId={currentSession?.id}
                    contractId={currentSession?.contract_id}
                    initialAgent={currentSession?.agent_type || 'general'}
                    onSessionCreated={(session) => {
                      setCurrentSession(session)
                    }}
                  />
                ) : (
                  <SimpleChat key={sessionKey} />
                )}
              </div>
              
            </div>
          </div>

          {/* Info Cards */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-2xl mb-2">🏠</div>
              <h3 className="font-semibold text-gray-900 mb-2">Contratos de Locação</h3>
              <p className="text-sm text-gray-600">
                Especialista em aluguel, reformas, rescisão e direitos locatários
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-2xl mb-2">💰</div>
              <h3 className="font-semibold text-gray-900 mb-2">Contratos Financeiros</h3>
              <p className="text-sm text-gray-600">
                Expert em empréstimos, cartões, CDC e direitos do consumidor
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-2xl mb-2">📱</div>
              <h3 className="font-semibold text-gray-900 mb-2">Telecomunicações</h3>
              <p className="text-sm text-gray-600">
                Especialista em telefonia, internet e regulamentação Anatel
              </p>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  )
}