'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlertTriangle, CheckCircle, Eye, Download } from 'lucide-react'

export default function ContractSimulation() {
  const [currentStep, setCurrentStep] = useState(0)
  const [isSimulating, setIsSimulating] = useState(false)
  const [showResults, setShowResults] = useState(false)

  const simulationSteps = [
    {
      title: "Contrato Carregado",
      description: "Contrato de Aluguel - 3 páginas detectadas",
      icon: "📄",
      progress: 25
    },
    {
      title: "Analisando Cláusulas",
      description: "IA identificando termos e condições...",
      icon: "🤖",
      progress: 50
    },
    {
      title: "Verificando Riscos",
      description: "Comparando com legislação brasileira...",
      icon: "⚖️",
      progress: 75
    },
    {
      title: "Relatório Pronto",
      description: "Análise completa finalizada!",
      icon: "✅",
      progress: 100
    }
  ]

  const mockAnalysisResults = {
    riskLevel: "Alto Risco",
    issues: [
      {
        type: "Cláusula Abusiva",
        severity: "alta",
        title: "Multa Excessiva por Rescisão",
        description: "Multa de 6 salários mínimos por rescisão antecipada excede o limite legal de 3 salários.",
        article: "Art. 4º da Lei 8.245/91"
      },
      {
        type: "Direito Limitado",
        severity: "media",
        title: "Manutenção da Geladeira",
        description: "Contrato atribui ao inquilino responsabilidade por defeitos em equipamentos que deveriam ser do proprietário.",
        article: "Art. 22 da Lei 8.245/91"
      },
      {
        type: "Informação Clara",
        severity: "baixa",
        title: "Reajuste Anual Definido",
        description: "Índice de reajuste está claramente especificado (IGPM).",
        article: "Conforme legislação"
      }
    ],
    recommendations: [
      "Negociar redução da multa rescisória para 3 salários mínimos",
      "Solicitar exclusão da responsabilidade por manutenção de equipamentos do imóvel",
      "Considerar incluir cláusula de vistoria detalhada"
    ]
  }

  // Start simulation function
  const startSimulation = () => {
    setIsSimulating(true)
    setShowResults(false)
    setCurrentStep(0)
    
    // Progress through steps
    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev >= simulationSteps.length - 1) {
          clearInterval(stepInterval)
          setIsSimulating(false)
          setShowResults(true)
          return prev
        }
        return prev + 1
      })
    }, 2000) // 2 seconds per step
  }

  // Auto-start simulation once
  useEffect(() => {
    startSimulation()
  }, [])

  return (
    <div className="max-w-4xl mx-auto">
      {/* Auto-running Simulation */}
        <div className="space-y-6">
          {/* Progress Bar */}
          <div className="bg-white rounded-lg p-6 shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold">Processando Contrato</h3>
              <span className="text-sm text-gray-600">{simulationSteps[currentStep]?.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div 
                className="bg-gradient-to-r from-blue-600 to-purple-600 h-3 rounded-full transition-all duration-500"
                style={{ width: `${simulationSteps[currentStep]?.progress}%` }}
              ></div>
            </div>
            <div className="mt-4 flex items-center gap-3">
              <span className="text-2xl">{simulationSteps[currentStep]?.icon}</span>
              <div>
                <p className="font-medium">{simulationSteps[currentStep]?.title}</p>
                <p className="text-sm text-gray-600">{simulationSteps[currentStep]?.description}</p>
              </div>
            </div>
          </div>

          {/* Results */}
          {showResults && (
            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
              <div className="bg-gradient-to-r from-red-500 to-orange-500 text-white p-4">
                <div className="flex items-center gap-3">
                  <AlertTriangle className="h-6 w-6" />
                  <div>
                    <h3 className="font-bold text-lg">Relatório de Análise</h3>
                    <p className="text-red-100">Status: {mockAnalysisResults.riskLevel}</p>
                  </div>
                </div>
              </div>
              
              <div className="p-6 space-y-6">
                <div>
                  <h4 className="font-semibold text-lg mb-4">Problemas Identificados</h4>
                  <div className="space-y-4">
                    {mockAnalysisResults.issues.map((issue, index) => (
                      <Card key={index} className="border-l-4" style={{
                        borderLeftColor: issue.severity === 'alta' ? '#ef4444' : 
                                        issue.severity === 'media' ? '#f59e0b' : '#10b981'
                      }}>
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <Badge variant={issue.severity === 'alta' ? 'danger' : 
                                              issue.severity === 'media' ? 'warning' : 'success'}>
                                  {issue.type}
                                </Badge>
                                {issue.severity === 'baixa' && <CheckCircle className="h-4 w-4 text-green-500" />}
                                {issue.severity !== 'baixa' && <AlertTriangle className="h-4 w-4 text-red-500" />}
                              </div>
                              <h5 className="font-medium mb-1">{issue.title}</h5>
                              <p className="text-sm text-gray-600 mb-2">{issue.description}</p>
                              <p className="text-xs text-blue-600 font-medium">{issue.article}</p>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold text-lg mb-4">Recomendações</h4>
                  <ul className="space-y-2">
                    {mockAnalysisResults.recommendations.map((rec, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <span className="text-green-500 mt-1">✓</span>
                        <span className="text-sm">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="flex gap-3 pt-4">
                  <Button 
                    onClick={startSimulation}
                    variant="outline"
                    className="flex-1"
                  >
                    🔄 Ver Novamente
                  </Button>
                  <Button 
                    className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    onClick={() => window.open('/plataforma/analise', '_blank')}
                  >
                    🚀 Analisar Meu Contrato
                  </Button>
                </div>
              </div>
            </div>
          )}
        </div>
    </div>
  )
}