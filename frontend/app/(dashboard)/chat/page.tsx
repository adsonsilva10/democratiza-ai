'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'

// Mock data dos contratos disponíveis para chat
const availableContracts = [
  {
    id: 1,
    title: 'Contrato de Locação - Apartamento Centro',
    type: 'rental',
    riskLevel: 'medium',
    uploadDate: '2025-09-15',
    emoji: '🏠'
  },
  {
    id: 2,
    title: 'Plano de Internet - Operadora XYZ',
    type: 'telecom',
    riskLevel: 'low',
    uploadDate: '2025-09-10',
    emoji: '📱'
  },
  {
    id: 3,
    title: 'Empréstimo Pessoal - Banco ABC',
    type: 'financial',
    riskLevel: 'high',
    uploadDate: '2025-09-08',
    emoji: '💰'
  },
  {
    id: 4,
    title: 'Seguro Auto - Seguradora DEF',
    type: 'insurance',
    riskLevel: 'medium',
    uploadDate: '2025-09-05',
    emoji: '🛡️'
  },
  {
    id: 5,
    title: 'Conta Corrente - Banco Digital',
    type: 'financial',
    riskLevel: 'low',
    uploadDate: '2025-08-28',
    emoji: '💰'
  },
  {
    id: 6,
    title: 'Plano de Saúde - Operadora Health+',
    type: 'health',
    riskLevel: 'high',
    uploadDate: '2025-08-20',
    emoji: '🏥'
  }
]

const riskColors = {
  low: 'bg-green-100 text-green-800 border-green-300',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  high: 'bg-red-100 text-red-800 border-red-300'
}

const riskLabels = {
  low: 'Baixo',
  medium: 'Médio',
  high: 'Alto'
}

interface ChatMessage {
  id: number
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default function ChatPage() {
  const [selectedContract, setSelectedContract] = useState<typeof availableContracts[0] | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(scrollToBottom, [messages])

  const handleSelectContract = (contract: typeof availableContracts[0]) => {
    setSelectedContract(contract)
    setMessages([{
      id: 1,
      type: 'assistant',
      content: `Olá! Sou sua assistente jurídica especializada em análise de contratos. Selecionei o contrato "${contract.title}" para nossa conversa. Como posso ajudá-lo a entender melhor este documento?

Algumas perguntas que posso responder:
• Quais são os principais riscos deste contrato?
• Existem cláusulas abusivas?
• Como posso cancelar este contrato?
• Quais são meus direitos e deveres?
• Há alternativas de negociação?

Fique à vontade para fazer suas perguntas!`,
      timestamp: new Date()
    }])
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !selectedContract) return

    // Adicionar mensagem do usuário
    const userMessage: ChatMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)

    // Simular resposta da IA (substituir pela integração real)
    setTimeout(() => {
      const assistantResponse: ChatMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: generateMockResponse(inputMessage, selectedContract),
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantResponse])
      setIsTyping(false)
    }, 1500)
  }

  const generateMockResponse = (question: string, contract: typeof availableContracts[0]) => {
    const lowerQuestion = question.toLowerCase()
    
    if (lowerQuestion.includes('risco') || lowerQuestion.includes('perigo')) {
      return `Com base na análise do contrato "${contract.title}", identifiquei os seguintes riscos principais:

${contract.riskLevel === 'high' ? 
  '🔴 **Alto Risco Detectado:**\n• Cláusulas potencialmente abusivas\n• Condições desfavoráveis ao consumidor\n• Possíveis armadilhas contratuais' :
  contract.riskLevel === 'medium' ?
  '🟡 **Risco Moderado:**\n• Algumas cláusulas merecem atenção\n• Termos que podem ser negociados\n• Pontos de vigilância identificados' :
  '🟢 **Baixo Risco:**\n• Contrato bem equilibrado\n• Termos dentro da normalidade\n• Poucos pontos de atenção'
}

Gostaria que eu detalhe algum ponto específico?`
    }

    if (lowerQuestion.includes('cancelar') || lowerQuestion.includes('rescind')) {
      return `Para o contrato "${contract.title}", estas são as condições de cancelamento:

📋 **Procedimentos de Rescisão:**
• Aviso prévio necessário: 30 dias
• Forma de comunicação: Por escrito (carta registrada ou e-mail)
• Multas aplicáveis: Verificar cláusula específica
• Direito de arrependimento: 7 dias (se aplicável)

⚠️ **Atenção:** Sempre verifique as cláusulas de penalidade antes de proceder com o cancelamento.

Quer que eu analise as cláusulas específicas de rescisão deste contrato?`
    }

    if (lowerQuestion.includes('cláusula') || lowerQuestion.includes('clausula')) {
      return `Analisando as cláusulas do contrato "${contract.title}":

📑 **Principais Cláusulas Identificadas:**
• Cláusulas de pagamento e reajuste
• Condições de prestação de serviço
• Penalidades e multas
• Condições de rescisão
• Foro e jurisdição

🔍 **Pontos que merecem atenção:**
• Verifique se há cláusulas de renovação automática
• Observe as condições de reajuste de preços
• Analise as penalidades por inadimplência

Sobre qual cláusula específica você gostaria de saber mais?`
    }

    // Resposta genérica
    return `Entendi sua pergunta sobre "${contract.title}". Com base na análise jurídica deste contrato, posso fornecer orientações específicas sobre os termos e condições.

💡 **Minha recomendação:**
Sempre leia atentamente todas as cláusulas antes de assinar qualquer documento. Este contrato apresenta nível de risco **${riskLabels[contract.riskLevel as keyof typeof riskLabels]}**.

Você pode fazer perguntas mais específicas como:
• "Quais são as multas por cancelamento?"
• "Como funciona o reajuste de preços?"
• "Quais são meus direitos como consumidor?"

Como posso ajudá-lo melhor?`
  }

  return (
    <div className="w-full h-full max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          🤖 Chat com IA Jurídica
        </h1>
        <p className="text-gray-600 text-base sm:text-lg">
          Tire suas dúvidas sobre contratos específicos com nossa assistente especializada
        </p>
      </div>

      <div className="flex flex-col lg:flex-row gap-6 h-[calc(100vh-200px)]">
        
        {/* Painel Esquerdo: Lista de Contratos - 40% */}
        <div className="lg:w-2/5 bg-white rounded-xl shadow-lg p-6 flex flex-col">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              📋 Seus Contratos
            </h2>
            <Link 
              href="/dashboard/historico"
              className="text-blue-600 hover:text-blue-700 text-sm"
            >
              Ver todos →
            </Link>
          </div>

          <div className="flex-1 overflow-y-auto space-y-3">
            {availableContracts.map((contract) => (
              <div
                key={contract.id}
                onClick={() => handleSelectContract(contract)}
                className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 hover:shadow-md ${
                  selectedContract?.id === contract.id
                    ? 'border-blue-500 bg-blue-50 shadow-md'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-3">
                    <span className="text-xl">{contract.emoji}</span>
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900 text-sm leading-tight">
                        {contract.title}
                      </h3>
                    </div>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium border ${
                    riskColors[contract.riskLevel as keyof typeof riskColors]
                  }`}>
                    {riskLabels[contract.riskLevel as keyof typeof riskLabels]}
                  </span>
                </div>
                <p className="text-xs text-gray-600">
                  Analisado em {new Date(contract.uploadDate).toLocaleDateString('pt-BR')}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-4 pt-4 border-t border-gray-200">
            <Link 
              href="/dashboard/analise"
              className="w-full flex items-center justify-center px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
            >
              ➕ Analisar novo contrato
            </Link>
          </div>
        </div>

        {/* Painel Direito: Chat Interface - 60% */}
        <div className="lg:w-3/5 bg-white rounded-xl shadow-lg flex flex-col">
          {selectedContract ? (
            <>
              {/* Header do Chat */}
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{selectedContract.emoji}</span>
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {selectedContract.title}
                    </h3>
                    <p className="text-sm text-gray-600">
                      Assistente IA especializada • Online
                    </p>
                  </div>
                </div>
              </div>

              {/* Área de Mensagens */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] p-4 rounded-lg ${
                        message.type === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">
                        {message.content}
                      </div>
                      <div className={`text-xs mt-2 ${
                        message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                      }`}>
                        {message.timestamp.toLocaleTimeString('pt-BR', { 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}
                      </div>
                    </div>
                  </div>
                ))}

                {isTyping && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 p-4 rounded-lg">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-75"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse delay-150"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input de Mensagem */}
              <div className="p-6 border-t border-gray-200">
                <div className="flex space-x-3">
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Digite sua pergunta sobre o contrato..."
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={!inputMessage.trim()}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Enviar
                  </button>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  💡 Dica: Seja específico em suas perguntas para obter respostas mais precisas
                </p>
              </div>
            </>
          ) : (
            /* Estado Vazio */
            <div className="flex-1 flex items-center justify-center p-12">
              <div className="text-center">
                <div className="text-6xl mb-6">🤖</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Selecione um contrato para começar
                </h3>
                <p className="text-gray-600 mb-8 max-w-md leading-relaxed">
                  Escolha um dos contratos na lista ao lado para iniciar uma conversa 
                  com nossa IA especializada em análise jurídica.
                </p>
                <div className="space-y-3 text-sm text-gray-500">
                  <p className="flex items-center justify-center">
                    <span className="mr-2">✨</span>
                    Respostas personalizadas para cada contrato
                  </p>
                  <p className="flex items-center justify-center">
                    <span className="mr-2">⚡</span>
                    Análise jurídica instantânea
                  </p>
                  <p className="flex items-center justify-center">
                    <span className="mr-2">🔒</span>
                    Informações seguras e confidenciais
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}