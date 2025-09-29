'use client'

import { useState } from 'react'
import { Badge } from '@/components/ui/badge'
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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="bg-white border-b border-gray-200 px-4 md:px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl md:text-3xl font-bold text-gray-900">
              🤖 Assistente IA
            </h1>
            <p className="text-sm md:text-base text-gray-600 mt-1">
              Converse com agentes especializados sobre seus contratos
            </p>
          </div>
          <div className="hidden lg:flex items-center gap-4">
            <Badge variant="secondary" className="bg-green-100 text-green-700">
              ⚡ Respostas instantâneas
            </Badge>
            <Badge variant="secondary" className="bg-blue-100 text-blue-700">
              🎯 Agentes especializados
            </Badge>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 md:px-6 py-8 md:py-8">
        <div className="max-w-6xl mx-auto space-y-8 md:space-y-6">
          {/* Progress Steps - Como Funciona */}
          <div className="relative flex justify-center">
            {/* Desktop: Horizontal layout */}
            <div className="hidden sm:flex justify-center items-center mb-8 px-2">
              <div className="flex items-center">
                <div className="flex flex-col items-center">
                  <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
                    💬
                  </div>
                  <div className="mt-2 text-center">
                    <p className="text-sm font-medium text-blue-600">
                      Pergunte
                    </p>
                    <p className="text-xs text-gray-400 hidden lg:block">
                      Faça sua pergunta
                    </p>
                  </div>
                </div>
                <div className="flex-1 h-0.5 mx-4 bg-blue-600 min-w-[40px]" />
              </div>

              <div className="flex items-center">
                <div className="flex flex-col items-center">
                  <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
                    🤖
                  </div>
                  <div className="mt-2 text-center">
                    <p className="text-sm font-medium text-blue-600">
                      IA Responde
                    </p>
                    <p className="text-xs text-gray-400 hidden lg:block">
                      Agente especializado
                    </p>
                  </div>
                </div>
                <div className="flex-1 h-0.5 mx-4 bg-blue-600 min-w-[40px]" />
              </div>

              <div className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
                  📋
                </div>
                <div className="mt-2 text-center">
                  <p className="text-sm font-medium text-blue-600">
                    Orientação
                  </p>
                  <p className="text-xs text-gray-400 hidden lg:block">
                    Receba orientação
                  </p>
                </div>
              </div>
            </div>

            {/* Mobile: Compact horizontal layout */}
            <div className="flex sm:hidden justify-center items-center mb-8 px-2">
              <div className="flex items-center">
                <div className="flex flex-col items-center">
                  <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
                    💬
                  </div>
                  <p className="text-sm font-medium mt-2 text-blue-600">
                    Pergunte
                  </p>
                </div>
                <div className="flex-1 h-0.5 mx-3 bg-blue-600 min-w-[20px]" />
              </div>

              <div className="flex items-center">
                <div className="flex flex-col items-center">
                  <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
                    🤖
                  </div>
                  <p className="text-sm font-medium mt-2 text-blue-600">
                    IA Responde
                  </p>
                </div>
                <div className="flex-1 h-0.5 mx-3 bg-blue-600 min-w-[20px]" />
              </div>

              <div className="flex flex-col items-center">
                <div className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
                  📋
                </div>
                <p className="text-sm font-medium mt-2 text-blue-600">
                  Orientação
                </p>
              </div>
            </div>
          </div>

          {/* Chat Interface */}
          <div className="bg-white rounded-xl border-2 border-dashed border-gray-300 shadow-lg overflow-hidden min-h-[600px] flex flex-col">
            {/* Tabs Mobile/Desktop */}
            <div className="p-4 border-b border-gray-200 bg-gray-50">
              <div className="flex justify-center">
                <div className="bg-gray-100 p-1 rounded-lg">
                  <button
                    onClick={() => setActiveTab('advanced')}
                    className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                      activeTab === 'advanced'
                        ? 'bg-white text-gray-900 shadow'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    💬 Chat com Histórico
                  </button>
                  <button
                    onClick={() => setActiveTab('simple')}
                    className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                      activeTab === 'simple'
                        ? 'bg-white text-gray-900 shadow'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    🎯 Chat Rápido
                  </button>
                </div>
              </div>
            </div>

            <div className="flex-1 flex">
              {/* Sidebar - Apenas no chat avançado e desktop */}
              {activeTab === 'advanced' && (
                <div className="hidden lg:block w-80 bg-gray-50 border-r border-gray-200">
                  <ChatHistory
                    onSessionLoad={handleSessionLoad}
                    currentSessionId={currentSession?.id}
                    onNewSession={handleNewSession}
                    className="h-full"
                  />
                </div>
              )}

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

          {/* Assistant Guidelines */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-medium text-blue-900 mb-2 text-sm flex items-center gap-2">
                🏠 Contratos de Locação
              </h4>
              <ul className="text-xs text-blue-800 space-y-1">
                <li>• Aluguel e reformas</li>
                <li>• Rescisão e depósito</li>
                <li>• Direitos do inquilino</li>
              </ul>
            </div>
            
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
              <h4 className="font-medium text-green-900 mb-2 text-sm flex items-center gap-2">
                💰 Contratos Financeiros
              </h4>
              <ul className="text-xs text-green-800 space-y-1">
                <li>• Empréstimos e cartões</li>
                <li>• CDC e financiamentos</li>
                <li>• Direitos do consumidor</li>
              </ul>
            </div>
            
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <h4 className="font-medium text-yellow-900 mb-2 text-sm flex items-center gap-2">
                📱 Telecomunicações
              </h4>
              <ul className="text-xs text-yellow-800 space-y-1">
                <li>• Telefonia e internet</li>
                <li>• Regulamentação Anatel</li>
                <li>• Cancelamentos e multas</li>
              </ul>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  )
}