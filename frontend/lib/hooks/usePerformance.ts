'use client'

import { useState, useEffect } from 'react'
import { performanceMonitor, PerformanceAnalyzer, CoreWebVitals, getStoredMetrics } from '@/lib/performance'

export function usePerformance() {
  const [metrics, setMetrics] = useState<CoreWebVitals>({
    LCP: null,
    FID: null,
    CLS: null,
    TTFB: null,
    FCP: null
  })
  
  const [performanceScore, setPerformanceScore] = useState<number>(0)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!performanceMonitor) return

    // Coletar métricas iniciais
    const currentMetrics = performanceMonitor.getCurrentMetrics()
    setMetrics(currentMetrics)
    
    // Calcular score inicial
    const score = PerformanceAnalyzer.getPerformanceScore()
    setPerformanceScore(score)
    
    setIsLoading(false)

    // Atualizar métricas periodicamente
    const interval = setInterval(() => {
      if (performanceMonitor) {
        const updatedMetrics = performanceMonitor.collectCurrentMetrics()
        setMetrics(updatedMetrics)
      }
      
      const updatedScore = PerformanceAnalyzer.getPerformanceScore()
      setPerformanceScore(updatedScore)
    }, 5000) // A cada 5 segundos

    return () => clearInterval(interval)
  }, [])

  const getMetricsSummary = () => {
    return PerformanceAnalyzer.getMetricsSummary()
  }

  const getAllMetrics = () => {
    return getStoredMetrics()
  }

  return {
    metrics,
    performanceScore,
    isLoading,
    getMetricsSummary,
    getAllMetrics
  }
}

// Hook para monitoramento de tempo de carregamento de página
export function usePageLoad() {
  const [pageLoadTime, setPageLoadTime] = useState<number | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const measurePageLoad = () => {
      if (typeof window === 'undefined') return

      // Usar Performance API
      const navigationEntry = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming

      if (navigationEntry) {
        const loadTime = navigationEntry.loadEventEnd - navigationEntry.fetchStart
        setPageLoadTime(Math.round(loadTime))
      } else {
        // Fallback para browsers mais antigos
        window.addEventListener('load', () => {
          const loadTime = performance.now()
          setPageLoadTime(Math.round(loadTime))
        })
      }
      
      setIsLoading(false)
    }

    // Aguardar carregamento completo
    if (document.readyState === 'complete') {
      measurePageLoad()
    } else {
      window.addEventListener('load', measurePageLoad)
      return () => window.removeEventListener('load', measurePageLoad)
    }
  }, [])

  return { pageLoadTime, isLoading }
}

// Hook para monitoramento de API calls
export function useApiPerformance() {
  const [apiMetrics, setApiMetrics] = useState<Array<{
    url: string
    method: string
    duration: number
    status: number
    timestamp: number
  }>>([])

  useEffect(() => {
    // Carregar métricas do localStorage
    const loadStoredMetrics = () => {
      try {
        const stored = JSON.parse(localStorage.getItem('democratiza_ai_api_metrics') || '[]')
        setApiMetrics(stored)
      } catch (error) {
        console.warn('Erro ao carregar métricas de API:', error)
      }
    }

    loadStoredMetrics()

    // Atualizar a cada 10 segundos
    const interval = setInterval(loadStoredMetrics, 10000)
    return () => clearInterval(interval)
  }, [])

  const getAverageApiTime = () => {
    if (apiMetrics.length === 0) return 0
    const totalTime = apiMetrics.reduce((sum, metric) => sum + metric.duration, 0)
    return Math.round(totalTime / apiMetrics.length)
  }

  const getApiErrorRate = () => {
    if (apiMetrics.length === 0) return 0
    const errorCount = apiMetrics.filter(metric => metric.status >= 400).length
    return Math.round((errorCount / apiMetrics.length) * 100)
  }

  const getApiMetricsByEndpoint = () => {
    const byEndpoint: Record<string, {
      count: number
      averageTime: number
      errorRate: number
      fastest: number
      slowest: number
    }> = {}

    apiMetrics.forEach(metric => {
      if (!byEndpoint[metric.url]) {
        byEndpoint[metric.url] = {
          count: 0,
          averageTime: 0,
          errorRate: 0,
          fastest: Infinity,
          slowest: 0
        }
      }

      const endpoint = byEndpoint[metric.url]
      endpoint.count++
      endpoint.fastest = Math.min(endpoint.fastest, metric.duration)
      endpoint.slowest = Math.max(endpoint.slowest, metric.duration)
    })

    // Calcular médias e taxas de erro
    Object.keys(byEndpoint).forEach(url => {
      const metrics = apiMetrics.filter(m => m.url === url)
      const totalTime = metrics.reduce((sum, m) => sum + m.duration, 0)
      const errors = metrics.filter(m => m.status >= 400).length
      
      byEndpoint[url].averageTime = Math.round(totalTime / metrics.length)
      byEndpoint[url].errorRate = Math.round((errors / metrics.length) * 100)
    })

    return byEndpoint
  }

  return {
    apiMetrics,
    getAverageApiTime,
    getApiErrorRate,
    getApiMetricsByEndpoint
  }
}