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
    status: 'analyzed'
  },
  {
    id: 2,
    title: 'Plano de Internet - Operadora XYZ',
    type: 'telecom',
    riskLevel: 'low',
    uploadDate: '2025-09-10',
    status: 'analyzed'
  },
  {
    id: 3,
    title: 'Empréstimo Pessoal - Banco ABC',
    type: 'financial',
    riskLevel: 'high',
    uploadDate: '2025-09-08',
    status: 'processing'
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
  financial: '💰'
}

export default function DashboardPage() {
  return (
    <div className="w-full max-w-7xl mx-auto">
      {/* Header melhorado */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          📊 Dashboard
        </h1>
        <p className="text-gray-600 text-base sm:text-lg">
          Acompanhe seus contratos e análises em tempo real
        </p>
      </div>

      <div className="space-y-8">
        {/* Stats Cards melhorados */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="text-3xl mr-4 flex-shrink-0">📄</div>
              <div className="min-w-0 flex-1">
                <p className="text-2xl sm:text-3xl font-bold text-gray-900">{mockContracts.length}</p>
                <p className="text-gray-600 font-medium">Contratos Total</p>
              </div>
            </div>
            <div className="text-blue-500 opacity-20">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"></path>
                <path fillRule="evenodd" d="M4 5a2 2 0 012-2v1a1 1 0 001 1h6a1 1 0 001-1V3a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3z" clipRule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-200 border border-green-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="text-3xl mr-4 flex-shrink-0">⚡</div>
              <div className="min-w-0 flex-1">
                <p className="text-2xl sm:text-3xl font-bold text-green-700">
                  {mockContracts.filter(c => c.status === 'analyzed').length}
                </p>
                <p className="text-green-600 font-medium">Analisados</p>
              </div>
            </div>
            <div className="text-green-500 opacity-20">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-red-50 to-pink-50 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-200 border border-red-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="text-3xl mr-4 flex-shrink-0">⚠️</div>
              <div className="min-w-0 flex-1">
                <p className="text-2xl sm:text-3xl font-bold text-red-700">
                  {mockContracts.filter(c => c.riskLevel === 'high').length}
                </p>
                <p className="text-red-600 font-medium">Alto Risco</p>
              </div>
            </div>
            <div className="text-red-500 opacity-20">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-yellow-50 to-orange-50 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-200 border border-yellow-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="text-3xl mr-4 flex-shrink-0 animate-spin">🔄</div>
              <div className="min-w-0 flex-1">
                <p className="text-2xl sm:text-3xl font-bold text-yellow-700">
                  {mockContracts.filter(c => c.status === 'processing').length}
                </p>
                <p className="text-yellow-600 font-medium">Processando</p>
              </div>
            </div>
            <div className="text-yellow-500 opacity-20">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

        {/* Quick Actions melhoradas */}
        <div className="bg-white p-8 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold text-gray-900 mb-6">🚀 Ações Rápidas</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
          <Link 
            href="/dashboard/upload"
            className="flex items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 transition-colors w-full min-w-0"
          >
            <div className="text-2xl mr-3 flex-shrink-0">📤</div>
            <div className="min-w-0 flex-1">
              <p className="font-medium truncate">Novo Upload</p>
              <p className="text-sm text-gray-600 truncate">Analisar novo contrato</p>
            </div>
          </Link>
          
          <Link 
            href="/chat"
            className="flex items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 transition-colors w-full min-w-0"
          >
            <div className="text-2xl mr-3 flex-shrink-0">💬</div>
            <div className="min-w-0 flex-1">
              <p className="font-medium truncate">Chat com IA</p>
              <p className="text-sm text-gray-600 truncate">Tirar dúvidas jurídicas</p>
            </div>
          </Link>
          
          <Link 
            href="/dashboard/contracts"
            className="flex items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 transition-colors w-full min-w-0"
          >
            <div className="text-2xl mr-3 flex-shrink-0">📊</div>
            <div className="min-w-0 flex-1">
              <p className="font-medium truncate">Ver Relatórios</p>
              <p className="text-sm text-gray-600 truncate">Análises detalhadas</p>
            </div>
          </Link>
        </div>
      </div>

        {/* Recent Contracts melhorados */}
        <div className="bg-white p-8 rounded-xl shadow-lg">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 gap-2">
            <h2 className="text-xl font-bold text-gray-900">📋 Contratos Recentes</h2>
          <Link 
            href="/dashboard/contracts"
            className="text-blue-600 hover:text-blue-700 text-sm flex-shrink-0"
          >
            Ver todos →
          </Link>
        </div>
        
        <div className="space-y-4 w-full">
          {mockContracts.map((contract) => (
            <div key={contract.id} className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 border rounded-lg gap-3 w-full">
              <div className="flex items-center space-x-4 min-w-0 flex-1">
                <div className="text-2xl flex-shrink-0">
                  {typeEmojis[contract.type as keyof typeof typeEmojis]}
                </div>
                <div className="min-w-0 flex-1">
                  <h3 className="font-medium truncate">{contract.title}</h3>
                  <p className="text-sm text-gray-600 truncate">
                    Enviado em {new Date(contract.uploadDate).toLocaleDateString('pt-BR')}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center justify-between sm:justify-end space-x-3 flex-shrink-0">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  riskColors[contract.riskLevel as keyof typeof riskColors]
                } truncate`}>
                  {riskLabels[contract.riskLevel as keyof typeof riskLabels]}
                </span>
                
                {contract.status === 'analyzed' ? (
                  <button className="text-blue-600 hover:text-blue-700 text-sm whitespace-nowrap">
                    Ver Análise
                  </button>
                ) : (
                  <span className="text-gray-500 text-sm whitespace-nowrap">Processando...</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

        {/* Tips */}
        <div className="bg-blue-50 p-6 rounded-xl border border-blue-200">
          <h3 className="font-semibold text-blue-900 mb-3 text-lg">💡 Dica do Dia</h3>
          <p className="text-blue-800 text-base leading-relaxed">
            Sempre leia as cláusulas de rescisão antecipada antes de assinar um contrato. 
            Elas podem conter multas ou condições que impactem significativamente seus direitos.
          </p>
        </div>
      </div>
    </div>
  )
}