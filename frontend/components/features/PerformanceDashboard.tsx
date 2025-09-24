'use client'

import { usePerformance, usePageLoad, useApiPerformance } from '@/lib/hooks/usePerformance'
import { useState } from 'react'

interface MetricCardProps {
  title: string
  value: number | null
  unit: string
  rating?: 'good' | 'needs-improvement' | 'poor'
  description: string
}

function MetricCard({ title, value, unit, rating, description }: MetricCardProps) {
  const getRatingColor = (rating?: string) => {
    switch (rating) {
      case 'good': return 'text-green-600 bg-green-50 border-green-200'
      case 'needs-improvement': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'poor': return 'text-red-600 bg-red-50 border-red-200'
      default: return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getRatingIcon = (rating?: string) => {
    switch (rating) {
      case 'good': return '✅'
      case 'needs-improvement': return '⚠️'
      case 'poor': return '❌'
      default: return '📊'
    }
  }

  return (
    <div className={`rounded-lg border-2 p-4 ${getRatingColor(rating)}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium opacity-75">{title}</p>
          <p className="text-2xl font-bold">
            {value !== null ? `${value}${unit}` : '---'}
          </p>
          <p className="text-xs opacity-60 mt-1">{description}</p>
        </div>
        <div className="text-2xl">
          {getRatingIcon(rating)}
        </div>
      </div>
    </div>
  )
}

function PerformanceScore({ score }: { score: number }) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 50) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBackground = (score: number) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 50) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  return (
    <div className={`rounded-lg p-6 ${getScoreBackground(score)} border-2`}>
      <div className="text-center">
        <h3 className="text-lg font-semibold mb-2">Score de Performance</h3>
        <div className={`text-4xl font-bold ${getScoreColor(score)}`}>
          {score}/100
        </div>
        <p className="text-sm opacity-75 mt-2">
          {score >= 80 && 'Excelente performance! 🚀'}
          {score >= 50 && score < 80 && 'Performance boa, pode melhorar 📈'}
          {score < 50 && 'Performance precisa de atenção ⚠️'}
        </p>
      </div>
    </div>
  )
}

function MetricsSummary() {
  const { getMetricsSummary } = usePerformance()
  const [summary, setSummary] = useState(() => getMetricsSummary())

  const refreshSummary = () => {
    setSummary(getMetricsSummary())
  }

  return (
    <div className="bg-white rounded-lg border p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Resumo das Métricas</h3>
        <button 
          onClick={refreshSummary}
          className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Atualizar
        </button>
      </div>
      
      <div className="grid gap-4">
        <div className="text-sm">
          <span className="font-medium">Total de medições:</span> {summary.total}
        </div>
        
        {Object.entries(summary.byMetric).map(([metric, data]) => (
          <div key={metric} className="border rounded p-3">
            <div className="font-medium mb-2">{metric}</div>
            <div className="grid grid-cols-3 gap-2 text-sm">
              <div className="text-green-600">
                ✅ Bom: {data.good}
              </div>
              <div className="text-yellow-600">
                ⚠️ Regular: {data.needsImprovement}
              </div>
              <div className="text-red-600">
                ❌ Ruim: {data.poor}
              </div>
            </div>
            <div className="text-xs mt-2 text-gray-600">
              Média: {data.average}ms
            </div>
          </div>
        ))}

        {Object.keys(summary.byPage).length > 0 && (
          <div className="border-t pt-4">
            <h4 className="font-medium mb-2">Por Página:</h4>
            {Object.entries(summary.byPage).map(([page, count]) => (
              <div key={page} className="text-sm flex justify-between">
                <span>{page}</span>
                <span>{count} medições</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default function PerformanceDashboard() {
  const { metrics, performanceScore, isLoading } = usePerformance()
  const { pageLoadTime } = usePageLoad()
  const { getAverageApiTime, getApiErrorRate } = useApiPerformance()

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  const getRating = (metric: string, value: number | null): 'good' | 'needs-improvement' | 'poor' | undefined => {
    if (value === null) return undefined
    
    const thresholds: Record<string, { good: number; poor: number }> = {
      LCP: { good: 2500, poor: 4000 },
      FID: { good: 100, poor: 300 },
      CLS: { good: 0.1, poor: 0.25 },
      TTFB: { good: 800, poor: 1800 },
      FCP: { good: 1800, poor: 3000 }
    }

    const threshold = thresholds[metric]
    if (!threshold) return undefined

    if (value <= threshold.good) return 'good'
    if (value <= threshold.poor) return 'needs-improvement'
    return 'poor'
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">
          📊 Dashboard de Performance
        </h1>
        <p className="text-gray-600">
          Monitore as métricas de performance da aplicação em tempo real
        </p>
      </div>

      {/* Score Geral */}
      <div className="mb-6">
        <PerformanceScore score={performanceScore} />
      </div>

      {/* Core Web Vitals */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Core Web Vitals</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <MetricCard
            title="LCP"
            value={metrics.LCP}
            unit="ms"
            rating={getRating('LCP', metrics.LCP)}
            description="Largest Contentful Paint"
          />
          <MetricCard
            title="FID"
            value={metrics.FID}
            unit="ms"
            rating={getRating('FID', metrics.FID)}
            description="First Input Delay"
          />
          <MetricCard
            title="CLS"
            value={metrics.CLS ? Math.round(metrics.CLS * 1000) / 1000 : null}
            unit=""
            rating={getRating('CLS', metrics.CLS)}
            description="Cumulative Layout Shift"
          />
          <MetricCard
            title="TTFB"
            value={metrics.TTFB}
            unit="ms"
            rating={getRating('TTFB', metrics.TTFB)}
            description="Time to First Byte"
          />
          <MetricCard
            title="FCP"
            value={metrics.FCP}
            unit="ms"
            rating={getRating('FCP', metrics.FCP)}
            description="First Contentful Paint"
          />
          <MetricCard
            title="Page Load"
            value={pageLoadTime}
            unit="ms"
            description="Tempo total de carregamento"
          />
        </div>
      </div>

      {/* API Performance */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Performance da API</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <MetricCard
            title="Tempo Médio API"
            value={getAverageApiTime()}
            unit="ms"
            description="Tempo médio de resposta da API"
          />
          <MetricCard
            title="Taxa de Erro"
            value={getApiErrorRate()}
            unit="%"
            description="Porcentagem de requisições com erro"
          />
        </div>
      </div>

      {/* Resumo Detalhado */}
      <MetricsSummary />

      {/* Alertas */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 className="font-semibold text-blue-800 mb-2">💡 Dicas de Performance</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• LCP abaixo de 2.5s é considerado bom</li>
          <li>• FID abaixo de 100ms proporciona boa experiência</li>
          <li>• CLS abaixo de 0.1 evita mudanças de layout inesperadas</li>
          <li>• TTFB abaixo de 800ms indica boa performance do servidor</li>
        </ul>
      </div>
    </div>
  )
}