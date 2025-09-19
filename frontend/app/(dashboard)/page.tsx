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
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="text-2xl mr-3">📄</div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{mockContracts.length}</p>
              <p className="text-gray-600">Contratos Total</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="text-2xl mr-3">⚡</div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {mockContracts.filter(c => c.status === 'analyzed').length}
              </p>
              <p className="text-gray-600">Analisados</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="text-2xl mr-3">⚠️</div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {mockContracts.filter(c => c.riskLevel === 'high').length}
              </p>
              <p className="text-gray-600">Alto Risco</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="text-2xl mr-3">🔄</div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {mockContracts.filter(c => c.status === 'processing').length}
              </p>
              <p className="text-gray-600">Processando</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-4">Ações Rápidas</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link 
            href="/dashboard/upload"
            className="flex items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 transition-colors"
          >
            <div className="text-2xl mr-3">📤</div>
            <div>
              <p className="font-medium">Novo Upload</p>
              <p className="text-sm text-gray-600">Analisar novo contrato</p>
            </div>
          </Link>
          
          <Link 
            href="/dashboard/chat"
            className="flex items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 transition-colors"
          >
            <div className="text-2xl mr-3">💬</div>
            <div>
              <p className="font-medium">Chat com IA</p>
              <p className="text-sm text-gray-600">Tirar dúvidas jurídicas</p>
            </div>
          </Link>
          
          <Link 
            href="/dashboard/contracts"
            className="flex items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 transition-colors"
          >
            <div className="text-2xl mr-3">📊</div>
            <div>
              <p className="font-medium">Ver Relatórios</p>
              <p className="text-sm text-gray-600">Análises detalhadas</p>
            </div>
          </Link>
        </div>
      </div>

      {/* Recent Contracts */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Contratos Recentes</h2>
          <Link 
            href="/dashboard/contracts"
            className="text-blue-600 hover:text-blue-700 text-sm"
          >
            Ver todos →
          </Link>
        </div>
        
        <div className="space-y-4">
          {mockContracts.map((contract) => (
            <div key={contract.id} className="flex items-center justify-between p-4 border rounded-lg">
              <div className="flex items-center space-x-4">
                <div className="text-2xl">
                  {typeEmojis[contract.type as keyof typeof typeEmojis]}
                </div>
                <div>
                  <h3 className="font-medium">{contract.title}</h3>
                  <p className="text-sm text-gray-600">
                    Enviado em {new Date(contract.uploadDate).toLocaleDateString('pt-BR')}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  riskColors[contract.riskLevel as keyof typeof riskColors]
                }`}>
                  {riskLabels[contract.riskLevel as keyof typeof riskLabels]}
                </span>
                
                {contract.status === 'analyzed' ? (
                  <button className="text-blue-600 hover:text-blue-700 text-sm">
                    Ver Análise
                  </button>
                ) : (
                  <span className="text-gray-500 text-sm">Processando...</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tips */}
      <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
        <h3 className="font-semibold text-blue-900 mb-2">💡 Dica do Dia</h3>
        <p className="text-blue-800">
          Sempre leia as cláusulas de rescisão antecipada antes de assinar um contrato. 
          Elas podem conter multas ou condições que impactem significativamente seus direitos.
        </p>
      </div>
    </div>
  )
}