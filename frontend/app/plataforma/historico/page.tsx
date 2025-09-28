'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function HistoricoPage() {
  const [filter, setFilter] = useState('todos')
  const router = useRouter()

  // Dados simulados com status de assinatura
  const contratos = [
    {
      id: 1,
      nome: 'Contrato de Locação - Apto 101',
      data: '2025-09-20',
      tipo: 'Locação',
      risco: 'Alto',
      riscoColor: 'bg-red-100 text-red-800',
      arquivo: 'contrato_locacao_101.pdf',
      assinado: false,
      podeAssinar: true
    },
    {
      id: 2,
      nome: 'Contrato de Internet - Fibra 200MB',
      data: '2025-09-18',
      tipo: 'Telecomunicações',
      risco: 'Médio',
      riscoColor: 'bg-yellow-100 text-yellow-800',
      arquivo: 'contrato_internet_fibra.pdf',
      assinado: true,
      podeAssinar: false
    },
    {
      id: 3,
      nome: 'Contrato de Financiamento Veicular',
      data: '2025-09-15',
      tipo: 'Financeiro',
      risco: 'Baixo',
      riscoColor: 'bg-green-100 text-green-800',
      arquivo: 'financiamento_veiculo.pdf',
      assinado: false,
      podeAssinar: true
    },
    {
      id: 4,
      nome: 'Contrato de Cartão de Crédito Premium',
      data: '2025-09-12',
      tipo: 'Financeiro',
      risco: 'Alto',
      riscoColor: 'bg-red-100 text-red-800',
      arquivo: 'cartao_credito_premium.pdf',
      assinado: true,
      podeAssinar: false
    }
  ]

  const filteredContratos = filter === 'todos' 
    ? contratos 
    : contratos.filter(c => c.risco.toLowerCase() === filter)

  const handleViewContract = (contratoId: number) => {
    router.push(`/dashboard/analise?contratoId=${contratoId}`)
  }

  const handleSignContract = (contratoId: number) => {
    router.push(`/dashboard/assinatura?contratoId=${contratoId}&fromHistory=true`)
  }

  const downloadContract = (contratoId: number) => {
    // Simular download do contrato
    console.log(`Baixando contrato ${contratoId}`)
  }

  return (
    <div className="p-4 sm:p-6">
      <div className="mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl font-bold text-gray-900 mb-3 sm:mb-4">
          📚 Histórico de Contratos
        </h1>
        
        {/* Filtros - Otimizado para Mobile sem Scroll */}
        <div className="grid grid-cols-4 gap-2 sm:flex sm:gap-3">
          <button
            onClick={() => setFilter('todos')}
            className={`px-2 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors text-center ${
              filter === 'todos' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            <span className="block sm:hidden">📋</span>
            <span className="hidden sm:block">Todos</span>
          </button>
          <button
            onClick={() => setFilter('alto')}
            className={`px-2 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors text-center ${
              filter === 'alto' ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            <span className="block sm:hidden">🔴</span>
            <span className="hidden sm:block">Alto Risco</span>
          </button>
          <button
            onClick={() => setFilter('médio')}
            className={`px-2 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors text-center ${
              filter === 'médio' ? 'bg-yellow-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            <span className="block sm:hidden">🟡</span>
            <span className="hidden sm:block">Médio Risco</span>
          </button>
          <button
            onClick={() => setFilter('baixo')}
            className={`px-2 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors text-center ${
              filter === 'baixo' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            <span className="block sm:hidden">🟢</span>
            <span className="hidden sm:block">Baixo Risco</span>
          </button>
        </div>
        
        {/* Indicador do filtro ativo no mobile */}
        <div className="block sm:hidden mt-2">
          <span className="text-xs text-gray-500">
            Filtro: <span className="font-medium text-gray-700">
              {filter === 'todos' ? 'Todos os contratos' : 
               filter === 'alto' ? 'Alto risco' : 
               filter === 'médio' ? 'Médio risco' : 'Baixo risco'}
            </span>
          </span>
        </div>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 lg:gap-6 mb-6 sm:mb-8">
        <div className="bg-white p-3 sm:p-4 lg:p-6 rounded-lg shadow">
          <h3 className="text-xs sm:text-sm font-medium text-gray-500">Total Analisado</h3>
          <p className="text-lg sm:text-xl lg:text-2xl font-bold text-gray-900">{contratos.length}</p>
        </div>
        <div className="bg-white p-3 sm:p-4 lg:p-6 rounded-lg shadow">
          <h3 className="text-xs sm:text-sm font-medium text-gray-500">Assinados</h3>
          <p className="text-lg sm:text-xl lg:text-2xl font-bold text-green-600">
            {contratos.filter(c => c.assinado).length}
          </p>
        </div>
        <div className="bg-white p-3 sm:p-4 lg:p-6 rounded-lg shadow">
          <h3 className="text-xs sm:text-sm font-medium text-gray-500">Pendentes</h3>
          <p className="text-lg sm:text-xl lg:text-2xl font-bold text-orange-600">
            {contratos.filter(c => !c.assinado && c.podeAssinar).length}
          </p>
        </div>
        <div className="bg-white p-3 sm:p-4 lg:p-6 rounded-lg shadow">
          <h3 className="text-xs sm:text-sm font-medium text-gray-500">Alto Risco</h3>
          <p className="text-lg sm:text-xl lg:text-2xl font-bold text-red-600">
            {contratos.filter(c => c.risco === 'Alto').length}
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
                {/* Header com ícone e título */}
                <div className="flex items-start gap-3 mb-3">
                  <div className="text-blue-600 flex-shrink-0">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-medium text-gray-900 leading-tight mb-1">{contrato.nome}</h3>
                    <div className="flex items-center gap-3 text-xs text-gray-500">
                      <span>📅 {new Date(contrato.data).toLocaleDateString('pt-BR')}</span>
                      <span>📂 {contrato.tipo}</span>
                    </div>
                  </div>
                </div>
                
                {/* Tags de status em linha separada */}
                <div className="flex items-center gap-2 mb-3 flex-wrap">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${contrato.riscoColor}`}>
                    {contrato.risco} Risco
                  </span>
                  {contrato.assinado && (
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 flex items-center gap-1">
                      ✅ Assinado
                    </span>
                  )}
                  {contrato.podeAssinar && !contrato.assinado && (
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 flex items-center gap-1">
                      ⏳ Pendente
                    </span>
                  )}
                </div>
                
                {/* Rodapé com arquivo e ações */}
                <div className="flex justify-between items-center">
                  <span className="text-xs text-gray-500 truncate flex-1 pr-2">📎 {contrato.arquivo}</span>
                  <div className="flex gap-1 flex-shrink-0">
                    <button 
                      onClick={() => handleViewContract(contrato.id)}
                      className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                      title="Ver análise"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </button>
                    {contrato.podeAssinar && !contrato.assinado && (
                      <button 
                        onClick={() => handleSignContract(contrato.id)}
                        className="p-2 text-gray-400 hover:text-green-600 transition-colors"
                        title="Assinar contrato"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                        </svg>
                      </button>
                    )}
                    <button 
                      onClick={() => downloadContract(contrato.id)}
                      className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                      title="Download"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
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
                  <div className="flex items-center gap-3">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${contrato.riscoColor}`}>
                      {contrato.risco} Risco
                    </span>
                    
                    {/* Status de Assinatura */}
                    {contrato.assinado && (
                      <span className="px-3 py-1 rounded-full bg-green-100 text-green-800 text-sm font-medium flex items-center gap-1">
                        ✅ Assinado
                      </span>
                    )}
                    
                    {contrato.podeAssinar && !contrato.assinado && (
                      <span className="px-3 py-1 rounded-full bg-yellow-100 text-yellow-800 text-sm font-medium flex items-center gap-1">
                        ⏳ Aguardando Assinatura
                      </span>
                    )}
                  </div>
                  
                  <div className="flex gap-2">
                    <button 
                      onClick={() => handleViewContract(contrato.id)}
                      className="px-3 py-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-1 text-sm font-medium"
                      title="Ver análise"
                    >
                      👁️ Ver Análise
                    </button>
                    
                    {contrato.assinado ? (
                      <button 
                        onClick={() => downloadContract(contrato.id)}
                        className="px-3 py-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors flex items-center gap-1 text-sm font-medium"
                        title="Baixar contrato assinado"
                      >
                        📥 Download
                      </button>
                    ) : contrato.podeAssinar ? (
                      <button 
                        onClick={() => handleSignContract(contrato.id)}
                        className="px-3 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-lg transition-colors flex items-center gap-1 text-sm font-medium"
                        title="Assinar contrato"
                      >
                        ✍️ Assinar
                      </button>
                    ) : null}
                    
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