'use client'

import Link from 'next/link'

// Mock data para demonstração
const mockContracts = [
  {
    id: 1,
    title: 'Contrato de Locação - Apartamento Centro',
    type: 'rental',
    riskLevel: 'medium',
    uploadDate: '2025-09-15',
    status: 'analyzed',
    summary: 'Cláusulas de reajuste anual com IGP-M. Taxa de administração de 8%.'
  },
  {
    id: 2,
    title: 'Plano de Internet - Operadora XYZ',
    type: 'telecom',
    riskLevel: 'low',
    uploadDate: '2025-09-10',
    status: 'analyzed',
    summary: 'Fidelidade de 12 meses. Velocidade garantida em 80% do contratado.'
  },
  {
    id: 3,
    title: 'Empréstimo Pessoal - Banco ABC',
    type: 'financial',
    riskLevel: 'high',
    uploadDate: '2025-09-08',
    status: 'analyzed',
    summary: 'Taxa de juros alta (3,2% a.m.). Cláusula de vencimento antecipado.'
  },
  {
    id: 4,
    title: 'Seguro Auto - Seguradora DEF',
    type: 'insurance',
    riskLevel: 'medium',
    uploadDate: '2025-09-05',
    status: 'analyzed',
    summary: 'Cobertura limitada para terceiros. Franquia elevada para sinistros.'
  }
]

// Principais riscos identificados
const topRisks = [
  {
    risk: 'Juros Abusivos',
    count: 12,
    percentage: 35,
    severity: 'high'
  },
  {
    risk: 'Cláusulas de Fidelidade',
    count: 8,
    percentage: 23,
    severity: 'medium'
  },
  {
    risk: 'Multas Excessivas',
    count: 6,
    percentage: 17,
    severity: 'high'
  },
  {
    risk: 'Renovação Automática',
    count: 4,
    percentage: 12,
    severity: 'medium'
  }
]

const riskColors = {
  low: 'bg-green-100 text-green-800',
  medium: 'bg-yellow-100 text-yellow-800',
  high: 'bg-red-100 text-red-800'
}

const riskLabels = {
  low: 'Baixo Risco',
  medium: 'Médio Risco',
  high: 'Alto Risco'
}

const typeEmojis = {
  rental: '🏠',
  telecom: '📱',
  financial: '💰',
  insurance: '🛡️'
}

export default function DashboardPage() {
  const totalContracts = mockContracts.length
  const analyzedContracts = mockContracts.filter(c => c.status === 'analyzed').length
  const highRiskContracts = mockContracts.filter(c => c.riskLevel === 'high').length
  const recentContracts = mockContracts.slice(0, 3)

  return (
    <div className="w-full max-w-7xl mx-auto">
      {/* Header Principal */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900">
            🏠 Home
          </h1>
          <div className="text-sm text-gray-500">
            Última atualização: {new Date().toLocaleDateString('pt-BR')} às {new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
        <p className="text-gray-600 text-base sm:text-lg">
          Visão geral da sua análise de contratos e principais alertas
        </p>
      </div>

      {/* Layout em Blocos Organizados */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        
        {/* Bloco 1: Estatísticas Principais - 2 colunas */}
        <div className="lg:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-lg mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
              📊 Estatísticas Gerais
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg border border-blue-100">
                <div className="text-3xl font-bold text-blue-600">{totalContracts}</div>
                <div className="text-sm text-blue-700 font-medium">Total de Contratos</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg border border-green-100">
                <div className="text-3xl font-bold text-green-600">{analyzedContracts}</div>
                <div className="text-sm text-green-700 font-medium">Analisados</div>
              </div>
              <div className="text-center p-4 bg-red-50 rounded-lg border border-red-100">
                <div className="text-3xl font-bold text-red-600">{highRiskContracts}</div>
                <div className="text-sm text-red-700 font-medium">Alto Risco</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg border border-purple-100">
                <div className="text-3xl font-bold text-purple-600">{Math.round((analyzedContracts / totalContracts) * 100)}%</div>
                <div className="text-sm text-purple-700 font-medium">Taxa Análise</div>
              </div>
            </div>
          </div>

          {/* Bloco: Principais Riscos Identificados */}
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
              ⚠️ Principais Riscos Identificados
            </h2>
            <div className="space-y-4">
              {topRisks.map((risk, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${
                      risk.severity === 'high' ? 'bg-red-500' : 'bg-yellow-500'
                    }`}></div>
                    <span className="font-medium">{risk.risk}</span>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-600">{risk.count} contratos</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            risk.severity === 'high' ? 'bg-red-500' : 'bg-yellow-500'
                          }`}
                          style={{ width: `${risk.percentage}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">{risk.percentage}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 text-center">
              <Link 
                href="/dashboard/historico"
                className="text-blue-600 hover:text-blue-700 font-medium text-sm"
              >
                Ver análise completa →
              </Link>
            </div>
          </div>
        </div>

        {/* Bloco 2: Histórico Recente - 1 coluna */}
        <div className="lg:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center justify-between">
              📋 Contratos Recentes
              <Link 
                href="/dashboard/historico"
                className="text-blue-600 hover:text-blue-700 text-sm font-normal"
              >
                Ver todos
              </Link>
            </h2>
            <div className="space-y-4">
              {recentContracts.map((contract) => (
                <div key={contract.id} className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">{typeEmojis[contract.type as keyof typeof typeEmojis]}</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        riskColors[contract.riskLevel as keyof typeof riskColors]
                      }`}>
                        {riskLabels[contract.riskLevel as keyof typeof riskLabels]}
                      </span>
                    </div>
                  </div>
                  <h3 className="font-medium text-gray-900 mb-2 text-sm leading-tight">
                    {contract.title}
                  </h3>
                  <p className="text-xs text-gray-600 mb-3 leading-relaxed">
                    {contract.summary}
                  </p>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-500">
                      {new Date(contract.uploadDate).toLocaleDateString('pt-BR')}
                    </span>
                    <button className="text-blue-600 hover:text-blue-700 text-xs font-medium">
                      Ver detalhes
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Seção de Ações Rápidas */}
      <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
          🚀 Ações Rápidas
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link 
            href="/dashboard/analise"
            className="flex items-center p-6 border-2 border-dashed border-blue-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-all duration-200 group"
          >
            <div className="text-3xl mr-4 group-hover:scale-110 transition-transform duration-200">📤</div>
            <div>
              <p className="font-semibold text-gray-900 mb-1">Nova Análise</p>
              <p className="text-sm text-gray-600">Upload e análise de contrato</p>
            </div>
          </Link>
          
          <Link 
            href="/dashboard/chat"
            className="flex items-center p-6 border-2 border-dashed border-green-300 rounded-lg hover:border-green-400 hover:bg-green-50 transition-all duration-200 group"
          >
            <div className="text-3xl mr-4 group-hover:scale-110 transition-transform duration-200">💬</div>
            <div>
              <p className="font-semibold text-gray-900 mb-1">Chat com IA</p>
              <p className="text-sm text-gray-600">Tire dúvidas jurídicas</p>
            </div>
          </Link>
          
          <Link 
            href="/dashboard/historico"
            className="flex items-center p-6 border-2 border-dashed border-purple-300 rounded-lg hover:border-purple-400 hover:bg-purple-50 transition-all duration-200 group"
          >
            <div className="text-3xl mr-4 group-hover:scale-110 transition-transform duration-200">📊</div>
            <div>
              <p className="font-semibold text-gray-900 mb-1">Ver Histórico</p>
              <p className="text-sm text-gray-600">Análises anteriores</p>
            </div>
          </Link>
        </div>
      </div>

      {/* Dica do Dia */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border border-blue-200 shadow-lg">
        <div className="flex items-start space-x-4">
          <div className="text-3xl">💡</div>
          <div>
            <h3 className="font-semibold text-blue-900 mb-2 text-lg">Dica Jurídica do Dia</h3>
            <p className="text-blue-800 text-base leading-relaxed">
              <strong>Atenção às cláusulas de rescisão antecipada:</strong> Antes de assinar qualquer contrato, 
              sempre verifique as condições para cancelamento antecipado. Muitas vezes essas cláusulas contêm 
              multas abusivas ou condições que podem impactar significativamente seus direitos como consumidor.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}