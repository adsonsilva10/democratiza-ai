'use client'

import Link from 'next/link'
import { useState } from 'react'

// Mock data expandido para histórico
const allContracts = [
  {
    id: 1,
    title: 'Contrato de Locação - Apartamento Centro',
    type: 'rental',
    riskLevel: 'medium',
    uploadDate: '2025-09-15',
    status: 'analyzed',
    summary: 'Cláusulas de reajuste anual com IGP-M. Taxa de administração de 8%.',
    keyPoints: [
      'Taxa de administração acima da média (8%)',
      'Reajuste baseado no IGP-M pode ser volátil',
      'Caução equivalente a 3 meses de aluguel'
    ],
    riskScore: 65
  },
  {
    id: 2,
    title: 'Plano de Internet - Operadora XYZ',
    type: 'telecom',
    riskLevel: 'low',
    uploadDate: '2025-09-10',
    status: 'analyzed',
    summary: 'Fidelidade de 12 meses. Velocidade garantida em 80% do contratado.',
    keyPoints: [
      'Fidelidade de 12 meses com multa proporcional',
      'Velocidade garantida apenas 80% do contratado',
      'Suporte técnico 24h incluído'
    ],
    riskScore: 30
  },
  {
    id: 3,
    title: 'Empréstimo Pessoal - Banco ABC',
    type: 'financial',
    riskLevel: 'high',
    uploadDate: '2025-09-08',
    status: 'analyzed',
    summary: 'Taxa de juros alta (3,2% a.m.). Cláusula de vencimento antecipado.',
    keyPoints: [
      'Taxa de juros muito alta (3,2% ao mês)',
      'Cláusula de vencimento antecipado por atraso',
      'Sem carência para pagamento antecipado'
    ],
    riskScore: 85
  },
  {
    id: 4,
    title: 'Seguro Auto - Seguradora DEF',
    type: 'insurance',
    riskLevel: 'medium',
    uploadDate: '2025-09-05',
    status: 'analyzed',
    summary: 'Cobertura limitada para terceiros. Franquia elevada para sinistros.',
    keyPoints: [
      'Cobertura para terceiros limitada a R$ 100.000',
      'Franquia alta para vidros (R$ 500)',
      'Renovação automática com reajuste'
    ],
    riskScore: 55
  },
  {
    id: 5,
    title: 'Conta Corrente - Banco Digital',
    type: 'financial',
    riskLevel: 'low',
    uploadDate: '2025-08-28',
    status: 'analyzed',
    summary: 'Sem anuidade. Taxas transparentes para serviços extras.',
    keyPoints: [
      'Conta sem anuidade ou taxas de manutenção',
      'Tarifas transparentes para serviços adicionais',
      'Possibilidade de portabilidade gratuita'
    ],
    riskScore: 20
  },
  {
    id: 6,
    title: 'Plano de Saúde - Operadora Health+',
    type: 'health',
    riskLevel: 'high',
    uploadDate: '2025-08-20',
    status: 'analyzed',
    summary: 'Carências extensas. Cobertura limitada para procedimentos especiais.',
    keyPoints: [
      'Carência de 180 dias para cirurgias',
      'Exclusão de tratamentos experimentais',
      'Reajuste anual por faixa etária'
    ],
    riskScore: 78
  }
]

const typeEmojis = {
  rental: '🏠',
  telecom: '📱',
  financial: '💰',
  insurance: '🛡️',
  health: '🏥'
}

const typeLabels = {
  rental: 'Locação',
  telecom: 'Telecom',
  financial: 'Financeiro',
  insurance: 'Seguro',
  health: 'Saúde'
}

const riskColors = {
  low: 'bg-green-100 text-green-800 border-green-300',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  high: 'bg-red-100 text-red-800 border-red-300'
}

const riskLabels = {
  low: 'Baixo Risco',
  medium: 'Médio Risco',
  high: 'Alto Risco'
}

export default function HistoricoPage() {
  const [filterType, setFilterType] = useState('all')
  const [filterRisk, setFilterRisk] = useState('all')
  const [sortBy, setSortBy] = useState('date')
  const [searchTerm, setSearchTerm] = useState('')

  // Filtrar contratos
  const filteredContracts = allContracts
    .filter(contract => {
      if (filterType !== 'all' && contract.type !== filterType) return false
      if (filterRisk !== 'all' && contract.riskLevel !== filterRisk) return false
      if (searchTerm && !contract.title.toLowerCase().includes(searchTerm.toLowerCase())) return false
      return true
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.uploadDate).getTime() - new Date(a.uploadDate).getTime()
        case 'risk':
          return b.riskScore - a.riskScore
        case 'name':
          return a.title.localeCompare(b.title)
        default:
          return 0
      }
    })

  const getRiskScoreColor = (score: number) => {
    if (score <= 40) return 'text-green-600'
    if (score <= 70) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="w-full max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          📚 Histórico de Contratos
        </h1>
        <p className="text-gray-600 text-base sm:text-lg">
          Visualize e gerencie todos os contratos que já foram analisados
        </p>
      </div>

      {/* Filtros e Busca */}
      <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Busca */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Buscar contrato
            </label>
            <input
              type="text"
              placeholder="Digite o nome do contrato..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Filtro por Tipo */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tipo de contrato
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              <option value="all">Todos os tipos</option>
              <option value="rental">Locação</option>
              <option value="telecom">Telecom</option>
              <option value="financial">Financeiro</option>
              <option value="insurance">Seguro</option>
              <option value="health">Saúde</option>
            </select>
          </div>

          {/* Filtro por Risco */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nível de risco
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={filterRisk}
              onChange={(e) => setFilterRisk(e.target.value)}
            >
              <option value="all">Todos os níveis</option>
              <option value="low">Baixo risco</option>
              <option value="medium">Médio risco</option>
              <option value="high">Alto risco</option>
            </select>
          </div>

          {/* Ordenação */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Ordenar por
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="date">Data mais recente</option>
              <option value="risk">Maior risco</option>
              <option value="name">Nome A-Z</option>
            </select>
          </div>
        </div>
      </div>

      {/* Estatísticas Rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <div className="text-2xl font-bold text-blue-600">{filteredContracts.length}</div>
          <div className="text-sm text-blue-700">Contratos encontrados</div>
        </div>
        <div className="bg-red-50 p-4 rounded-lg border border-red-200">
          <div className="text-2xl font-bold text-red-600">
            {filteredContracts.filter(c => c.riskLevel === 'high').length}
          </div>
          <div className="text-sm text-red-700">Alto risco</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <div className="text-2xl font-bold text-yellow-600">
            {filteredContracts.filter(c => c.riskLevel === 'medium').length}
          </div>
          <div className="text-sm text-yellow-700">Médio risco</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <div className="text-2xl font-bold text-green-600">
            {filteredContracts.filter(c => c.riskLevel === 'low').length}
          </div>
          <div className="text-sm text-green-700">Baixo risco</div>
        </div>
      </div>

      {/* Lista de Contratos */}
      <div className="space-y-6">
        {filteredContracts.map((contract) => (
          <div key={contract.id} className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-200">
            <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
              
              {/* Informações Principais */}
              <div className="flex-1">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{typeEmojis[contract.type as keyof typeof typeEmojis]}</span>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">
                        {contract.title}
                      </h3>
                      <div className="flex items-center space-x-3">
                        <span className="text-sm text-gray-600">
                          {typeLabels[contract.type as keyof typeof typeLabels]}
                        </span>
                        <span className="text-sm text-gray-400">•</span>
                        <span className="text-sm text-gray-600">
                          {new Date(contract.uploadDate).toLocaleDateString('pt-BR')}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium border ${
                      riskColors[contract.riskLevel as keyof typeof riskColors]
                    }`}>
                      {riskLabels[contract.riskLevel as keyof typeof riskLabels]}
                    </span>
                    <div className={`text-lg font-bold ${getRiskScoreColor(contract.riskScore)}`}>
                      {contract.riskScore}%
                    </div>
                  </div>
                </div>

                <p className="text-gray-700 mb-4 leading-relaxed">
                  {contract.summary}
                </p>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Principais pontos identificados:</h4>
                  <ul className="space-y-1">
                    {contract.keyPoints.map((point, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start">
                        <span className="text-blue-500 mr-2 mt-1">•</span>
                        {point}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Ações */}
              <div className="flex flex-col space-y-3 lg:min-w-[200px]">
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  Ver Análise Completa
                </button>
                <Link 
                  href={`/dashboard/chat?contract=${contract.id}`}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-center"
                >
                  💬 Chat sobre este contrato
                </Link>
                <button className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors text-sm">
                  📥 Baixar PDF
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Mensagem quando não há resultados */}
      {filteredContracts.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📭</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Nenhum contrato encontrado
          </h3>
          <p className="text-gray-600 mb-6">
            Tente ajustar os filtros ou faça uma nova busca
          </p>
          <Link 
            href="/dashboard/analise"
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            📤 Analisar novo contrato
          </Link>
        </div>
      )}
    </div>
  )
}