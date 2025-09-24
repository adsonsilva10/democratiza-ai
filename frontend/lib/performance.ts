/**
 * Sistema de Performance Monitoring - Frontend
 * Coleta métricas de Core Web Vitals sem APIs externas
 */

// Tipos para as métricas de performance
export interface PerformanceMetric {
  name: string
  value: number
  rating: 'good' | 'needs-improvement' | 'poor'
  timestamp: number
  url: string
  userAgent: string
}

export interface CoreWebVitals {
  LCP: number | null  // Largest Contentful Paint
  FID: number | null  // First Input Delay  
  CLS: number | null  // Cumulative Layout Shift
  TTFB: number | null // Time to First Byte
  FCP: number | null  // First Contentful Paint
}

// Thresholds para classificação das métricas
const THRESHOLDS = {
  LCP: { good: 2500, poor: 4000 },
  FID: { good: 100, poor: 300 },
  CLS: { good: 0.1, poor: 0.25 },
  TTFB: { good: 800, poor: 1800 },
  FCP: { good: 1800, poor: 3000 }
}

// Função para classificar performance
function getRating(metric: keyof typeof THRESHOLDS, value: number): 'good' | 'needs-improvement' | 'poor' {
  const threshold = THRESHOLDS[metric]
  if (value <= threshold.good) return 'good'
  if (value <= threshold.poor) return 'needs-improvement'
  return 'poor'
}

// Storage local das métricas
const STORAGE_KEY = 'democratiza_ai_performance_metrics'

function saveMetric(metric: PerformanceMetric) {
  try {
    const existingMetrics = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
    existingMetrics.push(metric)
    
    // Manter apenas últimas 100 métricas
    const recentMetrics = existingMetrics.slice(-100)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(recentMetrics))
  } catch (error) {
    console.error('Erro ao salvar métrica de performance:', error)
  }
}

export function getStoredMetrics(): PerformanceMetric[] {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  } catch (error) {
    console.error('Erro ao recuperar métricas:', error)
    return []
  }
}

// Core Web Vitals Collection
export class PerformanceMonitor {
  private metrics: CoreWebVitals = {
    LCP: null,
    FID: null,
    CLS: null,
    TTFB: null,
    FCP: null
  }

  constructor() {
    this.initializeMonitoring()
  }

  private initializeMonitoring() {
    if (typeof window === 'undefined') return

    // LCP - Largest Contentful Paint
    this.observeLCP()
    
    // FID - First Input Delay
    this.observeFID()
    
    // CLS - Cumulative Layout Shift
    this.observeCLS()
    
    // TTFB - Time to First Byte
    this.measureTTFB()
    
    // FCP - First Contentful Paint
    this.observeFCP()
  }

  private observeLCP() {
    if ('PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries()
          const lastEntry = entries[entries.length - 1] as any
          
          if (lastEntry) {
            this.metrics.LCP = Math.round(lastEntry.startTime)
            this.saveMetric('LCP', this.metrics.LCP)
          }
        })
        
        observer.observe({ type: 'largest-contentful-paint', buffered: true })
      } catch (error) {
        console.warn('LCP monitoring não disponível:', error)
      }
    }
  }

  private observeFID() {
    if ('PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries()
          entries.forEach((entry: any) => {
            if (entry.processingStart && entry.startTime) {
              this.metrics.FID = Math.round(entry.processingStart - entry.startTime)
              this.saveMetric('FID', this.metrics.FID)
            }
          })
        })
        
        observer.observe({ type: 'first-input', buffered: true })
      } catch (error) {
        console.warn('FID monitoring não disponível:', error)
      }
    }
  }

  private observeCLS() {
    if ('PerformanceObserver' in window) {
      try {
        let clsValue = 0
        
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries()
          entries.forEach((entry: any) => {
            if (!entry.hadRecentInput) {
              clsValue += entry.value
            }
          })
          
          this.metrics.CLS = Math.round(clsValue * 1000) / 1000
          this.saveMetric('CLS', this.metrics.CLS)
        })
        
        observer.observe({ type: 'layout-shift', buffered: true })
      } catch (error) {
        console.warn('CLS monitoring não disponível:', error)
      }
    }
  }

  private measureTTFB() {
    if ('performance' in window && performance.timing) {
      // Usar Navigation Timing API
      window.addEventListener('load', () => {
        const navTiming = performance.timing
        const ttfb = navTiming.responseStart - navTiming.requestStart
        
        if (ttfb > 0) {
          this.metrics.TTFB = ttfb
          this.saveMetric('TTFB', ttfb)
        }
      })
    }
  }

  private observeFCP() {
    if ('PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries()
          entries.forEach((entry: any) => {
            if (entry.name === 'first-contentful-paint') {
              this.metrics.FCP = Math.round(entry.startTime)
              this.saveMetric('FCP', this.metrics.FCP)
            }
          })
        })
        
        observer.observe({ type: 'paint', buffered: true })
      } catch (error) {
        console.warn('FCP monitoring não disponível:', error)
      }
    }
  }

  private saveMetric(name: string, value: number) {
    const metric: PerformanceMetric = {
      name,
      value,
      rating: getRating(name as keyof typeof THRESHOLDS, value),
      timestamp: Date.now(),
      url: window.location.pathname,
      userAgent: navigator.userAgent.substring(0, 100) // Truncar para não ocupar muito espaço
    }

    saveMetric(metric)

    // Log para desenvolvimento
    if (process.env.NODE_ENV === 'development') {
      console.log(`📊 Performance [${name}]:`, value, `(${metric.rating})`)
    }
  }

  // Método público para obter métricas atuais
  public getCurrentMetrics(): CoreWebVitals {
    return { ...this.metrics }
  }

  // Método para forçar coleta de métricas disponíveis
  public collectCurrentMetrics(): CoreWebVitals {
    // Navigation Timing para TTFB
    if (typeof window !== 'undefined' && performance.timing) {
      const navTiming = performance.timing
      if (navTiming.responseStart && navTiming.requestStart) {
        const ttfb = navTiming.responseStart - navTiming.requestStart
        if (ttfb > 0 && !this.metrics.TTFB) {
          this.metrics.TTFB = ttfb
          this.saveMetric('TTFB', ttfb)
        }
      }
    }

    return this.getCurrentMetrics()
  }
}

// API para análise das métricas
export class PerformanceAnalyzer {
  static getMetricsSummary() {
    const metrics = getStoredMetrics()
    const summary = {
      total: metrics.length,
      byMetric: {} as Record<string, { good: number; needsImprovement: number; poor: number; average: number }>,
      byPage: {} as Record<string, number>,
      recentTrend: [] as Array<{ date: string; average: number }>
    }

    // Agrupar por tipo de métrica
    metrics.forEach(metric => {
      if (!summary.byMetric[metric.name]) {
        summary.byMetric[metric.name] = { good: 0, needsImprovement: 0, poor: 0, average: 0 }
      }

      summary.byMetric[metric.name][metric.rating === 'needs-improvement' ? 'needsImprovement' : metric.rating]++
      
      // Contar por página
      summary.byPage[metric.url] = (summary.byPage[metric.url] || 0) + 1
    })

    // Calcular médias
    Object.keys(summary.byMetric).forEach(metricName => {
      const metricData = metrics.filter(m => m.name === metricName)
      const avg = metricData.reduce((sum, m) => sum + m.value, 0) / metricData.length
      summary.byMetric[metricName].average = Math.round(avg)
    })

    return summary
  }

  static getPerformanceScore(): number {
    const metrics = getStoredMetrics()
    if (metrics.length === 0) return 0

    const scores: number[] = metrics.map(metric => {
      switch (metric.rating) {
        case 'good': return 100
        case 'needs-improvement': return 50
        case 'poor': return 0
        default: return 0
      }
    })

    return Math.round(scores.reduce((sum: number, score: number) => sum + score, 0) / scores.length)
  }
}

// Instância global
export const performanceMonitor = typeof window !== 'undefined' ? new PerformanceMonitor() : null