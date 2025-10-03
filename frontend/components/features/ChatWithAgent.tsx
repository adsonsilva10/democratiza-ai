'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { Send, Bot, User, Wifi, WifiOff, AlertCircle } from 'lucide-react'

interface ChatMessage {
  id: string
  content: string
  sender: 'user' | 'assistant'
  timestamp: Date
  context?: Record<string, any>
  type?: 'text' | 'error' | 'system'
}

interface ChatWithAgentProps {
  initialAgent?: string
  onContractSelect?: () => void
  sessionId?: string
  contractId?: string
  onSessionCreated?: (session: { id: string; contract_id?: string }) => void
}

interface WebSocketMessage {
  type: 'ai_response' | 'error' | 'connection_established' | 'typing_indicator' | 'pong'
  message?: string
  context?: Record<string, any>
  timestamp?: string
  message_id?: string
  is_typing?: boolean
  error?: string
}

export default function ChatWithAgent({ sessionId, contractId, onSessionCreated }: ChatWithAgentProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const [connectionError, setConnectionError] = useState<string | null>(null)
  
  const wsRef = useRef<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const pingIntervalRef = useRef<NodeJS.Timeout | null>(null)

  // WebSocket connection management
  const connectWebSocket = useCallback(() => {
    if (!sessionId) return
    
    try {
      setConnectionError(null)
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${protocol}//${window.location.host}/api/v1/chat/ws/${sessionId}`
      
      wsRef.current = new WebSocket(wsUrl)
      
      wsRef.current.onopen = () => {
        console.log(' WebSocket connected')
        setIsConnected(true)
        setConnectionError(null)
        
        // Start ping interval for connection health
        pingIntervalRef.current = setInterval(() => {
          if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({ type: 'ping' }))
          }
        }, 30000) // Ping every 30 seconds
      }
      
      wsRef.current.onmessage = (event) => {
        try {
          const data: WebSocketMessage = JSON.parse(event.data)
          
          switch (data.type) {
            case 'connection_established':
              console.log(' Connection established:', data.message)
              break
              
            case 'ai_response':
              if (data.message) {
                const aiMessage: ChatMessage = {
                  id: data.message_id || Date.now().toString(),
                  content: data.message,
                  sender: 'assistant',
                  timestamp: new Date(data.timestamp || Date.now()),
                  context: data.context,
                  type: 'text'
                }
                setMessages(prev => [...prev, aiMessage])
              }
              setIsLoading(false)
              setIsTyping(false)
              break
              
            case 'error':
              const errorMessage: ChatMessage = {
                id: Date.now().toString(),
                content: data.message || 'Erro desconhecido',
                sender: 'assistant',
                timestamp: new Date(),
                type: 'error'
              }
              setMessages(prev => [...prev, errorMessage])
              setIsLoading(false)
              setIsTyping(false)
              break
              
            case 'typing_indicator':
              setIsTyping(data.is_typing || false)
              break
              
            case 'pong':
              // Connection is alive
              break
          }
        } catch (err) {
          console.error(' Failed to parse WebSocket message:', err)
        }
      }
      
      wsRef.current.onclose = (event) => {
        console.log(' WebSocket closed:', event.code, event.reason)
        setIsConnected(false)
        setIsLoading(false)
        setIsTyping(false)
        
        // Clear ping interval
        if (pingIntervalRef.current) {
          clearInterval(pingIntervalRef.current)
          pingIntervalRef.current = null
        }
        
        // Attempt to reconnect after delay (unless explicitly closed)
        if (event.code !== 1000 && event.code !== 1001) {
          setConnectionError('Conex�o perdida. Tentando reconectar...')
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log(' Attempting to reconnect...')
            connectWebSocket()
          }, 3000)
        }
      }
      
      wsRef.current.onerror = (error) => {
        console.error(' WebSocket error:', error)
        setConnectionError('Erro de conex�o')
      }
      
    } catch (error) {
      console.error(' Failed to connect WebSocket:', error)
      setConnectionError('Falha ao conectar')
    }
  }, [sessionId])

  // Cleanup function
  const disconnectWebSocket = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close(1000, 'Component unmounting')
      wsRef.current = null
    }
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }
    
    if (pingIntervalRef.current) {
      clearInterval(pingIntervalRef.current)
      pingIntervalRef.current = null
    }
  }, [])

  // Effect to manage WebSocket lifecycle
  useEffect(() => {
    if (sessionId) {
      connectWebSocket()
    }
    
    return () => {
      disconnectWebSocket()
    }
  }, [sessionId, connectWebSocket, disconnectWebSocket])

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSend = async () => {
    if (!inputMessage.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      return
    }

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date(),
      type: 'text'
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setInputMessage('')

    try {
      // Send message via WebSocket
      const payload = {
        type: 'user_message',
        message: inputMessage.trim(),
        contract_id: contractId,
        timestamp: new Date().toISOString()
      }

      wsRef.current.send(JSON.stringify(payload))
    } catch (error) {
      console.error(' Failed to send message:', error)
      setIsLoading(false)
      
      // Add error message
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        content: 'Erro ao enviar mensagem. Tente novamente.',
        sender: 'assistant',
        timestamp: new Date(),
        type: 'error'
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString('pt-BR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const getConnectionStatus = () => {
    if (connectionError) {
      return (
        <div className="flex items-center gap-2 text-red-600 text-sm">
          <AlertCircle className="h-4 w-4" />
          {connectionError}
        </div>
      )
    }
    
    if (!isConnected) {
      return (
        <div className="flex items-center gap-2 text-gray-500 text-sm">
          <WifiOff className="h-4 w-4" />
          Desconectado
        </div>
      )
    }
    
    return (
      <div className="flex items-center gap-2 text-green-600 text-sm">
        <Wifi className="h-4 w-4" />
        Conectado
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-sm border">
      {/* Header */}
      <div className="flex-shrink-0 border-b p-4 bg-gray-50 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-100 p-2 rounded-full">
              <Bot className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Assistente Jur�dico</h3>
              <p className="text-sm text-gray-500">
                {isTyping ? 'Digitando...' : 'Pronto para ajudar'}
              </p>
            </div>
          </div>
          {getConnectionStatus()}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <Bot className="h-12 w-12 mx-auto mb-3 text-gray-400" />
            <p className="text-lg font-medium mb-2">Bem-vindo ao Chat Jur�dico!</p>
            <p className="text-sm">
              Fa�a perguntas sobre seu contrato ou quest�es jur�dicas gerais.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : message.type === 'error'
                    ? 'bg-red-50 border border-red-200 text-red-800'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <div className="flex items-start gap-2">
                  {message.sender === 'assistant' && (
                    <div className="flex-shrink-0 mt-1">
                      {message.type === 'error' ? (
                        <AlertCircle className="h-4 w-4 text-red-500" />
                      ) : (
                        <Bot className="h-4 w-4 text-gray-600" />
                      )}
                    </div>
                  )}
                  <div className="flex-1">
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <div
                      className={`text-xs mt-1 ${
                        message.sender === 'user' ? 'text-blue-200' : 'text-gray-500'
                      }`}
                    >
                      {formatTime(message.timestamp)}
                    </div>
                    
                    {/* Show agent type if available */}
                    {message.context?.agent_type && (
                      <div className="text-xs mt-1 opacity-70">
                        Agente: {message.context.agent_type}
                      </div>
                    )}
                    
                    {/* Show legal references if available */}
                    {message.context?.legal_references && message.context.legal_references.length > 0 && (
                      <div className="text-xs mt-1 opacity-70">
                        Refer�ncias: {message.context.legal_references.map((ref: any) => ref.law).join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-3 py-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}} />
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex-shrink-0 border-t bg-white p-4">
        <div className="flex items-end gap-3">
          <textarea
            placeholder={isConnected ? "Digite sua mensagem..." : "Conectando..."}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSend()
              }
            }}
            rows={2}
            className="flex-1 p-3 border border-gray-300 rounded-xl resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed text-sm"
            disabled={!isConnected || isLoading}
          />
          <Button
            onClick={handleSend}
            disabled={!inputMessage.trim() || !isConnected || isLoading}
            size="icon"
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white w-10 h-10 rounded-full shrink-0 transition-all duration-200"
          >
            {isLoading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  )
}
