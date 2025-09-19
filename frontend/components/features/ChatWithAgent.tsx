'use client'

import { useState, useRef, useEffect } from 'react'
import apiClient, { ChatSession, ChatMessage } from '@/lib/api'

interface ChatWithAgentProps {
  contractId?: string
  sessionId?: string
  onSessionCreated?: (session: ChatSession) => void
}

export default function ChatWithAgent({ contractId, sessionId, onSessionCreated }: ChatWithAgentProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (sessionId) {
      loadSession(sessionId)
    } else if (contractId) {
      createNewSession()
    }
  }, [sessionId, contractId])

  const loadSession = async (sessionId: string) => {
    if (!contractId) return
    
    try {
      console.log('Loading session:', sessionId)
    } catch (error) {
      console.error('Erro ao carregar sessão:', error)
    }
  }

  const createNewSession = async () => {
    if (!contractId) return
    
    try {
      const mockSession: ChatSession = {
        id: `session-${Date.now()}`,
        contract_id: contractId,
        messages: [],
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
      setCurrentSession(mockSession)
      onSessionCreated?.(mockSession)
    } catch (error) {
      console.error('Erro ao criar sessão:', error)
    }
  }

  const sendMessage = async () => {
    if (!inputMessage.trim() || !currentSession || isLoading) return

    const userMessage: ChatMessage = {
      id: `msg-${Date.now()}`,
      content: inputMessage,
      role: 'user',
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      setTimeout(() => {
        const aiResponse: ChatMessage = {
          id: `response-${Date.now()}`,
          content: 'Obrigado pela sua pergunta. Esta é uma resposta simulada do assistente jurídico.',
          role: 'assistant',
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, aiResponse])
        setIsLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error)
      setMessages(prev => [...prev, {
        id: `error-${Date.now()}`,
        content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.',
        role: 'assistant',
        timestamp: new Date().toISOString()
      }])
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const getMessageIcon = (role: string) => {
    switch (role) {
      case 'user':
        return '👤'
      case 'assistant':
        return '🤖'
      default:
        return '💬'
    }
  }

  const formatTimestamp = (timestamp: string) => {
    try {
      return new Date(timestamp).toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch (error) {
      return ''
    }
  }

  return (
    <div className="flex flex-col h-full bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-gray-50 rounded-t-lg">
        <div className="flex items-center space-x-2">
          <span className="text-lg">🤖</span>
          <h3 className="text-lg font-semibold text-gray-800">
            Assistente Jurídico IA
          </h3>
        </div>
        {currentSession && (
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span>Online</span>
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <span className="text-4xl mb-4">💬</span>
            <h4 className="text-lg font-medium mb-2">Inicie uma conversa</h4>
            <p className="text-sm text-center max-w-md">
              Faça perguntas sobre o contrato, peça esclarecimentos ou solicite análises específicas.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div className="flex max-w-xs lg:max-w-md xl:max-w-lg space-x-2">
                {message.role !== 'user' && (
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm">
                      {getMessageIcon(message.role)}
                    </div>
                  </div>
                )}
                
                <div
                  className={`px-4 py-2 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <p className={`text-xs mt-1 ${
                    message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                  }`}>
                    {formatTimestamp(message.timestamp)}
                  </p>
                </div>

                {message.role === 'user' && (
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm">
                      {getMessageIcon(message.role)}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex max-w-xs lg:max-w-md xl:max-w-lg space-x-2">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm">
                  🤖
                </div>
              </div>
              <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-gray-200 bg-gray-50 rounded-b-lg">
        <div className="flex space-x-2">
          <div className="flex-1">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Digite sua mensagem..."
              disabled={isLoading || !currentSession}
              className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              rows={2}
            />
          </div>
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading || !currentSession}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors duration-200 flex items-center space-x-2"
          >
            {isLoading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <span>📤</span>
            )}
            <span className="hidden sm:inline">
              {isLoading ? 'Enviando...' : 'Enviar'}
            </span>
          </button>
        </div>
        
        {!currentSession && contractId && (
          <div className="mt-2 text-sm text-yellow-600 bg-yellow-50 p-2 rounded">
            ⚠️ Criando sessão de chat...
          </div>
        )}
      </div>
    </div>
  )
}