'use client'

import { useState } from 'react'

// Mock data expandida
const mockContracts = [
  {
    id: 1,
    title: 'Contrato de Locação - Apartamento Centro',
    type: 'rental',
    riskLevel: 'medium',
    uploadDate: '2025-09-15',
    status: 'analyzed',
    fileSize: '2.1 MB',
    issues: 3,
    recommendations: 2
  },
  {
    id: 2,
    title: 'Plano de Internet - Operadora XYZ',
    type: 'telecom',
    riskLevel: 'low',
    uploadDate: '2025-09-10',
    status: 'analyzed',
    fileSize: '1.8 MB',
    issues: 1,
    recommendations: 1
  },
  {
    id: 3,
    title: 'Empréstimo Pessoal - Banco ABC',
    type: 'financial',
    riskLevel: 'high',
    uploadDate: '2025-09-08',
    status: 'processing',
    fileSize: '3.2 MB',
    issues: 0,
    recommendations: 0
  },
  {
    id: 4,
    title: 'Contrato de Trabalho - Empresa Tech',
    type: 'employment',
    riskLevel: 'low',
    uploadDate: '2025-09-05',
    status: 'analyzed',
    fileSize: '2.7 MB',
    issues: 2,
    recommendations: 3
  },
  {
    id: 5,
    title: 'Seguro Auto - Seguradora Beta',
    type: 'insurance',
    riskLevel: 'medium',
    uploadDate: '2025-09-01',
    status: 'analyzed',
    fileSize: '4.1 MB',
    issues: 4,
    recommendations: 2
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
  employment: '💼',
  insurance: '🛡️'
}

const typeLabels = {
  rental: 'Locação',
  telecom: 'Telecomunicações',
  financial: 'Financeiro',
  employment: 'Trabalho',
  insurance: 'Seguro'
}

export default function ContractsPage() {
  const [filter, setFilter] = useState('all')
  const [sortBy, setSortBy] = useState('date')

  const filteredContracts = mockContracts.filter(contract => {
    if (filter === 'all') return true
    if (filter === 'high-risk') return contract.riskLevel === 'high'
    if (filter === 'processing') return contract.status === 'processing'
    return contract.type === filter
  })

  const sortedContracts = [...filteredContracts].sort((a, b) => {
    if (sortBy === 'date') {
      return new Date(b.uploadDate).getTime() - new Date(a.uploadDate).getTime()
    }
    if (sortBy === 'risk') {
      const riskOrder = { high: 3, medium: 2, low: 1 }
      return riskOrder[b.riskLevel as keyof typeof riskOrder] - riskOrder[a.riskLevel as keyof typeof riskOrder]
    }
    return a.title.localeCompare(b.title)
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Meus Contratos</h1>
          <p className="text-gray-600">Gerencie e analise todos os seus contratos</p>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
          📤 Novo Upload
        </button>
      </div>

      {/* Filters and Search */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Buscar contratos..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div className="flex gap-2">
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Todos os tipos</option>
              <option value="rental">Locação</option>
              <option value="telecom">Telecomunicações</option>
              <option value="financial">Financeiro</option>
              <option value="employment">Trabalho</option>
              <option value="insurance">Seguro</option>
              <option value="high-risk">Alto Risco</option>
              <option value="processing">Processando</option>
            </select>
            
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="date">Data de Upload</option>
              <option value="risk">Nível de Risco</option>
              <option value="name">Nome</option>
            </select>
          </div>
        </div>
      </div>

      {/* Contracts Grid */}
      <div className="grid gap-6">
        {sortedContracts.map((contract) => (
          <div key={contract.id} className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-4">
                <div className="text-3xl">
                  {typeEmojis[contract.type as keyof typeof typeEmojis]}
                </div>
                
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {contract.title}
                  </h3>
                  
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                    <span>{typeLabels[contract.type as keyof typeof typeLabels]}</span>
                    <span>•</span>
                    <span>{contract.fileSize}</span>
                    <span>•</span>
                    <span>Enviado em {new Date(contract.uploadDate).toLocaleDateString('pt-BR')}</span>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      riskColors[contract.riskLevel as keyof typeof riskColors]
                    }`}>
                      {riskLabels[contract.riskLevel as keyof typeof riskLabels]}
                    </span>
                    
                    {contract.status === 'analyzed' && (
                      <>
                        <span className="text-xs text-gray-500">
                          {contract.issues} questões encontradas
                        </span>
                        <span className="text-xs text-gray-500">
                          {contract.recommendations} recomendações
                        </span>
                      </>
                    )}
                    
                    {contract.status === 'processing' && (
                      <span className="text-xs text-blue-600">⏳ Processando...</span>
                    )}
                  </div>
                </div>
              </div>
              
              <div className="flex space-x-2">
                {contract.status === 'analyzed' ? (
                  <>
                    <button className="px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                      📊 Ver Análise
                    </button>
                    <button className="px-4 py-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors">
                      💬 Chat
                    </button>
                  </>
                ) : (
                  <button className="px-4 py-2 text-gray-400 cursor-not-allowed rounded-lg">
                    ⏳ Aguarde...
                  </button>
                )}
                
                <button className="px-4 py-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
                  📥 Download
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {sortedContracts.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📄</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhum contrato encontrado
          </h3>
          <p className="text-gray-600 mb-6">
            Tente ajustar os filtros ou fazer upload de novos contratos
          </p>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">
            📤 Primeiro Upload
          </button>
        </div>
      )}

      {/* Pagination */}
      {sortedContracts.length > 0 && (
        <div className="flex justify-center">
          <nav className="flex space-x-2">
            <button className="px-3 py-2 text-gray-500 hover:text-gray-700">
              ← Anterior
            </button>
            <button className="px-3 py-2 bg-blue-600 text-white rounded">
              1
            </button>
            <button className="px-3 py-2 text-gray-500 hover:text-gray-700">
              2
            </button>
            <button className="px-3 py-2 text-gray-500 hover:text-gray-700">
              Próximo →
            </button>
          </nav>
        </div>
      )}
    </div>
  )
}