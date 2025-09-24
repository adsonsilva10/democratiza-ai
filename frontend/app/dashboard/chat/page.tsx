'use client'

import { useState } from 'react'

interface Message {
  id: number
  text: string
  sender: 'user' | 'ai'
  timestamp: Date
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: 'Olá! Eu sou a IA do Democratiza AI. Posso te ajudar a tirar dúvidas sobre contratos, explicar cláusulas complexas e orientar sobre seus direitos. Como posso ajudar você hoje?',
      sender: 'ai',
      timestamp: new Date()
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isTyping, setIsTyping] = useState(false)

  const quickQuestions = [
    'O que é uma cláusula abusiva?',
    'Como posso cancelar um contrato?',
    'Quais são meus direitos como consumidor?',
    'Como identificar taxas escondidas?',
    'O que fazer se houver cobrança indevida?'
  ]

  const handleSendMessage = () => {
    if (!inputText.trim()) return

    const userMessage: Message = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsTyping(true)

    // Simular resposta da IA
    setTimeout(() => {
      const aiResponse: Message = {
        id: Date.now() + 1,
        text: generateAIResponse(inputText),
        sender: 'ai',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, aiResponse])
      setIsTyping(false)
    }, 2000)
  }

  const generateAIResponse = (question: string): string => {
    const responses = {
      default: 'Entendo sua dúvida sobre contratos. Com base na legislação brasileira e no CDC, posso te orientar que é importante sempre ler todas as cláusulas antes de assinar. Você gostaria que eu analise algum ponto específico do seu contrato?',
      'cláusula abusiva': 'Uma cláusula abusiva é aquela que coloca o consumidor em desvantagem exagerada, como multas desproporcionais, limitações excessivas de direitos ou transferência de responsabilidade do fornecedor para o consumidor. O CDC proíbe essas práticas.',
      'cancelar': 'O direito de cancelamento varia conforme o tipo de contrato. Para contratos feitos fora do estabelecimento comercial (online, telefone, domicílio), você tem 7 dias para desistir sem justificativa (direito de arrependimento). Outros contratos podem ter cláusulas específicas.',
      'direitos': 'Como consumidor, você tem direitos garantidos pelo CDC: informação clara, proteção contra práticas abusivas, direito de arrependimento, garantia dos produtos/serviços, e possibilidade de cancelamento em caso de cláusulas abusivas.'
    }

    const lowerQuestion = question.toLowerCase()
    
    if (lowerQuestion.includes('cláusula') || lowerQuestion.includes('abusiva')) {
      return responses['cláusula abusiva']
    }
    if (lowerQuestion.includes('cancelar') || lowerQuestion.includes('cancelamento')) {
      return responses['cancelar']
    }
    if (lowerQuestion.includes('direito') || lowerQuestion.includes('consumidor')) {
      return responses['direitos']
    }
    
    return responses.default
  }

  const handleQuickQuestion = (question: string) => {
    setInputText(question)
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 sm:p-6 border-b bg-white">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-900">Chat com IA Jurídica</h1>
        <p className="text-sm sm:text-base text-gray-600 mt-1 sm:mt-2">Tire suas dúvidas sobre contratos e direitos do consumidor</p>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row">
        {/* Área do Chat */}
        <div className="flex-1 flex flex-col order-2 lg:order-1">
          {/* Mensagens */}
          <div className="flex-1 overflow-y-auto p-3 sm:p-4 lg:p-6 space-y-3 sm:space-y-4 bg-gray-50">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[85%] sm:max-w-md lg:max-w-3xl px-3 sm:px-4 py-2 sm:py-3 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-900 shadow-sm border'
                }`}>
                  {message.sender === 'ai' && (
                    <div className="flex items-center mb-2">
                      <div className="w-5 h-5 sm:w-6 sm:h-6 bg-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold mr-2">
                        AI
                      </div>
                      <span className="text-xs sm:text-sm text-gray-500">Democratiza AI</span>
                    </div>
                  )}
                  <p className="text-sm sm:text-base leading-relaxed">{message.text}</p>
                  <p className={`text-xs mt-1 sm:mt-2 ${
                    message.sender === 'user' ? 'text-blue-200' : 'text-gray-400'
                  }`}>
                    {message.timestamp.toLocaleTimeString('pt-BR', { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </p>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-white text-gray-900 shadow-sm border max-w-[85%] sm:max-w-md lg:max-w-3xl px-3 sm:px-4 py-2 sm:py-3 rounded-lg">
                  <div className="flex items-center mb-2">
                    <div className="w-5 h-5 sm:w-6 sm:h-6 bg-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold mr-2">
                      AI
                    </div>
                    <span className="text-xs sm:text-sm text-gray-500">Democratiza AI está digitando...</span>
                  </div>
                  <div className="flex space-x-1">
                    <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input de mensagem */}
          <div className="p-3 sm:p-4 lg:p-6 bg-white border-t">
            <div className="flex gap-2 sm:gap-3 lg:gap-4">
              <div className="flex-1">
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Digite sua pergunta sobre contratos..."
                  className="w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <button
                onClick={handleSendMessage}
                disabled={!inputText.trim() || isTyping}
                className={`px-3 sm:px-4 lg:px-6 py-2 sm:py-3 rounded-lg font-medium transition-colors text-sm sm:text-base ${
                  inputText.trim() && !isTyping
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                <span className="hidden sm:inline">Enviar</span>
                <span className="sm:hidden">📤</span>
              </button>
            </div>
          </div>
        </div>

        {/* Sidebar com perguntas rápidas - Mobile primeiro */}
        <div className="lg:w-80 bg-white border-t lg:border-t-0 lg:border-l p-3 sm:p-4 lg:p-6 order-1 lg:order-2">
          <h3 className="font-semibold text-gray-900 mb-3 lg:mb-4 text-sm sm:text-base">Perguntas Frequentes</h3>
          
          {/* Mobile: scroll horizontal, Desktop: vertical */}
          <div className="flex lg:flex-col gap-2 lg:gap-3 overflow-x-auto lg:overflow-x-visible pb-2 lg:pb-0">
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleQuickQuestion(question)}
                className="flex-shrink-0 lg:flex-shrink lg:w-full text-left p-2 sm:p-3 text-xs sm:text-sm text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors whitespace-nowrap lg:whitespace-normal min-w-[200px] lg:min-w-0"
              >
                {question}
              </button>
            ))}
          </div>

          <div className="mt-4 lg:mt-8 p-3 sm:p-4 bg-blue-50 rounded-lg">
            <div className="text-blue-600 mb-2">
              <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h4 className="font-medium text-gray-900 mb-1 text-sm sm:text-base">Dica</h4>
            <p className="text-xs sm:text-sm text-gray-600">
              Para uma análise mais precisa, você pode fazer upload do seu contrato na página de Análise.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}