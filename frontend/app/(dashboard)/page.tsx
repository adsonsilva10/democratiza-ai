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
    <div className="space-y-6 w-full overflow-x-hidden">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 w-full">
        <div className="bg-white p-4 sm:p-6 rounded-lg shadow w-full">
          <div className="flex items-center">
            <div className="text-2xl mr-3 flex-shrink-0">📄</div>
            <div className="min-w-0 flex-1">
              <p className="text-xl sm:text-2xl font-bold text-gray-900 truncate">{mockContracts.length}</p>
              <p className="text-gray-600 text-sm sm:text-base truncate">Contratos Total</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 sm:p-6 rounded-lg shadow w-full">
          <div className="flex items-center">
            <div className="text-2xl mr-3 flex-shrink-0">⚡</div>
            <div className="min-w-0 flex-1">
              <p className="text-xl sm:text-2xl font-bold text-gray-900 truncate">
                {mockContracts.filter(c => c.status === 'analyzed').length}
              </p>
              <p className="text-gray-600 text-sm sm:text-base truncate">Analisados</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 sm:p-6 rounded-lg shadow w-full">
          <div className="flex items-center">
            <div className="text-2xl mr-3 flex-shrink-0">⚠️</div>
            <div className="min-w-0 flex-1">
              <p className="text-xl sm:text-2xl font-bold text-gray-900 truncate">
                {mockContracts.filter(c => c.riskLevel === 'high').length}
              </p>
              <p className="text-gray-600 text-sm sm:text-base truncate">Alto Risco</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 sm:p-6 rounded-lg shadow w-full">
          <div className="flex items-center">
            <div className="text-2xl mr-3 flex-shrink-0">🔄</div>
            <div className="min-w-0 flex-1">
              <p className="text-xl sm:text-2xl font-bold text-gray-900 truncate">
                {mockContracts.filter(c => c.status === 'processing').length}
              </p>
              <p className="text-gray-600 text-sm sm:text-base truncate">Processando</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-4 sm:p-6 rounded-lg shadow w-full">
        <h2 className="text-lg font-semibold mb-4 truncate">Ações Rápidas</h2>
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

      {/* Recent Contracts */}
      <div className="bg-white p-4 sm:p-6 rounded-lg shadow w-full">
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 gap-2 w-full">
          <h2 className="text-lg font-semibold truncate">Contratos Recentes</h2>
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
      <div className="bg-blue-50 p-4 sm:p-6 rounded-lg border border-blue-200 w-full">
        <h3 className="font-semibold text-blue-900 mb-2">💡 Dica do Dia</h3>
        <p className="text-blue-800 text-sm sm:text-base leading-relaxed">
          Sempre leia as cláusulas de rescisão antecipada antes de assinar um contrato. 
          Elas podem conter multas ou condições que impactem significativamente seus direitos.
        </p>
      </div>
    </div>
  )
}