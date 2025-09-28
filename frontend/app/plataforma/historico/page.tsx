'use client'

import { useState, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { 
  Search, 
  FileText, 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  Eye,
  Download,
  ChevronDown,
  ChevronRight
} from 'lucide-react'

// Tipos de dados
interface ContractAnalysis {
  id: string
  fileName: string
  contractType: 'rental' | 'telecom' | 'financial' | 'insurance'
  analysisDate: string
  riskLevel: 'alto' | 'medio' | 'baixo'
  status: 'completed' | 'processing' | 'error'
  issuesFound: number
  fileSize: string
}

// Dados mock
const mockContracts: ContractAnalysis[] = [
  {
    id: '1',
    fileName: 'Contrato de Locação - Apto 101',
    contractType: 'rental',
    analysisDate: '2025-09-20T14:30:00Z',
    riskLevel: 'alto',
    status: 'completed',
    issuesFound: 7,
    fileSize: '2.4 MB'
  },
  {
    id: '2', 
    fileName: 'Contrato de Internet - Fibra 200MB',
    contractType: 'telecom',
    analysisDate: '2025-09-18T09:15:00Z',
    riskLevel: 'medio',
    status: 'completed',
    issuesFound: 3,
    fileSize: '1.8 MB'
  },
  {
    id: '3',
    fileName: 'Contrato de Financiamento Veicular',
    contractType: 'financial', 
    analysisDate: '2025-09-15T16:45:00Z',
    riskLevel: 'baixo',
    status: 'completed',
    issuesFound: 1,
    fileSize: '3.1 MB'
  },
  {
    id: '4',
    fileName: 'Contrato de Cartão de Crédito Premium',
    contractType: 'financial',
    analysisDate: '2025-09-12T11:20:00Z', 
    riskLevel: 'alto',
    status: 'completed',
    issuesFound: 12,
    fileSize: '1.2 MB'
  },
  {
    id: '5',
    fileName: 'Seguro Auto Porto Seguro',
    contractType: 'insurance',
    analysisDate: '2025-09-10T13:30:00Z',
    riskLevel: 'baixo',
    status: 'completed',
    issuesFound: 2,
    fileSize: '4.2 MB'
  },
  {
    id: '6',
    fileName: 'Contrato Plano de Saúde Familiar',
    contractType: 'insurance',
    analysisDate: '2025-09-05T10:15:00Z',
    riskLevel: 'baixo',
    status: 'processing',
    issuesFound: 0,
    fileSize: '2.8 MB'
  }
]

const contractTypeLabels = {
  rental: { label: 'Locação', icon: '🏠', color: 'bg-blue-50 text-blue-700 border-blue-200' },
  telecom: { label: 'Telecom', icon: '📱', color: 'bg-green-50 text-green-700 border-green-200' },
  financial: { label: 'Financeiro', icon: '💳', color: 'bg-purple-50 text-purple-700 border-purple-200' },
  insurance: { label: 'Seguro', icon: '🛡️', color: 'bg-orange-50 text-orange-700 border-orange-200' }
}

const riskLevelConfig = {
  alto: { label: 'Alto Risco', color: 'bg-red-100 text-red-800', icon: AlertTriangle },
  medio: { label: 'Médio Risco', color: 'bg-yellow-100 text-yellow-800', icon: Clock },
  baixo: { label: 'Baixo Risco', color: 'bg-green-100 text-green-800', icon: CheckCircle }
}

export default function HistoricoPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState<string>('all')
  const [expandedCard, setExpandedCard] = useState<string | null>(null)
  const router = useRouter()

  // Filtros e busca
  const filteredContracts = useMemo(() => {
    let filtered = mockContracts

    // Busca por nome
    if (searchTerm) {
      filtered = filtered.filter(contract => 
        contract.fileName.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Filtro por tipo
    if (filterType !== 'all') {
      filtered = filtered.filter(contract => contract.contractType === filterType)
    }

    // Ordenação por data
    filtered.sort((a, b) => {
      return new Date(b.analysisDate).getTime() - new Date(a.analysisDate).getTime()
    })

    return filtered
  }, [searchTerm, filterType])

  // Estatísticas
  const stats = useMemo(() => {
    const completed = mockContracts.filter(c => c.status === 'completed')
    const totalIssues = completed.reduce((sum, c) => sum + c.issuesFound, 0)
    const highRisk = completed.filter(c => c.riskLevel === 'alto').length
    
    return {
      total: mockContracts.length,
      completed: completed.length,
      processing: mockContracts.filter(c => c.status === 'processing').length,
      totalIssues,
      highRisk
    }
  }, [])

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const viewAnalysis = (contractId: string) => {
    router.push(`/plataforma/analise/resultado?id=${contractId}`)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-4 md:px-6 py-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-xl md:text-3xl font-bold text-gray-900">
              Histórico de Análises
            </h1>
            <p className="text-sm md:text-base text-gray-600 mt-1">
              Acompanhe todas as suas análises de contratos
            </p>
          </div>
          
          <Button 
            onClick={() => router.push('/plataforma/analise')}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
          >
            📄 Nova Análise
          </Button>
        </div>
      </div>

      <div className="container mx-auto px-4 md:px-6 py-6 md:py-8">
        
        {/* Estatísticas Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
          <Card>
            <CardContent className="p-3 md:p-4 text-center">
              <div className="text-xl md:text-2xl font-bold text-blue-600">{stats.total}</div>
              <div className="text-xs text-gray-500">Total</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-3 md:p-4 text-center">
              <div className="text-xl md:text-2xl font-bold text-green-600">{stats.completed}</div>
              <div className="text-xs text-gray-500">Concluídas</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-3 md:p-4 text-center">
              <div className="text-xl md:text-2xl font-bold text-orange-600">{stats.processing}</div>
              <div className="text-xs text-gray-500">Processando</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-3 md:p-4 text-center">
              <div className="text-xl md:text-2xl font-bold text-red-600">{stats.totalIssues}</div>
              <div className="text-xs text-gray-500">Problemas</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-3 md:p-4 text-center">
              <div className="text-xl md:text-2xl font-bold text-red-600">{stats.highRisk}</div>
              <div className="text-xs text-gray-500">Alto Risco</div>
            </CardContent>
          </Card>


        </div>

        {/* Filtros e Busca */}
        <Card className="mb-6">
          <CardContent className="p-4">
            <div className="flex flex-col md:flex-row gap-4">
              {/* Busca */}
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="Buscar por nome do contrato..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              
              {/* Filtros Simples */}
              <div className="flex flex-wrap gap-2">
                <Button
                  variant={filterType === 'all' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setFilterType('all')}
                >
                  Todos
                </Button>
                <Button
                  variant={filterType === 'rental' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setFilterType('rental')}
                >
                  🏠 Locação
                </Button>
                <Button
                  variant={filterType === 'telecom' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setFilterType('telecom')}
                >
                  📱 Telecom
                </Button>
                <Button
                  variant={filterType === 'financial' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setFilterType('financial')}
                >
                  💳 Financeiro
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Lista de Contratos */}
        <div className="space-y-4">
          {filteredContracts.length === 0 ? (
            <Card>
              <CardContent className="p-12 text-center">
                <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Nenhum contrato encontrado
                </h3>
                <p className="text-gray-500 mb-4">
                  Ajuste os filtros ou faça uma nova análise
                </p>
                <Button 
                  onClick={() => router.push('/plataforma/analise')}
                  className="bg-gradient-to-r from-blue-600 to-purple-600"
                >
                  📄 Nova Análise
                </Button>
              </CardContent>
            </Card>
          ) : (
            filteredContracts.map((contract) => {
              const contractConfig = contractTypeLabels[contract.contractType]
              const riskConfig = riskLevelConfig[contract.riskLevel as keyof typeof riskLevelConfig]
              const RiskIcon = riskConfig?.icon
              const isExpanded = expandedCard === contract.id

              return (
                <Card key={contract.id} className="transition-all duration-200 hover:shadow-md">
                  <CardContent className="p-4">
                    {/* Desktop: Layout horizontal */}
                    <div className="hidden md:flex items-center justify-between">
                      <div className="flex items-center gap-4 flex-1">
                        {/* Ícone do tipo */}
                        <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center text-xl flex-shrink-0">
                          {contractConfig.icon}
                        </div>
                        
                        {/* Info principal */}
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold text-gray-900 truncate">{contract.fileName}</h3>
                          <div className="flex items-center gap-2 mt-1 flex-wrap">
                            <Badge className={contractConfig.color} variant="outline">
                              {contractConfig.label}
                            </Badge>
                            {contract.status === 'completed' && riskConfig && (
                              <Badge className={riskConfig.color} variant="outline">
                                {RiskIcon && <RiskIcon className="h-3 w-3 mr-1" />}
                                {riskConfig.label}
                              </Badge>
                            )}
                            {contract.status === 'processing' && (
                              <Badge className="bg-blue-100 text-blue-800" variant="outline">
                                <Clock className="h-3 w-3 mr-1" />
                                Processando
                              </Badge>
                            )}

                          </div>
                        </div>
                        
                        {/* Estatísticas */}
                        <div className="text-center px-4">
                          <div className="font-semibold text-lg">
                            {contract.status === 'completed' ? contract.issuesFound : '-'}
                          </div>
                          <div className="text-xs text-gray-500">Problemas</div>
                        </div>
                        
                        {/* Data */}
                        <div className="text-right px-4">
                          <div className="text-sm font-medium text-gray-900">
                            {formatDate(contract.analysisDate)}
                          </div>
                          <div className="text-xs text-gray-500">{contract.fileSize}</div>
                        </div>
                      </div>
                      
                      {/* Ações */}
                      <div className="flex items-center gap-2">
                        {contract.status === 'completed' && (
                          <Button
                            size="sm"
                            variant="outline" 
                            onClick={() => viewAnalysis(contract.id)}
                          >
                            <Eye className="h-4 w-4 mr-1" />
                            Ver Análise
                          </Button>
                        )}

                      </div>
                    </div>

                    {/* Mobile: Layout vertical */}
                    <div className="md:hidden">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-3 flex-1 min-w-0">
                          <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center text-lg flex-shrink-0">
                            {contractConfig.icon}
                          </div>
                          <div className="flex-1 min-w-0">
                            <h3 className="font-semibold text-gray-900 text-sm line-clamp-2 leading-tight">
                              {contract.fileName}
                            </h3>
                            <div className="text-xs text-gray-500 mt-1">
                              {formatDate(contract.analysisDate)} • {contract.fileSize}
                            </div>
                          </div>
                        </div>
                        
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setExpandedCard(isExpanded ? null : contract.id)}
                          className="p-1"
                        >
                          {isExpanded ? 
                            <ChevronDown className="h-4 w-4" /> : 
                            <ChevronRight className="h-4 w-4" />
                          }
                        </Button>
                      </div>
                      
                      {/* Badges */}
                      <div className="flex flex-wrap gap-2 mb-3">
                        <Badge className={contractConfig.color} variant="outline">
                          {contractConfig.label}
                        </Badge>
                        {contract.status === 'completed' && riskConfig && (
                          <Badge className={riskConfig.color} variant="outline">
                            {RiskIcon && <RiskIcon className="h-3 w-3 mr-1" />}
                            {riskConfig.label}
                          </Badge>
                        )}
                        {contract.status === 'processing' && (
                          <Badge className="bg-blue-100 text-blue-800" variant="outline">
                            <Clock className="h-3 w-3 mr-1" />
                            Processando
                          </Badge>
                        )}

                      </div>
                      
                      {/* Estatísticas rápidas */}
                      {!isExpanded && contract.status === 'completed' && (
                        <div className="text-sm text-gray-600">
                          <strong>{contract.issuesFound}</strong> problemas encontrados
                        </div>
                      )}
                      
                      {/* Conteúdo expandido */}
                      {isExpanded && (
                        <div className="mt-4 pt-4 border-t border-gray-100 space-y-3">
                          {contract.status === 'completed' && (
                            <div className="grid grid-cols-2 gap-4 text-sm">
                              <div>
                                <div className="text-gray-500">Problemas</div>
                                <div className="font-semibold">{contract.issuesFound}</div>
                              </div>
                              <div>
                                <div className="text-gray-500">Status</div>
                                <div className="font-semibold">Concluído</div>
                              </div>
                            </div>
                          )}
                          
                          <div className="flex gap-2">
                            {contract.status === 'completed' && (
                              <Button
                                size="sm"
                                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600"
                                onClick={() => viewAnalysis(contract.id)}
                              >
                                <Eye className="h-4 w-4 mr-1" />
                                Ver Análise
                              </Button>
                            )}
                            <Button
                              size="sm"
                              variant="outline"
                              className="flex-1"
                            >
                              <Download className="h-4 w-4 mr-1" />
                              Download
                            </Button>
                          </div>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )
            })
          )}
        </div>

        {/* Paginação - Placeholder para implementação futura */}
        {filteredContracts.length > 0 && (
          <div className="flex justify-center mt-8">
            <div className="text-sm text-gray-500">
              Mostrando {filteredContracts.length} de {mockContracts.length} contratos
            </div>
          </div>
        )}
      </div>
    </div>
  )
}