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
  
  // Hook para detectar se é mobile
  const [isMobile, setIsMobile] = useState(false)
  
  useEffect(() => {
    // Detectar se é mobile baseado no tamanho da tela
    const checkIsMobile = () => {
      setIsMobile(window.innerWidth < 768) // md breakpoint
    }
    
    checkIsMobile()
    window.addEventListener('resize', checkIsMobile)
    
    return () => window.removeEventListener('resize', checkIsMobile)
  }, [])
  
  useEffect(() => {
    // Definir chat expandido por padrão no mobile
    if (isMobile) {
      setIsChatExpanded(true)
    }
  }, [isMobile])
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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 overflow-x-hidden">
      {/* Skip Link para acessibilidade */}
      <a 
        href="#main-content" 
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-600 text-white px-4 py-2 rounded z-50"
      >
        Pular para o conteúdo principal
      </a>
      
      {/* Header Responsivo */}
      <header className="bg-white border-b border-gray-200" role="banner">
        <div className="px-6 md:px-8 py-6 md:py-6">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              onClick={() => router.push('/plataforma/historico')}
              className="h-14 w-14 p-0"
              aria-label="Voltar para a página de histórico de contratos"
            >
              <ArrowLeft className="h-6 w-6" aria-hidden="true" />
            </Button>
            
            <div className="flex-1">
              <h1 className="text-2xl md:text-2xl font-bold text-gray-900">
                Resultado da Análise
              </h1>
              <p className="text-base md:text-base text-gray-600 mt-1">
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
      </header>

      <main id="main-content" className="container mx-auto px-6 md:px-8 py-6 md:py-8 max-w-4xl overflow-x-hidden">
        
        {/* Visão Geral do Contrato */}
        <Card className="mb-8">
          <CardContent className="p-6 md:p-8">
            <div className="flex flex-col md:flex-row gap-6">
              {/* Desktop: Ícone + Flag de risco lado a lado */}
              <div className="hidden md:flex items-center gap-4 flex-shrink-0">
                <div className="w-16 h-16 bg-gray-100 rounded-xl flex items-center justify-center text-2xl">
                  {contractConfig.icon}
                </div>
                <Badge className={`${riskConfig.color} text-sm px-4 py-2 text-base inline-flex items-center gap-2`} variant="outline">
                  <RiskIcon className="h-5 w-5 flex-shrink-0" />
                  <span>{riskConfig.label}</span>
                </Badge>
              </div>

              {/* Mobile: Layout original + Desktop: Apenas estatísticas */}
              <div className="flex-1">
                <div className="flex flex-col gap-4">
                  {/* Primeira linha: Score/Problemas/Pontos + + Data/Tamanho */}
                  <div className="flex flex-col md:flex-row md:items-center gap-4 md:gap-6">
                    {/* Mobile: Ícone + Nome + Badges */}
                    <div className="flex items-center gap-4 md:hidden">
                      <div className="w-16 h-16 bg-gray-100 rounded-xl flex items-center justify-center text-2xl flex-shrink-0">
                        {contractConfig.icon}
                      </div>
                      <div className="min-w-0 flex-1">
                        <h2 className="text-xl font-semibold text-gray-900 truncate">{analysis.fileName}</h2>
                        <div className="flex flex-wrap gap-3 mt-3">
                          <Badge className={`${contractConfig.color} text-sm px-3 py-1`} variant="outline">
                            {contractConfig.label}
                          </Badge>
                          <Badge className={`${riskConfig.color} text-sm px-3 py-1`} variant="outline">
                            <RiskIcon className="h-4 w-4 mr-1" />
                            {riskConfig.label}
                          </Badge>
                        </div>
                      </div>
                    </div>

                    {/* Estatísticas: Score, Problemas, Pontos + */}
                    <div className="flex gap-4">
                      <div className="text-center p-3 bg-gray-50 rounded-lg">
                        <div className="text-3xl font-bold text-gray-900">{analysis.overallScore}</div>
                        <div className="text-sm text-gray-500 mt-1">Score Geral</div>
                      </div>
                      <div className="text-center p-3 bg-red-50 rounded-lg">
                        <div className="text-3xl font-bold text-red-600">{analysis.issuesFound}</div>
                        <div className="text-sm text-gray-500 mt-1">Problemas</div>
                      </div>
                      <div className="text-center p-3 bg-green-50 rounded-lg">
                        <div className="text-3xl font-bold text-green-600">{analysis.positivePoints}</div>
                        <div className="text-sm text-gray-500 mt-1">Pontos +</div>
                      </div>
                    </div>

                    {/* Data e Tamanho */}
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-base font-medium text-gray-900">{formatDate(analysis.analysisDate)}</div>
                      <div className="text-sm text-gray-500 mt-1">{analysis.fileSize}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Problemas Encontrados */}
        <Card className="mb-8" role="region" aria-labelledby="problems-title">
          <CardHeader>
            <CardTitle id="problems-title" className="flex items-center gap-2 text-red-700">
              <AlertTriangle className="h-5 w-5" aria-hidden="true" />
              Problemas Encontrados 
              <span className="sr-only">({analysis.issuesFound} problemas identificados)</span>
              <span aria-hidden="true">({analysis.issuesFound})</span>
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
                <div 
                  key={problem.id} 
                  className={`border-2 rounded-lg ${config.color}`}
                  role="button"
                  tabIndex={0}
                  aria-expanded={isExpanded}
                  aria-controls={`problem-details-${problem.id}`}
                  aria-label={`${problem.title}. Severidade: ${problem.severity}. ${isExpanded ? 'Pressione para recolher' : 'Pressione para expandir'} detalhes`}
                >
                  <div 
                    className="p-5 md:p-4 cursor-pointer"
                    onClick={() => toggleProblem(problem.id)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault()
                        toggleProblem(problem.id)
                      }
                    }}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-start gap-3 md:gap-3 flex-1 min-w-0">
                        <Icon className="h-5 w-5 md:h-5 md:w-5 mt-1 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold text-lg md:text-lg mb-2 break-words">{problem.title}</h3>
                          <p className="text-base opacity-90 mb-3">{problem.description}</p>
                          <Badge variant="outline" className="text-sm px-2 py-1">
                            {problem.category}
                          </Badge>
                        </div>
                      </div>
                      {isExpanded ? <ChevronUp className="h-6 w-6" /> : <ChevronDown className="h-6 w-6" />}
                    </div>
                  </div>
                  
                  {isExpanded && (
                    <div 
                      id={`problem-details-${problem.id}`}
                      className="px-5 md:px-4 pb-5 md:pb-4 border-t border-current/20"
                      role="region"
                      aria-label="Detalhes do problema"
                    >
                      <div className="mt-5 space-y-5">
                        <div>
                          <h4 className="font-medium text-base mb-3">📋 Cláusula Específica:</h4>
                          <div className="bg-white/70 p-4 md:p-3 rounded text-sm md:text-sm italic break-words">
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
        <Card className="mb-8" role="region" aria-labelledby="positives-title">
          <CardHeader>
            <CardTitle id="positives-title" className="flex items-center gap-2 text-green-700">
              <CheckCircle className="h-5 w-5" aria-hidden="true" />
              Pontos Positivos
              <span className="sr-only">({analysis.positivePoints} aspectos favoráveis identificados)</span>
              <span aria-hidden="true">({analysis.positivePoints})</span>
            </CardTitle>
            <CardDescription>
              Aspectos favoráveis e bem estruturados do contrato
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {analysis.positives.map((positive) => (
              <div key={positive.id} className="bg-green-50 border-2 border-green-200 rounded-lg p-5 md:p-4">
                <div className="flex items-start gap-3 md:gap-3">
                  <CheckCircle className="h-5 w-5 md:h-5 md:w-5 text-green-600 mt-1 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-lg md:text-lg text-green-800 mb-2 break-words">{positive.title}</h3>
                    <p className="text-base text-green-700 mb-4">{positive.description}</p>
                    <div className="bg-white/70 p-4 md:p-3 rounded text-sm md:text-sm italic text-green-800 mb-3 break-words">
                      "{positive.clause}"
                    </div>
                    <Badge variant="outline" className="text-sm px-2 py-1 text-green-700 border-green-300">
                      {positive.category}
                    </Badge>
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Chat com Assistente IA */}
        <Card className="mb-8" role="region" aria-labelledby="chat-title">
          <CardHeader className="p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <MessageCircle className="h-6 w-6 text-blue-600" aria-hidden="true" />
                <CardTitle id="chat-title" className="text-blue-700 text-xl">Assistente IA - Tire suas Dúvidas</CardTitle>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsChatExpanded(!isChatExpanded)}
                className="md:hidden h-14 w-14"
                aria-label={isChatExpanded ? 'Recolher chat' : 'Expandir chat'}
                aria-expanded={isChatExpanded}
                aria-controls="chat-content"
              >
                {isChatExpanded ? <ChevronUp className="h-5 w-5" aria-hidden="true" /> : <ChevronDown className="h-5 w-5" aria-hidden="true" />}
              </Button>
            </div>
            <CardDescription className="text-base mt-2">
              Faça perguntas sobre seu contrato ou questões jurídicas gerais
            </CardDescription>
          </CardHeader>
          
          <CardContent id="chat-content" className={`${isChatExpanded ? 'block' : 'hidden md:block'} p-6`}>
            {/* Área de Mensagens */}
            <div 
              className="h-80 md:h-80 overflow-y-auto bg-gray-50 rounded-lg p-5 md:p-4 mb-6 space-y-4 md:space-y-4 max-w-full"
              role="log"
              aria-live="polite"
              aria-label="Histórico da conversa com o assistente de IA"
              tabIndex={0}
            >
              {chatMessages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${
                    message.type === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  {message.type === 'assistant' && (
                    <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <Bot className="h-5 w-5 text-white" />
                    </div>
                  )}
                  
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      message.type === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white border border-gray-200 text-gray-900'
                    }`}
                  >
                    <p className="text-base leading-relaxed">{message.content}</p>
                    <div className="text-sm opacity-70 mt-3">
                      {message.timestamp.toLocaleTimeString('pt-BR', { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </div>
                  </div>
                  
                  {message.type === 'user' && (
                    <div className="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <User className="h-5 w-5 text-white" />
                    </div>
                  )}
                </div>
              ))}
              
              {/* Indicador de digitação */}
              {isTyping && (
                <div className="flex gap-3 justify-start">
                  <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="h-5 w-5 text-white" />
                  </div>
                  <div className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center gap-3">
                      <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
                      <span className="text-base text-gray-600">Assistente está digitando...</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={chatEndRef} />
            </div>
            
            {/* Input de Mensagem */}
            <div className="flex gap-3">
              <label htmlFor="chat-input" className="sr-only">
                Digite sua pergunta sobre o contrato para o assistente de IA
              </label>
              <Input
                id="chat-input"
                placeholder="Digite sua pergunta sobre o contrato..."
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                className="flex-1 h-14 text-base px-4"
                disabled={isTyping}
                aria-describedby="chat-help"
              />
              <Button
                onClick={handleSendMessage}
                disabled={!chatInput.trim() || isTyping}
                className="bg-blue-600 hover:bg-blue-700 h-14 w-14"
                aria-label={isTyping ? 'Aguarde, mensagem sendo processada' : 'Enviar mensagem para o assistente'}
              >
                <Send className="h-5 w-5" aria-hidden="true" />
              </Button>
            </div>
            <div id="chat-help" className="sr-only">
              Faça perguntas sobre o contrato ou questões jurídicas. Pressione Enter para enviar.
            </div>
            
            {/* Sugestões de Perguntas */}
            <div className="mt-6">
              <p className="text-base text-gray-600 mb-3">
                <span aria-hidden="true">💡</span> Sugestões de perguntas:
              </p>
              <div className="flex flex-wrap gap-2 md:gap-2 max-w-full" role="group" aria-label="Perguntas de exemplo">
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
                    aria-label={`Pergunta de exemplo: ${suggestion}`}
                    className="min-h-[44px] text-xs"
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
        <div className="md:hidden flex gap-2 mb-6 max-w-full">
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
          <CardContent className="p-4 md:p-6 text-center">
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
      </main>
    </div>
  )
}