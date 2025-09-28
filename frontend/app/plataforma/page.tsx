'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import Link from 'next/link'

// Interfaces para tipagem dos dados
interface InsightData {
  economiaTotal: number
  riscosEvitados: number
  contratosMaisArriscados: string[]
  alertasAtivos: Alert[]
  tendenciasMensais: TrendData[]
  recomendacoes: Recommendation[]
  proximasAcoes: Action[]
}

interface Alert {
  id: string
  tipo: 'prazo' | 'risco' | 'oportunidade'
  titulo: string
  descricao: string
  severidade: 'baixa' | 'média' | 'alta' | 'crítica'
  dataLimite?: string
  acao?: string
}

interface Recommendation {
  id: string
  categoria: 'economia' | 'juridico' | 'negociacao'
  titulo: string
  valor: number
  confianca: number
}

interface TrendData {
  mes: string
  contratos: number
  economia: number
  riscos: number
}

interface Action {
  id: string
  titulo: string
  descricao: string
  urgencia: 'baixa' | 'média' | 'alta'
  prazo: string
}

export default function PlataformaPage() {
  const [insights, setInsights] = useState<InsightData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [userProfile, setUserProfile] = useState<any>(null)
  const [showFloatingButton, setShowFloatingButton] = useState(false)

  useEffect(() => {
    const loadDashboardData = async () => {
      // Simular carregamento de dados da API
      setTimeout(() => {
        setUserProfile({
          name: 'Adson Silva',
          planType: 'professional',
          contractsAnalyzed: 23,
          signaturesCompleted: 12,
          hasAnalyzedContracts: true // Mude para false para testar estado inicial
        })

        setInsights({
          economiaTotal: 8547.30,
          riscosEvitados: 12,
          contratosMaisArriscados: ['Telecomunicações', 'Financeiro', 'Locação'],
          alertasAtivos: [
            {
              id: '1',
              tipo: 'prazo',
              titulo: 'Contrato de Internet Vencendo',
              descricao: 'Seu contrato com a Vivo vence em 15 dias. Hora de renegociar!',
              severidade: 'alta',
              dataLimite: '2025-10-15',
              acao: 'Analisar opções de renovação'
            },
            {
              id: '2',
              tipo: 'oportunidade',
              titulo: 'Economia Potencial Identificada',
              descricao: 'Detectamos cláusulas em 3 contratos que podem gerar R$ 1.200 de economia',
              severidade: 'média'
            },
            {
              id: '3',
              tipo: 'risco',
              titulo: 'Cláusula Abusiva Detectada',
              descricao: 'Contrato de cartão de crédito possui taxa de juros acima do permitido',
              severidade: 'crítica'
            }
          ],
          tendenciasMensais: [
            { mes: 'Jul', contratos: 8, economia: 2100, riscos: 3 },
            { mes: 'Ago', contratos: 12, economia: 3200, riscos: 5 },
            { mes: 'Set', contratos: 15, economia: 4500, riscos: 7 }
          ],
          recomendacoes: [
            {
              id: '1',
              categoria: 'economia',
              titulo: 'Renegociar taxa do cartão de crédito',
              valor: 450.00,
              confianca: 85
            },
            {
              id: '2',
              categoria: 'juridico',
              titulo: 'Revisar cláusula de reajuste do aluguel',
              valor: 280.00,
              confianca: 92
            },
            {
              id: '3',
              categoria: 'negociacao',
              titulo: 'Solicitar desconto no plano de internet',
              valor: 120.00,
              confianca: 78
            }
          ],
          proximasAcoes: [
            {
              id: '1',
              titulo: 'Revisar contrato do cartão',
              descricao: 'Análise urgente necessária devido a cláusulas abusivas',
              urgencia: 'alta',
              prazo: '3 dias'
            }
          ]
        })
        setIsLoading(false)
      }, 1500)
    }

    loadDashboardData()
  }, [])

  // Controle do Floating Action Button
  useEffect(() => {
    const handleScroll = () => {
      // Mostra FAB quando usuário faz scroll para baixo (após os cards principais)
      setShowFloatingButton(window.scrollY > 400)
    }
    
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Funções auxiliares para UI
  const getSeverityColor = (severidade: string) => {
    const colors = {
      'baixa': 'bg-blue-100 text-blue-800',
      'média': 'bg-yellow-100 text-yellow-800', 
      'alta': 'bg-orange-100 text-orange-800',
      'crítica': 'bg-red-100 text-red-800'
    }
    return colors[severidade as keyof typeof colors] || colors.baixa
  }

  const getAlertIcon = (tipo: string) => {
    const icons = {
      'prazo': '⏰',
      'risco': '⚠️',
      'oportunidade': '💰'
    }
    return icons[tipo as keyof typeof icons] || '📋'
  }

  const getCategoryColor = (categoria: string) => {
    const colors = {
      'economia': 'text-green-600',
      'juridico': 'text-blue-600',
      'negociacao': 'text-purple-600'
    }
    return colors[categoria as keyof typeof colors] || 'text-gray-600'
  }

  // Loading State
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 p-4 sm:p-6">
        <div className="max-w-6xl mx-auto">
          {/* Loading skeleton */}
          <div className="mb-6">
            <div className="h-8 bg-gray-200 rounded w-80 mb-2 animate-pulse"></div>
            <div className="h-6 bg-gray-200 rounded w-96 animate-pulse"></div>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {Array.from({ length: 4 }).map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardContent className="p-6">
                  <div className="h-4 bg-gray-200 rounded w-20 mb-2"></div>
                  <div className="h-8 bg-gray-200 rounded w-16 mb-1"></div>
                  <div className="h-3 bg-gray-200 rounded w-24"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // Estado inicial - usuário novo (experiência simplificada)
  if (!userProfile?.hasAnalyzedContracts) {
    return (
      <div className="p-4 lg:p-6">
        <h1 className="text-xl lg:text-2xl font-bold text-gray-900 mb-4 lg:mb-6">Dashboard</h1>
        
        {/* Call-to-Action Principal */}
        <div className="mb-6 lg:mb-8">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 lg:p-8 text-white text-center">
            <h2 className="text-xl lg:text-2xl font-bold mb-3">Bem-vindo ao Democratiza AI!</h2>
            <p className="text-blue-100 mb-4 lg:mb-6 text-base lg:text-lg">Comece analisando seu primeiro contrato e descubra os riscos ocultos</p>
            <Link href="/plataforma/analise">
              <Button className="bg-white text-blue-600 px-6 py-3 lg:px-8 lg:py-4 rounded-lg font-semibold hover:bg-gray-50 transition-colors text-base lg:text-lg">
                🔍 Analisar Meu Primeiro Contrato
              </Button>
            </Link>
          </div>
        </div>

        {/* Seção de contratos (vazia) */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b">
            <h2 className="text-lg font-medium text-gray-900">Seus Contratos Aparecerão Aqui</h2>
          </div>
          <div className="p-6">
            <div className="text-center py-6 lg:py-8">
              <div className="text-gray-400 mb-4">
                <div className="text-5xl lg:text-6xl mb-2">�</div>
              </div>
              <p className="text-gray-500 mb-2 text-sm lg:text-base">Nenhum contrato analisado ainda</p>
              <p className="text-xs lg:text-sm text-gray-400 px-4">Seus contratos analisados aparecerão aqui com seus respectivos níveis de risco</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Dashboard principal com insights
  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">
            Visão Geral da Plataforma
          </h1>
          <p className="text-gray-600">
            Acompanhe suas análises e mantenha seus contratos seguros
          </p>
        </div>

        {/* Métricas Principais - Dois blocos em destaque */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Análises Realizadas */}
          <Card className="border-2 border-blue-200 bg-gradient-to-r from-blue-50 to-blue-100">
            <CardContent className="p-6">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl">
                    📊
                  </div>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Análises Realizadas</h3>
                <p className="text-sm text-gray-600 mb-4">Total de contratos verificados</p>
                <div className="text-4xl font-bold text-blue-600">
                  {userProfile?.contractsAnalyzed}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Riscos Evitados */}
          <Card className="border-2 border-red-200 bg-gradient-to-r from-red-50 to-red-100">
            <CardContent className="p-6">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center text-white text-2xl">
                    ⚠️
                  </div>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Riscos Evitados</h3>
                <p className="text-sm text-gray-600 mb-4">Problemas identificados e prevenidos</p>
                <div className="text-4xl font-bold text-red-600">
                  {insights?.riscosEvitados}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Hero CTA - Nova Análise */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200 rounded-xl p-6 text-center mb-8">
          <h3 className="text-xl font-bold text-gray-800 mb-2">
            Pronto para uma nova análise?
          </h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            Faça upload do seu contrato e receba insights detalhados em minutos
          </p>
          <Link href="/plataforma/analise">
            <Button size="lg" className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-4 px-8 text-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200">
              <span className="mr-2">�</span>
              Fazer Nova Análise
            </Button>
          </Link>
        </div>

        {/* Histórico dos Últimos Contratos */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              � Últimos Contratos Analisados
              <Badge variant="outline">{userProfile?.contractsAnalyzed}</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Lista de contratos simulados */}
              {[
                {
                  id: '1',
                  nome: 'Contrato de Internet Vivo Fibra',
                  tipo: 'Telecomunicações',
                  data: '2025-09-25',
                  risco: 'Alto',
                  riscoColor: 'bg-red-100 text-red-800',
                  economia: 'R$ 120,00/mês'
                },
                {
                  id: '2', 
                  nome: 'Cartão de Crédito Nubank',
                  tipo: 'Financeiro',
                  data: '2025-09-22',
                  risco: 'Médio',
                  riscoColor: 'bg-yellow-100 text-yellow-800',
                  economia: 'R$ 89,50/ano'
                },
                {
                  id: '3',
                  nome: 'Contrato de Aluguel Apartamento',
                  tipo: 'Locação',
                  data: '2025-09-18',
                  risco: 'Baixo',
                  riscoColor: 'bg-green-100 text-green-800',
                  economia: 'R$ 200,00 única'
                },
                {
                  id: '4',
                  nome: 'Plano de Saúde SulAmérica',
                  tipo: 'Saúde',
                  data: '2025-09-15',
                  risco: 'Médio',
                  riscoColor: 'bg-yellow-100 text-yellow-800',
                  economia: 'R$ 156,00/mês'
                },
                {
                  id: '5',
                  nome: 'Financiamento Veicular Banco do Brasil',
                  tipo: 'Financeiro',
                  data: '2025-09-10',
                  risco: 'Alto',
                  riscoColor: 'bg-red-100 text-red-800',
                  economia: 'R$ 2.300,00 total'
                }
              ].map((contrato) => (
                <div key={contrato.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    {/* Informações principais */}
                    <div className="flex-1">
                      <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                        <h4 className="font-medium text-gray-900">{contrato.nome}</h4>
                        <Badge variant="outline" className="text-xs w-fit">{contrato.tipo}</Badge>
                      </div>
                      <p className="text-sm text-gray-600">
                        Analisado em {new Date(contrato.data).toLocaleDateString('pt-BR')}
                      </p>
                    </div>
                    
                    {/* Métricas e ação */}
                    <div className="flex flex-col sm:flex-row sm:items-center gap-3">
                      <div className="flex items-center gap-3">
                        <Badge className={`${contrato.riscoColor} text-xs`}>
                          {contrato.risco} Risco
                        </Badge>
                        <span className="text-sm font-semibold text-green-600">
                          💰 {contrato.economia}
                        </span>
                      </div>
                      <Button size="sm" variant="outline" className="w-full sm:w-auto">
                        Ver Análise
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Footer do card com link para ver todos */}
            <div className="flex justify-center pt-4 border-t border-gray-100">
              <Link href="/plataforma/historico">
                <Button variant="outline" className="w-full sm:w-auto">
                  Ver Todos os Contratos →
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Floating Action Button - Aparece durante scroll */}
        {showFloatingButton && (
          <div className="fixed bottom-6 right-6 z-50 md:bottom-8 md:right-8">
            <Link href="/plataforma/analise">
              <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white w-14 h-14 md:w-auto md:h-auto md:px-6 md:py-3 rounded-full md:rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center group animate-pulse">
                <span className="text-xl md:hidden">📄</span>
                <span className="hidden md:flex items-center gap-2 font-semibold">
                  📄 Nova Análise
                </span>
              </Button>
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}