'use client'

import { useState, useRef, useEffect } from 'react'

interface Message {
  id: string
  text: string
  sender: 'user' | 'agent'
  timestamp: Date
  typing?: boolean
}

interface SimpleChatProps {
  contractId?: string
  agentType?: 'rental' | 'telecom' | 'financial' | 'classifier'
  className?: string
}

const AGENT_NAMES = {
  rental: 'Agente de Locação',
  telecom: 'Agente de Telecomunicações',
  financial: 'Agente Financeiro',
  classifier: 'Agente Classificador'
}

const AGENT_EMOJIS = {
  rental: '🏠',
  telecom: '📱',
  financial: '💰',
  classifier: '🤖'
}

export default function SimpleChat({ 
  contractId, 
  agentType = 'classifier',
  className = '' 
}: SimpleChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: `Olá! Sou o ${AGENT_NAMES[agentType]} ${AGENT_EMOJIS[agentType]}. Como posso ajudá-lo a entender melhor seu contrato?`,
      sender: 'agent',
      timestamp: new Date()
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const simulateAgentResponse = async (userMessage: string): Promise<string> => {
    // Simular delay de processamento
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))

    // Respostas mockadas baseadas no tipo de agente
    const responses = {
      rental: [
        'Analisando as cláusulas de locação do seu contrato...',
        'Identifiquei algumas questões importantes sobre reajuste de aluguel.',
        'Esta cláusula de multa parece estar dentro dos padrões legais.',
        'Recomendo atenção especial à cláusula de rescisão antecipada.'
      ],
      telecom: [
        'Verificando as condições do seu plano de telecomunicações...',
        'Encontrei informações sobre fidelidade e cancelamento.',
        'Os valores de multa estão de acordo com a regulamentação da ANATEL.',
        'Esta cláusula sobre velocidade de internet precisa ser avaliada.'
      ],
      financial: [
        'Analisando os termos financeiros do contrato...',
        'As taxas de juros estão dentro dos limites permitidos pelo Banco Central.',
        'Identifiquei algumas cláusulas que podem gerar custos adicionais.',
        'Recomendo revisar as condições de pagamento antecipado.'
      ],
      classifier: [
        'Analisando o tipo e categoria do contrato...',
        'Este parece ser um contrato de prestação de serviços.',
        'Identifiquei elementos típicos de contratos B2C.',
        'Classificando o nível de risco baseado nas cláusulas encontradas.'
      ]
    }

    // Selecionar resposta baseada no conteúdo da mensagem
    const agentResponses = responses[agentType]
    if (userMessage.toLowerCase().includes('cláusula')) {
      return `Sobre cláusulas: ${agentResponses[Math.floor(Math.random() * agentResponses.length)]}`
    } else if (userMessage.toLowerCase().includes('multa')) {
      return `Sobre multas: ${agentResponses[Math.floor(Math.random() * agentResponses.length)]}`
    } else if (userMessage.toLowerCase().includes('rescisão')) {
      return `Sobre rescisão: ${agentResponses[Math.floor(Math.random() * agentResponses.length)]}`
    } else {
      return agentResponses[Math.floor(Math.random() * agentResponses.length)]
    }
  }

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText.trim(),
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsLoading(true)

    // Adicionar indicador de digitação
    const typingMessage: Message = {
      id: 'typing',
      text: '...',
      sender: 'agent',
      timestamp: new Date(),
      typing: true
    }
    setMessages(prev => [...prev, typingMessage])

    try {
      const agentResponse = await simulateAgentResponse(userMessage.text)
      
      // Remover indicador de digitação e adicionar resposta
      setMessages(prev => {
        const withoutTyping = prev.filter(msg => msg.id !== 'typing')
        return [...withoutTyping, {
          id: Date.now().toString(),
          text: agentResponse,
          sender: 'agent',
          timestamp: new Date()
        }]
      })
    } catch (error) {
      setMessages(prev => {
        const withoutTyping = prev.filter(msg => msg.id !== 'typing')
        return [...withoutTyping, {
          id: Date.now().toString(),
          text: 'Desculpe, ocorreu um erro. Tente novamente.',
          sender: 'agent',
          timestamp: new Date()
        }]
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('pt-BR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className={`bg-white rounded-lg shadow-lg flex flex-col h-96 ${className}`}>
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">{AGENT_EMOJIS[agentType]}</span>
          <div>
            <h3 className="font-semibold">{AGENT_NAMES[agentType]}</h3>
            <p className="text-sm opacity-90">
              {isLoading ? 'Digitando...' : 'Online'}
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`
                max-w-xs lg:max-w-md px-4 py-2 rounded-lg
                ${message.sender === 'user'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-gray-100 text-gray-900 rounded-bl-none'
                }
                ${message.typing ? 'animate-pulse' : ''}
              `}
            >
              <p className="text-sm">{message.text}</p>
              <p className={`text-xs mt-1 ${
                message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'
              }`}>
                {formatTime(message.timestamp)}
              </p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <textarea
            ref={inputRef}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Digite sua pergunta sobre o contrato..."
            className="flex-1 p-2 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={2}
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white p-2 rounded-lg transition-colors"
          >
            {isLoading ? '⏳' : '📤'}
          </button>
        </div>
        
        <div className="mt-2 flex flex-wrap gap-2">
          {['Explicar cláusulas', 'Verificar multas', 'Condições de rescisão'].map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => {
                setInputText(suggestion)
                inputRef.current?.focus()
              }}
              className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-2 py-1 rounded transition-colors"
              disabled={isLoading}
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}