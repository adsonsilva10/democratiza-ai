'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  ArrowLeft, 
  FileText, 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  Download,
  Share2,
  Eye,
  Calendar,
  User
} from 'lucide-react'

// Tipos de dados para o resultado da análise
interface ContractAnalysisResult {
  id: string
  fileName: string
  contractType: 'rental' | 'telecom' | 'financial' | 'insurance'
  analysisDate: string
  riskLevel: 'alto' | 'medio' | 'baixo'
  status: 'completed' | 'processing' | 'error'
  issuesFound: number
  fileSize: string
  summary: {
    totalClauses: number
    problematicClauses: number
    score: number
  }
  issues: Array<{
    id: string
    type: 'abusive' | 'unclear' | 'financial' | 'legal'
    severity: 'alto' | 'medio' | 'baixo'
    title: string
    description: string
    clause: string
    recommendation: string
  }>
  positivePoints: Array<{
    id: string
    title: string
    description: string
  }>
}

// Mock data expandido
const mockAnalysisResult: ContractAnalysisResult = {
  id: '1',
  fileName: 'Contrato_Aluguel_Apartamento_Centro.pdf',
  contractType: 'rental',
  analysisDate: '2024-01-15T10:30:00Z',
  riskLevel: 'medio',
  status: 'completed',
  issuesFound: 7,
  fileSize: '2.1 MB',
  summary: {
    totalClauses: 24,
    problematicClauses: 7,
    score: 68
  },
  issues: [
    {
      id: '1',
      type: 'abusive',
      severity: 'alto',
      title: 'Cláusula de Reajuste Abusiva',
      description: 'O contrato permite reajustes semestrais acima do permitido por lei.',
      clause: 'Cláusula 8.2 - O valor do aluguel poderá ser reajustado a cada 6 meses...',
      recommendation: 'Negocie para que o reajuste seja anual e baseado em índices oficiais (IGPM/IPCA).'
    },
    {
      id: '2',
      type: 'financial',
      severity: 'medio',
      title: 'Multa Excessiva por Quebra de Contrato',
      description: 'A multa de 6 meses está acima do padrão de mercado.',
      clause: 'Cláusula 12.1 - Em caso de rescisão antecipada, será devida multa...',
      recommendation: 'Negocie para reduzir a multa para 2-3 meses de aluguel.'
    },
    {
      id: '3',
      type: 'unclear',
      severity: 'baixo',
      title: 'Responsabilidades de Manutenção Pouco Claras',
      description: 'Não está bem definido quem arca com pequenos reparos.',
      clause: 'Cláusula 15.3 - A manutenção do imóvel será responsabilidade...',
      recommendation: 'Solicite especificação clara sobre responsabilidades de manutenção.'
    }
  ],
  positivePoints: [
    {
      id: '1',
      title: 'Prazo de Aviso Prévio Adequado',
      description: 'O prazo de 30 dias para aviso prévio está de acordo com a lei.'
    },
    {
      id: '2',
      title: 'Garantia Locatícia Clara',
      description: 'As condições da garantia (fiança) estão bem especificadas.'
    }
  ]
}

const contractTypeLabels = {
  rental: { label: 'Locação', icon: '🏠', color: 'bg-blue-50 text-blue-700 border-blue-200' },
  telecom: { label: 'Telecom', icon: '📡', color: 'bg-green-50 text-green-700 border-green-200' },
  financial: { label: 'Financeiro', icon: '💳', color: 'bg-purple-50 text-purple-700 border-purple-200' },
  insurance: { label: 'Seguro', icon: '🛡️', color: 'bg-orange-50 text-orange-700 border-orange-200' }
}

const riskLevelConfig = {
  alto: { label: 'Alto Risco', color: 'bg-red-100 text-red-800', icon: AlertTriangle },
  medio: { label: 'Médio Risco', color: 'bg-yellow-100 text-yellow-800', icon: Clock },
  baixo: { label: 'Baixo Risco', color: 'bg-green-100 text-green-800', icon: CheckCircle }
}

const issueTypeConfig = {
  abusive: { label: 'Cláusula Abusiva', color: 'bg-red-50 text-red-700 border-red-200' },
  unclear: { label: 'Cláusula Pouco Clara', color: 'bg-yellow-50 text-yellow-700 border-yellow-200' },
  financial: { label: 'Questão Financeira', color: 'bg-purple-50 text-purple-700 border-purple-200' },
  legal: { label: 'Questão Legal', color: 'bg-blue-50 text-blue-700 border-blue-200' }
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

export default function ResultadoAnalise() {
  const [analysisData, setAnalysisData] = useState<ContractAnalysisResult | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()
  const searchParams = useSearchParams()
  const contractId = searchParams.get('id')

  useEffect(() => {
    // Simular carregamento de dados
    // Em produção, fazer chamada para API aqui
    setTimeout(() => {
      setAnalysisData(mockAnalysisResult)
      setLoading(false)
    }, 1000)
  }, [contractId])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
        <Card className="p-8">
          <div className="flex items-center gap-3">
            <Clock className="h-6 w-6 animate-spin text-blue-600" />
            <span className="text-lg">Carregando análise...</span>
          </div>
        </Card>
      </div>
    )
  }

  if (!analysisData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
        <Card className="p-8 text-center">
          <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Análise não encontrada</h2>
          <p className="text-gray-600 mb-4">O contrato solicitado não foi encontrado.</p>
          <Button onClick={() => router.push('/plataforma/historico')}>
            Voltar ao Histórico
          </Button>
        </Card>
      </div>
    )
  }

  const contractConfig = contractTypeLabels[analysisData.contractType]
  const riskConfig = riskLevelConfig[analysisData.riskLevel]
  const RiskIcon = riskConfig?.icon

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="px-4 py-4 md:px-8 md:py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => router.push('/plataforma/historico')}
                className="p-2 md:p-3"
              >
                <ArrowLeft className="h-4 w-4 md:h-5 md:w-5" />
              </Button>
              <div>
                <h1 className="text-xl md:text-2xl font-bold text-gray-900">Resultado da Análise</h1>
                <p className="text-sm md:text-base text-gray-600 mt-1">{analysisData.fileName}</p>
              </div>
            </div>
            
            <div className="flex gap-2">
              <Button variant="outline" size="sm" className="text-sm">
                <Download className="h-4 w-4 mr-2" />
                Download
              </Button>
              <Button variant="outline" size="sm" className="text-sm">
                <Share2 className="h-4 w-4 mr-2" />
                Compartilhar
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Conteúdo Principal */}
      <div className="px-4 py-6 md:px-8 md:py-8">
        <div className="max-w-6xl mx-auto space-y-6">
          
          {/* Resumo da Análise */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 md:gap-6">
            {/* Card Principal */}
            <Card className="md:col-span-2">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center text-xl">
                      {contractConfig.icon}
                    </div>
                    <div>
                      <CardTitle className="text-lg">Informações Gerais</CardTitle>
                      <div className="flex flex-wrap gap-2 mt-2">
                        <Badge className={contractConfig.color} variant="outline">
                          {contractConfig.label}
                        </Badge>
                        <Badge className={riskConfig.color} variant="outline">
                          {RiskIcon && <RiskIcon className="h-3 w-3 mr-1" />}
                          {riskConfig.label}
                        </Badge>
                      </div>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="text-gray-500 mb-1">Data da Análise</div>
                    <div className="font-semibold">{formatDate(analysisData.analysisDate)}</div>
                  </div>
                  <div>
                    <div className="text-gray-500 mb-1">Tamanho do Arquivo</div>
                    <div className="font-semibold">{analysisData.fileSize}</div>
                  </div>
                  <div>
                    <div className="text-gray-500 mb-1">Total de Cláusulas</div>
                    <div className="font-semibold">{analysisData.summary.totalClauses}</div>
                  </div>
                  <div>
                    <div className="text-gray-500 mb-1">Score de Segurança</div>
                    <div className="font-semibold">{analysisData.summary.score}/100</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Cards de Estatísticas */}
            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold text-red-600 mb-1">{analysisData.issuesFound}</div>
                <div className="text-sm text-gray-600">Problemas Encontrados</div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold text-green-600 mb-1">{analysisData.positivePoints.length}</div>
                <div className="text-sm text-gray-600">Pontos Positivos</div>
              </CardContent>
            </Card>
          </div>

          {/* Problemas Encontrados */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-red-600" />
                Problemas Encontrados ({analysisData.issues.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {analysisData.issues.map((issue) => {
                const issueTypeInfo = issueTypeConfig[issue.type]
                const severityConfig = riskLevelConfig[issue.severity]
                
                return (
                  <div key={issue.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
                    <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-3 mb-3">
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-900 mb-2">{issue.title}</h4>
                        <div className="flex flex-wrap gap-2 mb-3">
                          <Badge className={issueTypeInfo.color} variant="outline">
                            {issueTypeInfo.label}
                          </Badge>
                          <Badge className={severityConfig.color} variant="outline">
                            {severityConfig.label}
                          </Badge>
                        </div>
                      </div>
                    </div>
                    
                    <div className="space-y-3 text-sm">
                      <div>
                        <h5 className="font-medium text-gray-700 mb-1">Descrição:</h5>
                        <p className="text-gray-600">{issue.description}</p>
                      </div>
                      
                      <div>
                        <h5 className="font-medium text-gray-700 mb-1">Cláusula:</h5>
                        <div className="bg-gray-50 p-3 rounded border-l-4 border-gray-300">
                          <p className="text-gray-700 italic">{issue.clause}</p>
                        </div>
                      </div>
                      
                      <div>
                        <h5 className="font-medium text-green-700 mb-1">💡 Recomendação:</h5>
                        <p className="text-green-700 bg-green-50 p-3 rounded">{issue.recommendation}</p>
                      </div>
                    </div>
                  </div>
                )
              })}
            </CardContent>
          </Card>

          {/* Pontos Positivos */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                Pontos Positivos ({analysisData.positivePoints.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {analysisData.positivePoints.map((point) => (
                <div key={point.id} className="flex items-start gap-3 p-4 bg-green-50 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-green-800 mb-1">{point.title}</h4>
                    <p className="text-green-700 text-sm">{point.description}</p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Botão de Ação */}
          <div className="text-center pt-6">
            <Button 
              onClick={() => router.push('/plataforma/analise')}
              className="bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-3 text-lg"
            >
              <FileText className="h-5 w-5 mr-2" />
              Analisar Outro Contrato
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}