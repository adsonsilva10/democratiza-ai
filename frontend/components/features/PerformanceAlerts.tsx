'use client'

import { useState, useEffect } from 'react'
import { PerformanceAnalyzer } from '@/lib/performance'

interface AlertType {
  id: string
  type: 'warning' | 'error' | 'info'
  title: string
  message: string
  timestamp: number
  metric?: string
  value?: number
}

export default function PerformanceAlerts() {
  const [alerts, setAlerts] = useState<AlertType[]>([])
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const checkPerformance = () => {
      const newAlerts: AlertType[] = []
      const score = PerformanceAnalyzer.getPerformanceScore()
      
      // Alerta de performance baixa
      if (score < 50 && score > 0) {
        newAlerts.push({
          id: 'low-performance',
          type: 'error',
          title: 'Performance Crítica',
          message: `Score de performance está em ${score}/100. Considere otimizar a aplicação.`,
          timestamp: Date.now()
        })
      } else if (score < 80 && score >= 50) {
        newAlerts.push({
          id: 'medium-performance',
          type: 'warning',
          title: 'Performance Regular',
          message: `Score de performance está em ${score}/100. Há espaço para melhorias.`,
          timestamp: Date.now()
        })
      }

      // Verificar métricas de API
      if (typeof window !== 'undefined') {
        try {
          const apiMetrics = JSON.parse(localStorage.getItem('democratiza_ai_api_metrics') || '[]')
          const recentMetrics = apiMetrics.filter((m: any) => Date.now() - m.timestamp < 300000) // Últimos 5 minutos
          
          if (recentMetrics.length > 0) {
            const avgTime = recentMetrics.reduce((sum: number, m: any) => sum + m.duration, 0) / recentMetrics.length
            const errorRate = recentMetrics.filter((m: any) => m.status >= 400).length / recentMetrics.length * 100
            
            // Alerta de API lenta
            if (avgTime > 2000) {
              newAlerts.push({
                id: 'slow-api',
                type: 'warning',
                title: 'API Lenta',
                message: `Tempo médio de resposta da API está em ${Math.round(avgTime)}ms`,
                timestamp: Date.now(),
                metric: 'API Response Time',
                value: Math.round(avgTime)
              })
            }
            
            // Alerta de taxa de erro alta
            if (errorRate > 20) {
              newAlerts.push({
                id: 'high-error-rate',
                type: 'error',
                title: 'Alta Taxa de Erro',
                message: `${Math.round(errorRate)}% das requisições estão falhando`,
                timestamp: Date.now(),
                metric: 'API Error Rate',
                value: Math.round(errorRate)
              })
            }
          }
        } catch (error) {
          // Silently fail
        }
      }

      if (newAlerts.length > 0) {
        setAlerts(prev => {
          // Evitar alertas duplicados
          const existingIds = prev.map(a => a.id)
          const uniqueNewAlerts = newAlerts.filter(a => !existingIds.includes(a.id))
          return [...prev, ...uniqueNewAlerts].slice(-10) // Manter últimos 10 alertas
        })
        setIsVisible(true)
      }
    }

    // Verificar performance a cada 30 segundos
    const interval = setInterval(checkPerformance, 30000)
    
    // Verificação inicial
    checkPerformance()

    return () => clearInterval(interval)
  }, [])

  const dismissAlert = (id: string) => {
    setAlerts(prev => prev.filter(a => a.id !== id))
    if (alerts.length <= 1) {
      setIsVisible(false)
    }
  }

  const dismissAll = () => {
    setAlerts([])
    setIsVisible(false)
  }

  if (!isVisible || alerts.length === 0) return null

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'error': return '🚨'
      case 'warning': return '⚠️'
      case 'info': return 'ℹ️'
      default: return '📊'
    }
  }

  const getAlertColor = (type: string) => {
    switch (type) {
      case 'error': return 'bg-red-50 border-red-200 text-red-800'
      case 'warning': return 'bg-yellow-50 border-yellow-200 text-yellow-800'
      case 'info': return 'bg-blue-50 border-blue-200 text-blue-800'
      default: return 'bg-gray-50 border-gray-200 text-gray-800'
    }
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 max-w-sm w-full">
      <div className="bg-white rounded-lg shadow-lg border-2 border-gray-200">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h3 className="font-semibold text-gray-800 flex items-center">
            📊 Alertas de Performance
            <span className="ml-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
              {alerts.length}
            </span>
          </h3>
          <div className="flex gap-2">
            <button
              onClick={dismissAll}
              className="text-gray-400 hover:text-gray-600 text-sm"
            >
              Limpar
            </button>
            <button
              onClick={() => setIsVisible(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Alerts List */}
        <div className="max-h-64 overflow-y-auto">
          {alerts.map(alert => (
            <div
              key={alert.id}
              className={`p-4 border-b last:border-b-0 ${getAlertColor(alert.type)}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center mb-1">
                    <span className="mr-2">{getAlertIcon(alert.type)}</span>
                    <h4 className="font-medium text-sm">{alert.title}</h4>
                  </div>
                  <p className="text-sm opacity-90">{alert.message}</p>
                  {alert.metric && alert.value && (
                    <div className="mt-2 text-xs opacity-75">
                      {alert.metric}: {alert.value}
                      {alert.metric.includes('Time') ? 'ms' : 
                       alert.metric.includes('Rate') ? '%' : ''}
                    </div>
                  )}
                  <div className="text-xs opacity-60 mt-1">
                    {new Date(alert.timestamp).toLocaleTimeString()}
                  </div>
                </div>
                <button
                  onClick={() => dismissAlert(alert.id)}
                  className="text-current opacity-50 hover:opacity-75 ml-2"
                >
                  ✕
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="p-3 bg-gray-50 text-center">
          <p className="text-xs text-gray-600">
            Monitoramento automático ativo
          </p>
        </div>
      </div>
    </div>
  )
}