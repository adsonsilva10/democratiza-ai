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

export default function DashboardPage() {
  const [insights, setInsights] = useState<InsightData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [userProfile, setUserProfile] = useState<any>(null)

  useEffect(() => {
    const loadDashboardData = async () => {
      // TODO: Buscar dados reais da API
      // Por enquanto, inicializar com estado vazio
      setTimeout(() => {
        setUserProfile({
          name: 'Usuário',
          planType: 'free',
          contractsAnalyzed: 0,
          signaturesCompleted: 0,
          hasAnalyzedContracts: false // Estado inicial sem contratos
        })

        setInsights({
          economiaTotal: 0,
          riscosEvitados: 0,
          contratosMaisArriscados: [],
          alertasAtivos: [],
          tendenciasMensais: [],
          recomendacoes: [],
          proximasAcoes: []
        })
        setIsLoading(false)
      }, 800)
    }

    loadDashboardData()
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
            <Link href="/dashboard/analise">
              <Button className="bg-white text-blue-600 px-6 py-3 lg:px-8 lg:py-4 rounded-lg font-semibold hover:bg-gray-50 transition-colors text-base lg:text-lg">
                � Analisar Meu Primeiro Contrato
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
        {/* Header personalizado */}
        <div className="mb-6 sm:mb-8">
          <div className="flex items-start sm:items-center gap-3 mb-2">
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center flex-shrink-0">
              <span className="text-lg sm:text-xl">🧠</span>
            </div>
            <div className="min-w-0 flex-1">
              <h1 className="text-lg sm:text-xl lg:text-2xl font-bold text-gray-900 leading-tight">
                Bom dia, {userProfile?.name}! 👋
              </h1>
              <p className="text-sm sm:text-base text-gray-600 mt-0.5">
                Seus insights jurídicos personalizados
              </p>
            </div>
          </div>
        </div>

        {/* Métricas Principais */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {/* Economia Total */}
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-4 sm:p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2 gap-1 sm:gap-2">
                <span className="text-xs sm:text-sm font-medium text-gray-600">💰 Economia Gerada</span>
                <Badge className="bg-green-100 text-green-800 text-xs self-start sm:self-center">+15%</Badge>
              </div>
              <div className="text-xl sm:text-2xl font-bold text-gray-900 mb-1">
                R$ {insights?.economiaTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
              </div>
              <p className="text-xs text-gray-500">Total economizado este ano</p>
            </CardContent>
          </Card>

          {/* Riscos Evitados */}
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-4 sm:p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2 gap-1 sm:gap-2">
                <span className="text-xs sm:text-sm font-medium text-gray-600">🛡️ Riscos Evitados</span>
                <Badge className="bg-blue-100 text-blue-800 text-xs self-start sm:self-center">Este mês</Badge>
              </div>
              <div className="text-xl sm:text-2xl font-bold text-gray-900 mb-1">
                {insights?.riscosEvitados}
              </div>
              <p className="text-xs text-gray-500">Cláusulas abusivas detectadas</p>
            </CardContent>
          </Card>

          {/* Análises Realizadas */}
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-4 sm:p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2 gap-1 sm:gap-2">
                <span className="text-xs sm:text-sm font-medium text-gray-600">🔍 Análises</span>
                <Badge className="bg-purple-100 text-purple-800 text-xs self-start sm:self-center">Este mês</Badge>
              </div>
              <div className="text-xl sm:text-2xl font-bold text-gray-900 mb-1">
                {userProfile?.contractsAnalyzed}
              </div>
              <p className="text-xs text-gray-500">Contratos analisados</p>
            </CardContent>
          </Card>

          {/* Assinaturas */}
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-4 sm:p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2 gap-1 sm:gap-2">
                <span className="text-xs sm:text-sm font-medium text-gray-600">✍️ Assinaturas</span>
                <Badge className="bg-emerald-100 text-emerald-800 text-xs self-start sm:self-center">Concluídas</Badge>
              </div>
              <div className="text-xl sm:text-2xl font-bold text-gray-900 mb-1">
                {userProfile?.signaturesCompleted}
              </div>
              <p className="text-xs text-gray-500">Documentos assinados</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
          {/* Coluna Principal - Alertas e Recomendações */}
          <div className="lg:col-span-2 space-y-4 sm:space-y-6">
            {/* Alertas Ativos */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  🚨 Alertas Ativos
                  <Badge variant="outline">{insights?.alertasAtivos.length}</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {insights?.alertasAtivos.map((alerta) => (
                    <div key={alerta.id} className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors">
                      {/* Header do alerta - mobile friendly */}
                      <div className="flex items-start gap-3 mb-3">
                        <span className="text-xl flex-shrink-0 mt-0.5">{getAlertIcon(alerta.tipo)}</span>
                        <div className="flex-1 min-w-0">
                          <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                            <h4 className="font-medium text-gray-900 text-sm sm:text-base">{alerta.titulo}</h4>
                            <Badge className={`${getSeverityColor(alerta.severidade)} text-xs flex-shrink-0`}>
                              {alerta.severidade}
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-600 leading-relaxed mb-2">{alerta.descricao}</p>
                          {alerta.dataLimite && (
                            <p className="text-xs text-orange-600 font-medium">
                              ⏰ Prazo: {new Date(alerta.dataLimite).toLocaleDateString('pt-BR')}
                            </p>
                          )}
                        </div>
                      </div>
                      
                      {/* Botão de ação - largura total em mobile */}
                      <div className="flex justify-end pt-2 border-t border-gray-100">
                        <Button size="sm" variant="outline" className="w-full sm:w-auto">
                          Ver Detalhes
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recomendações de IA */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  🎯 Recomendações Personalizadas
                  <Badge className="bg-gradient-to-r from-blue-100 to-purple-100 text-gray-800">IA</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {insights?.recomendacoes.map((rec) => (
                    <div key={rec.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                      {/* Conteúdo da recomendação */}
                      <div className="mb-4">
                        <h4 className="font-medium text-gray-900 mb-3 text-sm sm:text-base leading-relaxed">{rec.titulo}</h4>
                        
                        {/* Métricas - stack em mobile */}
                        <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4">
                          <span className="text-sm text-green-600 font-semibold">
                            💰 Economia: R$ {rec.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                          </span>
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-gray-500">Confiança:</span>
                            <Progress value={rec.confianca} className="w-16 h-2" />
                            <span className="text-xs text-gray-600">{rec.confianca}%</span>
                          </div>
                        </div>
                      </div>
                      
                      {/* Botão de ação - largura total em mobile */}
                      <div className="flex justify-end pt-3 border-t border-gray-100">
                        <Button 
                          size="sm" 
                          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 w-full sm:w-auto"
                        >
                          Aplicar Recomendação
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar - Ações Rápidas e Navegação */}
          <div className="space-y-4 sm:space-y-6">
            {/* Ações Rápidas */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base sm:text-lg">⚡ Ações Rápidas</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 sm:space-y-3">
                  <Link href="/dashboard/analise">
                    <Button className="w-full justify-start gap-2 sm:gap-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-sm sm:text-base py-2 sm:py-3">
                      <span>🔍</span>
                      <span>Nova Análise</span>
                    </Button>
                  </Link>
                  
                  <Link href="/dashboard/assinatura">
                    <Button variant="outline" className="w-full justify-start gap-2 sm:gap-3 text-sm sm:text-base py-2 sm:py-3">
                      <span>✍️</span>
                      <span>Assinar Documento</span>
                    </Button>
                  </Link>
                  
                  <Link href="/dashboard/historico">
                    <Button variant="outline" className="w-full justify-start gap-2 sm:gap-3 text-sm sm:text-base py-2 sm:py-3">
                      <span>📜</span>
                      <span>Ver Histórico</span>
                    </Button>
                  </Link>
                  
                  <Link href="/dashboard/chat">
                    <Button variant="outline" className="w-full justify-start gap-2 sm:gap-3 text-sm sm:text-base py-2 sm:py-3">
                      <span>💬</span>
                      <span>Chat Jurídico</span>
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>

            {/* Setores Mais Arriscados */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base sm:text-lg">📊 Setores de Alto Risco</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {insights?.contratosMaisArriscados.map((setor, index) => (
                    <div key={setor} className="flex items-center justify-between py-1">
                      <span className="text-xs sm:text-sm font-medium text-gray-700">{setor}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-red-500"></div>
                        <span className="text-xs text-gray-500">Alto</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Suporte */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base sm:text-lg">🆘 Precisa de Ajuda?</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 sm:space-y-3">
                  <Link href="/dashboard/suporte">
                    <Button variant="outline" className="w-full justify-start gap-2 sm:gap-3 text-sm sm:text-base py-2 sm:py-3">
                      <span>📚</span>
                      <span>Central de Ajuda</span>
                    </Button>
                  </Link>
                  
                  <Button variant="outline" className="w-full justify-start gap-2 sm:gap-3 text-sm sm:text-base py-2 sm:py-3" onClick={() => window.open('https://wa.me/5511999999999', '_blank')}>
                    <span>📱</span>
                    <span>Suporte WhatsApp</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Footer com call-to-action para upgrade */}
        {userProfile?.planType !== 'enterprise' && (
          <div className="mt-8">
            <Card className="bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
              <CardContent className="p-6">
                <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div>
                    <h3 className="font-bold text-gray-900 mb-1">🚀 Desbloqueie Insights Avançados</h3>
                    <p className="text-gray-600 text-sm">
                      Análises mais profundas, alertas em tempo real e relatórios personalizados
                    </p>
                  </div>
                  <Link href="/dashboard/planos">
                    <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 whitespace-nowrap">
                      Ver Planos Premium
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}