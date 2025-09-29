'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { 
  ArrowLeft, 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  FileText, 
  Download, 
  Share2,
  MessageCircle,
  Send,
  Bot,
  User,
  Loader2,
  ChevronDown,
  ChevronUp
} from 'lucide-react'

// Interface para mensagens do chat
interface ChatMessage {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
}

// Interface expandida para análise
interface ContractAnalysis {
  id: string
  fileName: string
  contractType: 'rental' | 'telecom' | 'financial' | 'insurance'
  analysisDate: string
  riskLevel: 'alto' | 'medio' | 'baixo'
  status: 'completed' | 'processing' | 'error'
  issuesFound: number
  positivePoints: number
  fileSize: string
  overallScore: number
  problems: Array<{
    id: string
    title: string
    description: string
    severity: 'alto' | 'medio' | 'baixo'
    clause: string
    recommendation: string
    category: string
  }>
  positives: Array<{
    id: string
    title: string
    description: string
    clause: string
    category: string
  }>
}

// Mock data expandido
const mockAnalysis: ContractAnalysis = {
  id: '1',
  fileName: 'Contrato de Locação - Apto 101.pdf',
  contractType: 'rental',
  analysisDate: '2025-09-20T14:30:00Z',
  riskLevel: 'alto',
  status: 'completed',
  issuesFound: 7,
  positivePoints: 5,
  fileSize: '2.4 MB',
  overallScore: 6.2,
  problems: [
    {
      id: '1',
      title: 'Cláusula de Reajuste Abusiva',
      description: 'O contrato prevê reajuste semestral acima do índice legal permitido.',
      severity: 'alto',
      clause: 'Cláusula 12.1: "O valor do aluguel será reajustado semestralmente pelo índice IPCA + 2%"',
      recommendation: 'Negociar reajuste anual conforme lei 8.245/91, limitado ao IPCA ou IGPM.',
      category: 'Condições Financeiras'
    },
    {
      id: '2',
      title: 'Multa Rescisória Desproporcional',
      description: 'Multa por rescisão antecipada excede o limite legal de 3 aluguéis.',
      severity: 'alto',
      clause: 'Cláusula 15.2: "Em caso de rescisão antecipada, multa de 6 meses de aluguel"',
      recommendation: 'Reduzir multa para no máximo 3 aluguéis conforme legislação vigente.',
      category: 'Penalidades'
    },
    {
      id: '3',
      title: 'Responsabilidade por Danos Estruturais',
      description: 'Locatário responsabilizado por danos que são de responsabilidade do proprietário.',
      severity: 'medio',
      clause: 'Cláusula 8.3: "Locatário responsável por todos os reparos no imóvel"',
      recommendation: 'Especificar que reparos estruturais são de responsabilidade do locador.',
      category: 'Responsabilidades'
    }
  ],
  positives: [
    {
      id: '1',
      title: 'Prazo de Aviso Prévio Adequado',
      description: 'Contrato estabelece prazo de 30 dias para aviso prévio, conforme legislação.',
      clause: 'Cláusula 14.1: "Qualquer das partes deverá comunicar com 30 dias de antecedência"',
      category: 'Prazos'
    },
    {
      id: '2',
      title: 'Garantia Locatícia Clara',
      description: 'Forma de garantia bem definida sem exigências abusivas.',
      clause: 'Cláusula 5.1: "Garantia mediante fiador ou seguro-fiança"',
      category: 'Garantias'
    },
    {
      id: '3',
      title: 'Descrição Detalhada do Imóvel',
      description: 'Imóvel bem caracterizado com área, dependências e estado de conservação.',
      clause: 'Cláusula 2.1: Descrição completa das dependências e características',
      category: 'Especificações'
    }
  ]
}

const contractTypeLabels = {
  rental: { label: 'Locação', icon: '🏠', color: 'bg-blue-50 text-blue-700 border-blue-200' },
  telecom: { label: 'Telecom', icon: '📱', color: 'bg-green-50 text-green-700 border-green-200' },
  financial: { label: 'Financeiro', icon: '💳', color: 'bg-purple-50 text-purple-700 border-purple-200' },
  insurance: { label: 'Seguro', icon: '🛡️', color: 'bg-orange-50 text-orange-700 border-orange-200' }
}

const riskLevelConfig = {
  alto: { label: 'Alto Risco', color: 'bg-red-100 text-red-800 border-red-200', icon: AlertTriangle },
  medio: { label: 'Médio Risco', color: 'bg-yellow-100 text-yellow-800 border-yellow-200', icon: Clock },
  baixo: { label: 'Baixo Risco', color: 'bg-green-100 text-green-800 border-green-200', icon: CheckCircle }
}

const severityConfig = {
  alto: { color: 'bg-red-50 border-red-200 text-red-800', icon: AlertTriangle },
  medio: { color: 'bg-yellow-50 border-yellow-200 text-yellow-800', icon: Clock },
  baixo: { color: 'bg-blue-50 border-blue-200 text-blue-800', icon: CheckCircle }
}

export default function ResultadoPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const contractId = searchParams.get('id')
  const [loading, setLoading] = useState(true)
  const [analysis, setAnalysis] = useState<ContractAnalysis | null>(null)
  const [expandedProblems, setExpandedProblems] = useState<Set<string>>(new Set())
  
  // Estados do Chat
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'assistant',
      content: 'Olá! Sou o assistente de análise de contratos da Democratiza AI. Posso responder perguntas sobre seu contrato ou esclarecer dúvidas jurídicas. Como posso ajudar?',
      timestamp: new Date()
    }
  ])
  const [chatInput, setChatInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [isChatExpanded, setIsChatExpanded] = useState(false)
  const chatEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Simular carregamento
    const timer = setTimeout(() => {
      setAnalysis(mockAnalysis)
      // Expandir todos os problemas por padrão
      const allProblemIds = new Set(mockAnalysis.problems.map(p => p.id))
      setExpandedProblems(allProblemIds)
      setLoading(false)
    }, 1500)

    return () => clearTimeout(timer)
  }, [contractId])

  useEffect(() => {
    // Auto-scroll do chat
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [chatMessages])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Carregando Análise</h2>
          <p className="text-gray-600">Processando dados do contrato...</p>
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Análise Não Encontrada</h2>
          <p className="text-gray-600 mb-4">Não foi possível carregar os dados da análise.</p>
          <Button onClick={() => router.push('/plataforma/historico')}>
            Voltar ao Histórico
          </Button>
        </div>
      </div>
    )
  }

  const contractConfig = contractTypeLabels[analysis.contractType]
  const riskConfig = riskLevelConfig[analysis.riskLevel]
  const RiskIcon = riskConfig.icon

  const toggleProblem = (problemId: string) => {
    const newExpanded = new Set(expandedProblems)
    if (newExpanded.has(problemId)) {
      newExpanded.delete(problemId)
    } else {
      newExpanded.add(problemId)
    }
    setExpandedProblems(newExpanded)
  }

  const handleSendMessage = async () => {
    if (!chatInput.trim()) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: chatInput.trim(),
      timestamp: new Date()
    }

    setChatMessages(prev => [...prev, userMessage])
    setChatInput('')
    setIsTyping(true)

    // Simular resposta da IA
    setTimeout(() => {
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: generateResponseForQuestion(userMessage.content),
        timestamp: new Date()
      }
      setChatMessages(prev => [...prev, assistantMessage])
      setIsTyping(false)
    }, 2000)
  }

  const generateResponseForQuestion = (question: string): string => {
    const lowerQuestion = question.toLowerCase()
    
    if (lowerQuestion.includes('multa') || lowerQuestion.includes('rescis')) {
      return 'Com base na análise do seu contrato, identifiquei que a multa rescisória de 6 meses está acima do limite legal. A Lei do Inquilinato (8.245/91) permite multa máxima de 3 aluguéis. Recomendo negociar essa redução antes da assinatura.'
    }
    
    if (lowerQuestion.includes('reajuste') || lowerQuestion.includes('aluguel')) {
      return 'O reajuste semestral previsto no contrato não está de acordo com a legislação. A lei permite reajuste anual, limitado a índices como IPCA ou IGPM. O "IPCA + 2%" pode ser considerado abusivo. Sugiro renegociar para reajuste anual pelo IPCA.'
    }
    
    if (lowerQuestion.includes('garantia') || lowerQuestion.includes('fiador')) {
      return 'Seu contrato apresenta opções de garantia adequadas: fiador ou seguro-fiança. Isso está conforme a legislação e oferece flexibilidade. O seguro-fiança pode ser mais prático se você não tiver fiador disponível.'
    }
    
    if (lowerQuestion.includes('direito') || lowerQuestion.includes('lei')) {
      return 'Os principais direitos do locatário incluem: imóvel em condições de habitabilidade, reajuste anual (não semestral), multa rescisória limitada, e não responsabilidade por danos estruturais. Seu contrato apresenta algumas cláusulas que podem limitar esses direitos.'
    }
    
    return 'Baseado na análise do seu contrato de locação, posso ajudar com questões específicas sobre as cláusulas identificadas. Você tem alguma dúvida sobre os problemas encontrados ou quer saber mais sobre seus direitos como locatário?'
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header Responsivo */}
      <div className="bg-white border-b border-gray-200">
        <div className="px-4 md:px-8 py-4 md:py-6">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              onClick={() => router.push('/plataforma/historico')}
              className="h-10 w-10 p-0"
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            
            <div className="flex-1">
              <h1 className="text-xl md:text-2xl font-bold text-gray-900">
                Resultado da Análise
              </h1>
              <p className="text-sm md:text-base text-gray-600 mt-1">
                {analysis.fileName}
              </p>
            </div>
            
            <div className="flex gap-2">
              <Button variant="outline" size="sm" className="hidden md:flex">
                <Download className="h-4 w-4 mr-2" />
                Download
              </Button>
              <Button variant="outline" size="sm" className="hidden md:flex">
                <Share2 className="h-4 w-4 mr-2" /> 
                Compartilhar
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 md:px-8 py-6 md:py-8 max-w-4xl">
        
        {/* Visão Geral do Contrato */}
        <Card className="mb-8">
          <CardContent className="p-6 md:p-8">
            <div className="flex flex-col md:flex-row md:items-center gap-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-gray-100 rounded-xl flex items-center justify-center text-2xl">
                  {contractConfig.icon}
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">{analysis.fileName}</h2>
                  <div className="flex flex-wrap gap-2 mt-2">
                    <Badge className={contractConfig.color} variant="outline">
                      {contractConfig.label}
                    </Badge>
                    <Badge className={riskConfig.color} variant="outline">
                      <RiskIcon className="h-3 w-3 mr-1" />
                      {riskConfig.label}
                    </Badge>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:ml-auto">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">{analysis.overallScore}</div>
                  <div className="text-xs text-gray-500">Score Geral</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">{analysis.issuesFound}</div>
                  <div className="text-xs text-gray-500">Problemas</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{analysis.positivePoints}</div>
                  <div className="text-xs text-gray-500">Pontos +</div>
                </div>
                <div className="text-center">
                  <div className="text-sm font-medium text-gray-900">{formatDate(analysis.analysisDate)}</div>
                  <div className="text-xs text-gray-500">{analysis.fileSize}</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Problemas Encontrados */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-700">
              <AlertTriangle className="h-5 w-5" />
              Problemas Encontrados ({analysis.issuesFound})
            </CardTitle>
            <CardDescription>
              Cláusulas que podem ser prejudiciais ou necessitam atenção especial
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {analysis.problems.map((problem) => {
              const config = severityConfig[problem.severity]
              const Icon = config.icon
              const isExpanded = expandedProblems.has(problem.id)

              return (
                <div key={problem.id} className={`border-2 rounded-lg ${config.color}`}>
                  <div 
                    className="p-4 cursor-pointer"
                    onClick={() => toggleProblem(problem.id)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3 flex-1">
                        <Icon className="h-5 w-5 mt-0.5 flex-shrink-0" />
                        <div className="flex-1">
                          <h3 className="font-semibold text-lg mb-1">{problem.title}</h3>
                          <p className="text-sm opacity-90 mb-2">{problem.description}</p>
                          <Badge variant="outline" className="text-xs">
                            {problem.category}
                          </Badge>
                        </div>
                      </div>
                      {isExpanded ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
                    </div>
                  </div>
                  
                  {isExpanded && (
                    <div className="px-4 pb-4 border-t border-current/20">
                      <div className="mt-4 space-y-4">
                        <div>
                          <h4 className="font-medium text-sm mb-2">📋 Cláusula Específica:</h4>
                          <div className="bg-white/70 p-3 rounded text-sm italic">
                            "{problem.clause}"
                          </div>
                        </div>
                        <div>
                          <h4 className="font-medium text-sm mb-2">💡 Recomendação:</h4>
                          <p className="text-sm">{problem.recommendation}</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </CardContent>
        </Card>

        {/* Pontos Positivos */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-green-700">
              <CheckCircle className="h-5 w-5" />
              Pontos Positivos ({analysis.positivePoints})
            </CardTitle>
            <CardDescription>
              Aspectos favoráveis e bem estruturados do contrato
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {analysis.positives.map((positive) => (
              <div key={positive.id} className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg text-green-800 mb-1">{positive.title}</h3>
                    <p className="text-sm text-green-700 mb-3">{positive.description}</p>
                    <div className="bg-white/70 p-3 rounded text-sm italic text-green-800 mb-2">
                      "{positive.clause}"
                    </div>
                    <Badge variant="outline" className="text-xs text-green-700 border-green-300">
                      {positive.category}
                    </Badge>
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Chat com Assistente IA */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <MessageCircle className="h-5 w-5 text-blue-600" />
                <CardTitle className="text-blue-700">Assistente IA - Tire suas Dúvidas</CardTitle>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsChatExpanded(!isChatExpanded)}
                className="md:hidden"
              >
                {isChatExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </Button>
            </div>
            <CardDescription>
              Faça perguntas sobre seu contrato ou questões jurídicas gerais
            </CardDescription>
          </CardHeader>
          
          <CardContent className={`${isChatExpanded ? 'block' : 'hidden md:block'}`}>
            {/* Área de Mensagens */}
            <div className="h-80 overflow-y-auto bg-gray-50 rounded-lg p-4 mb-4 space-y-4">
              {chatMessages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${
                    message.type === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {message.type === 'assistant' && (
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <Bot className="h-4 w-4 text-white" />
                    </div>
                  )}
                  
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      message.type === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white border border-gray-200 text-gray-900'
                    }`}
                  >
                    <p className="text-sm leading-relaxed">{message.content}</p>
                    <div className="text-xs opacity-70 mt-2">
                      {message.timestamp.toLocaleTimeString('pt-BR', { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </div>
                  </div>
                  
                  {message.type === 'user' && (
                    <div className="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <User className="h-4 w-4 text-white" />
                    </div>
                  )}
                </div>
              ))}
              
              {/* Indicador de digitação */}
              {isTyping && (
                <div className="flex gap-3 justify-start">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="h-4 w-4 text-white" />
                  </div>
                  <div className="bg-white border border-gray-200 rounded-lg p-3">
                    <div className="flex items-center gap-2">
                      <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
                      <span className="text-sm text-gray-600">Assistente está digitando...</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={chatEndRef} />
            </div>
            
            {/* Input de Mensagem */}
            <div className="flex gap-2">
              <Input
                placeholder="Digite sua pergunta sobre o contrato..."
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                className="flex-1"
                disabled={isTyping}
              />
              <Button
                onClick={handleSendMessage}
                disabled={!chatInput.trim() || isTyping}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
            
            {/* Sugestões de Perguntas */}
            <div className="mt-4">
              <p className="text-sm text-gray-600 mb-2">💡 Sugestões de perguntas:</p>
              <div className="flex flex-wrap gap-2">
                {[
                  'Como negociar a multa rescisória?',
                  'O reajuste está correto?',
                  'Quais são meus direitos?',
                  'Posso contestar essas cláusulas?'
                ].map((suggestion, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    size="sm"
                    onClick={() => setChatInput(suggestion)}
                    className="text-xs"
                    disabled={isTyping}
                  >
                    {suggestion}
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Botões de Ação Mobile */}
        <div className="md:hidden flex gap-3 mb-6">
          <Button variant="outline" className="flex-1">
            <Download className="h-4 w-4 mr-2" />
            Download
          </Button>
          <Button variant="outline" className="flex-1">
            <Share2 className="h-4 w-4 mr-2" />
            Compartilhar
          </Button>
        </div>

        {/* CTA Nova Análise */}
        <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
          <CardContent className="p-6 text-center">
            <h3 className="text-xl font-bold mb-2">Precisa analisar outro contrato?</h3>
            <p className="mb-4 opacity-90">
              Continue protegendo seus direitos com nossas análises detalhadas
            </p>
            <Button 
              variant="secondary"
              className="bg-white text-blue-600 hover:bg-gray-100"
              onClick={() => router.push('/plataforma/analise')}
            >
              📄 Nova Análise
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}