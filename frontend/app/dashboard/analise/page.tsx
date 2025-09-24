'use client'

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'

interface AnalysisResult {
  id: string
  fileName: string
  contractType: string
  riskLevel: 'Alto' | 'Médio' | 'Baixo'
  riskScore: number
  summary: string
  issues: Array<{
    type: 'critical' | 'warning' | 'info'
    title: string
    description: string
    clause: string
    suggestion?: string
  }>
  analysis: {
    abusiveClauses: number
    financialRisks: number
    legalCompliance: number
    consumerRights: number
  }
}

interface ChatMessage {
  id: string
  text: string
  sender: 'user' | 'ai'
  timestamp: Date
}

export default function AnalisePage() {
  const searchParams = useSearchParams()
  const contratoId = searchParams?.get('contratoId')
  
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [showResults, setShowResults] = useState(false)
  const [showChat, setShowChat] = useState(false)
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([])
  const [chatInput, setChatInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setUploadedFile(file)
    }
  }

  const handleAnalyzeContract = () => {
    setIsAnalyzing(true)
    // Simular análise por 3 segundos
    setTimeout(() => {
      setIsAnalyzing(false)
      // Simular resultado da análise
      const mockResult: AnalysisResult = {
        id: 'analysis-' + Date.now(),
        fileName: uploadedFile?.name || 'contrato.pdf',
        contractType: 'Locação Residencial',
        riskLevel: 'Alto',
        riskScore: 8.2,
        summary: 'Este contrato apresenta várias cláusulas que podem ser prejudiciais ao locatário, incluindo multas excessivas e limitações de direitos.',
        issues: [
          {
            type: 'critical',
            title: 'Cláusula de Multa Abusiva',
            description: 'Multa de rescisão de 6 meses de aluguel é considerada excessiva pela legislação.',
            clause: 'Cláusula 15.2 - "Em caso de rescisão antecipada pelo locatário, será cobrada multa de 6 (seis) meses de aluguel."',
            suggestion: 'A multa máxima legal é de 3 meses de aluguel. Negocie a redução desta cláusula.'
          },
          {
            type: 'critical',
            title: 'Transferência Indevida de Responsabilidade',
            description: 'O locatário está assumindo responsabilidades que são do proprietário.',
            clause: 'Cláusula 8.1 - "Todas as despesas de manutenção e reparos são de responsabilidade do locatário."',
            suggestion: 'Reparos estruturais e manutenção predial devem ser responsabilidade do proprietário.'
          },
          {
            type: 'warning',
            title: 'Reajuste Anual Automático',
            description: 'Cláusula de reajuste pode gerar aumentos acima da inflação.',
            clause: 'Cláusula 4.3 - "O valor do aluguel será reajustado anualmente pelo IGPM."',
            suggestion: 'Considere negociar um teto máximo para o reajuste anual.'
          },
          {
            type: 'info',
            title: 'Prazo de Aviso Prévio',
            description: 'Prazo de 90 dias para aviso prévio está dentro da normalidade.',
            clause: 'Cláusula 12.1 - "O aviso prévio para rescisão deve ser de 90 dias."'
          }
        ],
        analysis: {
          abusiveClauses: 2,
          financialRisks: 3,
          legalCompliance: 6,
          consumerRights: 4
        }
      }
      setAnalysisResult(mockResult)
      setShowResults(true)
    }, 3000)
  }

  const handleNewAnalysis = () => {
    setShowResults(false)
    setAnalysisResult(null)
    setUploadedFile(null)
    setShowChat(false)
    setChatMessages([])
  }

  // Carregar contrato existente se vier do histórico
  useEffect(() => {
    if (contratoId) {
      // Simular carregamento do contrato do histórico
      const mockResult: AnalysisResult = {
        id: contratoId,
        fileName: 'contrato_locacao_101.pdf',
        contractType: 'Locação Residencial',
        riskLevel: 'Alto',
        riskScore: 8.2,
        summary: 'Este contrato apresenta várias cláusulas que podem ser prejudiciais ao locatário, incluindo multas excessivas e limitações de direitos.',
        issues: [
          {
            type: 'critical',
            title: 'Cláusula de Multa Abusiva',
            description: 'Multa de rescisão de 6 meses de aluguel é considerada excessiva pela legislação.',
            clause: 'Cláusula 15.2 - "Em caso de rescisão antecipada pelo locatário, será cobrada multa de 6 (seis) meses de aluguel."',
            suggestion: 'A multa máxima legal é de 3 meses de aluguel. Negocie a redução desta cláusula.'
          },
          {
            type: 'critical',
            title: 'Transferência Indevida de Responsabilidade',
            description: 'O locatário está assumindo responsabilidades que são do proprietário.',
            clause: 'Cláusula 8.1 - "Todas as despesas de manutenção e reparos são de responsabilidade do locatário."',
            suggestion: 'Reparos estruturais e manutenção predial devem ser responsabilidade do proprietário.'
          },
          {
            type: 'warning',
            title: 'Reajuste Anual Automático',
            description: 'Cláusula de reajuste pode gerar aumentos acima da inflação.',
            clause: 'Cláusula 4.3 - "O valor do aluguel será reajustado anualmente pelo IGPM."',
            suggestion: 'Considere negociar um teto máximo para o reajuste anual.'
          }
        ],
        analysis: {
          abusiveClauses: 2,
          financialRisks: 3,
          legalCompliance: 6,
          consumerRights: 4
        }
      }
      setAnalysisResult(mockResult)
      setShowResults(true)
    }
  }, [contratoId])

  const handleChatToggle = () => {
    setShowChat(!showChat)
    if (!showChat && chatMessages.length === 0) {
      // Inicializar chat com mensagem da IA
      const welcomeMessage: ChatMessage = {
        id: 'welcome-' + Date.now(),
        text: `Olá! Analisei seu contrato "${analysisResult?.fileName}" e identifiquei alguns pontos importantes. Posso esclarecer dúvidas sobre as cláusulas, explicar os riscos encontrados ou sugerir como proceder. O que gostaria de saber?`,
        sender: 'ai',
        timestamp: new Date()
      }
      setChatMessages([welcomeMessage])
    }
  }

  const handleSendMessage = async () => {
    if (!chatInput.trim() || isTyping) return

    const userMessage: ChatMessage = {
      id: 'user-' + Date.now(),
      text: chatInput,
      sender: 'user',
      timestamp: new Date()
    }

    setChatMessages(prev => [...prev, userMessage])
    setChatInput('')
    setIsTyping(true)

    // Simular chamada RAG para o backend
    try {
      // Aqui seria a chamada real para o backend com RAG
      const response = await fetch('/api/v1/chat/contract', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contractId: analysisResult?.id,
          message: chatInput,
          context: analysisResult
        }),
      })

      // Por enquanto, simular resposta
      setTimeout(() => {
        const aiResponse: ChatMessage = {
          id: 'ai-' + Date.now(),
          text: generateContextualResponse(chatInput, analysisResult),
          sender: 'ai',
          timestamp: new Date()
        }
        setChatMessages(prev => [...prev, aiResponse])
        setIsTyping(false)
      }, 2000)
    } catch (error) {
      setIsTyping(false)
    }
  }

  const generateContextualResponse = (question: string, contract: AnalysisResult | null): string => {
    const lowerQuestion = question.toLowerCase()
    
    if (lowerQuestion.includes('multa') || lowerQuestion.includes('rescisão')) {
      return 'Sobre a multa de rescisão: identifiquei que o contrato prevê 6 meses de aluguel, o que é excessivo. Pela Lei do Inquilinato (Lei 8.245/91), a multa não pode exceder 3 meses. Você pode negociar a redução ou questionar juridicamente se já assinou.'
    }
    
    if (lowerQuestion.includes('manutenção') || lowerQuestion.includes('reparo')) {
      return 'Quanto à manutenção: o contrato transfere todos os reparos para você, mas isso não é correto. Reparos estruturais, problemas elétricos/hidráulicos principais e questões prediais são responsabilidade do proprietário. Apenas pequenos reparos e manutenção básica são do locatário.'
    }
    
    if (lowerQuestion.includes('reajuste') || lowerQuestion.includes('aumento')) {
      return 'Sobre o reajuste: o contrato usa o IGPM, que pode ser mais alto que outros índices. Você pode sugerir o IPCA ou negociar um teto máximo anual. O reajuste só pode ocorrer após 12 meses do contrato ou do último reajuste.'
    }
    
    if (lowerQuestion.includes('direito') || lowerQuestion.includes('posso')) {
      return 'Seus direitos como locatário incluem: receber o imóvel em boas condições, ter privacidade, não sofrer aumentos abusivos, e poder rescindir o contrato (respeitando as condições). Posso explicar qualquer direito específico que tenha dúvida.'
    }
    
    return `Analisando sua pergunta sobre o contrato de ${contract?.contractType}, posso dizer que é importante sempre verificar se as cláusulas respeitam seus direitos como consumidor. Gostaria que eu explique algum ponto específico das ${contract?.issues.length} questões que identifiquei?`
  }

  if (showResults && analysisResult) {
    return (
      <div className="p-4 sm:p-6">
        {/* Header com resultado */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2">Análise Concluída</h1>
            <p className="text-sm sm:text-base text-gray-600">{analysisResult.fileName}</p>
          </div>
          <button
            onClick={handleNewAnalysis}
            className="mt-3 sm:mt-0 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm sm:text-base"
          >
            Nova Análise
          </button>
        </div>

        {/* Resumo do Risco */}
        <div className="bg-white rounded-lg shadow p-4 sm:p-6 mb-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
            <div>
              <h2 className="text-lg sm:text-xl font-semibold text-gray-900">Nível de Risco</h2>
              <p className="text-sm text-gray-600">{analysisResult.contractType}</p>
            </div>
            <div className="mt-3 sm:mt-0 flex items-center gap-3">
              <div className="text-right">
                <div className={`text-2xl sm:text-3xl font-bold ${
                  analysisResult.riskLevel === 'Alto' ? 'text-red-600' :
                  analysisResult.riskLevel === 'Médio' ? 'text-yellow-600' : 'text-green-600'
                }`}>
                  {analysisResult.riskScore}/10
                </div>
                <div className={`text-sm font-medium ${
                  analysisResult.riskLevel === 'Alto' ? 'text-red-600' :
                  analysisResult.riskLevel === 'Médio' ? 'text-yellow-600' : 'text-green-600'
                }`}>
                  {analysisResult.riskLevel} Risco
                </div>
              </div>
              <div className={`w-12 h-12 sm:w-16 sm:h-16 rounded-full flex items-center justify-center ${
                analysisResult.riskLevel === 'Alto' ? 'bg-red-100' :
                analysisResult.riskLevel === 'Médio' ? 'bg-yellow-100' : 'bg-green-100'
              }`}>
                <span className="text-xl sm:text-2xl">
                  {analysisResult.riskLevel === 'Alto' ? '⚠️' :
                   analysisResult.riskLevel === 'Médio' ? '⚡' : '✅'}
                </span>
              </div>
            </div>
          </div>
          <p className="text-sm sm:text-base text-gray-700 leading-relaxed">{analysisResult.summary}</p>
        </div>

        {/* Métricas de Análise */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6">
          <div className="bg-white p-3 sm:p-4 rounded-lg shadow text-center">
            <div className="text-lg sm:text-2xl font-bold text-red-600">{analysisResult.analysis.abusiveClauses}</div>
            <div className="text-xs sm:text-sm text-gray-600">Cláusulas Abusivas</div>
          </div>
          <div className="bg-white p-3 sm:p-4 rounded-lg shadow text-center">
            <div className="text-lg sm:text-2xl font-bold text-yellow-600">{analysisResult.analysis.financialRisks}</div>
            <div className="text-xs sm:text-sm text-gray-600">Riscos Financeiros</div>
          </div>
          <div className="bg-white p-3 sm:p-4 rounded-lg shadow text-center">
            <div className="text-lg sm:text-2xl font-bold text-blue-600">{analysisResult.analysis.legalCompliance}</div>
            <div className="text-xs sm:text-sm text-gray-600">Conformidade Legal</div>
          </div>
          <div className="bg-white p-3 sm:p-4 rounded-lg shadow text-center">
            <div className="text-lg sm:text-2xl font-bold text-green-600">{analysisResult.analysis.consumerRights}</div>
            <div className="text-xs sm:text-sm text-gray-600">Direitos Protegidos</div>
          </div>
        </div>

        {/* Ações Recomendadas */}
        <div className="bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-200 rounded-lg p-4 mb-6">
          <h3 className="text-lg font-semibold text-indigo-900 mb-3">Próximos Passos</h3>
          <div className="flex flex-wrap gap-2">
            <button 
              onClick={() => setChatInput('Como posso contestar as cláusulas abusivas?')}
              className="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm"
            >
              📋 Contestar Cláusulas
            </button>
            <button 
              onClick={() => setChatInput('Quais são meus direitos neste contrato?')}
              className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
            >
              ⚖️ Meus Direitos
            </button>
            <button 
              onClick={() => setChatInput('Como posso negociar melhores condições?')}
              className="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
            >
              🤝 Negociar
            </button>
            <button className="px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm">
              📄 Gerar Relatório
            </button>
          </div>
        </div>

        {/* Problemas Identificados */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-4 sm:p-6 border-b">
            <h3 className="text-lg font-semibold text-gray-900">Problemas Identificados</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {analysisResult.issues.map((issue, index) => (
              <div key={index} className="p-4 sm:p-6">
                <div className="flex items-start gap-3">
                  <div className={`flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 rounded-full flex items-center justify-center ${
                    issue.type === 'critical' ? 'bg-red-100 text-red-600' :
                    issue.type === 'warning' ? 'bg-yellow-100 text-yellow-600' : 'bg-blue-100 text-blue-600'
                  }`}>
                    <span className="text-sm sm:text-base">
                      {issue.type === 'critical' ? '🚨' : issue.type === 'warning' ? '⚠️' : 'ℹ️'}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm sm:text-base font-medium text-gray-900 mb-2">{issue.title}</h4>
                    <p className="text-xs sm:text-sm text-gray-600 mb-3">{issue.description}</p>
                    
                    <div className="bg-gray-50 p-3 rounded-lg mb-3">
                      <p className="text-xs sm:text-sm font-medium text-gray-700 mb-1">Cláusula:</p>
                      <p className="text-xs sm:text-sm text-gray-600 italic">"{issue.clause}"</p>
                    </div>
                    
                    {issue.suggestion && (
                      <div className="bg-green-50 p-3 rounded-lg">
                        <p className="text-xs sm:text-sm font-medium text-green-800 mb-1">💡 Sugestão:</p>
                        <p className="text-xs sm:text-sm text-green-700">{issue.suggestion}</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chat Integrado */}
        {showChat && (
          <div className="mt-6 bg-white rounded-lg shadow">
            <div className="p-4 border-b flex items-center justify-between">
              <h3 className="font-semibold text-gray-900">Chat sobre o Contrato</h3>
              <button
                onClick={() => setShowChat(false)}
                className="p-1 text-gray-400 hover:text-gray-600"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="h-80 overflow-y-auto p-4 space-y-4">
              {chatMessages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[80%] px-3 py-2 rounded-lg text-sm ${
                    message.sender === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}>
                    {message.sender === 'ai' && (
                      <div className="flex items-center mb-1">
                        <div className="w-4 h-4 bg-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold mr-2">
                          AI
                        </div>
                        <span className="text-xs text-gray-500">Democratiza AI</span>
                      </div>
                    )}
                    <p>{message.text}</p>
                    <p className={`text-xs mt-1 ${
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
                  <div className="bg-gray-100 text-gray-900 max-w-[80%] px-3 py-2 rounded-lg text-sm">
                    <div className="flex items-center mb-1">
                      <div className="w-4 h-4 bg-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold mr-2">
                        AI
                      </div>
                      <span className="text-xs text-gray-500">Analisando...</span>
                    </div>
                    <div className="flex space-x-1">
                      <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div className="p-4 border-t">
              {/* Perguntas Sugeridas */}
              {chatMessages.length <= 1 && (
                <div className="mb-4">
                  <p className="text-xs text-gray-500 mb-2">Perguntas sugeridas:</p>
                  <div className="flex flex-wrap gap-2">
                    {[
                      'Como posso contestar a multa?',
                      'Quais são meus direitos?',
                      'O reajuste está correto?',
                      'Posso negociar as cláusulas?'
                    ].map((suggestion) => (
                      <button
                        key={suggestion}
                        onClick={() => setChatInput(suggestion)}
                        className="px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded hover:bg-blue-100 transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Pergunte sobre o contrato..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!chatInput.trim() || isTyping}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors text-sm ${
                    chatInput.trim() && !isTyping
                      ? 'bg-blue-600 text-white hover:bg-blue-700'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  Enviar
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Ações Rápidas */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
          <button 
            onClick={handleChatToggle}
            className={`flex items-center justify-center gap-2 p-3 sm:p-4 rounded-lg transition-colors ${
              showChat 
                ? 'bg-blue-700 text-white' 
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            <span className="text-sm sm:text-base">💬</span>
            <span className="text-sm sm:text-base font-medium">
              {showChat ? 'Fechar Chat' : 'Conversar com IA'}
            </span>
          </button>
          <button className="flex items-center justify-center gap-2 p-3 sm:p-4 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
            <span className="text-sm sm:text-base">📄</span>
            <span className="text-sm sm:text-base font-medium">Baixar Relatório</span>
          </button>
          <button className="flex items-center justify-center gap-2 p-3 sm:p-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
            <span className="text-sm sm:text-base">📤</span>
            <span className="text-sm sm:text-base font-medium">Compartilhar</span>
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 sm:p-6">
      <h1 className="text-xl sm:text-2xl font-bold text-gray-900 mb-6">Análise de Contratos</h1>
      
      {/* Upload Section */}
      <div className="bg-white rounded-lg shadow p-4 sm:p-6 mb-6 sm:mb-8">
        <h2 className="text-base sm:text-lg font-semibold text-gray-900 mb-4">Fazer Upload do Contrato</h2>
        
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 sm:p-8 text-center hover:border-blue-400 transition-colors">
          <div className="space-y-3 sm:space-y-4">
            <div className="text-gray-400">
              <svg className="w-10 h-10 sm:w-12 sm:h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            
            <div>
              <h3 className="text-base sm:text-lg font-medium text-gray-900 mb-2">
                {uploadedFile ? uploadedFile.name : 'Arraste e solte seu contrato aqui'}
              </h3>
              <p className="text-sm sm:text-base text-gray-500">
                {uploadedFile ? 'Arquivo selecionado! Clique em analisar para continuar.' : 'Ou clique para selecionar um arquivo'}
              </p>
              <p className="text-xs sm:text-sm text-gray-400 mt-2">Suporta PDF, DOC, DOCX até 10MB</p>
            </div>
            
            <div>
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="inline-flex items-center px-4 sm:px-6 py-2 sm:py-3 border border-transparent text-sm sm:text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 cursor-pointer transition-colors"
              >
                📎 Selecionar Arquivo
              </label>
            </div>
          </div>
        </div>
        
        {uploadedFile && (
          <div className="mt-4 sm:mt-6 flex justify-center">
            <button
              onClick={handleAnalyzeContract}
              disabled={isAnalyzing}
              className={`px-6 sm:px-8 py-2 sm:py-3 rounded-lg font-semibold transition-colors text-sm sm:text-base ${
                isAnalyzing 
                  ? 'bg-gray-400 text-gray-700 cursor-not-allowed' 
                  : 'bg-green-600 text-white hover:bg-green-700'
              }`}
            >
              {isAnalyzing ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-4 w-4 sm:h-5 sm:w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analisando...
                </span>
              ) : (
                '🔍 Analisar Contrato'
              )}
            </button>
          </div>
        )}
      </div>

      {/* Analysis Types */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-6 sm:mb-8">
        <div className="bg-white rounded-lg shadow p-4 sm:p-6">
          <div className="text-blue-600 mb-3 sm:mb-4">
            <svg className="w-6 h-6 sm:w-8 sm:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Análise Rápida</h3>
          <p className="text-sm sm:text-base text-gray-600">Identificação automática de cláusulas abusivas e pontos de atenção</p>
        </div>

        <div className="bg-white rounded-lg shadow p-4 sm:p-6">
          <div className="text-purple-600 mb-3 sm:mb-4">
            <svg className="w-6 h-6 sm:w-8 sm:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Análise Profunda</h3>
          <p className="text-sm sm:text-base text-gray-600">Análise detalhada com sugestões de melhorias e alternativas</p>
        </div>

        <div className="bg-white rounded-lg shadow p-4 sm:p-6 sm:col-span-2 lg:col-span-1">
          <div className="text-green-600 mb-3 sm:mb-4">
            <svg className="w-6 h-6 sm:w-8 sm:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2">Chat Assistido</h3>
          <p className="text-sm sm:text-base text-gray-600">Converse com nossa IA sobre dúvidas específicas do contrato</p>
        </div>
      </div>

      {/* Recent Analysis */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-4 sm:p-6 border-b">
          <h2 className="text-base sm:text-lg font-medium text-gray-900">Análises Recentes</h2>
        </div>
        <div className="p-4 sm:p-6">
          <div className="text-center py-6 sm:py-8 text-gray-500">
            <svg className="w-10 h-10 sm:w-12 sm:h-12 mx-auto mb-3 sm:mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-sm sm:text-base">Nenhuma análise realizada ainda. Faça upload de um contrato para começar!</p>
          </div>
        </div>
      </div>
    </div>
  )
}