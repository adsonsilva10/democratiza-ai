'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function HistoricoPage() {
  const [filter, setFilter] = useState('todos')
  const router = useRouter()

  // Dados simulados - em produção viriam de uma API
  const contratos = [
    {
      id: 1,
      nome: 'Contrato de Locação - Apto 101',
      data: '2025-09-20',
      tipo: 'Locação',
      risco: 'Alto',
      riscoColor: 'bg-red-100 text-red-800',
      arquivo: 'contrato_locacao_101.pdf'
    },
    {
      id: 2,
      nome: 'Contrato de Internet - Fibra 200MB',
      data: '2025-09-18',
      tipo: 'Telecomunicações',
      risco: 'Médio',
      riscoColor: 'bg-yellow-100 text-yellow-800',
      arquivo: 'contrato_internet_fibra.pdf'
    },
    {
      id: 3,
      nome: 'Contrato de Financiamento Veicular',
      data: '2025-09-15',
      tipo: 'Financeiro',
      risco: 'Baixo',
      riscoColor: 'bg-green-100 text-green-800',
      arquivo: 'financiamento_veiculo.pdf'
    },
    {
      id: 4,
      nome: 'Contrato de Cartão de Crédito Premium',
      data: '2025-09-12',
      tipo: 'Financeiro',
      risco: 'Alto',
      riscoColor: 'bg-red-100 text-red-800',
      arquivo: 'cartao_credito_premium.pdf'
    }
  ]

  const filteredContratos = filter === 'todos' 
    ? contratos 
    : contratos.filter(c => c.risco.toLowerCase() === filter)

  const handleViewContract = (contratoId: number) => {
    // Navegar para a página de análise com o ID do contrato
    router.push(`/dashboard/analise?contratoId=${contratoId}`)
  }

  return (
    <div className="p-4 sm:p-6">
      <div className="mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-900 mb-3 sm:mb-4">Histórico de Contratos</h1>
        
        {/* Filtros - Mobile: scroll horizontal, Desktop: normal */}
        <div className="flex gap-2 overflow-x-auto pb-2 sm:pb-0">
          <button
            onClick={() => setFilter('todos')}
            className={`flex-shrink-0 px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
              filter === 'todos' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Todos
          </button>
          <button
            onClick={() => setFilter('alto')}
            className={`flex-shrink-0 px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors whitespace-nowrap ${
              filter === 'alto' ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Alto Risco
          </button>
          <button
            onClick={() => setFilter('médio')}
            className={`flex-shrink-0 px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors whitespace-nowrap ${
              filter === 'médio' ? 'bg-yellow-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Médio Risco
          </button>
          <button
            onClick={() => setFilter('baixo')}
            className={`flex-shrink-0 px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors whitespace-nowrap ${
              filter === 'baixo' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Baixo Risco
          </button>
        </div>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 lg:gap-6 mb-6 sm:mb-8">
        <div className="bg-white p-3 sm:p-4 lg:p-6 rounded-lg shadow">
          <h3 className="text-xs sm:text-sm font-medium text-gray-500">Total Analisado</h3>
          <p className="text-lg sm:text-xl lg:text-2xl font-bold text-gray-900">{contratos.length}</p>
        </div>
        <div className="bg-white p-3 sm:p-4 lg:p-6 rounded-lg shadow">
          <h3 className="text-xs sm:text-sm font-medium text-gray-500">Alto Risco</h3>
          <p className="text-lg sm:text-xl lg:text-2xl font-bold text-red-600">
            {contratos.filter(c => c.risco === 'Alto').length}
          </p>
        </div>
        <div className="bg-white p-3 sm:p-4 lg:p-6 rounded-lg shadow">
          <h3 className="text-xs sm:text-sm font-medium text-gray-500">Médio Risco</h3>
          <p className="text-lg sm:text-xl lg:text-2xl font-bold text-yellow-600">
            {contratos.filter(c => c.risco === 'Médio').length}
          </p>
        </div>
        <div className="bg-white p-3 sm:p-4 lg:p-6 rounded-lg shadow">
          <h3 className="text-xs sm:text-sm font-medium text-gray-500">Baixo Risco</h3>
          <p className="text-lg sm:text-xl lg:text-2xl font-bold text-green-600">
            {contratos.filter(c => c.risco === 'Baixo').length}
          </p>
        </div>
      </div>

      {/* Lista de Contratos */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-4 sm:p-6 border-b">
          <h2 className="text-base sm:text-lg font-medium text-gray-900">
            Contratos Analisados ({filteredContratos.length})
          </h2>
        </div>
        <div className="divide-y divide-gray-200">
          {filteredContratos.map((contrato) => (
            <div key={contrato.id} className="p-4 sm:p-6 hover:bg-gray-50 transition-colors">
              
              {/* Mobile Layout */}
              <div className="block sm:hidden">
                <div className="flex items-start gap-3 mb-3">
                  <div className="text-blue-600 flex-shrink-0">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-medium text-gray-900 truncate">{contrato.nome}</h3>
                    <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                      <span>📅 {new Date(contrato.data).toLocaleDateString('pt-BR')}</span>
                      <span>📂 {contrato.tipo}</span>
                    </div>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium flex-shrink-0 ${contrato.riscoColor}`}>
                    {contrato.risco}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-500">📎 {contrato.arquivo}</span>
                  <div className="flex gap-1">
                    <button 
                      onClick={() => handleViewContract(contrato.id)}
                      className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                      title="Ver análise"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                    <button className="p-2 text-gray-400 hover:text-green-600 transition-colors">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </button>
                    <button className="p-2 text-gray-400 hover:text-red-600 transition-colors">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              {/* Desktop Layout */}
              <div className="hidden sm:flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-4">
                    <div className="text-blue-600">
                      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-gray-900">{contrato.nome}</h3>
                      <div className="flex items-center gap-4 mt-1 text-sm text-gray-500">
                        <span>📅 {new Date(contrato.data).toLocaleDateString('pt-BR')}</span>
                        <span>📂 {contrato.tipo}</span>
                        <span>📎 {contrato.arquivo}</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${contrato.riscoColor}`}>
                    {contrato.risco} Risco
                  </span>
                  
                  <div className="flex gap-2">
                    <button 
                      onClick={() => handleViewContract(contrato.id)}
                      className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                      title="Ver análise"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                    <button className="p-2 text-gray-400 hover:text-green-600 transition-colors">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </button>
                    <button className="p-2 text-gray-400 hover:text-red-600 transition-colors">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}